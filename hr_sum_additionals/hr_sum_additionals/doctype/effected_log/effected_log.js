// frappe.provide("erpnext.public");
// frappe.provide("erpnext.controllers");


frappe.ui.form.on('Effected log', {
	get_all_effects: function(frm) {
		frappe.call({
			method: "hr_sum_additionals.api.calculate.calc",
			args: {
			  employee: frm.doc.employee || "",
			  start_date: frm.doc.from_date || "",
			  end_date: frm.doc.to_date || "",
			  salary_component: frm.doc.salary_component || "",
			  status: frm.doc.docstatus == 1
			}, 
			callback: function (r) {
				if(r){
				  let items = r.message;
				  update_items_table(frm , items);
				}
			},
		  });
	}
});



frappe.ui.form.on('Effected log',{
	create_additional_salary: async function(frm){
		frm.save();
		// if(frm.doc.docstatus == 'Save'){
        const sourceTable = frm.doc.employee_effects; 
        for (const sourceRow of sourceTable) {
			let log = frappe.model.get_new_doc("Additional Salary");
			log.employee = sourceRow.employee;
			log.salary_component = sourceRow.component;
			log.amount = sourceRow.amount;
			// const date = new Date();
			// let currentDay= String(date.getDate()).padStart(2, '0');
			// let currentMonth = String(date.getMonth()+1).padStart(2,"0");
			// let currentYear = date.getFullYear();
			// let currentDate = `${currentYear}-${currentMonth}-${currentDay}`;
			log.payroll_date = frm.doc.posting_date;
			try {
                await frappe.call({
                    method: 'frappe.client.submit',
                    args: {
                        doc: log
                    }
                });
            } catch (error) {
                frappe.msgprint(`Error creating and submitting Additional Salary: ${error}`);
                return;
            }
        }
		frappe.msgprint("Done ");
	}
// }
});

  function update_items_table(frm , items) {
	frm.doc.employee_effects = [];
	items.forEach((item) => {
	//   console.log(items);
	  frm.add_child("employee_effects", {
		employee: item.employee,
		employee_name: item.employee_name,
		component: item.salary_component,
		amount: item.amount
		
	  });
	});
	refresh_field("employee_effects");
  }
