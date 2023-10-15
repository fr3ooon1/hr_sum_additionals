import datetime
import frappe
from sap.qr_generator import get_qr
from multiprocessing import Process, Queue

@frappe.whitelist()
# def calc(employee = '' , start_date ='' , end_date =''):

#     """
#     return a list of dicts of Employee Effects(child table), filtured on the 
#     function input, if there wasn't any input the function return all waiting Quality
#     items without filter
    
#     employee = Employee Effects employee
#     start_date = the creation date of Product Order Details created on or after the start_date
#     end_date = the creation date of Product Order Details created on or before the end_date    
#     """


#     query = """  SELECT
#         `employee` AS `employee` ,
#        `employee_name` AS `employee_name`,
#         SUM(`amount`) AS `amount`,
#         `salary_component` AS `component`
#         FROM
#         `tabEffected salaries`  
#         GROUP BY
#        `employee` , `employee_name` , `salary_component` """
    
#     if employee:
#         query += f" AND employee='{employee}'"

#     if start_date:
#         query += f" AND creation>='{start_date}'"

#     if end_date:
#         end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
#         end_date += datetime.timedelta(days=1)
#         query += f" AND creation<='{end_date}' "

#     data = frappe.db.sql(query , as_dict=1)
#     return data



def calc(employee='', start_date='', end_date='',salary_component='',status=''):
    """
    Return a list of dicts of Employee Effects (child table), filtered based on the function input.
    If there are no input filters, the function returns all waiting Quality items without filters.

    employee = Employee Effected salaries
    salary_component = Salary Component Effected salaries
    start_date = the creation date of Effected salaries created on or after the start_date
    end_date = the creation date of Effected salaries created on or before the end_date
    """

    filters = []

    if employee:
        filters.append(('employee', '=', employee))

    if salary_component:
        filters.append(('salary_component', '=', salary_component))

    if start_date:
        start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        filters.append(('payroll_date', '>=', start_date_obj))

    if end_date:
        end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        # end_date_obj += datetime.timedelta(days=1)  # Add 1 day to include the end_date
        filters.append(('payroll_date', '<=', end_date_obj))
    if status:
        filters.append(('docstatus', '=', 1))


    data = frappe.get_all(
        "Effected salaries",
        filters=filters,
        fields=["employee", "employee_name", "SUM(amount) as amount", "salary_component"],
        group_by="employee,employee_name,salary_component"  # Use a string with comma-separated fields
    )

    return data


@frappe.whitelist()
def getPenaltiesRule(related_perimmision_type = None , departement = None , permission_type = None , designation= None, employee_grade= None , branch = None , employment_type = None):
    filters = []
    if related_perimmision_type:
        filters.append(('related_perimmision_type', '=', 'Permission'))
    
    elif departement:
        filters.append(('departement', '=', departement))
    
    elif permission_type:
        filters.append(('permission_type', '=', permission_type))

    elif designation:
        filters.append(('designation', '=', designation))
    
    elif employee_grade:
        filters.append(('employee_grade', '=', employee_grade))

    elif branch:
        filters.append(('branch', '=', branch))

    elif employment_type:
        filters.append(('employment_type', '=', employment_type))
    


    data = frappe.get_all(
        "Penalties Rules",
        filters=filters,
        fields = ["name" , "enable" , "rate" , "salary_effects" , "calculation_method" , "fixed_amount_value" , "leave_type" , "related_perimmision_type" , "is_repeated" ,"calculation_way" ]

    )
    for field in data :
        penalty_data = frappe.get_all("Penalties Data",filters={"parent":field["name"]},fields=["leave_allocation","effected_salaries","calculation_method","fixed_amount_value","rate","field_name","leave_type","days"])
        field["penalties_data"] = penalty_data

    for temp in data :
        condition_rules = frappe.get_all("Condition Rules",filters={"parent":temp["name"]},fields=["from","to","value","rate"])
        temp["condition_rules"] = condition_rules
    
    return data
    








# @frappe.whitelist()
# def calc():
#     data = frappe.db.sql(""" SELECT
#        `employee` AS `employee`,
#         SUM(`amount`) AS `amount`,
#         `salary_component` AS `component`
#         FROM
#         `tabEffected salaries`
#         WHERE
#          MONTH(`payroll_date`) = MONTH(CURRENT_DATE())
#          AND YEAR(`payroll_date`) = YEAR(CURRENT_DATE())     
#         GROUP BY
#        `employee` , `salary_component`
#      """, as_dict=1)
#     return data
