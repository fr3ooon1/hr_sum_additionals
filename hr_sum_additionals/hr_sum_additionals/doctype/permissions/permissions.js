frappe.ui.form.on('Permissions', {
    test: function(frm) {	
		let employee = frm.doc.employee;
		let date = frm.doc.date;
		let doctype = frm.doctype;
		let from_time = frm.doc.from_time;
		let to_time = frm.doc.to_time;
		let name = frm.doc.name;
		let get_the_rule1 = get_the_rule (employee , date , doctype , from_time , to_time , name);
		// let the_function_to_amount1 = the_function_to_amount (get_the_rule1 , employee , from_time , to_time )
		// console.log(the_function_to_amount1);
		frm.set_value('different', get_the_rule1);
	}
});

function get_the_rule (employee , date , doctype , to_time , from_time , name){
	var name ;
	frappe.call({
		async: false,
		method: 'hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules.get_the_rule',
		args: {
		employee_id: employee , 
		date: date,
		doctype: doctype,
		dt2: from_time,
		dt1: to_time,
		ref_docname: name
		 	},
		callback: function (r) {
			if (r) {
				name = r.message ;
			}
		}
	})
	return name ;
}

function the_function_to_amount (name , employee , dt2 , dt1 ){
	var amount ;
	frappe.call({
		async: false,
		method: 'hr_sum_additionals.hr_sum_additionals.doctype.penalties_rules.penalties_rules.the_function_to_amount',
		args: {
		name1: name , 
		employee: employee,
		dt2: dt2,
		dt1: dt1
		 	},
		callback: function (r) {
			if (r) {
				amount = r.message ;
			}
		}
	})
	return amount ;
}

// frappe.ui.form.on('Permissions', {
//     test: function(frm) {
// 		var employee = frm.doc.employee
// 		var employeedata = getEmployeeData (employee);
// 		var rules = getRules();
		
// 		var emp_branch = employeedata.branch;
// 		var emp_department = employeedata.department;
// 		var emp_designation = employeedata.designation;
// 		var emp_employment_type = employeedata.employment_type;
// 		var emp_grade = employeedata.grade;
// 		var date = frm.doc.date;
// 		var permission_type = frm.doc.permission_type;
// 		var rulename;

		


// 		for (let i = 0; i < rules.length ; i++){
// 			let rule = rules[i];
// 			if (rule.related_perimmision_type === 'Permission'){
// 				if(rule.enable == 1){
// 					if(rule.permission_type === permission_type ){
// 						if (isDateBetween(date,rule.from_date,rule.to_date) || (rule.from_date == "" && rule.to_date == "") || (rule.from_date == null && rule.to_date == null)){
// 							if(rule.branch === emp_branch || rule.branch == null || rule.branch == ""){
// 								if(rule.departement === emp_department || rule.departement == null || rule.departement == ""){
// 									if(rule.designation === emp_designation || rule.designation == null || rule.designation == ""){
// 										if(rule.employment_type === emp_employment_type || rule.employment_type == null || rule.employment_type == ""){
// 											if(rule.employee_grade === emp_grade || rule.employee_grade == null || rule.employee_grade == ""){
// 												rulename = rule.name;
// 											}
// 										}
// 									}
// 								}	
// 							}
// 						}
// 					}
// 				}
// 			}
// 		}
		
// 		var fr3on = ruleData (rulename);
// 		console.log(fr3on);
// 		const enable = fr3on['enable'];
//         let rate = fr3on['rate'];
// 		let salary_effects = fr3on['salary_effects'];
// 		let fixed_amount_value = fr3on['fixed_amount_value'];
// 		let calculation_method = fr3on['calculation_method'];
// 		let leave_type = fr3on['leave_type'];
// 		let leaves_day = fr3on['leaves_day'];
// 		var dt1 = new Date(frm.doc.from_time);
// 		var dt2 = new Date(frm.doc.to_time);
// 		let defTime = diff_hours(dt1 , dt2);
// 		let related_perimmision_type = fr3on['related_perimmision_type'];
// 		let name_of_rule = fr3on['name'];
// 		let ref_docname = frm.doc.name;
// 		let calculation_way = fr3on['calculation_way'];
// 		let reptead_every = fr3on['reptead_every'];
// 		let is_repeated = fr3on['is_repeated'];
// 		frm.set_value('different',defTime );
// 		frm.refresh_field('different');
// 		const condition_rules = fr3on['condition_rules'] ;
// 		const penalties_data = fr3on['penalties_data'];
// 		console.log(penalties_data);
// 		let amount = 0;
// 		if (enable ==1){
// 			if(is_repeated == 1){
// 				if(reptead_every === 'Month'){
// 					frappe.call({
// 						method: 'hr_sum_additionals.api.calculate.getHistoryPenaltiesDataMonthly',
// 						args: {
// 							employee: frm.doc.employee, 
// 							salary_component: salary_effects,
// 							},
// 						callback: function (r) {
// 							if (r) {
// 								const temp = r.message;
// 								var temp2 = temp.length;
// 								var memo = temp2 +1;
// 								if (calculation_way === 'simple'){
// 									for (let i = 0; i < penalties_data.length; i++) {
// 										const rule = penalties_data[i];
// 										if(calculation_method === 'Fixed Amount'){									
// 											if (rule.times >= memo) {
// 												amount = rule.fixed_amount_value; 
// 												console.log(amount);
// 											}else if (rule.times < memo){
// 												amount = rule.fixed_amount_value;
// 												console.log(amount);
// 												}						
// 										}
												
