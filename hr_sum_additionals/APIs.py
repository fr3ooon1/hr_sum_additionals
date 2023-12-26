import requests
import frappe


@frappe.whitelist()
def getmaximum (name):
    get_permission_data = frappe.get_doc("Permission" , name)
    get_permission_type_data = frappe.get_doc("permission type components" , get_permission_data.permission_type )
    value = get_permission_type_data.value
    from_date = get_permission_type_data.from_date
    to_date = get_permission_type_data.to_date
    get_permissions = frappe.db.get_list("Permission" , filters = {
            'employee_name':get_permission_data.employee_name,
            'date':['between',[from_date,to_date]],
            'permission_type':get_permission_data.permission_type,
            'workflow_status':"Approved",
            })
    if get_permission_type_data.maximum == "Maximum Hours":
        for i in get_permissions:
            one_permission = frappe.get_doc("Permission" , i.name)
            counter = counter + float(diff_hours(one_permission.from_time , one_permission.to_time))
        counter = counter + float(diff_hours (get_permission_data.from_time , get_permission_data.to_time))
        if counter > value:
            return False
        else:
            return True
        
    elif get_permission_type_data.maximum == "Maximum Times":
        number_of_permission = len(get_permissions)
        if number_of_permission > value:
            return False
        else:
            return True


from datetime import timedelta , datetime

@frappe.whitelist()
def diff_hours(dt2, dt1):
    future_date = datetime.strptime(str(dt2), "%H:%M:%S")
    now_parts = datetime.strptime(str(dt1), "%H:%M:%S")
    time_difference = (future_date - now_parts)
    total_amount = (time_difference.total_seconds() / 60)
    result = total_amount / 60
    return float(abs(result))


@frappe.whitelist(allow_guest=True)
def baios(customer):
    
    api_url = 'http://0.0.0.0:90/api/resource/Sales Invoice/ACC-SINV-2023-00754/'
    headers = {"authorization": "token 7a7d7b488b9023d:37ecbe12e237c57"}

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()

        data = response.json()

       
        if data.get("data") and data["data"].get("customer") == customer:
            
            customer = data["data"]["customer"]
            name = data["data"]["name"]
            due_date = data["data"]["due_date"]
            paid_amount = data["data"]["paid_amount"]

          
            extracted_data = {
                "Customer": customer,
                "due_date": due_date,
                "paid_amount":paid_amount,
                "name":name,
            }
            
            return {"success": True, "data": extracted_data}
        else:
            return {"success": False, "message": "Employee not found"}

    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Request failed: {str(e)}"}
    except Exception as ex:
        return {"success": False, "message": str(ex)}