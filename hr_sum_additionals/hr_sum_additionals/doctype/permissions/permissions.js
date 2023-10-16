frappe.ui.form.on('Permissions', {
	test(frm){
		frappe.call({
            method: 'hr_sum_additionals.api.calculate.getPenaltiesRule',
            args: {
                related_perimmision_type: 'Permission', 
				departement: frm.doc.department,
				permission_type: frm.doc.permission_type ,
				designation: frm.doc.designation,
				employee_grade: frm.doc.employee_grade,
				branch: frm.doc.branch,
				employment_type: frm.doc.employment_type,
            },
            callback: function (r) {
                if (r) {
					let employee = frm.doc.employee;
                    const fr3on2 = r.message;
					const fr3on = fr3on2[0];
					const enable = fr3on['enable'];
                    let rate = fr3on['rate'];
					let salary_effects = fr3on['salary_effects'];
					let fixed_amount_value = fr3on['fixed_amount_value'];
					// console.log(fixed_amount_value);
					let calculation_method = fr3on['calculation_method'];
					console.log(calculation_method);
					let date = frm.doc.date;
					let leave_type = fr3on['leave_type'];
					let leaves_day = fr3on['leaves_day'];
					var dt1 = new Date(frm.doc.from_time);
					var dt2 = new Date(frm.doc.to_time);
					let defTime = diff_hours(dt1 , dt2);
					let related_perimmision_type = fr3on['related_perimmision_type'];
					let name_of_rule = fr3on['name'];
					let ref_docname = frm.doc.name;
					let calculation_way = fr3on['calculation_way'];
					let reptead_every = fr3on['reptead_every'];
					console.log(calculation_way);
					let is_repeated = fr3on['is_repeated'];
					frm.set_value('different',defTime );
					frm.refresh_field('different');
					const condition_rules = fr3on['condition_rules'] ;
					const penalties_data = fr3on['penalties_data'];
					console.log(penalties_data);
					console.log(condition_rules);
					let amount = 0;
					if (enable ==1){
					if(is_repeated == 1){
						if(reptead_every === 'Month'){
							frappe.call({
								method: 'hr_sum_additionals.api.calculate.getHistoryPenaltiesDataMonthly',
								args: {
									employee: frm.doc.employee, 
									salary_component: salary_effects,
								},
								callback: function (r) {
									if (r) {
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
									}
								}
							});
						} else if (reptead_every === 'Quarter'){
							frappe.call({
								method: 'hr_sum_additionals.api.calculate.getHistoryPenaltiesDataQuarterly',
								args: {
									employee: frm.doc.employee, 
									salary_component: salary_effects,
								},
								callback: function (r) {
									if (r) {
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
									}
								}
							});

						} else if (reptead_every === 'Year'){
							frappe.call({
								method: 'hr_sum_additionals.api.calculate.getHistoryPenaltiesDataYearly',
								args: {
									employee: frm.doc.employee, 
									salary_component: salary_effects,
								},
								callback: function (r) {
									if (r) {
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
									}
								}
							});

						} else if (reptead_every === 'STOP'){
							frappe.call({
								method: 'hr_sum_additionals.api.calculate.getHistoryPenaltiesDataALL',
								args: {
									employee: frm.doc.employee, 
									salary_component: salary_effects,
								},
								callback: function (r) {
									if (r) {
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
									}
								}
							});

						}
						
						
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
							console.log(amount);
						} else if (calculation_method === 'Value On A specific Field'){
							amount = defTime * rate ;
						}
						
					}
					// if (frm.doc.workflow_state === 'Approved') {
						
					if (frm.doc.permission_type === 'over time' || frm.doc.permission_type === 'Work in Holidays' || frm.doc.permission_type === 'Shift Request' ) {
						if (frm.doc.select === 'New Day Leave'){
							updateLeaveAllocation(employee , leave_type , leaves_day);
					}
						else if(frm.doc.select === 'Additional Salary' ){
							createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule , related_perimmision_type ,ref_docname );								
						}
					}				
				
					else if (frm.doc.permission_type === 'Exit Early' || frm.doc.permission_type === 'Late Enter' || frm.doc.permission_type === 'Missions') {
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
	frappe.msgprint(rate);


}

function updateLeaveAllocation (employee , leave_type , leaves_day){
    
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
		  temp = temp + leaves_day ;
		  
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