// 										else if (calculation_method === 'Value On A specific Field'){
// 											if (rule.times >= memo ) {
// 												amount = rule.rate * defTime; 
// 											}else if (rule.times < memo){
// 												amount = rule.fixed_amount_value;
// 												console.log(amount);
// 											}
// 										}
												
// 											}	
// 										}
// 										if (frm.doc.permission_type === 'over time' || frm.doc.permission_type === 'Work in Holidays' || frm.doc.permission_type === 'Shift Request' ) {
// 											if (frm.doc.select === 'New Day Leave'){
// 												updateLeaveAllocation(employee , leave_type , leaves_day);
// 										}
// 											else if(frm.doc.select === 'Additional Salary' ){
// 												createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule , related_perimmision_type ,ref_docname );								
// 											}
// 										}				
									
// 										else if (frm.doc.permission_type === 'Exit Early' || frm.doc.permission_type === 'Late Enter' || frm.doc.permission_type === 'Missions') {
// 											createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule,related_perimmision_type , ref_docname) ;
										
// 									}
// 												}
												
// 											}
// 										});
// 									} else if (reptead_every === 'Quarter'){
// 										frappe.call({
// 											method: 'hr_sum_additionals.api.calculate.getHistoryPenaltiesDataQuarterly',
// 											args: {
// 												employee: frm.doc.employee, 
// 												salary_component: salary_effects,
// 											},
// 											callback: function (r) {
// 												if (r) {
// 													const temp = r.message;
// 													var temp2 = temp.length;
// 											var memo = temp2 +1;
// 											if (calculation_way === 'simple'){
// 												for (let i = 0; i < penalties_data.length; i++) {
// 													const rule = penalties_data[i];
// 													if(rule.calculation_method === 'Fixed Amount'){
// 														if (rule.times <= memo) {
// 															amount = rule.fixed_amount_value; 
// 													}
// 												}
// 												else if (rule.calculation_method === 'Value On A specific Field'){
// 													if (rule.times <= memo ) {
// 														amount = rule.rate * defTime; 
// 													}
// 												}
// 											}	
// 										}
// 										if (frm.doc.permission_type === 'over time' || frm.doc.permission_type === 'Work in Holidays' || frm.doc.permission_type === 'Shift Request' ) {
// 											if (frm.doc.select === 'New Day Leave'){
// 												updateLeaveAllocation(employee , leave_type , leaves_day);
// 										}
// 											else if(frm.doc.select === 'Additional Salary' ){
// 												createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule , related_perimmision_type ,ref_docname );								
// 											}
// 										}				
									
// 										else if (frm.doc.permission_type === 'Exit Early' || frm.doc.permission_type === 'Late Enter' || frm.doc.permission_type === 'Missions') {
// 											createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule,related_perimmision_type , ref_docname) ;
										
// 									}
// 												}
// 											}
// 										});
			
