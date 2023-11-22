# Copyright (c) 2023, 1 and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.utils import getdate, get_time
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
def get_the_rule(employee_id, date, doctype, dt2, dt1, ref_docname):
    employee = frappe.get_doc("Employee", employee_id)
    doc_data = frappe.get_doc(doctype, ref_docname)
    permission_type = getattr(doc_data, 'permission_type', None)

    emp_branch = employee.branch
    emp_department = employee.department
    emp_designation = employee.designation
    emp_employment_type = employee.employment_type
    emp_grade = employee.grade

    rules = frappe.get_list("Penalties Rules")
    for i in rules:
        rule = frappe.get_doc("Penalties Rules", i.name)
        if rule.related_perimmision_type == doctype and rule.enable == 1:
            if is_date_between(date, rule.from_date, rule.to_date) or (rule.from_date == "" and rule.to_date == "") or (rule.from_date is None and rule.to_date is None):
                if rule.branch == emp_branch or rule.branch is None or rule.branch == "":
                    if rule.departement == emp_department or rule.departement is None or rule.departement == "":
                        if rule.designation == emp_designation or rule.designation is None or rule.designation == "":
                            if rule.employment_type == emp_employment_type or rule.employment_type is None or rule.employment_type == "":
                                if rule.employee_grade == emp_grade or rule.employee_grade is None or rule.employee_grade == "":
                                    if permission_type == rule.permission_type or permission_type is None:
                                        amount = the_function_to_amount(rule.name, employee, dt2, dt1)
                                        employee_id = employee.name
                                        salary_effects = rule.salary_effects
                                        rule_name = rule.name
                                        related_permission_type = rule.related_perimmision_type
                                        create_effected_salary(employee_id, salary_effects, amount, date, rule_name, related_permission_type, ref_docname)
                                        
                                        dif_time = diff_hours(dt2,dt1)
                                        return dif_time

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
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_monthly(employee, name.salary_effects)))
                return amount
            elif name.reptead_every == 'Year':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_yearly(employee, name.salary_effects)))
                return amount
            elif name.reptead_every == 'STOP':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_all(employee, name.salary_effects)))
                return amount
            elif name.reptead_every == 'Quarter':
                amount = the_rule_repeated(name1, def_time, len(get_history_penalties_data_quarterly(employee, name.salary_effects)))
                return amount
        elif name.is_repeated == 0:
            amount = the_rule_simpled(name1, def_time)
            print(def_time)
            print(name1)
            print(amount)
            return amount
    except Exception as e:
        # Print or log the exception message
        print(f"An error occurred: {str(e)}")
        # Optionally, raise the exception again to propagate it further
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
    penalties_month = penalties_month_array + 1
    times = 0
    amount = 0
    if name.calculation_way == 'simple':
        max_number = penalties_data[0]['fixed_amount_value']
        max_number1 = penalties_data[0]['rate']
        print(max_number)
        for rule in penalties_data:
            temp = rule['fixed_amount_value']
            temp1 = rule['rate']

            if name.calculation_method == 'Fixed Amount':
                if penalties_month <= times:
                    amount = rule['fixed_amount_value']
                elif temp > max_number:
                    max_number = temp
                    print(amount)
            elif name.calculation_method == 'Value On A specific Field':
                if penalties_month <= times:
                    max_number = rule['rate'] * def_time
                elif temp1 > max_number1:
                    max_number = temp1 * def_time
        return max_number

@frappe.whitelist()
def diff_hours(dt2, dt1):
    future_date = datetime.strptime(str(dt2), "%Y-%m-%d %H:%M:%S")
    now_parts = datetime.strptime(str(dt1), "%Y-%m-%d %H:%M:%S")
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



# # Copyright (c) 2023, 1 and contributors
# # For license information, please see license.txt

# import frappe
# from datetime import datetime
# from frappe.utils import getdate, get_time

# from frappe.model.document import Document

# class PenaltiesRules(Document):
# 	pass

# @frappe.whitelist()
# def create_effected_salary(employee, salary_effects, amount, payroll_date, name_of_rule, related_permission_type, ref_docname):
#     log = frappe.new_doc("Effected salaries")
#     log.employee = employee
#     log.salary_component = salary_effects
#     log.amount = amount
#     log.payroll_date = payroll_date
#     log.ref_docname = ref_docname
#     log.ref_doctype = related_permission_type
#     log.name_of_rule = name_of_rule
#     log.insert(ignore_permissions=True)
#     frappe.db.commit()
#     frappe.msgprint("Created")


