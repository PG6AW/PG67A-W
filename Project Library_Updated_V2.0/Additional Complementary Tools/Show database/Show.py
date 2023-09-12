# A comprehensive view of the database offering a representation of both its Tables in one view

import tkinter as tk
from tkinter import ttk
import sqlite3


conn = sqlite3.connect('library.db')
cursor = conn.cursor()

window = tk.Tk()
window.title("Library Database")
window.geometry("1000x700")
window.configure(bg="#011042")
window.resizable(False,False)

users_frame = ttk.Frame(window, padding="10")
users_frame.pack(side="top", pady=10, padx=10)

users_label = ttk.Label(users_frame, text="Users Table", font=("bold", 12))
users_label.pack(side="top", pady=10)

users_scrollbar = ttk.Scrollbar(users_frame)
users_scrollbar.pack(side="right", fill="y")

users_treeview = ttk.Treeview(users_frame, yscrollcommand=users_scrollbar.set)
users_treeview.pack(side="left", fill="both", expand=True)

users_scrollbar.configure(command=users_treeview.yview)

users_treeview["columns"] = ("User ID", "Username", "Password", "Borrowed Books by IDs", "Days Remaining", "Date Borrowed")
users_treeview.column("#0", width=0, stretch="no")
users_treeview.column("User ID", width=100, anchor="center")
users_treeview.column("Username", width=100, anchor="center")
users_treeview.column("Password", width=100, anchor="center")
users_treeview.column("Borrowed Books by IDs", width=200, anchor="center")
users_treeview.column("Days Remaining", width=100, anchor="center")
users_treeview.column("Date Borrowed", width=100, anchor="center")

for column in users_treeview["columns"]:
    users_treeview.heading(column, text=column, anchor="center")

cursor.execute("SELECT * FROM users")
users_data = cursor.fetchall()
for user in users_data:
    users_treeview.insert("", tk.END, values=user)

books_frame = ttk.Frame(window, padding="10")
books_frame.pack(side="top", pady=10, padx=10)

books_label = ttk.Label(books_frame, text="Books Table", font=("bold", 12))
books_label.pack(side="top", pady=10)

books_scrollbar = ttk.Scrollbar(books_frame)
books_scrollbar.pack(side="right", fill="y")

books_treeview = ttk.Treeview(books_frame, yscrollcommand=books_scrollbar.set)
books_treeview.pack(side="left", fill="both", expand=True)

books_scrollbar.configure(command=books_treeview.yview)

books_treeview["columns"] = ("Book ID", "Book Title", "Author", "Pages", "Instances", "Date Book Added")
books_treeview.column("#0", width=0, stretch="no")
books_treeview.column("Book ID", width=100, anchor="center")
books_treeview.column("Book Title", width=150, anchor="center")
books_treeview.column("Author", width=100, anchor="center")
books_treeview.column("Pages", width=100, anchor="center")
books_treeview.column("Instances", width=100, anchor="center")
books_treeview.column("Date Book Added", width=150, anchor="center")

for column in books_treeview["columns"]:
    books_treeview.heading(column, text=column, anchor="center")

cursor.execute("SELECT * FROM books")
books_data = cursor.fetchall()
for book in books_data:
    books_treeview.insert("", tk.END, values=book)

def retrieve_database_info():
    cursor.execute("SELECT * FROM users")
    users_data = cursor.fetchall()
    users_treeview.delete(*users_treeview.get_children())
    for user in users_data:
        users_treeview.insert("", tk.END, values=user)

    cursor.execute("SELECT * FROM books")
    books_data = cursor.fetchall()
    books_treeview.delete(*books_treeview.get_children())
    for book in books_data:
        books_treeview.insert("", tk.END, values=book)

def exit_the_program():
    window.destroy()

retrieve_button = ttk.Button(window, text="Retrieve Database info", command=retrieve_database_info)
retrieve_button.pack(side="top", pady=10)

exit_button = tk.Button(window, text="Exit", bg="Turquoise", fg="darkblue", font=("Arial", 8, "bold"), relief="raised", command = exit_the_program)
exit_button.configure(width=10, pady=5)
exit_button.pack()

window.mainloop()

conn.close()
