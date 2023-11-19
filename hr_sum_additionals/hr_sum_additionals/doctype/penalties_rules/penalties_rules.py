# Copyright (c) 2023, 1 and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from frappe.utils import getdate, get_time

from frappe.model.document import Document

class PenaltiesRules(Document):
	pass

@frappe.whitelist()
def create_effected_salary(employee, salary_effects, rate, payroll_date, name_of_rule, related_permission_type, ref_docname):
    log = frappe.new_doc("Effected salaries")
    log.employee = employee
    log.salary_component = salary_effects
    log.amount = rate
    log.payroll_date = payroll_date
    log.ref_docname = ref_docname
    log.ref_doctype = related_permission_type
    log.name_of_rule = name_of_rule
    log.insert(ignore_permissions=True)
    frappe.db.commit()
    frappe.msgprint("Created")


@frappe.whitelist()
def get_the_rule(employee_id , date , doctype , dt2 , dt1 , ref_docname):
	employee = []
	employee = frappe.get_doc("Employee",employee_id)
	emp_branch = employee.branch
	emp_department = employee.department
	emp_designation = employee.designation
	emp_employment_type = employee.employment_type
	emp_grade = employee.grade

	rules = frappe.db.get_list("Penalties Rules")
	for i in rules:
		rule = frappe.get_doc("Penalties Rules" , i.name )
		if rule.related_perimmision_type == doctype and rule.enable == 1:
			if is_date_between(date, rule.from_date, rule.to_date) or (rule.from_date == "" and rule.to_date == "") or (rule.from_date is None and rule.to_date is None):
				if rule.branch == emp_branch or rule.branch is None or rule.branch == "":
					if rule.departement == emp_department or rule.departement is None or rule.departement == "":
						if rule.designation == emp_designation or rule.designation is None or rule.designation == "":
							if rule.employment_type == emp_employment_type or rule.employment_type is None or rule.employment_type == "":
								if rule.employee_grade == emp_grade or rule.employee_grade is None or rule.employee_grade == "":
									amount = float(the_function_to_amount( rule.name , employee , dt2 , dt1))
									employee_id = employee.name
									salary_effects = rule.salary_effects
									rule_name = rule.name
									related_perimmision_type = rule.related_perimmision_type
	create_effected_salary(employee_id, salary_effects , amount, date, rule_name, related_perimmision_type, ref_docname)
	return amount
	
									

@frappe.whitelist()
def is_date_between(date_to_check, start_date, end_date):
    date_to_check = getdate(date_to_check)
    start_date = getdate(start_date) 
    end_date = getdate(end_date)   

    return start_date <= date_to_check <= end_date

@frappe.whitelist()
def the_function_to_amount ( name1 , employee , dt2 , dt1 ):
	print(name1)
	name = []
	name = frappe.get_doc("Penalties Rules",name1)
	defTime = diff_hours (dt2 , dt1)
	if name.is_repeated == 1:
		if name.reptead_every == 'Month':
			amount = the_rule_repeated(name , defTime ,  len(getHistoryPenaltiesDataMonthly (employee , name.salary_component)) )
		elif name.rereptead_every == 'Year':
			amount = the_rule_repeated(name , defTime ,  len(getHistoryPenaltiesDataYearly (employee , name.salary_component)) )
		elif name.rereptead_every == 'STOP':
			amount = the_rule_repeated(name , defTime ,  len(getHistoryPenaltiesDataALL (employee , name.salary_component)) )
		elif name.rereptead_every == 'Quarter':
			amount = the_rule_repeated(name , defTime ,  len(getHistoryPenaltiesDataQuarterly (employee , name.salary_component)) )
	else:
		amount = the_rule_simpled(name , defTime)
	return amount

@frappe.whitelist()
def the_rule_simpled(name1 , defTime):
	name = []
	name = frappe.get_doc("Penalties Rules",name1)
	if name.calculation_way == "has level":
		if name.calculation_method == 'Fixed Amount':
			print(name.condition_rules)
			for rule in name.condition_rules:
				if defTime > rule['from'] and defTime < rule['to']:
					amount = rule['value']
				elif defTime > rule['to']:
					amount = rule['value']
		elif name.calculation_method == 'Value On A specific Field':
			for rule in name.condition_rules:
				if defTime > rule['from'] and defTime < rule['to']:
					amount = rule['rate'] * defTime
				elif defTime > rule['to']:
					amount = rule['rate'] * defTime
	elif name.calculation_way == 'simple':
		if name.calculation_method == 'Fixed Amount':
			amount = name.fixed_amount_value
		elif name.calculation_method == 'Value On A specific Field':
			amount = defTime * name.rate
	
	return amount


@frappe.whitelist()
def the_rule_repeated(name1 , defTime , pennalties_month_array):
	name = []
	name = frappe.get_doc("Penalties Rules",name1)
	pennalties_month = pennalties_month_array + 1
	if name.calculation_way == 'simple':
		for rule in name.penalties_data:
			if name.calculation_method == 'Fixed Amount':
				if rule['times'] >= pennalties_month:
					amount = rule['fixed_amount_value']
				elif rule['times'] < pennalties_month:
					amount = rule['fixed_amount_value']
			elif name.calculation_method == 'Value On A specific Field':
				if rule['times'] >= pennalties_month:
					amount = rule['rate'] * defTime
				elif rule['times'] < pennalties_month:
					amount = rule['fixed_amount_value']
	elif name.calculation_method == 'Value On A specific Field':
		if rule['times'] >= pennalties_month:
			amount = rule['rate'] * defTime
		elif rule['times'] < pennalties_month:
			amount = rule['fixed_amount_value']

	return amount


@frappe.whitelist()
def diff_hours(dt2,dt1):
    futureDate = datetime.strptime(str(dt2), "%Y-%m-%d %H:%M:%S")
    nowParts = datetime.strptime(str(dt1), "%Y-%m-%d %H:%M:%S")
    timeDifference = (futureDate - nowParts)
    totalAmount = (timeDifference.total_seconds() / 60) 
    result = totalAmount / 60
    return abs(result)

@frappe.whitelist()
def getHistoryPenaltiesDataMonthly(employee='', salary_component=''):
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
def getHistoryPenaltiesDataYearly(employee='', salary_component=''):
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
def getHistoryPenaltiesDataALL(employee='', salary_component=''):
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
def getHistoryPenaltiesDataQuarterly(employee='', salary_component=''):
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