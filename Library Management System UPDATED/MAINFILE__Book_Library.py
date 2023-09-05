import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime


conn = sqlite3.connect("library.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    borrowed_ids TEXT,
                    days_remaining TEXT,
                    date_borrowed TEXT
                )""")
cursor.execute("""CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    author TEXT,
                    pages INTEGER,
                    instances INTEGER,
                    date_book_added TEXT
                )""")
conn.commit()

root = tk.Tk()
root.title("Library Management System")
root.geometry("300x980")
root.option_add("*Font", "Arial 12 bold")
root.configure(bg="yellow")

def add_book():
    title = book_title_entry.get()
    author = author_entry.get()
    pages = int(pages_entry.get())
    instances = int(instances_entry.get())
    
    if title == "" or author == "" or pages == 0 or instances == 0:
        messagebox.showerror("Error", "All fields must be filled in.")
        return
    
    cursor.execute("SELECT * FROM books WHERE title=?", (title,))
    book = cursor.fetchone()
    
    if book:
        cursor.execute("UPDATE books SET pages=?, instances=? WHERE id=?", (pages, instances, book[0]))
        conn.commit()
        messagebox.showinfo("Updated", "Book has been updated.")
    else:
        cursor.execute("INSERT INTO books (title, author, pages, instances, date_book_added) VALUES (?, ?, ?, ?, ?)",
                       (title, author, pages, instances, datetime.datetime.now()))
        conn.commit()
        messagebox.showinfo("Added", "New book has been added.")
    
    book_title_entry.delete(0, tk.END)
    author_entry.delete(0, tk.END)
    pages_entry.delete(0, tk.END)
    instances_entry.delete(0, tk.END)

def add_user():
    username = username_entry.get()
    password = password_entry.get()
    
    if username == "" or password == "":
        messagebox.showerror("Error", "All fields must be filled in.")
        return
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    if user:
        cursor.execute("UPDATE users SET password=? WHERE id=?", (password, user[0]))
        conn.commit()
        messagebox.showinfo("Updated", "User has been updated.")
    else:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Added", "New user has been added.")
    
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def retrieve_ids():
    username = username_entry_retrieve.get()
    title = book_title_entry_retrieve.get()
    
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    
    cursor.execute("SELECT * FROM books WHERE title=?", (title,))
    book = cursor.fetchone()
    
    user_id = user[0] if user else "User not found"
    book_id = book[0] if book else "Book not found"
    
    messagebox.showinfo("IDs", f"User ID: {user_id}\nBook ID: {book_id}")

def delete_book():
    book_id = int(book_id_entry_delete.get())
    
    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    
    if cursor.rowcount > 0:
        messagebox.showinfo("Deleted", "Book has been deleted.")
    else:
        messagebox.showerror("Error", "Book not found.")
    
    book_id_entry_delete.delete(0, tk.END)

def borrow_book():
    username = username_entry_borrow.get()
    password = password_entry_borrow.get()
    book_id = int(book_id_entry_borrow.get())
    days = int(days_entry_borrow.get())
    
    if username == "" or password == "" or book_id == 0 or days == 0:
        messagebox.showerror("Error", "All fields must be filled in.")
        return
    
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    
    if not user:
        messagebox.showerror("Error", "Invalid username or password.")
        return
    
    if not book:
        messagebox.showerror("Error", "Book not found.")
        return
    
    borrowed_ids = user[3].split(",") if user[3] else []
    if str(book_id) in borrowed_ids:
        messagebox.showerror("Error", "You have already borrowed this book.")
        return
    
    instances = book[4]
    if instances == 0:
        messagebox.showinfo("Unavailable", "This book is not available in the library.")
        return
    
    borrowed_ids.append(str(book_id))
    borrowed_ids_str = ",".join(borrowed_ids)
    
    cursor.execute("UPDATE users SET borrowed_ids=?, days_remaining=?, date_borrowed=? WHERE id=?",
                   (borrowed_ids_str, days, datetime.datetime.now(), user[0]))
    cursor.execute("UPDATE books SET instances=? WHERE id=?", (instances - 1, book[0]))
    conn.commit()
    
    messagebox.showinfo("Borrowed", "Book has been borrowed successfully.")

def return_book():
    username = username_entry_return.get()
    password = password_entry_return.get()
    book_id = int(book_id_entry_return.get())
    
    if username == "" or password == "" or book_id == 0:
        messagebox.showerror("Error", "All fields must be filled in.")
        return
    
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    cursor.execute("SELECT * FROM books WHERE id=?", (book_id,))
    book = cursor.fetchone()
    
    if not user:
        messagebox.showerror("Error", "Invalid username or password.")
        return
    
    if not book:
        messagebox.showerror("Error", "Book not found.")
        return
    
    borrowed_ids = user[3].split(",") if user[3] else []
    if str(book_id) not in borrowed_ids:
        messagebox.showerror("Error", "You have not borrowed this book.")
        return
    
    borrowed_ids.remove(str(book_id))
    borrowed_ids_str = ",".join(borrowed_ids)
    
    cursor.execute("UPDATE users SET borrowed_ids=? WHERE id=?", (borrowed_ids_str, user[0]))
    cursor.execute("UPDATE books SET instances=? WHERE id=?", (book[4] + 1, book[0]))
    
    if len(borrowed_ids) == 0:
        cursor.execute("UPDATE users SET days_remaining='user_exempt' WHERE id=?", (user[0],))
    
    conn.commit()
    
    messagebox.showinfo("Returned", "Book has been returned successfully.")

book_title_label = tk.Label(root, text="Book Title:")
book_title_label.pack()
book_title_entry = tk.Entry(root)
book_title_entry.pack()

author_label = tk.Label(root, text="Author:")
author_label.pack()
author_entry = tk.Entry(root)
author_entry.pack()

pages_label = tk.Label(root, text="Number of Pages:")
pages_label.pack()
pages_entry = tk.Entry(root)
pages_entry.pack()

instances_label = tk.Label(root, text="Number of Instances:")
instances_label.pack()
instances_entry = tk.Entry(root)
instances_entry.pack()

add_book_button = tk.Button(root, text="Add Book", command=add_book)
add_book_button.pack()

username_label = tk.Label(root, text="Username:")
username_label.pack()
username_entry = tk.Entry(root)
username_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()
password_entry = tk.Entry(root)
password_entry.pack()

add_user_button = tk.Button(root, text="Add User", command=add_user)
add_user_button.pack()

username_label_retrieve = tk.Label(root, text="Username:")
username_label_retrieve.pack()
username_entry_retrieve = tk.Entry(root)
username_entry_retrieve.pack()

book_title_label_retrieve = tk.Label(root, text="Book Title:")
book_title_label_retrieve.pack()
book_title_entry_retrieve = tk.Entry(root)
book_title_entry_retrieve.pack()

retrieve_ids_button = tk.Button(root, text="Retrieve IDs", command=retrieve_ids)
retrieve_ids_button.pack()

book_id_label_delete = tk.Label(root, text="Book ID:")
book_id_label_delete.pack()
book_id_entry_delete = tk.Entry(root)
book_id_entry_delete.pack()

delete_book_button = tk.Button(root, text="Delete Book", command=delete_book)
delete_book_button.pack()

username_label_borrow = tk.Label(root, text="Username:")
username_label_borrow.pack()
username_entry_borrow = tk.Entry(root)
username_entry_borrow.pack()

password_label_borrow = tk.Label(root, text="Password:")
password_label_borrow.pack()
password_entry_borrow = tk.Entry(root)
password_entry_borrow.pack()

book_id_label_borrow = tk.Label(root, text="Book ID:")
book_id_label_borrow.pack()
book_id_entry_borrow = tk.Entry(root)
book_id_entry_borrow.pack()

days_label_borrow = tk.Label(root, text="Number of Days:")
days_label_borrow.pack()
days_entry_borrow = tk.Entry(root)
days_entry_borrow.pack()

borrow_book_button = tk.Button(root, text="Borrow Book", command=borrow_book)
borrow_book_button.pack()

username_label_return = tk.Label(root, text="Username:")
username_label_return.pack()
username_entry_return = tk.Entry(root)
username_entry_return.pack()

password_label_return = tk.Label(root, text="Password:")
password_label_return.pack()
password_entry_return = tk.Entry(root)
password_entry_return.pack()

book_id_label_return = tk.Label(root, text="Book ID:")
book_id_label_return.pack()
book_id_entry_return = tk.Entry(root)
book_id_entry_return.pack()

return_book_button = tk.Button(root, text="Return Book", command=return_book)
return_book_button.pack()

root.mainloop()