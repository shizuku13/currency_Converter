import os
import requests
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk, messagebox


load_dotenv()

# Read API-key
API_KEY = os.getenv("API_KEY")

# Check API-key
if not API_KEY:
    messagebox.showerror("Ошибка", "API ключ не установлен")
    exit(1)

# Global variable for currencies
currencies = []


# Function for getting currency list
def get_currency_list():
    """Получить список доступных валют"""
    global currencies
    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            currencies = sorted(list(data["conversion_rates"].keys()))
            return currencies
        else:
            messagebox.showerror("Ошибка", "Не удалось получить список валют")
            return []
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибк�� подключения: {str(e)}")
        return []


# Function for converting currency
def convert_currency():
    """Конвертировать валюту"""
    base_currency = base_currency_var.get().upper()
    target_currency = target_currency_var.get().upper()
    amount_text = amount_entry.get().strip()

    # Validation
    if not amount_text:
        result_label.config(text="Введите сумму для конвертации", foreground="#999999")
        return

    try:
        amount = int(amount_text)
        if amount < 0:
            result_label.config(text="Сумма должна быть положительной", foreground="#E74C3C")
            return
    except ValueError:
        result_label.config(text="Введите только целые числа", foreground="#E74C3C")
        return

    if not base_currency or not target_currency:
        result_label.config(text="Выберите обе валюты", foreground="#E74C3C")
        return

    try:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
        response = requests.get(url, timeout=5)

        if response.status_code == 200:
            data = response.json()
            if target_currency in data["conversion_rates"]:
                rate = data["conversion_rates"][target_currency]
                converted_amount = amount * rate
                result_text = f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}"
                result_label.config(text=result_text, foreground="#2D5A4D")
            else:
                result_label. config(text="Целевая валюта не найдена", foreground="#E74C3C")
        else:
            result_label.config(text="API сервис недоступен", foreground="#E74C3C")
    except Exception as e:
        result_label.config(text=f"Ошибка:  {str(e)}", foreground="#E74C3C")


# Function for filtering currencies in real-time
def on_base_currency_change(event=None):
    """Фильтровать базовую валюту при вводе"""
    value = base_currency_var.get().upper()
    if value:
        filtered = [c for c in currencies if value in c]
        base_currency_menu['values'] = filtered if filtered else currencies
    else:
        base_currency_menu['values'] = currencies


def on_target_currency_change(event=None):
    """Фильтровать целевую валюту при вводе"""
    value = target_currency_var.get().upper()
    if value:
        filtered = [c for c in currencies if value in c]
        target_currency_menu['values'] = filtered if filtered else currencies
    else:
        target_currency_menu['values'] = currencies


# Validate amount input - only integers
def validate_amount(char):
    """Позволяет вводить только цифры"""
    return char.isdigit() or char == ""


# Create main window
root = tk.Tk()
root.title("💱 Конвертор валют")
root.geometry("500x650")
root.resizable(False, False)

# Set color scheme with pastel green and blue colors
BG_COLOR = "#E8F4F0"  # Soft pastel blue-green
PRIMARY_COLOR = "#A8D5BA"  # Pastel green
SECONDARY_COLOR = "#B3E5D8"  # Pastel cyan-green
TEXT_COLOR = "#2D5A4D"  # Dark teal-green
ACCENT_COLOR = "#87CEEB"  # Pastel sky blue
ERROR_COLOR = "#E74C3C"  # Red for errors

root.configure(bg=BG_COLOR)

# Configure ttk styles
style = ttk.Style()
style.theme_use('clam')

# Configure button style
style.configure(
    'Custom.TButton',
    background=PRIMARY_COLOR,
    foreground=TEXT_COLOR,
    borderwidth=1,
    relief='raised',
    padding=10,
    font=('Helvetica', 11, 'bold')
)
style.map('Custom.TButton',
    background=[('active', SECONDARY_COLOR), ('pressed', '#7FB3A0')])

# Configure combobox style
style.configure(
    'Custom.TCombobox',
    fieldbackground='white',
    background=SECONDARY_COLOR,
    foreground=TEXT_COLOR
)

# Title Label
title_label = tk.Label(
    root,
    text="💱 Конвертор Валют",
    font=("Helvetica", 24, "bold"),
    bg=BG_COLOR,
    foreground=TEXT_COLOR
)
title_label.pack(pady=20)

# Amount input section
amount_frame = tk.Frame(root, bg=BG_COLOR)
amount_frame.pack(pady=10, padx=20, fill='x')

tk.Label(
    amount_frame,
    text="Сумма (только целые числа):",
    font=("Helvetica", 12, "bold"),
    bg=BG_COLOR,
    foreground=TEXT_COLOR
).pack(anchor='w')

# Register validation function
vcmd = (root.register(validate_amount), '%S')

