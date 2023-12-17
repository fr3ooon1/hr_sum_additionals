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
def get_the_rule(employee_id, date, doctype, dt2, dt1, ref_docname , condition):
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
                                    amount = the_function_to_amount(rule.name, employee_id, dt2, dt1)
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
                                        
                                    dif_time = diff_hours(dt2,dt1)
                                    return dif_time


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

    second_dict = {cond['field_name']: cond for cond in conditions}

    for field_name, condition in all_fields.items():
        if field_name in second_dict:
            condition_info = second_dict[field_name]
            operator = condition_info.get("operator")
            value = condition_info.get("value")
            print(condition_info)
            print(operator)
            print(value)

            if operator == '==' and condition != value:
                return False
            elif operator == '!=' and condition == value:
                return False

    return True


@frappe.whitelist()
def is_date_between(date_to_check, start_date, end_date):
    date_to_check = getdate(date_to_check)
    start_date = getdate(start_date)
    end_date = getdate(end_date)
    return start_date <= date_to_check <= end_date

@frappe.whitelist()
def the_function_to_amount(name1, employee, dt2, dt1):
    try:
        amount = 0
        name = frappe.get_doc("Penalties Rules", name1)
        def_time = float(diff_hours(dt2, dt1))

        if name.is_repeated == 1:
            if name.reptead_every == 'Month':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_monthly(employee, name.salary_component)))
                return amount
            elif name.reptead_every == 'Year':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_yearly(employee, name.salary_component)))
                return amount
            elif name.reptead_every == 'NEVER':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_all(employee, name.salary_component)))
                return amount
            elif name.reptead_every == 'Quarter':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_quarterly(employee, name.salary_component)))
                return amount
        elif name.is_repeated == 0:
            amount = the_rule_simpled(name1, def_time)
            print(def_time)
            print(name1)
            print(amount)
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
def get_history_penalties_data_monthly(employee, salary_component):
    data = frappe.db.sql("""
        SELECT
            `employee` AS `employee`,
            `salary_component` AS `component`
        FROM
            `tabEffected salaries`
        WHERE
            `salary_component` = %s
            AND `employee` = %s
            AND MONTH(`payroll_date`) = MONTH(CURRENT_DATE())
            AND YEAR(`payroll_date`) = YEAR(CURRENT_DATE())
     """, (salary_component, employee), as_dict=1)

    return data

@frappe.whitelist()
def get_history_penalties_data_yearly(employee='', salary_component=''):
    data = frappe.db.sql("""
        SELECT
            `employee` AS `employee`,
            `salary_component` AS `component`
        FROM
            `tabEffected salaries`
        WHERE
            `salary_component` = %s
            AND `employee` = %s
            AND YEAR(`payroll_date`) = YEAR(CURRENT_DATE())
     """, (salary_component, employee), as_dict=1)

    return data

@frappe.whitelist()
def get_history_penalties_data_all(employee='', salary_component=''):
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
def get_history_penalties_data_quarterly(employee='', salary_component=''):
    data = frappe.db.sql("""
        SELECT
            `employee` AS `employee`,
            `salary_component` AS `component`
        FROM
            `tabEffected salaries`
        WHERE
            `salary_component` = %s
            AND `employee` = %s
            AND QUARTER(`payroll_date`) = QUARTER(CURRENT_DATE())
            AND YEAR(`payroll_date`) = YEAR(CURRENT_DATE())
     """, (salary_component, employee), as_dict=1)

    return data
