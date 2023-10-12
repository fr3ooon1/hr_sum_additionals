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