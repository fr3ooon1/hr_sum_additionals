from hrms.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
from hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules import get_the_rule
from frappe.utils import getdate , get_time
import frappe
from datetime import datetime


class CustomCheckin(EmployeeCheckin):
    def on_change(self):
        employee = self.employee
        doctype = "Employee Checkin"
        datatime = self.time
        date = getdate(datatime)
        time_checkIN = get_time(datatime)
        name = self.name
        # log_type = self.log_type
        shift = self.shift


        shift_data = frappe.get_doc("Shift Type" , shift)
        datetime_obj = datetime.strptime(str(shift_data.late_penalty_after ), "%H:%M:%S")
        to_time = datetime_obj.time()
        
        from_time = time_checkIN


        self.deduction = get_the_rule (employee , date , doctype , to_time , from_time , name )

    
# @frappe.whitelist()
# def dates ():
#     shift_data = frappe.get_doc("Shift Type" , "fr3on shift")
#     datetime_obj = datetime.strptime(str(shift_data.late_penalty_after ), "%H:%M:%S")
#     date = datetime_obj.date()
#     time = datetime_obj.time()

#     # Do something with date and time if needed
#     print("Date:", date)
#     print("Time:", time)
   


