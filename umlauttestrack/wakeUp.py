
#curl -X POST "http://192.168.1.2:8080/api/ethernet_WakeUp" -H  "accept: */*" -d ""
import requests

def send_wake_up():
    url = "http://192.168.1.2:8080/api/ethernet_WakeUp"
    headers = {
        "accept": "*/*"
    }
    data = ""

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        print("Request was successful")
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response:", response.text)

# Call the function
#send_post_request()