// 									} else if (reptead_every === 'Year'){
// 										frappe.call({
// 											method: 'hr_sum_additionals.api.calculate.getHistoryPenaltiesDataYearly',
// 											args: {
// 												employee: frm.doc.employee, 
// 												salary_component: salary_effects,
// 											},
// 											callback: function (r) {
// 												if (r) {
// 													const temp = r.message;
// 													var temp2 = temp.length;
// 											var memo = temp2 +1;
// 											if (calculation_way === 'simple'){
// 												for (let i = 0; i < penalties_data.length; i++) {
// 													const rule = penalties_data[i];
// 													if(rule.calculation_method === 'Fixed Amount'){
// 														if (rule.times <= memo) {
// 															amount = rule.fixed_amount_value; 
// 													}
// 												}
// 												else if (rule.calculation_method === 'Value On A specific Field'){
// 													if (rule.times <= memo ) {
// 														amount = rule.rate * defTime; 
// 													}
// 												}
// 											}	
// 										}
// 										if (frm.doc.permission_type === 'over time' || frm.doc.permission_type === 'Work in Holidays' || frm.doc.permission_type === 'Shift Request' ) {
// 											if (frm.doc.select === 'New Day Leave'){
// 												updateLeaveAllocation(employee , leave_type , leaves_day);
// 										}
// 											else if(frm.doc.select === 'Additional Salary' ){
// 												createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule , related_perimmision_type ,ref_docname );								
// 											}
// 										}				
									
// 										else if (frm.doc.permission_type === 'Exit Early' || frm.doc.permission_type === 'Late Enter' || frm.doc.permission_type === 'Missions') {
// 											createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule,related_perimmision_type , ref_docname) ;
										
// 									}
// 												}
// 											}
// 										});
			
// 									} else if (reptead_every === 'STOP'){
// 										frappe.call({
// 											method: 'hr_sum_additionals.api.calculate.getHistoryPenaltiesDataALL',
// 											args: {
// 												employee: frm.doc.employee, 
// 												salary_component: salary_effects,
// 											},
// 											callback: function (r) {
// 												if (r) {
// 													const temp = r.message;
// 													var temp2 = temp.length;
// 											var memo = temp2 +1;
// 											if (calculation_way === 'simple'){
// 												for (let i = 0; i < penalties_data.length; i++) {
// 													const rule = penalties_data[i];
// 													if(rule.calculation_method === 'Fixed Amount'){
// 														if (rule.times <= memo) {
// 															amount = rule.fixed_amount_value; 
// 													}
// 												}
// 												else if (rule.calculation_method === 'Value On A specific Field'){
// 													if (rule.times <= memo ) {
// 														amount = rule.rate * defTime; 
// 													}
// 												}
// 											}	
// 										}
// 										if (frm.doc.permission_type === 'over time' || frm.doc.permission_type === 'Work in Holidays' || frm.doc.permission_type === 'Shift Request' ) {
// 											if (frm.doc.select === 'New Day Leave'){
// 												updateLeaveAllocation(employee , leave_type , leaves_day);
// 										}
// 											else if(frm.doc.select === 'Additional Salary' ){
// 												createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule , related_perimmision_type ,ref_docname );								
// 											}
// 										}				
									
// 										else if (frm.doc.permission_type === 'Exit Early' || frm.doc.permission_type === 'Late Enter' || frm.doc.permission_type === 'Missions') {
// 											createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule,related_perimmision_type , ref_docname) ;
										
// 									}
// 												}
// 											}
// 										});
			
// 									}
									
									
// 								}	else	{
			
// 									if (calculation_way === 'has level'){
// 										if(calculation_method === 'Fixed Amount'){
// 											for (let i = 0; i < condition_rules.length; i++) {
// 												const rule = condition_rules[i];
// 												if (defTime > rule.from && defTime < rule.to) {
// 													amount = rule.value;
// 												}
// 												else if (defTime > rule.to) {
// 													amount = condition_rules[i]['value'];
// 												}
// 											  }
// 										} else if (calculation_method === 'Value On A specific Field'){
// 											for (let i = 0; i < condition_rules.length; i++) {
// 												const rule = condition_rules[i]; 
											  
// 												if (defTime > rule.from && defTime < rule.to) {
// 												  amount = rule.rate * defTime ; 
// 												}
// 												else if (defTime > rule.to){
// 													amount = condition_rules[i]['rate'] * defTime;
// 												}
// 											  }
// 										}
										
// 								} else if (calculation_way === 'simple'){
// 									if(calculation_method === 'Fixed Amount'){
// 										amount = fixed_amount_value ;
// 									} else if (calculation_method === 'Value On A specific Field'){
// 										amount = defTime * rate ;
// 									}
									
// 								}	
// 								if (frm.doc.permission_type === 'over time' || frm.doc.permission_type === 'Work in Holidays' || frm.doc.permission_type === 'Shift Request' ) {
// 									if (frm.doc.select === 'New Day Leave'){
// 										updateLeaveAllocation(employee , leave_type , leaves_day);
// 								}
// 									else if(frm.doc.select === 'Additional Salary' ){
// 										createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule , related_perimmision_type ,ref_docname );								
// 									}
// 								}				
							
