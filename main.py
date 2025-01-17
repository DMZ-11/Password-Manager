from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import sqlite3


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
               'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
               'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please make sure you haven't "
                                                  "let any fields empty!")

    else:

        is_ok = messagebox.askokcancel(title=website, message=f"Details: \nEmail: {email} "
                                                              f"\nPassword: {password}"
                                                              f"\nSave?")
        if is_ok:
            # Connect to a (new) database
            conn = sqlite3.connect("password_manager.db")

            # Create a cursor
            cur = conn.cursor()

            # Create a "password" table
            cur.execute('''CREATE TABLE IF NOT EXISTS password_manager (website TEXT, email TEXT, password TEXT)''')

            # Insert form data
            password_insert_query = '''INSERT INTO password_manager (website, email, password) VALUES(?, ?, ?)'''

            password_insert_tuple = (website, email, password)

            cur.execute(password_insert_query, password_insert_tuple)

            # Commit the changes
            conn.commit()

            # Close the connection
            cur.close()
            conn.close()

            # Clear form
            website_entry.delete(0, last=END)
            # email_entry.delete(0, last=END)
            password_entry.delete(0, last=END)

            website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry()
website_entry.grid(row=1, column=1, columnspan=2, sticky="EW")
website_entry.focus()

email_entry = Entry()
email_entry.grid(row=2, column=1, columnspan=2, sticky="EW")
email_entry.insert(0, "mymail@mail.com")

password_entry = Entry()
password_entry.grid(row=3, column=1, sticky="EW")

# Buttons
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="EW")

add_button = Button(text="Add", width=35, command=save)
add_button.grid(row=4, column=1, columnspan=2, sticky="EW")

window.mainloop()
