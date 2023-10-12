# Copyright (c) 2023, 1 and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Permissions(Document):
	pass



# # import frappe
# from frappe import _

# def diff_hours(dt1, dt2):
#     diff = abs((dt2 - dt1).total_seconds() / 3600)
#     return diff

# @frappe.whitelist()
# def update_effected_salaries(doc, method):
#     if doc.permission_type in ["Over Time", "Work in Holidays", "Shift Request", "Exit Early", "Late Enter"]:
#         penalties_rules = frappe.get_all("Penalties Rules",
#             filters={
#                 "departement": doc.departement,
#                 "related_perimmision_type": "Permission",
#                 "permission_type": doc.permission_type
#             },
#             fields=["rate", "salary_effects", "fixed_amount_value", "calculation_method", "leave_type"]
#         )

#         if penalties_rules:
#             rule = penalties_rules[0]
#             rate = rule.rate
#             salary_effects = rule.salary_effects
#             fixed_amount_value = rule.fixed_amount_value
#             calculation_method = rule.calculation_method
#             leave_type = rule.leave_type

#             dt1 = doc.from_time
#             dt2 = doc.to_time
#             def_time = diff_hours(dt1, dt2)
#             time_rate = def_time * rate

#             if doc.select == "New Day Leave":
#                 update_leave_allocation(doc.employee, leave_type)

#             elif doc.select == "Additional Salary" or not doc.select:
#                 if calculation_method == "Fixed Amount":
#                     create_additional_salary(doc.employee, salary_effects, fixed_amount_value, doc.date)
#                 elif calculation_method == "Value On A specific Field":
#                     create_additional_salary(doc.employee, salary_effects, time_rate, doc.date)

# @frappe.whitelist()
# def create_additional_salary(employee, salary_effects, rate, payroll_date):
#     log = frappe.new_doc("Effected salaries")
#     log.employee = employee
#     log.salary_component = salary_effects
#     log.amount = rate
#     log.payroll_date = payroll_date
#     log.insert()
#     frappe.msgprint(_("Created"))

# @frappe.whitelist()
# def update_leave_allocation(employee, leave_type):
#     leave_allocation = frappe.get_value("Leave Allocation",
#         filters={
#             "employee": employee,
#             "leave_type": leave_type
#         },
#         fieldname=["name", "new_leaves_allocated"]
#     )

#     if leave_allocation:
#         temp = leave_allocation[1] + 1
#         update_quality_profile(temp, leave_allocation[0], leave_type)

# @frappe.whitelist()
# def update_quality_profile(temp, employee, leave_type):
#     leave_allocation_name = frappe.get_value("Leave Allocation",
#         filters={
#             "employee": employee,
#             "leave_type": leave_type
#         },
#         fieldname="name"
#     )

#     if leave_allocation_name:
#         frappe.set_value("Leave Allocation", leave_allocation_name, "new_leaves_allocated", temp)
#         frappe.msgprint(_("Updated"))