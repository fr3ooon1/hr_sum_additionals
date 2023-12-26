import frappe
from datetime import datetime
from frappe.utils import getdate
from frappe.model.document import Document

class PenaltiesRules(Document):
    pass

@frappe.whitelist()
def create_effected_salary(employee, salary_effects, amount, payroll_date, name_of_rule, related_permission_type, ref_docname):
    log = frappe.new_doc("Effected salaries")
    log.employee = employee
    log.salary_component = salary_effects
    log.amount = amount
    log.payroll_date = payroll_date
    log.ref_docname = ref_docname
    log.ref_doctype = related_permission_type
    log.name_of_rule = name_of_rule
    log.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.msgprint("Created")

@frappe.whitelist()
def get_the_rule(employee_id, date, doctype, ref_docname):
    employee = frappe.get_doc("Employee", employee_id)
    doc_data = frappe.get_doc(doctype, ref_docname)
 

    emp_branch = employee.branch
    emp_department = employee.department
    emp_designation = employee.designation
    emp_employment_type = employee.employment_type
    emp_grade = employee.grade
    x=0

    rules = frappe.get_list(
        doctype = "Penalties Rules" , 
        filters = {
            'related_perimmision_type': doctype , 
            'enable' : 1,
            })
    for i in rules:
        rule = frappe.get_doc("Penalties Rules", i.name)
        if is_date_between(date, rule.from_date, rule.to_date):
            if rule.branch == emp_branch or rule.branch is None or rule.branch == "":
                if rule.departement == emp_department or rule.departement is None or rule.departement == "":
                    if rule.designation == emp_designation or rule.designation is None or rule.designation == "":
                        if rule.employment_type == emp_employment_type or rule.employment_type is None or rule.employment_type == "":
                            if rule.employee_grade == emp_grade or rule.employee_grade is None or rule.employee_grade == "":
                                if conditions(rule.name , doctype , ref_docname):
                                    if must_have_permission(doctype ,ref_docname , rule.name , employee.employee_name): 
                                        amount = the_function_to_amount(rule.name, employee_id , doctype , ref_docname , date)
                                        employee_id = employee.name
                                        salary_effects = rule.salary_component
                                        rule_name = rule.name
                                        related_permission_type = rule.related_perimmision_type
                                        if rule.effect_on_salary == 1:
                                            create_effected_salary(employee_id, salary_effects, amount, date, rule_name, related_permission_type, ref_docname)
                                        if rule.update_leave == 1:
                                            name_of_leave = frappe.db.get_value('Leave Allocation', {'employee_name': employee.employee_name , 'leave_type': rule.leave_type}, 'name')
                                            value_of_leave = frappe.db.get_value('Leave Allocation', {'employee_name': employee.employee_name , 'leave_type': rule.leave_type}, 'new_leaves_allocated')
                                            new_value_of_leave = float(value_of_leave) + amount
                                            frappe.db.set_value('Leave Allocation', name_of_leave, 'new_leaves_allocated', new_value_of_leave)
                                            frappe.db.set_value('Leave Allocation', name_of_leave, 'total_leaves_allocated', new_value_of_leave)
                                        # return amount


@frappe.whitelist()
def must_have_permission(doctype , ref_docname , rule_name  , employee_name):
        data_of_rule = frappe.get_doc("Penalties Rules" , rule_name)
        
        if data_of_rule.must_have_permission == 1 and doctype == 'Employee Checkin':
            number_of_permission = data_of_rule.number_of_permission
            counter = 0
            data = frappe.get_doc(doctype , ref_docname)
            time = data.time
            date = getdate(time)
            print(date)
            get_permissions = frappe.db.get_list(doctype = "Permission" ,filters = {
            'permission_type':['in', ['Late Enter', 'Travel' , 'Exit Early']], 
            'employee_name' : employee_name , 
            })
            print(get_permissions)
            for i in get_permissions:
                one_permission = frappe.get_doc("Permission" , i.name)
                counter = counter + float(diff_hours(one_permission.from_time , one_permission.to_time))
            print(counter)
            fr3o = frappe.db.get_list(doctype = "Permission" ,filters = {
            'permission_type':['in', ['Late Enter', 'Travel' , 'Exit Early']], 
            'employee_name' : employee_name , 
            'date': date
            })
            if len(fr3o) != 0:
                if counter <= number_of_permission:
                    frappe.throw("Had Permission")
                    return False
                else:
                    return True
            else:
                return True
        else:
            return True




@frappe.whitelist()
def is_valid_time(value):
    try:
        datetime.strptime(value, "%H:%M:%S")
        return True
    except ValueError:
        return False

from datetime import datetime
@frappe.whitelist()
def is_valid_date(value):
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
@frappe.whitelist()
def convert_string_to_float(value):
    if isinstance(value, str) and value.replace('.', '', 1).isdigit():
        return float(value)
    else:
        return value
    

