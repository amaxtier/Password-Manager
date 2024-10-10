import json
from tkinter import *
from tkinter import messagebox
from random import choice, shuffle, randint
import pyperclip


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F',
               'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
               'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": username,
            "password": password,
        }
    }

    if website.strip() == "" or password.strip() == "":
        messagebox.showinfo(title="oops", message="Please dont leave any fields open")
    else:
        try:
            with open("saved_passwords.json", "r") as file:
                # Reading old data
                data = json.load(file)
                #  Updating old data with new data
                data.update(new_data)
            with open("saved_passwords.json", "w") as file:
                # Saving the updated data
                json.dump(data, file, indent=4)

        except FileNotFoundError:
            with open("saved_passwords.json", "w") as file:
                # Saving the updated data
                json.dump(new_data, file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH JSON ------------------------------- #
def search():
    website = website_entry.get()
    try:
        with open("saved_passwords.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")
    else:
        if website in data:
            email = data[website].get("email")
            password = data[website].get("password")
            pyperclip.copy(password)
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message="No details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #
windows = Tk()

windows.title("Password Manager")
windows.config(padx=30, pady=30)

canvas = Canvas(width=200, height=200)
password_img = PhotoImage(file="images/logo.png")
canvas.create_image(100, 100, image=password_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

username_label = Label(text="Email/Username:")
username_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=17)
website_entry.focus()
website_entry.grid(row=1, column=1, sticky="EW")

username_entry = Entry(width=35)
username_entry.insert(0, "TEST@gmail.com")
username_entry.grid(row=2, column=1, columnspan=2, sticky="EW")

password_entry = Entry(width=17)
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=32, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

search_button = Button(text="Search", command=search)
search_button.grid(row=1, column=2, sticky="EW")

windows.mainloop()