frappe.ui.form.on('Permission', {
    on_submit: function(frm) {	
		let employee = frm.doc.employee;
		let date = frm.doc.date;
		let doctype = frm.doctype;
		let name = frm.doc.name;
		let get_the_rule1 = get_the_rule (employee , date , doctype ,  name );
	}
});


frappe.ui.form.on('Permission', {
	after_workflow_action: function(frm) {
		if (frm.doc.workflow_state === 'Approved') {		let from_time = frm.doc.from_time ; 
			let to_time = frm.doc.to_time ; 
			let dif = diff_hours(from_time , to_time )
			frm.set_value('custom_different', dif);
			frm.refresh_field('custom_different');
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


// function gethistory (employee_name , permission_type , date){
// 	frappe.call({
// 		async: false,
// 		method: 'frappe.client.get_list',
// 		args: {
// 		'doctype': 'Permission' ,
// 		filters:{
// 			'employee_name': employee_name,
// 			'permission_type':permission_type , 
// 			'date': ['between',['','']],
// 		}
		
// 		 	},
// 		callback: function (r) {
// 			if (r) {
// 				value = r.message ;
// 			}
// 		}
// 	})
// }