# Register Users and Books

import tkinter as tk
from tkinter import messagebox
import sqlite3

conn = sqlite3.connect("registry.db")
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    username TEXT,
                    name TEXT,
                    middle_name_last_name TEXT,
                    age INTEGER,
                    address TEXT,
                    phone_number TEXT,
                    national_id TEXT,
                    email TEXT,
                    postal_code TEXT
                )""")

cursor.execute("""CREATE TABLE IF NOT EXISTS books (
                    category TEXT,
                    book_id TEXT,
                    title TEXT,
                    author TEXT,
                    publisher TEXT,
                    year_of_publish TEXT,
                    isbn TEXT,
                    pages TEXT,
                    translated_by TEXT,
                    book_genre TEXT,
                    description TEXT
                )""")

def register_user():
    username = username_entry.get()
    name = name_entry.get()
    middle_name_last_name = middle_name_last_name_entry.get()
    age = age_entry.get()
    address = address_entry.get()
    phone_number = phone_number_entry.get()
    national_id = national_id_entry.get()
    email = email_entry.get()
    postal_code = postal_code_entry.get()

    username_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    middle_name_last_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_number_entry.delete(0, tk.END)
    national_id_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    postal_code_entry.delete(0, tk.END)

    if not (username and name and middle_name_last_name and age and address and phone_number and national_id and email and postal_code):
        messagebox.showerror("Error", "Please fill all fields")
        return

    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (username, name, middle_name_last_name, age, address, phone_number, national_id, email, postal_code))
    conn.commit()
    messagebox.showinfo("Success", "User registered successfully")

def register_book():
    category = category_var.get()
    book_id = book_id_entry.get()
    title = title_entry.get()
    author = author_entry.get()
    publisher = publisher_entry.get()
    year_of_publish = year_of_publish_entry.get()
    isbn = isbn_entry.get()
    pages = pages_entry.get()
    translated_by = translated_by_entry.get()
    book_genre = book_genre_entry.get()
    description = description_entry.get()

    book_id_entry.delete(0, tk.END)
    title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    publisher_entry.delete(0, tk.END)
    year_of_publish_entry.delete(0, tk.END)
    isbn_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)
    translated_by_entry.delete(0, tk.END)
    book_genre_entry.delete(0, tk.END)
    description_entry.delete(0, tk.END)

    if not (category and book_id and title and author and publisher and year_of_publish and isbn and pages and translated_by and book_genre and description):
        messagebox.showerror("Error", "Please fill all fields")
        return

    cursor.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (category, book_id, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre, description))
    conn.commit()
    messagebox.showinfo("Success", "Book registered successfully")

def show_registered_users():
    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()

    users_window = tk.Toplevel(window)
    users_window.title("Registered Users")

    xscrollbar = tk.Scrollbar(users_window, orient=tk.HORIZONTAL)
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    yscrollbar = tk.Scrollbar(users_window)
    yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(users_window, wrap=tk.NONE, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    text_widget.pack(expand=True, fill=tk.BOTH)

    for record in records:
        formatted_record = " ~~~~~~ ".join(str(data) for data in record)
        text_widget.insert(tk.END, formatted_record)
        text_widget.insert(tk.END, "\n")
        text_widget.insert(tk.END, "\n")

    xscrollbar.config(command=text_widget.xview)
    yscrollbar.config(command=text_widget.yview)

def show_registered_books():
    cursor.execute("SELECT * FROM books")
    records = cursor.fetchall()

    books_window = tk.Toplevel(window)
    books_window.title("Registered Books")

    xscrollbar = tk.Scrollbar(books_window, orient=tk.HORIZONTAL)
    xscrollbar.pack(side=tk.BOTTOM, fill=tk.X)

    yscrollbar = tk.Scrollbar(books_window)
    yscrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(books_window, wrap=tk.NONE, xscrollcommand=xscrollbar.set, yscrollcommand=yscrollbar.set)
    text_widget.pack(expand=True, fill=tk.BOTH)

    for record in records:
        formatted_record = " ~~~~~~ ".join(str(data) for data in record)
        text_widget.insert(tk.END, formatted_record)
        text_widget.insert(tk.END, "\n")
        text_widget.insert(tk.END, "\n")

    xscrollbar.config(command=text_widget.xview)
    yscrollbar.config(command=text_widget.yview)

def search_records():
    category = category_var.get()
    book_id = book_id_entry.get()
    title = title_entry.get()
    author = author_entry.get()
    publisher = publisher_entry.get()
    year_of_publish = year_of_publish_entry.get()
    isbn = isbn_entry.get()
    pages = pages_entry.get()
    translated_by = translated_by_entry.get()
    book_genre = book_genre_entry.get()
    description = description_entry.get()

    if any([category, book_id, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre, description]):
        cursor.execute("SELECT * FROM books WHERE category=? OR book_id=? OR title=? OR author=? OR publisher=? OR year_of_publish=? OR isbn=? OR pages=? OR translated_by=? OR book_genre=? OR description=?",
                       (category, book_id, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre, description))
        records = cursor.fetchall()

        if len(records) > 0:
            for i in records:
                messagebox.showinfo("Search Results", str(i).join("~~"))
        else:
            messagebox.showerror("Error", "No records to show!")

    username = username_entry.get()
    name = name_entry.get()
    middle_name_last_name = middle_name_last_name_entry.get()
    age = age_entry.get()
    address = address_entry.get()
    phone_number = phone_number_entry.get()
    national_id = national_id_entry.get()
    email = email_entry.get()
    postal_code = postal_code_entry.get()

    if any([username, name, middle_name_last_name, age, address, phone_number, national_id, email, postal_code]):
        cursor.execute("SELECT * FROM users WHERE username=? OR name=? OR middle_name_last_name=? OR age=? OR address=? OR phone_number=? OR national_id=? OR email=? OR postal_code=?",
                       (username, name, middle_name_last_name, age, address, phone_number, national_id, email, postal_code))
        records = cursor.fetchall()

        if len(records) > 0:
            for i in records:
                messagebox.showinfo("Search Results", str(i).join("~~"))
        else:
            messagebox.showerror("Error", "No records to show!")

def delete_book():

    booktitle = book_title_delete.get()

    cursor.execute("DELETE FROM books WHERE title=?", (booktitle,))
    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Deleted", "Book has been deleted.")
    else:
        messagebox.showerror("Error", "Book not found.")

    book_title_delete.delete(0, tk.END)

def delete_user():

    username = user_name_delete.get()

    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Deleted", "User has been deleted.")
    else:
        messagebox.showerror("Error", "User not found.")

    user_name_delete.delete(0, tk.END)

def exit_the_program():
    window.destroy()

window = tk.Tk()
window.title("Registry")
window.configure(bg="darkblue")
window.geometry("900x1100")
window.resizable(False,False)

left_pane = tk.Frame(window)
left_pane.config(bg="darkblue")
left_pane.pack(side=tk.LEFT, padx=10, pady=10)

left_header_label = tk.Label(left_pane, text="User Registry", font=("bold"))
left_header_label.config(bg="lightblue", font="impact 20", fg="#0000ff")
left_header_label.pack(pady=30)

username_label = tk.Label(left_pane, text="Username from library")
username_label.config(bg="lightblue")
username_label.pack(pady=7)
username_entry = tk.Entry(left_pane)
username_entry.config(bg="lightblue")
username_entry.pack()

space1 = tk.Label(left_pane, text="")
space1.configure(bg="darkblue")
space1.pack()

name_label = tk.Label(left_pane, text="Name")
name_label.config(bg="lightblue")
name_label.pack(pady=7)
name_entry = tk.Entry(left_pane)
name_entry.config(bg="lightblue")
name_entry.pack()

space2 = tk.Label(left_pane, text="")
space2.configure(bg="darkblue")
space2.pack()

middle_name_last_name_label = tk.Label(left_pane, text="Middle Name & Last Name")
middle_name_last_name_label.config(bg="lightblue")
middle_name_last_name_label.pack(pady=7)
middle_name_last_name_entry = tk.Entry(left_pane)
middle_name_last_name_entry.config(bg="lightblue")
middle_name_last_name_entry.pack()

space3 = tk.Label(left_pane, text="")
space3.configure(bg="darkblue")
space3.pack()

age_label = tk.Label(left_pane, text="Age")
age_label.config(bg="lightblue")
age_label.pack(pady=7)
age_entry = tk.Entry(left_pane)
age_entry.config(bg="lightblue")
age_entry.pack()

space4 = tk.Label(left_pane, text="")
space4.configure(bg="darkblue")
space4.pack()

address_label = tk.Label(left_pane, text="Address")
address_label.config(bg="lightblue")
address_label.pack(pady=7)
address_entry = tk.Entry(left_pane)
address_entry.config(bg="lightblue")
address_entry.pack()

space5 = tk.Label(left_pane, text="")
space5.configure(bg="darkblue")
space5.pack()

phone_number_label = tk.Label(left_pane, text="Phone Number")
phone_number_label.config(bg="lightblue")
phone_number_label.pack(pady=7)
phone_number_entry = tk.Entry(left_pane)
phone_number_entry.config(bg="lightblue")
phone_number_entry.pack()

space6 = tk.Label(left_pane, text="")
space6.configure(bg="darkblue")
space6.pack()

national_id_label = tk.Label(left_pane, text="National ID")
national_id_label.config(bg="lightblue")
national_id_label.pack(pady=7)
national_id_entry = tk.Entry(left_pane)
national_id_entry.config(bg="lightblue")
national_id_entry.pack()

space7 = tk.Label(left_pane, text="")
space7.configure(bg="darkblue")
space7.pack()

email_label = tk.Label(left_pane, text="Email")
email_label.config(bg="lightblue")
email_label.pack(pady=7)
email_entry = tk.Entry(left_pane)
email_entry.config(bg="lightblue")
email_entry.pack()

space8 = tk.Label(left_pane, text="")
space8.configure(bg="darkblue")
space8.pack()

postal_code_label = tk.Label(left_pane, text="Postal Code")
postal_code_label.config(bg="lightblue")
postal_code_label.pack(pady=7)
postal_code_entry = tk.Entry(left_pane)
postal_code_entry.config(bg="lightblue")
postal_code_entry.pack()

space9 = tk.Label(left_pane, text="")
space9.configure(bg="darkblue")
space9.pack()

register_user_button = tk.Button(left_pane, text="Register User", command=register_user)
register_user_button.config(bg="#00ff00", height="2")
register_user_button.pack(pady=10)

middleframe1 = tk.Frame(window)
middleframe1.config(bg="darkblue")
middleframe1.pack(side=tk.BOTTOM, padx=8, pady=9)
middleframe1.place(relx=0.5, rely=0.18, anchor=tk.N)

middlelabel1 = tk.Label(middleframe1, text="Anything Else! \u23CE", font="bold")
middlelabel1.config(bg="lightblue", font="impact 20", fg="#0000ff")
middlelabel1.pack(pady=30)

middleframe2 = tk.Frame(window)
middleframe2.config(bg="darkblue")
middleframe2.pack(side=tk.BOTTOM, padx=8, pady=9)
middleframe2.place(relx=0.5, rely=0.45, anchor=tk.N)

middlelabel2 = tk.Label(middleframe2, text="_______OR_______", font="bold")
middlelabel2.config(bg="darkblue", font="impact 20", fg="#00ff00")
middlelabel2.pack(pady=30)

middleframe3 = tk.Frame(window)
middleframe3.config(bg="darkblue")
middleframe3.pack(side=tk.BOTTOM, padx=8, pady=9)
middleframe3.place(relx=0.5, rely=0.8, anchor=tk.N)

exit_button = tk.Button(middleframe3, text="Exit", bg="purple", fg="yellow", relief="sunken", command=exit_the_program, font="Arial 17 bold")
exit_button.pack()

middle_frame_books = tk.Frame(window)
middle_frame_books.config(bg="darkblue")
middle_frame_books.pack(side=tk.BOTTOM, padx=8,pady=8)
middle_frame_books.place(relx=0.5, rely=0.35, anchor=tk.N)

book_title_delete_label = tk.Label(middle_frame_books, text="Title of the Book to Delete:", bg="yellow", fg="red", font="bold", width=25)
book_title_delete_label.pack()
book_title_delete = tk.Entry(middle_frame_books, width=50)
book_title_delete.pack(pady=2)
book_title_delete_button = tk.Button(middle_frame_books, text="Delete the Book", command=delete_book, bg="red", fg="yellow", font="boldest", width=15, relief="raised")
book_title_delete_button.pack(pady=5)

middle_frame_users = tk.Frame(window)
middle_frame_users.config(bg="darkblue")
middle_frame_users.pack(side=tk.BOTTOM, padx=8,pady=8)
middle_frame_users.place(relx=0.5, rely=0.6, anchor=tk.N)

user_name_delete_label = tk.Label(middle_frame_users, text="Username to Delete:", bg="yellow", fg="red", font="bold", width=25)
user_name_delete_label.pack()
user_name_delete = tk.Entry(middle_frame_users, width=50)
user_name_delete.pack(pady=2)
user_name_delete_button = tk.Button(middle_frame_users, text="Delete User", command=delete_user, bg="red", fg="yellow", font="boldest", width=15, relief="raised")
user_name_delete_button.pack(pady=5)

right_pane = tk.Frame(window)
right_pane.config(bg="darkblue")
right_pane.pack(side=tk.RIGHT, padx=10, pady=10)

space21 = tk.Label(right_pane, text="")
space21.configure(bg="darkblue", height=1)
space21.pack()

right_header_label = tk.Label(right_pane, text="Book Registry", font="bold")
right_header_label.config(bg="lightblue", font="impact 20", fg="#0000ff")
right_header_label.pack(pady=30)

category_label = tk.Label(right_pane, text="Book Category")
category_label.config(bg="lightblue")
category_label.pack(pady=7)
category_var = tk.StringVar(right_pane)
categories = ["Engineering", "Meta Physics", "Mathematics", "Motivational", "Narrative", "Comedy", "Memoir", "Fiction", "History", "Poetry", "Science", "Novel", "Phsychology", "Romance",
              "Academic", "Entertainment", "Science Fiction", "IT and Technology", "Biology", "Religious", "Spirituality", "Artificial Intelligence", "Correlated Artbook", "Geography",
              "Astrology", "Crime Fiction", "Antropology", "Robotics", "Graphics", "Video Game Franchise Books", "Relationship-Help", "Children", "Folklore", "Music",
              "Survival-Horror Fiction", "Self Improvement", "Historical Fiction", "Biography", "Thriller", "Inspired by True stories",
              "Mystery", "Art", "Ethnic and Culture", "Fantasy", "Other"]
category_var = tk.StringVar(right_pane)
category_var.set(categories[0])
category_dropdown = tk.OptionMenu(right_pane, category_var, *categories)
category_dropdown.config(font=("bold", 8), background="lightblue")
category_dropdown.pack()

space10 = tk.Label(right_pane, text="")
space10.configure(bg="darkblue")
space10.pack()

book_id_label = tk.Label(right_pane, text="Book ID from library")
book_id_label.config(bg="lightblue")
book_id_label.pack(pady=7)
book_id_entry = tk.Entry(right_pane)
book_id_entry.config(bg="lightblue")
book_id_entry.pack()

space11 = tk.Label(right_pane, text="")
space11.configure(bg="darkblue")
space11.pack()

title_label = tk.Label(right_pane, text="Title")
title_label.config(bg="lightblue")
title_label.pack(pady=7)
title_entry = tk.Entry(right_pane)
title_entry.configure(bg="lightblue")
title_entry.pack()

space12 = tk.Label(right_pane, text="")
space12.configure(bg="darkblue")
space12.pack()

author_label = tk.Label(right_pane, text="Author")
author_label.config(bg="lightblue")
author_label.pack(pady=7)
author_entry = tk.Entry(right_pane)
author_entry.config(bg="lightblue")
author_entry.pack()

space13 = tk.Label(right_pane, text="")
space13.configure(bg="darkblue")
space13.pack()

publisher_label = tk.Label(right_pane, text="Publisher")
publisher_label.config(bg="lightblue")
publisher_label.pack(pady=7)
publisher_entry = tk.Entry(right_pane)
publisher_entry.config(bg="lightblue")
publisher_entry.pack()

space14 = tk.Label(right_pane, text="")
space14.configure(bg="darkblue")
space14.pack()

year_of_publish_label = tk.Label(right_pane, text="Year of Publish")
year_of_publish_label.pack(pady=7)
year_of_publish_label.config(bg="lightblue")
year_of_publish_entry = tk.Entry(right_pane)
year_of_publish_entry.config(bg="lightblue")
year_of_publish_entry.pack()

space15 = tk.Label(right_pane, text="")
space15.configure(bg="darkblue")
space15.pack()

isbn_label = tk.Label(right_pane, text="ISBN")
isbn_label.config(bg="lightblue")
isbn_label.pack(pady=7)
isbn_entry = tk.Entry(right_pane)
isbn_entry.config(bg="lightblue")
isbn_entry.pack()

space16 = tk.Label(right_pane, text="")
space16.configure(bg="darkblue")
space16.pack()

pages_label = tk.Label(right_pane, text="Pages")
pages_label.config(bg="lightblue")
pages_label.pack(pady=7)
pages_entry = tk.Entry(right_pane)
pages_entry.config(bg="lightblue")
pages_entry.pack()

space17 = tk.Label(right_pane, text="")
space17.configure(bg="darkblue")
space17.pack()

translated_by_label = tk.Label(right_pane, text="Translated By")
translated_by_label.config(bg="lightblue")
translated_by_label.pack(pady=7)
translated_by_entry = tk.Entry(right_pane)
translated_by_entry.config(bg="lightblue")
translated_by_entry.pack()

space18 = tk.Label(right_pane, text="")
space18.configure(bg="darkblue")
space18.pack()

book_genre_label = tk.Label(right_pane, text="Book Genre")
book_genre_label.config(bg="lightblue")
book_genre_label.pack(pady=7)
book_genre_entry = tk.Entry(right_pane)
book_genre_entry.config(bg="lightblue")
book_genre_entry.pack()

space19 = tk.Label(right_pane, text="")
space19.configure(bg="darkblue")
space19.pack()

description_label = tk.Label(right_pane, text="Book Description")
description_label.config(bg="lightblue")
description_label.pack(pady=7)
description_entry = tk.Entry(right_pane)
description_entry.config(bg="lightblue")
description_entry.pack()

space20 = tk.Label(right_pane, text="")
space20.configure(bg="darkblue")
space20.pack()

register_book_button = tk.Button(right_pane, text="Register Book", command=register_book)
register_book_button.config(bg="#00ff00", height="2")
register_book_button.pack(pady=0)

upper_frame = tk.Frame(window)
upper_frame.config(bg="darkblue")
upper_frame.pack(side=tk.TOP, pady=6)

show_registered_users_button = tk.Button(upper_frame, text="Show Registered Users", bg="#00ff00", width="17", height="3", command=show_registered_users)
show_registered_users_button.pack(side=tk.LEFT,padx=1)

show_registered_books_button = tk.Button(upper_frame, text="Show Registered Books", bg="#00ff00", width="17", height="3", command=show_registered_books)
show_registered_books_button.pack(side=tk.LEFT,padx=1)

investigator_button = tk.Button(upper_frame, text="Investigator", bg="#00ff00", width="10", height="3", command=search_records)
investigator_button.pack(side=tk.LEFT,padx=1)

window.mainloop()

conn.close()
