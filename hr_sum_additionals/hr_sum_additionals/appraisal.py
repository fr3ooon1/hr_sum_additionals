from hrms.hr.doctype.appraisal.appraisal import Appraisal
from hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules import get_the_rule
import frappe
from datetime import datetime

class CustomAppraisal(Appraisal):
	def validate(self):
		doctype = "Appraisal"
		name = self.name
		employee = self.employee
		appraisal_cycle = self.appraisal_cycle
		appraisal_cycle_data = frappe.get_doc("Appraisal Cycle" , appraisal_cycle )
		date = appraisal_cycle_data.end_date
		
		get_the_rule(employee , date , doctype , name)

		