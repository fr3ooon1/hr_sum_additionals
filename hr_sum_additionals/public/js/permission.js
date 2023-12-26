frappe.ui.form.on('Permission', {
    after_save: function(frm) {	
		let from_time = frm.doc.from_time ; 
		let to_time = frm.doc.to_time ; 
		let dif = diff_hours(from_time , to_time )
		frm.set_value('custom_different', dif);
		frm.refresh_field('custom_different');
	}
});


frappe.ui.form.on('Permission', {
	after_workflow_action: function(frm) {
		if (frm.doc.workflow_state === 'Approved') {
			let employee = frm.doc.employee;
			let date = frm.doc.date;
			let doctype = frm.doctype;
			let name = frm.doc.name;
			get_the_rule (employee , date , doctype ,  name );		
		}
	}
})

function diff_hours(dt2, dt1) {
	var diff =(dt2.getTime() - dt1.getTime()) / 1000;
	diff /= (60 * 60);
	return Math.abs(diff);
}

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


frappe.ui.form.on('Permission', {
    before_save: function(frm) {	
		frappe.call({
			async: false,
			method: 'hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules.getmaximum',
			args: {
				name:frm.doc.name
				 },
			callback: function (r) {
				if (r) {
					frappe.validated = r.message ;
				}
			}
		})
	}
});