# @frappe.whitelist()
# def get_the_rule(employee_id , date , doctype , dt2 , dt1 , ref_docname):
# 	employee = []
# 	doc_data = []
# 	doc_data = frappe.get_doc(doctype ,ref_docname)
# 	permission_type = None
# 	if hasattr(doc_data, 'permission_type') and doc_data.permission_type is not None:
# 		permission_type = doc_data.permission_type
# 	employee = frappe.get_doc("Employee",employee_id)
# 	emp_branch = employee.branch
# 	emp_department = employee.department
# 	emp_designation = employee.designation
# 	emp_employment_type = employee.employment_type
# 	emp_grade = employee.grade

# 	rules = frappe.db.get_list("Penalties Rules")
# 	for i in rules:
# 		rule = frappe.get_doc("Penalties Rules" , i.name )
# 		if rule.related_perimmision_type == doctype and rule.enable == 1:
# 			if is_date_between(date, rule.from_date, rule.to_date) or (rule.from_date == "" and rule.to_date == "") or (rule.from_date is None and rule.to_date is None):
# 				if rule.branch == emp_branch or rule.branch is None or rule.branch == "":
# 					if rule.departement == emp_department or rule.departement is None or rule.departement == "":
# 						if rule.designation == emp_designation or rule.designation is None or rule.designation == "":
# 							if rule.employment_type == emp_employment_type or rule.employment_type is None or rule.employment_type == "":
# 								if rule.employee_grade == emp_grade or rule.employee_grade is None or rule.employee_grade == "":
# 									if permission_type == rule.permission_type or permission_type is None:
# 										amount = the_function_to_amount( rule.name , employee , dt2 , dt1)
# 										employee_id = employee.name
# 										salary_effects = rule.salary_effects
# 										rule_name = rule.name
# 										related_perimmision_type = rule.related_perimmision_type
# 	create_effected_salary(employee_id, salary_effects , amount, date, rule_name, related_perimmision_type, ref_docname)
# 	return amount
	
									

# @frappe.whitelist()
# def is_date_between(date_to_check, start_date, end_date):
#     date_to_check = getdate(date_to_check)
#     start_date = getdate(start_date) 
#     end_date = getdate(end_date)   

#     return start_date <= date_to_check <= end_date

# @frappe.whitelist()
# def the_function_to_amount ( name1 , employee , dt2 , dt1 ):
# 	name = []
# 	name = frappe.get_doc("Penalties Rules",name1)
# 	defTime = diff_hours (dt2 , dt1)
# 	if name.is_repeated == 1:
# 		if name.reptead_every == 'Month':
# 			amount = the_rule_repeated(name , defTime ,  len(getHistoryPenaltiesDataMonthly (employee , name.salary_component)) )
# 		elif name.rereptead_every == 'Year':
# 			amount = the_rule_repeated(name , defTime ,  len(getHistoryPenaltiesDataYearly (employee , name.salary_component)) )
# 		elif name.rereptead_every == 'STOP':
# 			amount = the_rule_repeated(name , defTime ,  len(getHistoryPenaltiesDataALL (employee , name.salary_component)) )
# 		elif name.rereptead_every == 'Quarter':
# 			amount = the_rule_repeated(name , defTime ,  len(getHistoryPenaltiesDataQuarterly (employee , name.salary_component)) )
# 	else:
# 		amount = the_rule_simpled(name , defTime)
# 	return amount

# @frappe.whitelist()
# def the_rule_simpled(name1 , defTime):
# 	name = []
# 	name = frappe.get_doc("Penalties Rules",name1)
# 	if name.calculation_way == "has level":
# 		if name.calculation_method == 'Fixed Amount':
# 			print(name.condition_rules)
# 			for rule in name.condition_rules:
# 				if defTime > rule['from'] and defTime < rule['to']:
# 					amount = rule['value']
# 				elif defTime > rule['to']:
# 					amount = rule['value']
# 		elif name.calculation_method == 'Value On A specific Field':
# 			for rule in name.condition_rules:
# 				if defTime > rule['from'] and defTime < rule['to']:
# 					amount = rule['rate'] * defTime
# 				elif defTime > rule['to']:
# 					amount = rule['rate'] * defTime
# 	elif name.calculation_way == 'simple':
# 		if name.calculation_method == 'Fixed Amount':
# 			amount = name.fixed_amount_value
# 		elif name.calculation_method == 'Value On A specific Field':
# 			amount = defTime * name.rate
	
# 	return amount


