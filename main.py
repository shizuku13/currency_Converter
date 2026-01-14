import os
import requests
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, messagebox


load_dotenv()

#Read API-key
API_KEY = os.getenv("API_KEY")

#chek API-key
if not API_KEY:
    messagebox.showerror("API key not set")
    exit(1)

#function for getting currency list
def get_currency_list():
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return list(data["conversion_rates"].keys())
    else:
        messagebox.showerror(title="Error", message=f"Can't get currency list.")
        return []

#function for converting currency
def convert_currency():
    base_currency = base_currency_var.get()  # ОШИБКА 1: было base_currency. get() - неправильное имя переменной
    target_currency = target_currency_var.get()
    amount = amount_entry.get()

    if not amount.isdigit():
        messagebox. showerror(title="Error", message="Please enter a valid amount.")
        return

    amount = float(amount)
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    response = requests. get(url)

    if response.status_code == 200:
        data = response.json()
        if target_currency in data["conversion_rates"]:
            rate = data["conversion_rates"][target_currency]
            converted_amount = amount * rate
            result_label.config(text=(f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}"))
        else:
            messagebox. showerror(title="Error", message="Not currency.")
    else:
        messagebox.showerror(title="Error", message="API dosn't work")

# Create main window
root = tk. Tk()
root.title("Currency Converter")
root.geometry("400x300")
root.resizable(width=False, height=False)

# get Currency list
currencies = get_currency_list()

#input and output fields
tk.Label(root, text="Currencies").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

tk.Label(root, text="Source Currency: ").pack()
base_currency_var = tk. StringVar(value="USD")
base_currency_menu = ttk. Combobox(root, textvariable=base_currency_var, values=currencies)  # ОШИБКА 2: ComboBox должен быть Combobox (маленькая буква)
base_currency_menu.pack()

tk.Label(root, text="Target Currency: ").pack()
target_currency_var = tk.StringVar(value="EUR")  # ОШИБКА 3: была переменная base_currency_var вместо target_currency_var
target_currency_menu = ttk.Combobox(root, textvariable=target_currency_var, values=currencies)  # ОШИБКА 2: ComboBox должен быть Combobox
target_currency_menu.pack()

#Button
convert_button = tk.Button(root, text="Convert", command=convert_currency)
convert_button.pack()

#Feald for result
result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack()

#Run the tkinter
root.mainloop()