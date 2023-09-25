#Monitor Library status and Search details solo or Combined

import tkinter as tk
from tkinter import messagebox
import sqlite3

def search_books():
    id_val = id_entry.get()
    title_val = title_entry.get()
    author_val = author_entry.get()
    pages_val = pages_entry.get()
    instances_val = instances_entry.get()

    if str(id_val) != "" :
        try:
            id_val = int(id_val)
        except ValueError:
            messagebox.showerror("Inappropriate Value", "Please enter a number for 'Book ID'!")
            return
    if str(pages_val) != "" :
        try:
            pages_val = int(pages_val)
        except ValueError:
            messagebox.showerror("Inappropriate Value", "Please enter a number for 'Pages'!")
            return
    if str(instances_val) != "" :
        try:
            instances_val = int(instances_val)
        except ValueError:
            messagebox.showerror("Inappropriate Value", "Please enter a number for 'Instances'!")
            return

    if not id_val and not title_val and not author_val and not pages_val and not instances_val:
        messagebox.showerror("Error", "Please fill in at least one of the fields.")
        return
    
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    query = "SELECT * FROM books WHERE 1=1"

    if id_val:
        query += f" AND id={id_val}"
    if title_val:
        query += f" AND title='{title_val}'"
    if author_val:
        query += f" AND author='{author_val}'"
    if pages_val:
        query += f" AND pages={pages_val}"
    if instances_val:
        query += f" AND instances={instances_val}"

    cursor.execute(query)
    rows = cursor.fetchall()

    if len(rows) == 0:
        messagebox.showinfo("No Results", "No books found matching the criteria.")
    else:
        result = ""
        for row in rows:
            result += f"ID: {row[0]}\nTitle: {row[1]}\nAuthor: {row[2]}\nPages: {row[3]}\nInstances: {row[4]}\n\n"
        messagebox.showinfo("Search Results", result)

    conn.close()

def search_users():
    id_val = user_id_entry.get()
    username_val = username_entry.get()
    password_val = password_entry.get()
    borrowed_ids_val = borrowed_ids_entry.get()
    days_remaining_val = days_remaining_entry.get()

    if str(id_val) != "" :
        try:
            id_val = int(id_val)
        except ValueError:
            messagebox.showerror("Inappropriate Value", "Please enter a number for 'User ID'!")
            return
    if str(days_remaining_val) != "" :
        try:
            days_remaining_val = int(days_remaining_val)
        except ValueError:
            messagebox.showerror("Inappropriate Value", "Please enter a number for 'Days Remaining'!")
            return

    if not id_val and not username_val and not password_val and not borrowed_ids_val and not days_remaining_val:
        messagebox.showerror("Error", "Please fill in at least one of the fields.")
        return

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    query = "SELECT * FROM users WHERE 1=1"

    if id_val:
        query += f" AND id={id_val}"
    if username_val:
        query += f" AND username='{username_val}'"
    if password_val:
        query += f" AND password='{password_val}'"
    if borrowed_ids_val:
        query += f" AND borrowed_ids='{borrowed_ids_val}'"
    if days_remaining_val:
        query += f" AND days_remaining={days_remaining_val}"

    cursor.execute(query)
    rows = cursor.fetchall()

    if len(rows) == 0:
        messagebox.showinfo("No Results", "No users found matching the criteria.")
    else:
        result = ""
        for row in rows:
            result += f"ID: {row[0]}\nUsername: {row[1]}\nPassword: {row[2]}\nBorrowed IDs: {row[3]}\nDays Remaining: {row[4]}\n\n"
        messagebox.showinfo("Search Results", result)

    conn.close()

def exit_the_program():
    window.destroy()

window = tk.Tk()
window.resizable(False,False)
window.title("Library Database Search")
window.geometry("300x880")
window.configure(bg="darkblue")

books_frame = tk.Frame(window, relief=tk.RAISED, borderwidth=2, bg="#f7cd25")
books_frame.pack(pady=20)

books_label = tk.Label(books_frame, text=" Search Books ", font=("bold", 20), bg="#f7cd25")
books_label.pack(pady=10)

id_label = tk.Label(books_frame, text="ID:", font=("bold", 12), bg="#f7cd25")
id_label.configure(font="calibri 14 bold")
id_label.pack()
id_entry = tk.Entry(books_frame, font=("bold", 12))
id_entry.configure(justify="center", font="calibri 12 bold", width=21)
id_entry.pack()