// 								else if (frm.doc.permission_type === 'Exit Early' || frm.doc.permission_type === 'Late Enter' || frm.doc.permission_type === 'Missions') {
// 									createAdditionalSalary(employee , salary_effects , amount , date , name_of_rule,related_perimmision_type , ref_docname) ;
								
// 							}
								
// 						}			
// 						}
// 							else {
// 								frappe.msgprint(e);
// 							}

       
//     }
// });

// function createAdditionalSalary(employee , salary_effects , rate , payroll_date , name_of_rule , related_perimmision_type , ref_docname) {
//     let log = frappe.model.get_new_doc("Effected salaries");
//     log.employee = employee;
//     log.salary_component = salary_effects;
//     log.amount = rate;
//     log.payroll_date = payroll_date;
// 	log.ref_docname = ref_docname;
// 	log.ref_doctype = related_perimmision_type;
// 	log.name_of_rule = name_of_rule ;
//     frappe.db.insert(log);
// 	frappe.msgprint("Created");	
// }

// function updateLeaveAllocation (employee , leave_type , leaves_day){
    
// 	frappe.call({
// 	  'method': 'frappe.client.get_value',
// 	  'args': {
// 	  'doctype': 'Leave Allocation',
// 	  'filters': {
// 		  'employee' : employee , 
// 		  'leave_type': leave_type
		  
// 	  },
// 	  'fieldname': ['new_leaves_allocated']
// 		  },
// 	  callback: function(r) {
		  
// 		  let temp = r.message.new_leaves_allocated;
// 		  temp = temp + leaves_day ;
		  
// 		  updateQualityProfile(temp , employee , leave_type); 

// 			  }
// })
// }

// function updateQualityProfile(temp , employee , leave_type) {
//   frappe.call({
// 	  'method': 'frappe.client.get_value',
// 	  'args': {
// 	  'doctype': 'Leave Allocation',
// 	  'filters': {
// 		  'employee' : employee , 
// 		  'leave_type': leave_type
// 	  },
// 	  fieldname: ['name'],
// 		  },
// 	  callback: function(r) {
// 		if(r.message){
		  
// 		  let tempName = r.message.name;
			  

// 	  frappe.call({
// 	  method: "frappe.client.set_value",
// 	  args: {
// 		  doctype: "Leave Allocation",
// 		  name: tempName,
// 		  fieldname:{
// 			  "new_leaves_allocated":temp,
// 			  }
// 		  },
// 	  callback: function(response) {
		  
// 		  msgprint('Updated');
// 	  }
//   });
// 	  } else {
// 	let log = frappe.model.get_new_doc("Leave Allocation");
//     log.employee = employee;
//     log.leave_type = leave_type;
//     log.new_leaves_allocated = temp;
// 	log.to_date = "31-12-2023"
//     frappe.db.insert(log);
// 	frappe.msgprint("Created");

// 	  }
// 	}
//   });
// }


// function diff_hours(dt2, dt1) 
//  {
//   var diff =(dt2.getTime() - dt1.getTime()) / 1000;
//   diff /= (60 * 60);
//   return Math.abs(diff);
//  }
 
// function isDateBetween(dateToCheck, startDate, endDate) {
//     dateToCheck = new Date(dateToCheck);
//     startDate = new Date(startDate);
//     endDate = new Date(endDate);

//     return dateToCheck >= startDate && dateToCheck <= endDate;
// }


// function getEmployeeData (employee){
// 	var employeedata ;
//     frappe.call({
//             async: false,
//             method: "frappe.client.get",
//             args: {
//                 doctype: "Employee",
//                 filters:{name:employee}
//             },
//             callback: function (r) {
// 				employeedata = r.message
//             },
//         });
// 		return employeedata;
//     }

// 	function getRules (){
// 		var ruls ;
// 		frappe.call({
// 				async: false,
// 				method: "frappe.client.get_list",
// 				args: {
// 					doctype: "Penalties Rules",
// 					fields:["name","enable","permission_type","branch","designation","departement","employee_grade","branch","employment_type","from_date","to_date","related_perimmision_type"]
// 				},
// 				callback: function (r) {
// 					ruls = r.message
// 				},
// 			});
// 			return ruls;
// 		}


// 		function ruleData (ruleName){
// 			var rulename ;
// 			frappe.call({
// 					async: false,
// 					method: "frappe.client.get",
// 					args: {
// 						doctype: "Penalties Rules",
// 						filters:{name:rulename}
// 					},
// 					callback: function (r) {
// 						rulename = r.message
// 					},
// 				});
// 				return rulename;
// 			}



// // if (frm.doc.workflow_state === 'Approved') {