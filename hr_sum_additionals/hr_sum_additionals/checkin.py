from hrms.hr.doctype.employee_checkin.employee_checkin import EmployeeCheckin
from hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules import get_the_rule
from frappe.utils import getdate , get_time
import frappe
from datetime import datetime


class CustomCheckin(EmployeeCheckin):
    def before_validate(self):
        shift_type = self.shift
        shift_data = frappe.get_doc("Shift Type" , shift_type )
        late_penalty_after = shift_data.late_penalty_after
        self.custom_late_penalty_after = late_penalty_after
        self.custom_deduction = calculate_dif_time_and_date(self.time , late_penalty_after)

    def on_change(self):
        employee = self.employee
        doctype = "Employee Checkin"
        datatime = self.time
        date = getdate(datatime)
        name = self.name
        get_the_rule (employee , date , doctype ,  name )



def calculate_dif_time_and_date(futureDate1,timeNow):
    futureDate = datetime.strptime(str(futureDate1), "%Y-%m-%d %H:%M:%S")
    nowParts = datetime.strptime(str(timeNow), "%H:%M:%S").time()
    nowDate = datetime(futureDate.year, futureDate.month, futureDate.day, int(nowParts.hour), int(nowParts.minute), int(nowParts.second))
    timeDifference = (futureDate - nowDate)
    totalAmount = (timeDifference.total_seconds() / 60) 
    result = totalAmount / 60
    print(result)
    return result
