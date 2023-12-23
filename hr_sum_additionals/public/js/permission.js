frappe.ui.form.on('Permission', {
    on_submit: function(frm) {	
		let employee = frm.doc.employee;
		let date = frm.doc.date;
		let doctype = frm.doctype;
		let from_time = frm.doc.from_time;
		let to_time = frm.doc.to_time;
		let name = frm.doc.name;
		let condition = "Different" ; 
		let get_the_rule1 = get_the_rule (employee , date , doctype ,  name );


		frm.set_value('custom_different', get_the_rule1);
	}
});

function get_the_rule (employee , date , doctype , name){
	var value ;
	frappe.call({
		async: false,
		method: 'hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules.get_the_rule',
		args: {
		employee_id: employee , 
		date: date,
		doctype: doctype,
		ref_docname: name
		 	},
		callback: function (r) {
			if (r) {
				value = r.message ;
			}
		}
	})
	return value ;
}
