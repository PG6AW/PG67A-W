# Register Users and Books

import tkinter as tk
from tkinter import messagebox , ttk
import sqlite3
import datetime
import getpass

conn = sqlite3.connect("registry.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    username TEXT UNIQUE,
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
                    book_id INTEGER UNIQUE,
                    title TEXT,
                    author TEXT,
                    publisher TEXT,
                    year_of_publish INTEGER,
                    isbn TEXT,
                    pages INTEGER,
                    translated_by TEXT,
                    book_genre TEXT,
                    description TEXT
                )""")
conn.commit()

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

    if str(age) != "" :
        try:
            age = int(age)
        except ValueError:
            messagebox.showerror("Inappropriate Value", "Please enter a Number for 'Age'!")
            return

    if not (username and name and middle_name_last_name and age and address and phone_number and national_id and email and postal_code):
        messagebox.showerror("Error", "Please fill all fields")
        return

    confirm_submission = messagebox.askyesno("Submission Confirmation", "Are you sure you're going to submit User data into database? Always Double-Check before you're sure to confirm!!")
    if confirm_submission:
        pass
    else:
        return

    try:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (username, name, middle_name_last_name, age, address, phone_number, national_id, email, postal_code))
        conn.commit()
        messagebox.showinfo("Success", "User registered successfully")
    except sqlite3.IntegrityError:
        cursor.execute(
            "UPDATE users SET name=?, middle_name_last_name=?, age=?, address=?, phone_number=?, national_id=?, email=?, postal_code=? WHERE username=?", (name, middle_name_last_name, age, address, phone_number, national_id, email, postal_code, username))
        conn.commit()
        messagebox.showinfo("Updated", "User info has been updated!")

    current_username = getpass.getuser()
    event_by_admin = current_username
    conn1 = sqlite3.connect("event_logs.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""CREATE TABLE IF NOT EXISTS registered_users (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    name TEXT,
                    middle_name_last_name TEXT,
                    age INTEGER,
                    address TEXT,
                    phone_number TEXT,
                    national_id TEXT,
                    email TEXT,
                    postal_code TEXT,
                    event_by_admin TEXT,
                    event_date TEXT
                    )""")
    conn1.commit()

    cursor1.execute("INSERT INTO registered_users (username, name, middle_name_last_name, age, address, phone_number, national_id, email, postal_code, event_by_admin, event_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (username, name, middle_name_last_name, age, address, phone_number, national_id, email, postal_code, event_by_admin, datetime.datetime.now()))
    conn1.commit()
    conn1.close()

    username_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    middle_name_last_name_entry.delete(0, tk.END)
    age_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    phone_number_entry.delete(0, tk.END)
    national_id_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    postal_code_entry.delete(0, tk.END)

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

    if book_id != "":
        try:
            book_id = int(book_id)
        except ValueError:
            messagebox.showerror("Inappropriate Value", "Please enter a Number for 'Book ID'!")
            return
    if year_of_publish != "":
        try:
            year_of_publish = int(year_of_publish)
        except ValueError:
            messagebox.showerror("Inappropriate Value", "Please enter a Number for 'Year of Publish'!")
            return
    if pages !="":
        try:
            pages = int(pages)
        except ValueError:
            messagebox.showerror("Inappropriate Value", "Please enter a Number for 'Pages'!")
            return

    if category == "SELECT_FROM_DROPDOWN" :
        messagebox.showerror("Error __Not_Selected__", "Please first select a Book_Category from the Dropdown_Menu!")
        return

    if not (category and book_id and title and author and publisher and year_of_publish and isbn and pages and translated_by and book_genre and description):
        messagebox.showerror("Error", "Please fill all fields")
        return

    confirm_submission = messagebox.askyesno("Submission Confirmation", "Are you sure you're going to submit book data into database? Always Double-Check before you're sure to confirm!!")
    if confirm_submission:
        pass
    else:
        return
    try:
        cursor.execute("INSERT INTO books VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (category, book_id, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre, description))
        conn.commit()
        messagebox.showinfo("Success", "Book registered successfully")
    except sqlite3.IntegrityError:
        cursor.execute("UPDATE books SET category=?, title=?, author=?, publisher=?, year_of_publish=?, isbn=?, pages=?, translated_by=?, book_genre=?, description=? WHERE book_id=?", (category, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre, description, book_id))
        conn.commit()
        messagebox.showinfo("Updated", "Book info has been updated!")

    current_username = getpass.getuser()
    event_by_admin = current_username
    conn1 = sqlite3.connect("event_logs.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""CREATE TABLE IF NOT EXISTS registered_books (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT,
                    book_id INTEGER,
                    title TEXT,
                    author TEXT,
                    publisher TEXT,
                    year_of_publish INTEGER,
                    isbn TEXT,
                    pages INTEGER,
                    translated_by TEXT,
                    book_genre TEXT,
                    description TEXT,
                    event_by_admin TEXT,
                    event_date TEXT
                    )""")
    conn1.commit()

    cursor1.execute("INSERT INTO registered_books (category, book_id, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre, description, event_by_admin, event_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (category, book_id, title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre, description, event_by_admin, datetime.datetime.now()))
    conn1.commit()
    conn1.close()

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
    hint_message = messagebox.askyesno("Hint", "By typing data in one or multiple fields of either User registry column or Book registry column down below and then firing the 'Investigator' button, you can search for books and users.\n\nPlease note that this can also work as a combined-data search by inputting multiple fields. It'll pop a record for each set of matching criteria ONLY if they exist!\n\n-- CONTINUE? --")
    if hint_message:
        pass
    else:
        return

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

    if str(booktitle) == "":
        messagebox.showerror("Error", "Empty Field!")
        return
    
    delete_confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you're going to delete the specified Book?")
    if delete_confirmation:
        pass
    else:
        return

    cursor.execute("DELETE FROM books WHERE title=?", (booktitle,))
    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Deleted", "Book has been deleted.")
        pass
    else:
        messagebox.showerror("Error", "Book not found.")
        return

    current_username = getpass.getuser()
    event_by_admin = current_username
    conn1 = sqlite3.connect("event_logs.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""CREATE TABLE IF NOT EXISTS deleted_registered_books (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_title TEXT,
                    event_by_admin TEXT,
                    event_date TEXT
                    )""")
    conn1.commit()

    cursor1.execute("INSERT INTO deleted_registered_books (book_title, event_by_admin, event_date) VALUES (?, ?, ?)",
                (booktitle, event_by_admin, datetime.datetime.now()))
    conn1.commit()
    conn1.close()

    book_title_delete.delete(0, tk.END)

def delete_user():

    username = user_name_delete.get()

    if str(username) == "":
        messagebox.showerror("Error", "Empty Field!")
        return
    
    delete_confirmation = messagebox.askyesno("Confirm Deletion", "Are you sure you're going to delete the specified User?")
    if delete_confirmation:
        pass
    else:
        return

    cursor.execute("DELETE FROM users WHERE username=?", (username,))
    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Deleted", "User has been deleted.")
        pass
    else:
        messagebox.showerror("Error", "User not found.")
        return

    current_username = getpass.getuser()
    event_by_admin = current_username
    conn1 = sqlite3.connect("event_logs.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""CREATE TABLE IF NOT EXISTS deleted_registered_users (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    event_by_admin TEXT,
                    event_date TEXT
                    )""")
    conn1.commit()

    cursor1.execute("INSERT INTO deleted_registered_users (username, event_by_admin, event_date) VALUES (?, ?, ?)",
                (username, event_by_admin, datetime.datetime.now()))
    conn1.commit()
    conn1.close()

    user_name_delete.delete(0, tk.END)

def exit_the_program():
    answer = messagebox.askyesno("Quit Message", "Are you sure you're going to quit the registry administrator environment?")
    if answer:
        conn.close()
        window.destroy()
    else:
        pass

def insert_to_users():
    conn = sqlite3.connect("registry.db")
    cursor = conn.cursor()
    username = username_entry.get()
    if username == "":
        messagebox.showerror("User Not Addressed", "To use this feature, you need to type at least a registered Username!\n\nHint: This feature allows you to modify User details with more convenience and without requiring you to type every single entry again so this way you can simply read over the details and change only what has to be updated.\nAll in All, its function aims to ensure higher precision and an optimal time management!")
        return
    try:
        if username:
            query = "SELECT name, middle_name_last_name, age, address, phone_number, national_id, email, postal_code FROM users WHERE username=?"
            cursor.execute(query, (username,))
            fetched = cursor.fetchall()
            if fetched is None:
                fetched = str(fetched)
            else:
                fetched = list(fetched)
                for i in fetched:
                    i = list(tuple(i))
                name_entry.delete(0, tk.END)
                name_entry.insert(tk.END, str(i[0]))
                middle_name_last_name_entry.delete(0, tk.END)
                middle_name_last_name_entry.insert(tk.END, str(i[1]))
                age_entry.delete(0, tk.END)
                age_entry.insert(tk.END, str(i[2]))
                address_entry.delete(0, tk.END)
                address_entry.insert(tk.END, str(i[3]))
                phone_number_entry.delete(0, tk.END)
                phone_number_entry.insert(tk.END, str(i[4]))
                national_id_entry.delete(0, tk.END)
                national_id_entry.insert(tk.END, str(i[5]))
                email_entry.delete(0, tk.END)
                email_entry.insert(tk.END, str(i[6]))
                postal_code_entry.delete(0, tk.END)
                postal_code_entry.insert(tk.END, str(i[7]))
        else:
            messagebox.showerror("error", "Seems local database is raw and fresh. Therefore, no sorta detail were currently returned!")
            return
    except UnboundLocalError:
        messagebox.showerror("error", "Invalid Username! There could be a reason that this User is yet not available in the local database!")
        return

def insert_to_books():
    conn = sqlite3.connect("registry.db")
    cursor = conn.cursor()
    Id = book_id_entry.get()
    if Id == "":
        messagebox.showerror("Book Not Addressed", "To use this feature, you need to type at least a registered Book ID!\n\nHint: This feature allows you to modify Book details with more convenience and without requiring you to type every single entry again so this way you can simply read over the details and change only what has to be updated.\nAll in All, its function aims to ensure higher precision and an optimal time management!")
        return
    try:
        if Id:
            query = "SELECT title, author, publisher, year_of_publish, isbn, pages, translated_by, book_genre, description FROM books WHERE book_id=?"
            cursor.execute(query, (Id,))
            fetched = cursor.fetchall()
            if fetched is None:
                fetched = str(fetched)
            else:
                fetched = list(fetched)
                for i in fetched:
                    i = list(tuple(i))
                title_entry.delete(0, tk.END)
                title_entry.insert(tk.END, str(i[0]))
                author_entry.delete(0, tk.END)
                author_entry.insert(tk.END, str(i[1]))
                publisher_entry.delete(0, tk.END)
                publisher_entry.insert(tk.END, str(i[2]))
                year_of_publish_entry.delete(0, tk.END)
                year_of_publish_entry.insert(tk.END, str(i[3]))
                isbn_entry.delete(0, tk.END)
                isbn_entry.insert(tk.END, str(i[4]))
                pages_entry.delete(0, tk.END)
                pages_entry.insert(tk.END, str(i[5]))
                translated_by_entry.delete(0, tk.END)
                translated_by_entry.insert(tk.END, str(i[6]))
                book_genre_entry.delete(0, tk.END)
                book_genre_entry.insert(tk.END, str(i[7]))
                description_entry.delete(0, tk.END)
                description_entry.insert(tk.END, str(i[8]))
        else:
            messagebox.showerror("error", "Seems local database is raw and fresh. Therefore, no sorta detail were currently returned!")
            return
    except UnboundLocalError:
        messagebox.showerror("error", "Invalid Book ID! There could be a reason that this Book is yet not available in the local database!")
        return

window = tk.Tk()
window.title("Registry")
window.configure(bg="darkblue")
window.geometry("970x1050")
window.resizable(False,False)

left_pane = tk.Frame(window)
left_pane.config(bg="darkblue")
left_pane.pack(side=tk.LEFT, padx=10, pady=15)
left_pane.place(relx=0.11, rely=0.06, anchor=tk.N)

left_header_label = tk.Label(left_pane, text="User Registry", font=("bold"))
left_header_label.config(bg="lightblue", font="impact 20", fg="#0000ff")
left_header_label.pack(pady=30)

username_label = tk.Label(left_pane, text="Username from library")
username_label.config(bg="lightblue", font="helvetica 11 bold")
username_label.pack(pady=7)
username_entry = tk.Entry(left_pane)
username_entry.config(bg="lightgreen", fg="darkblue", font="calibri 13 bold", justify="center")
username_entry.pack()

space1 = tk.Label(left_pane, text="")
space1.configure(bg="darkblue")
space1.pack()

name_label = tk.Label(left_pane, text="Name")
name_label.config(bg="lightblue", font="helvetica 11 bold")
name_label.pack(pady=7)
name_entry = tk.Entry(left_pane)
name_entry.config(bg="lightgreen", fg="darkblue", font="calibri 13 bold", justify="center")
name_entry.pack()

space2 = tk.Label(left_pane, text="")
space2.configure(bg="darkblue")
space2.pack()

middle_name_last_name_label = tk.Label(left_pane, text="Middle Name & Last Name")
middle_name_last_name_label.config(bg="lightblue", font="helvetica 11 bold")
middle_name_last_name_label.pack(pady=7)
middle_name_last_name_entry = tk.Entry(left_pane)
middle_name_last_name_entry.config(bg="lightgreen", fg="darkblue", font="calibri 13 bold", justify="center")
middle_name_last_name_entry.pack()

space3 = tk.Label(left_pane, text="")
space3.configure(bg="darkblue")
space3.pack()

age_label = tk.Label(left_pane, text="Age")
age_label.config(bg="lightblue", font="helvetica 11 bold")
age_label.pack(pady=7)
age_entry = tk.Entry(left_pane)
age_entry.config(bg="lightgreen", fg="darkblue", font="calibri 13 bold", justify="center")
age_entry.pack()

space4 = tk.Label(left_pane, text="")
space4.configure(bg="darkblue")
space4.pack()

address_label = tk.Label(left_pane, text="Address")
address_label.config(bg="lightblue", font="helvetica 11 bold")
address_label.pack(pady=7)
address_entry = tk.Entry(left_pane)
address_entry.config(bg="lightgreen", fg="darkblue", font="calibri 13 bold", justify="center")
address_entry.pack()

space5 = tk.Label(left_pane, text="")
space5.configure(bg="darkblue")
space5.pack()

phone_number_label = tk.Label(left_pane, text="Phone Number")
phone_number_label.config(bg="lightblue", font="helvetica 11 bold")
phone_number_label.pack(pady=7)
phone_number_entry = tk.Entry(left_pane)
phone_number_entry.config(bg="lightgreen", fg="darkblue", font="calibri 13 bold", justify="center")
phone_number_entry.pack()

space6 = tk.Label(left_pane, text="")
space6.configure(bg="darkblue")
space6.pack()

national_id_label = tk.Label(left_pane, text="National ID")
national_id_label.config(bg="lightblue", font="helvetica 11 bold")
national_id_label.pack(pady=7)
national_id_entry = tk.Entry(left_pane)
national_id_entry.config(bg="lightgreen", fg="darkblue", font="calibri 13 bold", justify="center")
national_id_entry.pack()

space7 = tk.Label(left_pane, text="")
space7.configure(bg="darkblue")
space7.pack()

email_label = tk.Label(left_pane, text="Email")
email_label.config(bg="lightblue", font="helvetica 11 bold")
email_label.pack(pady=7)
email_entry = tk.Entry(left_pane)
email_entry.config(bg="lightgreen", fg="darkblue", font="calibri 13 bold", justify="center")
email_entry.pack()

space8 = tk.Label(left_pane, text="")
space8.configure(bg="darkblue")
space8.pack()

postal_code_label = tk.Label(left_pane, text="Postal Code")
postal_code_label.config(bg="lightblue", font="helvetica 11 bold")
postal_code_label.pack(pady=7)
postal_code_entry = tk.Entry(left_pane)
postal_code_entry.config(bg="lightgreen", fg="darkblue", font="calibri 13 bold", justify="center")
postal_code_entry.pack()

space9 = tk.Label(left_pane, text="")
space9.configure(bg="darkblue")
space9.pack()

register_user_button = tk.Button(left_pane, text="Register/Update User", command=register_user)
register_user_button.config(bg="#00ff00", height="2")
register_user_button.pack(pady=10)

user_insert_button = tk.Button(window, text="Modify", command=insert_to_users)
user_insert_button.configure(font="arial 8 bold", pady=0, background="yellow", relief="ridge", fg="purple", width=10)
user_insert_button.place(relx=0.11, rely=0.925, anchor=tk.N)

middleframe1 = tk.Frame(window)
middleframe1.config(bg="darkblue")
middleframe1.pack(side=tk.BOTTOM, padx=8, pady=9)
middleframe1.place(relx=0.5, rely=0.007, anchor=tk.N)

middlelabel1 = tk.Label(middleframe1, text="Anything Else! \u23CE", font="bold")
middlelabel1.config(bg="lightblue", font="impact 20", fg="#0000ff")
middlelabel1.pack(pady=30)

middleframe5 = tk.Frame(window)
middleframe5.config(bg="darkblue")
middleframe5.pack(side=tk.BOTTOM, padx=8, pady=9)
middleframe5.place(relx=0.5, rely=0.22, anchor=tk.N)

middlelabel5 = tk.Label(middleframe5, text="____________OR____________", font="bold")
middlelabel5.config(bg="darkblue", font="impact 20", fg="#00ff00")
middlelabel5.pack(pady=30)

middleframe2 = tk.Frame(window)
middleframe2.config(bg="darkblue")
middleframe2.pack(side=tk.BOTTOM, padx=8, pady=9)
middleframe2.place(relx=0.5, rely=0.46, anchor=tk.N)

middlelabel2 = tk.Label(middleframe2, text="____________OR____________", font="bold")
middlelabel2.config(bg="darkblue", font="impact 20", fg="#00ff00")
middlelabel2.pack(pady=30)

middleframe3 = tk.Frame(window)
middleframe3.config(bg="darkblue")
middleframe3.pack(side=tk.BOTTOM, padx=8, pady=9)
middleframe3.place(relx=0.5, rely=0.8, anchor=tk.N)

middleframe4 = tk.Frame(window)
middleframe4.config(bg="darkblue")
middleframe4.pack(side=tk.BOTTOM, padx=8, pady=9)
middleframe4.place(relx=0.5, rely=0.14, anchor=tk.N)

exit_button = tk.Button(middleframe3, text="Exit", bg="purple", fg="yellow", relief="sunken", command=exit_the_program, font="Arial 17 bold")
exit_button.pack()

middleframe6 = tk.Frame(window)
middleframe6.config(bg="darkblue")
middleframe6.pack(side=tk.BOTTOM, padx=8, pady=9)
middleframe6.place(relx=0.5, rely=0.97, anchor=tk.N)

github_label = tk.Label(middleframe6, text="Made with Love by @PG6AW !", font="tahoma 11 bold", fg="green", bg="darkblue")
github_label.pack()

middle_frame_books = tk.Frame(window)
middle_frame_books.config(bg="darkblue")
middle_frame_books.pack(side=tk.BOTTOM, padx=8,pady=8)
middle_frame_books.place(relx=0.5, rely=0.35, anchor=tk.N)

book_title_delete_label = tk.Label(middle_frame_books, text="Title of the Book to Delete:", bg="yellow", fg="red", font="bold", width=25)
book_title_delete_label.pack()
book_title_delete = tk.Entry(middle_frame_books, width=35, justify="center", font="lotus 12 bold")
book_title_delete.pack(pady=5)
book_title_delete_button = tk.Button(middle_frame_books, text="Delete Book", command=delete_book, bg="red", fg="yellow", font="boldest", width=15, relief="raised")
book_title_delete_button.pack(pady=5)

middle_frame_users = tk.Frame(window)
middle_frame_users.config(bg="darkblue")
middle_frame_users.pack(side=tk.BOTTOM, padx=8,pady=8)
middle_frame_users.place(relx=0.5, rely=0.6, anchor=tk.N)

user_name_delete_label = tk.Label(middle_frame_users, text="Username to Delete:", bg="yellow", fg="red", font="bold", width=25)
user_name_delete_label.pack()
user_name_delete = tk.Entry(middle_frame_users, width=35, justify="center", font="lotus 12 bold")
user_name_delete.pack(pady=5)
user_name_delete_button = tk.Button(middle_frame_users, text="Delete User", command=delete_user, bg="red", fg="yellow", font="boldest", width=15, relief="raised")
user_name_delete_button.pack(pady=5)

right_pane = tk.Frame(window)
right_pane.config(bg="darkblue")
right_pane.pack(side=tk.RIGHT, padx=10, pady=15)
right_pane.place(relx=0.89, rely=0, anchor=tk.N)

space21 = tk.Label(right_pane, text="")
space21.configure(bg="darkblue", height=1)
space21.pack()

right_header_label = tk.Label(right_pane, text="Book Registry", font="bold")
right_header_label.config(bg="lightblue", font="impact 20", fg="#0000ff")
right_header_label.pack(pady=30)

category_label = tk.Label(right_pane, text="Book Category")
category_label.config(bg="lightblue", font="helvetica 11 bold")
category_label.pack(pady=7)

category_var = tk.StringVar(right_pane)
categories = ["SELECT_FROM_DROPDOWN", "Engineering", "Meta Physics", "Mathematics", "Motivational", "Narrative", "Comedy", "Memoir", "Fiction", "History", "Poetry", "Science", "Novel", 
               "Phsychology", "Romance","Academic", "Entertainment", "Science Fiction", "IT and Technology", "Biology", "Religious", "Spirituality", "Artificial Intelligence", 
               "Correlated Artbook", "Geography", "Astrology", "Crime Fiction", "Antropology", "Robotics", "Graphics", "Video Game Franchise Books", "Relationship-Help", "Children", 
               "Folklore", "Music", "Survival-Horror Fiction", "Self Improvement", "Historical Fiction", "Biography", "Thriller", "Inspired by True stories", "Mystery", "Art", 
               "Ethnic and Culture", "Fantasy", "Other"]
category_var.set(categories[0])
style = ttk.Style(right_pane)
style.configure('TMenubutton', foreground='blue', background='lightgreen', font=('Trebuchet MS', 10, 'bold'))
category_dropdown = ttk.OptionMenu(right_pane, category_var, *categories)
category_dropdown.pack()

space10 = tk.Label(right_pane, text="")
space10.configure(bg="darkblue")
space10.pack()

book_id_label = tk.Label(right_pane, text="Book ID from library")
book_id_label.config(bg="lightblue", font="helvetica 11 bold")
book_id_label.pack(pady=5)
book_id_entry = tk.Entry(right_pane)
book_id_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
book_id_entry.pack()

space11 = tk.Label(right_pane, text="")
space11.configure(bg="darkblue")
space11.pack()

title_label = tk.Label(right_pane, text="Title")
title_label.config(bg="lightblue", font="helvetica 11 bold")
title_label.pack(pady=5)
title_entry = tk.Entry(right_pane)
title_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
title_entry.pack()

space12 = tk.Label(right_pane, text="")
space12.configure(bg="darkblue")
space12.pack()

author_label = tk.Label(right_pane, text="Author")
author_label.config(bg="lightblue", font="helvetica 11 bold")
author_label.pack(pady=5)
author_entry = tk.Entry(right_pane)
author_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
author_entry.pack()

space13 = tk.Label(right_pane, text="")
space13.configure(bg="darkblue")
space13.pack()

publisher_label = tk.Label(right_pane, text="Publisher")
publisher_label.config(bg="lightblue", font="helvetica 11 bold")
publisher_label.pack(pady=5)
publisher_entry = tk.Entry(right_pane)
publisher_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
publisher_entry.pack()

space14 = tk.Label(right_pane, text="")
space14.configure(bg="darkblue")
space14.pack()

year_of_publish_label = tk.Label(right_pane, text="Year of Publish")
year_of_publish_label.pack(pady=5)
year_of_publish_label.config(bg="lightblue", font="helvetica 11 bold")
year_of_publish_entry = tk.Entry(right_pane)
year_of_publish_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
year_of_publish_entry.pack()

space15 = tk.Label(right_pane, text="")
space15.configure(bg="darkblue")
space15.pack()

isbn_label = tk.Label(right_pane, text="ISBN")
isbn_label.config(bg="lightblue", font="helvetica 11 bold")
isbn_label.pack(pady=5)
isbn_entry = tk.Entry(right_pane)
isbn_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
isbn_entry.pack()

space16 = tk.Label(right_pane, text="")
space16.configure(bg="darkblue")
space16.pack()

pages_label = tk.Label(right_pane, text="Pages")
pages_label.config(bg="lightblue", font="helvetica 11 bold")
pages_label.pack(pady=5)
pages_entry = tk.Entry(right_pane)
pages_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
pages_entry.pack()

space17 = tk.Label(right_pane, text="")
space17.configure(bg="darkblue")
space17.pack()

translated_by_label = tk.Label(right_pane, text="Translated By")
translated_by_label.config(bg="lightblue", font="helvetica 11 bold")
translated_by_label.pack(pady=5)
translated_by_entry = tk.Entry(right_pane)
translated_by_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
translated_by_entry.pack()

space18 = tk.Label(right_pane, text="")
space18.configure(bg="darkblue")
space18.pack()

book_genre_label = tk.Label(right_pane, text="Book Genre")
book_genre_label.config(bg="lightblue", font="helvetica 11 bold")
book_genre_label.pack(pady=5)
book_genre_entry = tk.Entry(right_pane)
book_genre_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
book_genre_entry.pack()

space19 = tk.Label(right_pane, text="")
space19.configure(bg="darkblue")
space19.pack()

description_label = tk.Label(right_pane, text="Book Description")
description_label.config(bg="lightblue", font="helvetica 11 bold")
description_label.pack(pady=5)
description_entry = tk.Entry(right_pane)
description_entry.config(bg="lightgreen", fg="darkblue", font="calibri 11 bold", justify="center", width=26)
description_entry.pack()

space20 = tk.Label(right_pane, text="")
space20.configure(bg="darkblue")
space20.pack()

register_book_button = tk.Button(right_pane, text="Register/Update Book", command=register_book)
register_book_button.config(bg="#00ff00", height="2")
register_book_button.pack(pady=0)

books_insert_button = tk.Button(window, text="Modify", command=insert_to_books)
books_insert_button.configure(font="arial 8 bold", pady=0, background="yellow", relief="ridge", fg="purple", width=10)
books_insert_button.place(relx=0.89, rely=0.97, anchor=tk.N)

upper_frame = tk.Frame(window)
upper_frame.config(bg="darkblue")
upper_frame.pack(side=tk.TOP, pady=6)

show_registered_users_button = tk.Button(middleframe4, text="Show Registered Users", bg="#00ff00", width="17", height="3", command=show_registered_users)
show_registered_users_button.pack(side=tk.LEFT,padx=1)

show_registered_books_button = tk.Button(middleframe4, text="Show Registered Books", bg="#00ff00", width="17", height="3", command=show_registered_books)
show_registered_books_button.pack(side=tk.LEFT,padx=1)

investigator_button = tk.Button(middleframe4, text="Investigator", bg="#00ff00", width="10", height="3", command=search_records)
investigator_button.pack(side=tk.LEFT,padx=1)

window.mainloop()
conn.close()