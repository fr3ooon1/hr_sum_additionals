frappe.listview_settings['Effected salaries'] = {
    onload: function(listview) {
            listview.page.add_inner_button(__("Calculate"), () => calculateAdditionalSalary()
            ,"Action");

    }
};


function calculateAdditionalSalary() {
	let resp = frappe.call({
        method: "hr_sum_additionals.api.calculate.calc",
        async: false,
        callback(resp) {
          console.log(resp);
        },
      });
}

