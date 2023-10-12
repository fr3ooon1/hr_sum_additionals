// if (frm.doc.workflow_state === 'Approved') {



frappe.ui.form.on('Permissions', {
	test(frm){
		
		frappe.call({
            method: 'frappe.client.get',
            args: {
                doctype: 'Penalties Rules',
                filters: {
					related_perimmision_type: 'Permission', 
					// departement: frm.doc.department || '',
					// permission_type: frm.doc.permission_type ,
					// designation: frm.doc.designation,
					// employee_grade: frm.doc.employee_grade,
					// branch: frm.doc.branch,
					// employment_type: frm.doc.employment_type,
				},
            },
            callback: function (r) {
                if (r.message) {
					let employee = frm.doc.employee;
					frappe.call({
						method:'frappe.client.get',
						args:{
							doctype: 'Employee',
							filters: {
							name: employee
						},
					},callback: function(r){
						const temp = r.message ;
						
					}
				});
					
                    let fr3on = r.message;
					let enable = fr3on.enable;
                    let rate = fr3on.rate;
					let salary_effects = fr3on.salary_effects;
					let fixed_amount_value = fr3on.fixed_amount_value;
					let calculation_method = fr3on.calculation_method;
					// let employee = frm.doc.employee;
					let date = frm.doc.date;
					let leave_type = fr3on.leave_type;
					var dt1 = new Date(frm.doc.from_time);
					var dt2 = new Date(frm.doc.to_time);
					let defTime = diff_hours(dt1 , dt2);
					let related_perimmision_type = fr3on.related_perimmision_type;
					let name_of_rule = fr3on.name;
					let ref_docname = frm.doc.name;
					let calculation_way = fr3on.calculation_way;
					let is_repeated = fr3on.is_repeated;
					frm.set_value('different',defTime );
					frm.refresh_field('different');
					const condition_rules = fr3on.condition_rules ;
					const penalties_data = fr3on.penalties_data;
					let amount = 0;
					if (enable ==1){
					if(is_repeated == 1){
						frappe.call({
							method:'frappe.client.get_list',
							args:{
								doctype:'Effected salaries',
								filters: {
									employee: frm.doc.employee,
									salary_component: salary_effects,
								},
							},
							callback: function(r){
								const temp = r.message;
								var temp2 = temp.length;
								var memo = temp2 +1;
								if (calculation_way === 'simple'){
									for (let i = 0; i < penalties_data.length; i++) {
										const rule = penalties_data[i];
										if(rule.calculation_method === 'Fixed Amount'){
											if (rule.times <= memo) {
												amount = rule.fixed_amount_value; 
										}
									}
									else if (rule.calculation_method === 'Value On A specific Field'){
										if (rule.times <= memo ) {
											amount = rule.rate * defTime; 
										}
									}
								}	
							}
						
						if (frm.doc.permission_type === 'over time' || frm.doc.permission_type === 'Work in Holidays' || frm.doc.permission_type === 'Shift Request' ) {
							if (frm.doc.select === 'New Day Leave'){
								updateLeaveAllocation(employee , leave_type);
						}
							else if(frm.doc.select === 'Additional Salary' ){
								createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule , related_perimmision_type ,ref_docname );								
							}
						}				
					
						else if (frm.doc.permission_type === 'Exit Early' || frm.doc.permission_type === 'Late Enter' ) {
							createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule,related_perimmision_type , ref_docname) ;
						
					}
								
							}	
							
						});
						
					}	else	{

						if (calculation_way === 'has level'){
							if(calculation_method === 'Fixed Amount'){
								for (let i = 0; i < condition_rules.length; i++) {
									const rule = condition_rules[i];
								  
									if (defTime > rule.from && defTime < rule.to) {
									  amount = rule.value; 
									}
								  }
							} else if (calculation_method === 'Value On A specific Field'){
								for (let i = 0; i < condition_rules.length; i++) {
									const rule = condition_rules[i]; 
								  
									if (defTime > rule.from && defTime < rule.to) {
									  amount = rule.rate * defTime ; 
									}
								  }
							}
							
					} else if (calculation_way === 'simple'){
						if(calculation_method === 'Fixed Amount'){
							amount = fixed_amount_value ;
						} else if (calculation_method === 'Value On A specific Field'){
							amount = defTime * rate ;
						}
						
					}
					// if (frm.doc.workflow_state === 'Approved') {
						
					if (frm.doc.permission_type === 'over time' || frm.doc.permission_type === 'Work in Holidays' || frm.doc.permission_type === 'Shift Request' ) {
						if (frm.doc.select === 'New Day Leave'){
							updateLeaveAllocation(employee , leave_type);
					}
						else if(frm.doc.select === 'Additional Salary' ){
							createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule , related_perimmision_type ,ref_docname );								
						}
					}				
				
					else if (frm.doc.permission_type === 'Exit Early' || frm.doc.permission_type === 'Late Enter' ) {
						createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule,related_perimmision_type , ref_docname) ;
					
				}
				}		
			}			
			}
				else {
					frappe.msgprint(e);
				}

		}
	});
		
	}

});

function createAdditionalSalary(employee , salary_effects , rate , payroll_date , name_of_rule , related_perimmision_type , ref_docname) {
    
    let log = frappe.model.get_new_doc("Effected salaries");
    log.employee = employee;
    log.salary_component = salary_effects;
    log.amount = rate;
    log.payroll_date = payroll_date;
	log.ref_docname = ref_docname;
	log.ref_doctype = related_perimmision_type;
	log.name_of_rule = name_of_rule ;
    frappe.db.insert(log);
	frappe.msgprint("Created");
}

function updateLeaveAllocation (employee , leave_type){
    
	frappe.call({
	  'method': 'frappe.client.get_value',
	  'args': {
	  'doctype': 'Leave Allocation',
	  'filters': {
		  'employee' : employee , 
		  'leave_type': leave_type
		  
	  },
	  'fieldname': ['new_leaves_allocated']
		  },
	  callback: function(r) {
		  
		  let temp = r.message.new_leaves_allocated;
		  temp = temp+1 ;
		  
		  updateQualityProfile(temp , employee , leave_type); 

			  }
})
}

function updateQualityProfile(temp , employee , leave_type) {
  frappe.call({
	  'method': 'frappe.client.get_value',
	  'args': {
	  'doctype': 'Leave Allocation',
	  'filters': {
		  'employee' : employee , 
		  'leave_type': leave_type
	  },
	  'fieldname': ['name']
		  },
	  callback: function(r) {
		  
		  let tempName = r.message.name;
			  

	  frappe.call({
	  method: "frappe.client.set_value",
	  args: {
		  doctype: "Leave Allocation",
		  name: tempName,
		  fieldname:{
			  "new_leaves_allocated":temp
			  }
		  },
	  callback: function(response) {
		  
		  msgprint('Updated');
	  }
  });
	  }
  });
}


function diff_hours(dt2, dt1) 
 {
  var diff =(dt2.getTime() - dt1.getTime()) / 1000;
  diff /= (60 * 60);
  return Math.abs(diff);
 }