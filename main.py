from tkinter import *
from tkinter import messagebox
import pyperclip
import json
import random


# ---------------------------- SEARCH FEATURE ------------------------------- #

def search_password():
    website = website_entry.get()
    try:
        with open("passwords.json", "r") as file:
            data = json.load(file)
            data_info = data[website]
    except KeyError:
        messagebox.showerror(title="Try Again", message=f"{website} entry does not exist!")
    except FileNotFoundError:
        messagebox.showerror(title="404", message="No file exist!")
    except json.JSONDecodeError:
        messagebox.showerror(title="404", message="No Data in file!")
    else:
        email = data_info["email"]
        password = data_info["password"]
        pyperclip.copy(password)
        email_entry.delete(0, END)
        email_entry.insert(0, email)
        password_entry.delete(0, END)
        password_entry.insert(0, password)


# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():
    password_entry.delete(0, END)

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    symbol_list = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    numbers_list = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = letter_list + symbol_list + numbers_list

    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    password_info = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        error()
    else:
        try:
            with open("passwords.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open("passwords.json", "w") as file:
                json.dump(password_info, file, indent=4)
        except json.JSONDecodeError:
            with open("passwords.json", "w") as file:
                json.dump(password_info, file, indent=4)
        else:
            data.update(password_info)
            with open("passwords.json", "w") as file:
                json.dump(data, file, indent=4)
        finally:
            email_entry.delete(0, END)
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


def error():
    messagebox.showerror(title="Incomplete Info.", message="Fill all the Information")


# ---------------------------- UI SETUP ------------------------------- #

FONT = "Courier"

window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(height=200, width=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels

website_label = Label(text="Website:", font=(FONT, 12, "normal"))
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:", font=(FONT, 12, "normal"))
email_label.grid(column=0, row=2)
password_label = Label(text="Password:", font=(FONT, 12, "normal"))
password_label.grid(column=0, row=3)

# Entries

website_entry = Entry(width=35)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=50)
email_entry.grid(column=1, row=2, columnspan=2)
password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)

# Buttons
search_button = Button(text="Search", font=(FONT, 11, "normal"), command=search_password)
search_button.grid(column=2, row=1)
generate_button = Button(text="Generate", font=(FONT, 11, "normal"), command=generate_password)
generate_button.grid(column=2, row=3)
add_button = Button(text="Add", font=(FONT, 11, "normal"), width=33, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
