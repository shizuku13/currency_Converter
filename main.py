import os
import requests
from dotenv import load_dotenv

load_dotenv()

#Read API-key
API_KEY = os.getenv("API_KEY")

#chek API-key
if not API_KEY:
    print("API key not set")
    exit(1)
else:
    print("API key set")

#take user input
base_currency = input("Put base currency: ").upper()
target_currency = input("Put target currency: ").upper()
amount = float(input("Put amount: "))

#formating request
url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
#url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/EUR"
#url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/pair/USD/UAH"
response = requests.get(url)


#check response API
if response.status_code == 200:
    print("API good")
    data = response.json()

#chack request status
    if data["result"] == "success":
        print("API good")

        #check currency in response
        if target_currency in data["conversion_rates"]:
            rate = data["conversion_rates"][target_currency]
            converted_amount = amount * rate
            print(f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
        else:
            print("Error. Not currency.")

    else:
        print("API dosen't work")

else:
    print("API error")
    print(f"Status code: {response.status_code}")
    print(f"Response: {response.text}")

