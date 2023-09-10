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
                    book_id TEXT,
                    title TEXT,
                    author TEXT,
                    publisher TEXT,
                    year_of_publish TEXT,
                    isbn TEXT,
                    pages TEXT,
                    translated_by TEXT,
                    book_genre TEXT
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

    if not (username and name and middle_name_last_name and age and address and phone_number and national_id and email and postal_code):
        messagebox.showerror("Error", "Please fill all fields")
        return

    cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (username, name, middle_name_last_name, age, address, phone_number, national_id, email, postal_code))
    conn.commit()
    messagebox.showinfo("Success", "User registered successfully")

def register_book():
    book_id = book_id_entry.get()
    title = title_entry.get()
    author = author_entry.get()
    publisher = publisher_entry.get()
    year_of_publish = year_of_publish_entry.get()
    isbn = isbn_entry.get()
    pages = pages_entry.get()
    translated_by = translated_by_entry.get()
    book_genre = book_genre_entry.get()

    if not (book_id and title and author and publisher and year_of_publish and isbn and pages and translated_by and book_genre):
        messagebox.showerror("Error", "Please fill all fields")
        return

    cursor.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   (book_id, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre))
    conn.commit()
    messagebox.showinfo("Success", "Book registered successfully")

def show_registered_users():
    cursor.execute("SELECT * FROM users")
    records = cursor.fetchall()

    users_window = tk.Toplevel(window)
    users_window.title("Registered Users")

    scrollbar = tk.Scrollbar(users_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(users_window, yscrollcommand=scrollbar.set)
    text_widget.pack()

    for record in records:
        text_widget.insert(tk.END, record)
        text_widget.insert(tk.END, "\n")

    scrollbar.config(command=text_widget.yview)

def show_registered_books():
    cursor.execute("SELECT * FROM books")
    records = cursor.fetchall()

    books_window = tk.Toplevel(window)
    books_window.title("Registered Books")

    scrollbar = tk.Scrollbar(books_window)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    text_widget = tk.Text(books_window, yscrollcommand=scrollbar.set)
    text_widget.pack()

    for record in records:
        text_widget.insert(tk.END, record)
        text_widget.insert(tk.END, "\n")

    scrollbar.config(command=text_widget.yview)

def search_records():
    book_id = book_id_entry.get()
    title = title_entry.get()
    author = author_entry.get()
    publisher = publisher_entry.get()
    year_of_publish = year_of_publish_entry.get()
    isbn = isbn_entry.get()
    pages = pages_entry.get()
    translated_by = translated_by_entry.get()
    book_genre = book_genre_entry.get()

    if any([book_id, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre]):
        cursor.execute("SELECT * FROM books WHERE book_id=? OR title=? OR author=? OR publisher=? OR year_of_publish=? OR isbn=? OR pages=? OR translated_by=? OR book_genre=?",
                       (book_id, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre))
        records = cursor.fetchall()

        messagebox.showinfo("Search Results", records)

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

        messagebox.showinfo("Search Results", records)

window = tk.Tk()
window.title("Registry")
window.configure(bg="darkblue")
window.geometry("700x500")
window.resizable(False,False)

left_pane = tk.Frame(window)
left_pane.config(bg="darkblue")
left_pane.pack(side=tk.LEFT, padx=10, pady=10)

left_header_label = tk.Label(left_pane, text="User Registry", font="bold")
left_header_label.config(bg="lightblue")
left_header_label.pack(pady=10)

username_label = tk.Label(left_pane, text="Username from library")
username_label.config(bg="lightblue")
username_label.pack()
username_entry = tk.Entry(left_pane)
username_entry.config(bg="lightblue")
username_entry.pack()

name_label = tk.Label(left_pane, text="Name")
name_label.config(bg="lightblue")
name_label.pack()
name_entry = tk.Entry(left_pane)
name_entry.config(bg="lightblue")
name_entry.pack()

middle_name_last_name_label = tk.Label(left_pane, text="Middle Name & Last Name")
middle_name_last_name_label.config(bg="lightblue")
middle_name_last_name_label.pack()
middle_name_last_name_entry = tk.Entry(left_pane)
middle_name_last_name_entry.config(bg="lightblue")
middle_name_last_name_entry.pack()

age_label = tk.Label(left_pane, text="Age")
age_label.config(bg="lightblue")
age_label.pack()
age_entry = tk.Entry(left_pane)
age_entry.config(bg="lightblue")
age_entry.pack()

address_label = tk.Label(left_pane, text="Address")
address_label.config(bg="lightblue")
address_label.pack()
address_entry = tk.Entry(left_pane)
address_entry.config(bg="lightblue")
address_entry.pack()

phone_number_label = tk.Label(left_pane, text="Phone Number")
phone_number_label.config(bg="lightblue")
phone_number_label.pack()
phone_number_entry = tk.Entry(left_pane)
phone_number_entry.config(bg="lightblue")
phone_number_entry.pack()

national_id_label = tk.Label(left_pane, text="National ID")
national_id_label.config(bg="lightblue")
national_id_label.pack()
national_id_entry = tk.Entry(left_pane)
national_id_entry.config(bg="lightblue")
national_id_entry.pack()

email_label = tk.Label(left_pane, text="Email")
email_label.config(bg="lightblue")
email_label.pack()
email_entry = tk.Entry(left_pane)
email_entry.config(bg="lightblue")
email_entry.pack()

postal_code_label = tk.Label(left_pane, text="Postal Code")
postal_code_label.config(bg="lightblue")
postal_code_label.pack()
postal_code_entry = tk.Entry(left_pane)
postal_code_entry.config(bg="lightblue")
postal_code_entry.pack()

register_user_button = tk.Button(left_pane, text="Register User", command=register_user)
register_user_button.config(bg="#00ff00", height="2")
register_user_button.pack(pady=10)

right_pane = tk.Frame(window)
right_pane.config(bg="darkblue")
right_pane.pack(side=tk.RIGHT, padx=10, pady=10)

right_header_label = tk.Label(right_pane, text="Books Registry", font="bold")
right_header_label.config(bg="lightblue")
right_header_label.pack(pady=10)

book_id_label = tk.Label(right_pane, text="Book ID from library")
book_id_label.config(bg="lightblue")
book_id_label.pack()
book_id_entry = tk.Entry(right_pane)
book_id_entry.config(bg="lightblue")
book_id_entry.pack()

title_label = tk.Label(right_pane, text="Title")
title_label.config(bg="lightblue")
title_label.pack()
title_entry = tk.Entry(right_pane)
title_entry.configure(bg="lightblue")
title_entry.pack()

author_label = tk.Label(right_pane, text="Author")
author_label.config(bg="lightblue")
author_label.pack()
author_entry = tk.Entry(right_pane)
author_entry.config(bg="lightblue")
author_entry.pack()

publisher_label = tk.Label(right_pane, text="Publisher")
publisher_label.config(bg="lightblue")
publisher_label.pack()
publisher_entry = tk.Entry(right_pane)
publisher_entry.config(bg="lightblue")
publisher_entry.pack()

year_of_publish_label = tk.Label(right_pane, text="Year of Publish")
year_of_publish_label.pack()
year_of_publish_label.config(bg="lightblue")
year_of_publish_entry = tk.Entry(right_pane)
year_of_publish_entry.config(bg="lightblue")
year_of_publish_entry.pack()

isbn_label = tk.Label(right_pane, text="ISBN")
isbn_label.config(bg="lightblue")
isbn_label.pack()
isbn_entry = tk.Entry(right_pane)
isbn_entry.config(bg="lightblue")
isbn_entry.pack()

pages_label = tk.Label(right_pane, text="Pages")
pages_label.config(bg="lightblue")
pages_label.pack()
pages_entry = tk.Entry(right_pane)
pages_entry.config(bg="lightblue")
pages_entry.pack()

translated_by_label = tk.Label(right_pane, text="Translated By")
translated_by_label.config(bg="lightblue")
translated_by_label.pack()
translated_by_entry = tk.Entry(right_pane)
translated_by_entry.config(bg="lightblue")
translated_by_entry.pack()

book_genre_label = tk.Label(right_pane, text="Book Genre")
book_genre_label.config(bg="lightblue")
book_genre_label.pack()
book_genre_entry = tk.Entry(right_pane)
book_genre_entry.config(bg="lightblue")
book_genre_entry.pack()

register_book_button = tk.Button(right_pane, text="Register Book", command=register_book)
register_book_button.config(bg="#00ff00", height="2")
register_book_button.pack(pady=10)

bottom_frame = tk.Frame(window)
bottom_frame.config(bg="darkblue")
bottom_frame.pack(pady=10)

show_registered_users_button = tk.Button(bottom_frame, text="Show Registered Users", bg="#00ff00", width="17", height="3", command=show_registered_users)
show_registered_users_button.pack(side=tk.LEFT, padx=10)

show_registered_books_button = tk.Button(bottom_frame, text="Show Registered Books", bg="#00ff00", width="17", height="3", command=show_registered_books)
show_registered_books_button.pack(side=tk.LEFT, padx=10)

investigator_button = tk.Button(bottom_frame, text="Investigator", bg="#00ff00", width="9", height="3", command=search_records)
investigator_button.pack(side=tk.LEFT, padx=10)

window.mainloop()

conn.close()