# @frappe.whitelist()
# def the_rule_repeated(name1 , defTime , pennalties_month_array):
# 	name = []
# 	name = frappe.get_doc("Penalties Rules",name1)
# 	pennalties_month = pennalties_month_array + 1
# 	if name.calculation_way == 'simple':
# 		for rule in name.penalties_data:
# 			if name.calculation_method == 'Fixed Amount':
# 				if rule['times'] >= pennalties_month:
# 					amount = rule['fixed_amount_value']
# 				elif rule['times'] < pennalties_month:
# 					amount = rule['fixed_amount_value']
# 			elif name.calculation_method == 'Value On A specific Field':
# 				if rule['times'] >= pennalties_month:
# 					amount = rule['rate'] * defTime
# 				elif rule['times'] < pennalties_month:
# 					amount = rule['fixed_amount_value']
# 	elif name.calculation_method == 'Value On A specific Field':
# 		if rule['times'] >= pennalties_month:
# 			amount = rule['rate'] * defTime
# 		elif rule['times'] < pennalties_month:
# 			amount = rule['fixed_amount_value']

# 	return amount


# @frappe.whitelist()
# def diff_hours(dt2,dt1):
#     futureDate = datetime.strptime(str(dt2), "%Y-%m-%d %H:%M:%S")
#     nowParts = datetime.strptime(str(dt1), "%Y-%m-%d %H:%M:%S")
#     timeDifference = (futureDate - nowParts)
#     totalAmount = (timeDifference.total_seconds() / 60) 
#     result = totalAmount / 60
#     return abs(result)

# @frappe.whitelist()
# def getHistoryPenaltiesDataMonthly(employee='', salary_component=''):
#     data = frappe.db.sql("""
#         SELECT
#             `employee` AS `employee`,
#             `salary_component` AS `component`
#         FROM
#             `tabEffected salaries`
#         WHERE
#             `salary_component` = %s
#             AND `employee` = %s
#             AND MONTH(`payroll_date`) = MONTH(CURRENT_DATE())
#             AND YEAR(`payroll_date`) = YEAR(CURRENT_DATE())
#      """, (salary_component, employee), as_dict=1)

#     return data

# @frappe.whitelist()
# def getHistoryPenaltiesDataYearly(employee='', salary_component=''):
#     data = frappe.db.sql("""
#         SELECT
#             `employee` AS `employee`,
#             `salary_component` AS `component`
#         FROM
#             `tabEffected salaries`
#         WHERE
#             `salary_component` = %s
#             AND `employee` = %s
#             AND YEAR(`payroll_date`) = YEAR(CURRENT_DATE())
#      """, (salary_component, employee), as_dict=1)

#     return data

# @frappe.whitelist()
# def getHistoryPenaltiesDataALL(employee='', salary_component=''):
#     data = frappe.db.sql("""
#         SELECT
#             `employee` AS `employee`,
#             `salary_component` AS `component`
#         FROM
#             `tabEffected salaries`
#         WHERE
#             `salary_component` = %s
#             AND `employee` = %s
#      """, (salary_component, employee), as_dict=1)

#     return data


# @frappe.whitelist()
# def getHistoryPenaltiesDataQuarterly(employee='', salary_component=''):
#     data = frappe.db.sql("""
#         SELECT
#             `employee` AS `employee`,
#             `salary_component` AS `component`
#         FROM
#             `tabEffected salaries`
#         WHERE
#             `salary_component` = %s
#             AND `employee` = %s
#             AND QUARTER(`payroll_date`) = QUARTER(CURRENT_DATE())
#             AND YEAR(`payroll_date`) = YEAR(CURRENT_DATE())
#      """, (salary_component, employee), as_dict=1)

#     return data

# import barcode
# from barcode.writer import ImageWriter

# # @frappe.whitelist()
# # def generate_barcode(first, sec, third):
# #     result = f"{first}-{sec}-{third}"  # Use f-strings for better readability
# #     EAN = barcode.get_barcode_class('code128')
    
# #     # Specify the desired writer (ImageWriter, in this case)
# #     my_barcode = EAN(result, writer=ImageWriter())
    
# #     # Provide a filename to save the generated barcode image
# #     filename = frappe.get_site_path("public", "files", f"{result}.png")
    
# #     # Save the barcode image
# #     my_barcode.save(filename)
    
# #     # Return the filename or any other relevant information
# #     return filename


# # import frappe
# # from io import BytesIO
# # import base64
# # import barcode
# # from barcode.writer import ImageWriter

# # frappe.whitelist()
# # def generate_barcode(first, sec, third):
# #     try:
# #         code128 = barcode.get_barcode_class('code128')
# #         result = f"{first}-{sec}-{third}"
# #         barcode_instance = code128(result, writer=ImageWriter())

# #         temp = BytesIO()
# #         barcode_instance.save(temp)
# #         temp.seek(0)

# #         b64 = base64.b64encode(temp.read())
# #         final =  "data:image/png;base64,{0}".format(b64.decode("utf-8"))
# #         return final
# #     except Exception as e:
# #         frappe.log_error("Error generating barcode: {}".format(str(e)))
# #         return None

