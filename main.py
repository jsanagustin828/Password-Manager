import json
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


# --------------Password Generator ----------------#

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for char in range(nr_letters)]
    password_list += [random.choice(symbols) for symbol in range(nr_symbols)]
    password_list += [random.choice(numbers) for num in range(nr_numbers)]

    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, f"{password}")
    pyperclip.copy(password)


# ---------------Functionality ------------------#

def find_password():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError as e:
        messagebox.showinfo(message=f"Could not find file. Enter data first.")
    else:
        if website in data:
            dict_email = data[website]["Email"]
            dict_password = data[website]["Password"]
            messagebox.showinfo(title="Info", message=f"Email: {dict_email}\nPassword: {dict_password}")
        elif website not in data:
            messagebox.showinfo(message=f"{website} not in the database.")


def save():
    website_txt = website_entry.get()
    user_email_txt = email_usrname_entry.get()
    password_txt = password_entry.get()

    new_data = {
        website_txt: {
            "Email": user_email_txt,
            "Password": password_txt
        }
    }

    if user_email_txt == "" or password_txt == "":
        messagebox.showinfo(title="Empty Fields", message="Don't leave any empty fields!")
    else:
        is_ok = messagebox.askokcancel(title="Title",
                                       message=f"You entered the following:\n\nEmail: {user_email_txt}\nPassword: {password_txt}"
                                               f"\n\nAre you okay to save this?")
        # if is_ok:
        #     with open("./data.txt", mode="a") as data_file:
        #         data_file.write(f"{website_txt} | {user_email_txt} | {password_txt}\n")

        # with open("./data.json", "w") as data_file:
        #     json.dump(new_data, data_file, indent=4)

        if is_ok:
            try:
                with open("./data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("./data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                data.update(new_data)

                with open("./data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ------------------ UI ------------------------ #
# Window
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = Canvas(width=200, height=200, highlightthickness=0)
my_pass_img = PhotoImage(file="./logo.png")
canvas.create_image(100, 100, image=my_pass_img)
canvas.grid(column=1, row=0)

# Website label
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

# Email/Username label
email_usrname = Label(text="Email/Username:")
email_usrname.grid(column=0, row=2)

# Password Label
password = Label(text="Password:")
password.grid(column=0, row=3)

# Website Entry
website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)

# Email/Username Entry
email_usrname_entry = Entry(width=36)
email_usrname_entry.grid(column=1, row=2, columnspan=2)
email_usrname_entry.focus()
email_usrname_entry.insert(0, "dummyemail@gmail.com")

# Password Entry
password_entry = Entry(width=21)
password_entry.grid(column=1, row=3)

# Search Button
search_btn = Button(text="Search", width=11, command=find_password)
search_btn.grid(column=2, row=1)

# Generate Password Button
generate_pwd_btn = Button(text="Generate Password", command=generate_password, width=11)
generate_pwd_btn.grid(column=2, row=3)

# Add Button
add_btn = Button(text="Add", width=34, command=save)
add_btn.grid(column=1, row=4, columnspan=3)

window.mainloop()
