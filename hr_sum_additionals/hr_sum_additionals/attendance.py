from hrms.hr.doctype.attendance.attendance import Attendance
from hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules import get_the_rule
import frappe


class CustomAttendance(Attendance):
    def on_change(self):
        empoloyee_name = self.empoloyee_name
        employee = frappe.db.get_value(doctype = "Employee" , filters = {'employee_name' , empoloyee_name } , fieldname = 'name')
        doctype = "Attendance"
        name = self.name
        date = self.date
        get_the_rule (employee , date , doctype ,  name )