from datetime import timedelta
@frappe.whitelist()
def conditions(name_of_rule, doctype, name):
    ref_data = frappe.get_doc(doctype, name)

    if not ref_data:
        frappe.msgprint(f"No document found with doctype: {doctype} and name: {name}")
        return False

    all_fields = ref_data.as_dict()

    conditions = frappe.get_all(
        doctype="Condition",
        filters={"parent": name_of_rule},
        fields=["field_name", "operator", "value"]
    )

    for i in conditions:
        value = i['value']
        if is_valid_time(value):
            time_object = datetime.strptime(value, "%H:%M:%S")
            i['value'] = timedelta(
                hours=time_object.hour,
                minutes=time_object.minute,
                seconds=time_object.second
            )
        if is_valid_date(value):
            date_object = datetime.strptime(value, "%Y-%m-%d")
            i['value'] = date_object.date()
        
        i['value'] = convert_string_to_float(value)


    print(conditions)

    second_dict = {cond['field_name']: cond for cond in conditions}

    for field_name, condition in all_fields.items():
        if field_name in second_dict:
            condition_info = second_dict[field_name]
            operator = condition_info.get("operator")
            value = condition_info.get("value")

            if operator == '==' and condition != value:
                return False
            elif operator == '!=' and condition == value:
                return False
            elif operator == '<' and not condition < value:
                return False
            elif operator == '>' and not condition > value:
                return False

    return True


@frappe.whitelist()
def is_date_between(date_to_check, start_date, end_date):
    date_to_check = getdate(date_to_check)
    start_date = getdate(start_date)
    end_date = getdate(end_date)
    return start_date <= date_to_check <= end_date

def calculate_dif_time_and_date(futureDate1,timeNow):
    futureDate = datetime.strptime(str(futureDate1), "%Y-%m-%d %H:%M:%S")
    nowParts = datetime.strptime(str(timeNow), "%H:%M:%S").time()
    nowDate = datetime(futureDate.year, futureDate.month, futureDate.day, int(nowParts.hour), int(nowParts.minute), int(nowParts.second))
    timeDifference = (futureDate - nowDate)
    totalAmount = (timeDifference.total_seconds() / 60) 
    result = totalAmount / 60
    print(result)
    return result

def calculate_dif_dateTime(futureDate1,timeNow):
    futureDate = datetime.strptime(str(futureDate1), "%Y-%m-%d %H:%M:%S")
    nowParts = datetime.strptime(str(timeNow), "%Y-%m-%d %H:%M:%S")
    nowDate = datetime(futureDate.year, futureDate.month, futureDate.day, int(nowParts.hour), int(nowParts.minute), int(nowParts.second))
    timeDifference = (futureDate - nowDate)
    totalAmount = (timeDifference.total_seconds() / 60) 
    result = totalAmount / 60
    print(result)
    return result

from frappe.utils import getdate 
from datetime import datetime, time
@frappe.whitelist()
def the_function_to_amount(name1, employee , doctype , ref_docname , date):
    try:
        amount = 0
        name = frappe.get_doc("Penalties Rules", name1)
        def_time = frappe.db.get_value(doctype, ref_docname, name.field_name)
        if def_time is None:
            if doctype == "Permission":
                doc = frappe.get_doc("Permission" , ref_docname)
                def_time = float(diff_hours(doc.from_time, doc.to_time))
            elif doctype == "Employee Checkin":
                doc = frappe.get_doc("Employee Checkin" , ref_docname)
                if doc.log_type == "IN":
                    time_of_login = doc.time
                    late_penalty_after = doc.late_penalty_after
                    if_def_time = calculate_dif_time_and_date (time_of_login , late_penalty_after)
                    if if_def_time > 0 and if_def_time < 4:
                        def_time = calculate_dif_dateTime (time_of_login , doc.shift_start)
                    elif if_def_time < 0:
                        frappe.throw("Not Late")    
                    elif if_def_time > 4:
                        frappe.throw("Absent")            
        print(def_time)

            

        if name.is_repeated == 1:
            if name.reptead_every == 'Month':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_monthly(employee, name.salary_component , date)))
                return amount
            elif name.reptead_every == 'Year':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_yearly(employee, name.salary_component , date)))
                return amount
            elif name.reptead_every == 'NEVER':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_all(employee, name.salary_component , date)))
                return amount
            elif name.reptead_every == 'Quarter':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_quarterly(employee, name.salary_component , date)))
                return amount
        elif name.is_repeated == 0:
            amount = the_rule_simpled(name1, def_time)
            return amount
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


@frappe.whitelist()
def the_rule_simpled(name1 , def_time1):
    def_time = float(def_time1)
    amount = 0
    name = []
    name = frappe.get_doc("Penalties Rules", name1)
    
    condition_rules = frappe.get_all(
        doctype="Condition Rules",
        filters={"parent": name1},
        fields=["from", "to", "value", "rate"]
    )
    if name.calculation_way == "has level":
        if name.calculation_method == 'Fixed Amount':
            for rule in condition_rules:
                if def_time >= rule['from'] and def_time < rule['to']:
                    amount = rule['value']
                elif def_time >= rule['to']:
                    amount = rule['value']
        elif name.calculation_method == 'Value On A specific Field':
            for rule in condition_rules:
                if def_time >= rule['from'] and def_time < rule['to']:
                    amount = rule['rate'] * def_time
                elif def_time >= rule['to']:
                    amount = rule['rate'] * def_time
    elif name.calculation_way == 'simple':
        if name.calculation_method == 'Fixed Amount':
            amount = name.fixed_amount_value
        elif name.calculation_method == 'Value On A specific Field':
            amount = def_time * float(name.rate)
    return amount