amount_entry = tk.Entry(
    amount_frame,
    font=("Helvetica", 14),
    width=25,
    bg='white',
    foreground=TEXT_COLOR,
    relief='solid',
    borderwidth=2,
    validate='key',
    validatecommand=vcmd
)
amount_entry.pack(fill='x', pady=8)

# Base currency section
base_frame = tk.Frame(root, bg=BG_COLOR)
base_frame.pack(pady=10, padx=20, fill='x')

tk.Label(
    base_frame,
    text="Исходная валюта:",
    font=("Helvetica", 12, "bold"),
    bg=BG_COLOR,
    foreground=TEXT_COLOR
).pack(anchor='w')

base_currency_var = tk.StringVar(value="USD")
base_currency_menu = ttk.Combobox(
    base_frame,
    textvariable=base_currency_var,
    values=currencies,
    font=("Helvetica", 12),
    width=22,
    state='normal'
)
base_currency_menu.pack(fill='x', pady=8)
base_currency_menu.bind('<KeyRelease>', on_base_currency_change)

# Target currency section
target_frame = tk. Frame(root, bg=BG_COLOR)
target_frame.pack(pady=10, padx=20, fill='x')

tk.Label(
    target_frame,
    text="Целевая валюта:",
    font=("Helvetica", 12, "bold"),
    bg=BG_COLOR,
    foreground=TEXT_COLOR
).pack(anchor='w')

target_currency_var = tk.StringVar(value="EUR")
target_currency_menu = ttk.Combobox(
    target_frame,
    textvariable=target_currency_var,
    values=currencies,
    font=("Helvetica", 12),
    width=22,
    state='normal'
)
target_currency_menu.pack(fill='x', pady=8)
target_currency_menu.bind('<KeyRelease>', on_target_currency_change)

# Buttons frame
buttons_frame = tk.Frame(root, bg=BG_COLOR)
buttons_frame.pack(pady=15)

# Convert button
convert_button = tk.Button(
    buttons_frame,
    text="🔄 Конвертировать",
    command=convert_currency,
    font=("Helvetica", 12, "bold"),
    bg=PRIMARY_COLOR,
    foreground=TEXT_COLOR,
    relief='raised',
    borderwidth=2,
    padx=30,
    pady=10,
    cursor="hand2",
    activebackground=SECONDARY_COLOR,
    activeforeground=TEXT_COLOR
)
convert_button.pack(side='left', padx=5)

# Swap button
def swap_currencies():
    """Поменять местами валюты"""
    base = base_currency_var.get()
    target = target_currency_var.get()
    base_currency_var.set(target)
    target_currency_var.set(base)

swap_btn = tk.Button(
    buttons_frame,
    text="⇅ Обмен",
    command=swap_currencies,
    font=("Helvetica", 11, "bold"),
    bg=ACCENT_COLOR,
    foreground=TEXT_COLOR,
    relief='raised',
    borderwidth=2,
    padx=20,
    pady=10,
    cursor="hand2",
    activebackground="#A0D8E8",
    activeforeground=TEXT_COLOR
)
swap_btn.pack(side='left', padx=5)

# Clear button
def clear_all():
    """Очистить все поля"""
    amount_entry.delete(0, tk.END)
    result_label.config(text="Введите сумму для конвертации", foreground="#999999")

clear_btn = tk.Button(
    buttons_frame,
    text="✖ Очистить",
    command=clear_all,
    font=("Helvetica", 11, "bold"),
    bg="#FFB3BA",
    foreground=TEXT_COLOR,
    relief='raised',
    borderwidth=2,
    padx=20,
    pady=10,
    cursor="hand2",
    activebackground="#FF9CA3",
    activeforeground=TEXT_COLOR
)
clear_btn.pack(side='left', padx=5)

# Result label
result_label = tk. Label(
    root,
    text="Введите сумму для конвертации",
    font=("Helvetica", 14, "bold"),
    bg=BG_COLOR,
    foreground="#999999",
    wraplength=450,
    pady=20
)
result_label.pack(pady=20)

# Info frame
info_frame = tk. Frame(root, bg=SECONDARY_COLOR, relief='solid', borderwidth=1)
info_frame.pack(pady=15, padx=20, fill='x')

info_label = tk.Label(
    info_frame,
    text="💡 Совет: Начните вводить название валюты для автодополнения\nЭ:  введите 'U' и увидите все валюты с буквой 'U'",
    font=("Helvetica", 9),
    bg=SECONDARY_COLOR,
    foreground=TEXT_COLOR,
    justify='left',
    wraplength=430
)
info_label.pack(pady=10, padx=10)

# Load currencies and run the app
currencies = get_currency_list()
base_currency_menu['values'] = currencies
target_currency_menu['values'] = currencies

root.mainloop()