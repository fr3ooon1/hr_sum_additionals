import requests
import frappe

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