@frappe.whitelist()
def the_rule_repeated(name1, def_time, penalties_month_array):
    name = frappe.get_doc("Penalties Rules", name1)
    penalties_data = frappe.get_all(
        doctype="Penalties Data",
        filters={"parent": name1},
        fields=["times", "fixed_amount_value", "rate"]
    )
    penalties_month = float(penalties_month_array) + 1
    sorted_array = sorted(penalties_data, key=lambda x: x['times'])
    print(penalties_month)

    max_number = None


    if name.calculation_method == 'Fixed Amount':
        for rule in sorted_array:
            fixed_amount_value = rule['fixed_amount_value']
            times = rule['times']

            if times == penalties_month:
                max_number = fixed_amount_value
                break 

        if max_number is None:
            max_number = sorted_array[-1]['fixed_amount_value']
    
    elif name.calculation_method == 'Value On A sepcific Field':
        for rule in sorted_array:
            rate = rule['rate']
            times = rule['times']

            if times == penalties_month:
                max_number = rate * def_time
                break 

        if max_number is None:
            max_number = sorted_array[-1]['rate'] * def_time

    return max_number



@frappe.whitelist()
def diff_hours(dt2, dt1):
    future_date = datetime.strptime(str(dt2), "%H:%M:%S")
    now_parts = datetime.strptime(str(dt1), "%H:%M:%S")
    time_difference = (future_date - now_parts)
    total_amount = (time_difference.total_seconds() / 60)
    result = total_amount / 60
    return float(abs(result))


@frappe.whitelist()
def get_history_penalties_data_monthly(employee, salary_component , date):
    data = frappe.db.sql("""
        SELECT
            `employee` AS `employee`,
            `salary_component` AS `component`
        FROM
            `tabEffected salaries`
        WHERE
            `salary_component` = %s
            AND `employee` = %s
            AND MONTH(`payroll_date`) = MONTH(%s)
        
     """, (salary_component, employee , date), as_dict=1)

    return data

@frappe.whitelist()
def get_history_penalties_data_yearly(employee, salary_component , date ):
    data = frappe.db.sql("""
        SELECT
            `employee` AS `employee`,
            `salary_component` AS `component`
        FROM
            `tabEffected salaries`
        WHERE
            `salary_component` = %s
            AND `employee` = %s
            AND YEAR(`payroll_date`) = YEAR(%s)
     """, (salary_component, employee , date), as_dict=1)

    return data

@frappe.whitelist()
def get_history_penalties_data_all(employee, salary_component, date ):
    data = frappe.db.sql("""
        SELECT
            `employee` AS `employee`,
            `salary_component` AS `component`
        FROM
            `tabEffected salaries`
        WHERE
            `salary_component` = %s
            AND `employee` = %s
     """, (salary_component, employee), as_dict=1)

    return data

@frappe.whitelist()
def get_history_penalties_data_quarterly(employee, salary_component , date ):
    data = frappe.db.sql("""
        SELECT
            `employee` AS `employee`,
            `salary_component` AS `component`
        FROM
            `tabEffected salaries`
        WHERE
            `salary_component` = %s
            AND `employee` = %s
            AND QUARTER(`payroll_date`) = QUARTER(%s)
     """, (salary_component, employee , date), as_dict=1)

    return data


@frappe.whitelist()
def getmaximum (name):
    get_permission_data = frappe.get_doc("Permission" , name)
    get_permission_type_data = frappe.get_doc("permission type components" , get_permission_data.permission_type )
    value = get_permission_type_data.value
    from_date = get_permission_type_data.from_date
    to_date = get_permission_type_data.to_date
    get_permissions = frappe.db.get_list("Permission" , filters = {
            'employee_name':get_permission_data.employee_name,
            'date':['between',[from_date,to_date]],
            'permission_type':get_permission_data.permission_type,
            'workflow_status':"Approved",
            })
    if get_permission_type_data.maximum == "Maximum Hours":
        for i in get_permissions:
            one_permission = frappe.get_doc("Permission" , i.name)
            counter = counter + float(diff_hours(one_permission.from_time , one_permission.to_time))
        counter = counter + float(diff_hours (get_permission_data.from_time , get_permission_data.to_time))
        if counter > value:
            return False
        else:
            return True
        
    elif get_permission_type_data.maximum == "Maximum Times":
        number_of_permission = len(get_permissions)
        if number_of_permission > value:
            return False
        else:
            return True
    elif get_permission_type_data.maximum is None or get_permission_type_data.maximum == '':
        return True