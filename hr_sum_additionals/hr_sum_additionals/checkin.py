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
        log_type = self.log_type
        shift = self.shift


        shift_data = frappe.get_doc("Shift Type" , shift)
        to_time = datetime.strptime(str(shift_data.late_penalty_after), "%H:%M:%S")
        from_time = datetime.strptime(str(time_checkIN), "%H:%M:%S")

        log_type_condition = "Log_type == "+log_type 
        shift_condition = "shift == "+shift
        condition = log_type_condition + " AND " +shift_condition


        self.deduction = get_the_rule (employee , date , doctype , to_time , from_time , name )