title_label = tk.Label(books_frame, text="Title:", font=("bold", 12), bg="#f7cd25")
title_label.configure(font="calibri 14 bold")
title_label.pack()
title_entry = tk.Entry(books_frame, font=("bold", 12))
title_entry.configure(justify="center", font="calibri 12 bold", width=21)
title_entry.pack()

author_label = tk.Label(books_frame, text="Author:", font=("bold", 12), bg="#f7cd25")
author_label.configure(font="calibri 14 bold")
author_label.pack()
author_entry = tk.Entry(books_frame, font=("bold", 12))
author_entry.configure(justify="center", font="calibri 12 bold", width=21)
author_entry.pack()

pages_label = tk.Label(books_frame, text="Pages:", font=("bold", 12), bg="#f7cd25")
pages_label.configure(font="calibri 14 bold")
pages_label.pack()
pages_entry = tk.Entry(books_frame, font=("bold", 12))
pages_entry.configure(justify="center", font="calibri 12 bold", width=21)
pages_entry.pack()

instances_label = tk.Label(books_frame, text="Instances:", font=("bold", 12), bg="#f7cd25")
instances_label.configure(font="calibri 14 bold")
instances_label.pack()
instances_entry = tk.Entry(books_frame, font=("bold", 12))
instances_entry.configure(justify="center", font="calibri 12 bold", width=21)
instances_entry.pack()

search_books_button = tk.Button(books_frame, bg="lightblue", relief="raised", text="Search", font=("bold", 12), command=search_books)
search_books_button.pack(pady=10)

users_frame = tk.Frame(window, relief=tk.RAISED, borderwidth=2, bg="#f7cd25")
users_frame.pack(pady=20)

users_label = tk.Label(users_frame, text=" Search Users ", font=("bold", 20), bg="#f7cd25")
users_label.pack(pady=10)

user_id_label = tk.Label(users_frame, text="ID:", font=("bold", 12), bg="#f7cd25")
user_id_label.configure(font="calibri 14 bold")
user_id_label.pack()
user_id_entry = tk.Entry(users_frame, font=("bold", 12))
user_id_entry.configure(justify="center", font="calibri 12 bold", width=21)
user_id_entry.pack()

username_label = tk.Label(users_frame, text="Username:", font=("bold", 12), bg="#f7cd25")
username_label.configure(font="calibri 14 bold")
username_label.pack()
username_entry = tk.Entry(users_frame, font=("bold", 12))
username_entry.configure(justify="center", font="calibri 12 bold", width=21)
username_entry.pack()

password_label = tk.Label(users_frame, text="Password:", font=("bold", 12), bg="#f7cd25")
password_label.configure(font="calibri 14 bold")
password_label.pack()
password_entry = tk.Entry(users_frame, font=("bold", 12))
password_entry.configure(justify="center", font="calibri 12 bold", width=21)
password_entry.pack()

borrowed_ids_label = tk.Label(users_frame, text="Borrowed IDs:", font=("bold", 12), bg="#f7cd25")
borrowed_ids_label.configure(font="calibri 14 bold")
borrowed_ids_label.pack()
borrowed_ids_entry = tk.Entry(users_frame, font=("bold", 12))
borrowed_ids_entry.configure(justify="center", font="calibri 12 bold", width=21)
borrowed_ids_entry.pack()

days_remaining_label = tk.Label(users_frame, text="Days Remaining:", font=("bold", 12), bg="#f7cd25")
days_remaining_label.configure(font="calibri 14 bold")
days_remaining_label.pack()
days_remaining_entry = tk.Entry(users_frame, font=("bold", 12))
days_remaining_entry.configure(justify="center", font="calibri 12 bold", width=21)
days_remaining_entry.pack()

search_users_button = tk.Button(users_frame, bg="lightblue", relief="raised", text="Search", font=("bold", 12), command=search_users)
search_users_button.pack(pady=10)

exit_button = tk.Button(window, text="Exit", bg="red", fg="darkblue", font=("impact", 10, "bold"), command=exit_the_program)
exit_button.configure(width=10, pady=5)
exit_button.pack()

window.mainloop()
