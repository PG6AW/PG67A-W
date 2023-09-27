import tkinter as tk
from tkinter import messagebox , TclError
import sqlite3
import datetime
from tkinter.font import Font
import subprocess
import getpass


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
                    title TEXT UNIQUE,
                    author TEXT,
                    pages INTEGER,
                    instances INTEGER,
                    date_book_added TEXT,
                    reserved_deletion TEXT
                )""")
conn.commit()

current_username = getpass.getuser()
event_by_admin = current_username

conn1 = sqlite3.connect("event_logs.db")
cursor1 = conn1.cursor()
cursor1.execute("""CREATE TABLE IF NOT EXISTS admin_enter_exit_log (
                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                admin TEXT,
                admin_enter_date TEXT,
                admin_exit_date TEXT
                )""")
conn1.commit()

cursor1.execute("INSERT INTO admin_enter_exit_log (admin, admin_enter_date) VALUES (?, ?)",
            (event_by_admin, datetime.datetime.now()))
conn1.commit()
conn1.close()

root = tk.Tk()
root.title("Library Management System")
root.resizable(False,False)
root.geometry("938x530")
root.option_add("*Font", "constantia 12 bold")
root.configure(bg="#000000")

def add_book():
    title = book_title_entry.get()
    author = author_entry.get()
    pages = pages_entry.get()
    instances = instances_entry.get()

    empty_list = []
    if str(title) == "" :
        empty_list.append("Book Title")
    if str(author) == "" :
        empty_list.append("Author")
    if str(pages) == "" :
        empty_list.append("Number of Pages")
    if str(instances) == "" :
        empty_list.append("Number of Instances")

    try:
        pages = int(pages)
    except (ValueError , TypeError):
        if str(pages) != "" :
            messagebox.showerror("Book Pages ValueType Error", "Value for 'Number of Pages' must be Numerical!")
            return
        else:
            pass
    try:
        instances = int(instances)
    except (ValueError , TypeError):
        if str(instances) != "" :
            messagebox.showerror("Book Instances ValueType Error", "Value for 'Number of Instances' must be Numerical!")
            return
        else:
            pass

    if title == "" or author == "" or str(pages) == "" or str(instances) == "":
        messagebox.showerror("Error", f"All fields must be filled in!\n\nThe following entries are empty:\n---> {' , '.join(empty_list)} <---")
        return
    
    if str(title) != "" and str(author) != "" and str(pages) != "" and str(instances) != "":
        book_add_cofirmation = messagebox.askyesno("Book-Add Confirmation", "Are you sure you're going to add this book?\nAlways double-check before you confirm!\n\nPlease note that you can always come back and Update the specific book identifying it with its Title from this applet.\n\n--CONFIRM AND CONTINUE?--")
        if book_add_cofirmation:
            pass
        else:
            return
        
    current_username = getpass.getuser()
    event_by_admin = current_username
    book_title = title
    book_author = author
    book_pages = pages
    book_instances = instances
    cursor.execute("SELECT * FROM books WHERE title=?", (title,))
    book = cursor.fetchone()

    if not book:
        cursor.execute("INSERT INTO books (title, author, pages, instances, date_book_added) VALUES (?, ?, ?, ?, ?)",
                    (title, author, pages, instances, datetime.datetime.now()))
        conn.commit()
        messagebox.showinfo("Added", "New book has been added!")

        cursor.execute("SELECT id FROM books WHERE title=?", (title,))
        book_id_tuple = cursor.fetchone()
        book_id = book_id_tuple[0] if book_id_tuple else None
        try:
            book_id = int(book_id)
        except (TypeError , ValueError):
            pass

        conn1 = sqlite3.connect("event_logs.db")
        cursor1 = conn1.cursor()
        cursor1.execute("""CREATE TABLE IF NOT EXISTS books_added (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        book_id INTEGER,
                        book_title TEXT,
                        book_author TEXT,
                        event_by_admin TEXT,
                        event_date TEXT
                        )""")
        conn1.commit()
        cursor1.execute("INSERT INTO books_added (book_id, book_title, book_author, event_by_admin, event_date) VALUES (?, ?, ?, ?, ?)",
                    (book_id, book_title, book_author, event_by_admin, datetime.datetime.now()))
        conn1.commit()
        conn1.close()
        book_title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        pages_entry.delete(0, tk.END)
        instances_entry.delete(0, tk.END)
        return
    
    cursor.execute("SELECT id FROM books WHERE title=?", (title,))
    book_id_tuple = cursor.fetchone()
    book_id = book_id_tuple[0] if book_id_tuple else None
    try:
        book_id = int(book_id)
    except (TypeError , ValueError):
        pass

    cursor.execute("SELECT reserved_deletion FROM books WHERE title=?", (title,))
    reserved_deletion = cursor.fetchone()
    if reserved_deletion is None:
        reserved_deletion = str(reserved_deletion)
    else:
        reserved_deletion = list(reserved_deletion)
        for i in reserved_deletion:
            i = str(i)
    if i != "Reserved":

        if book:
            cursor.execute(
                "UPDATE books SET author=?, pages=?, instances=? WHERE id=?", (author, pages, instances, book[0]))
            conn.commit()
            messagebox.showinfo("Updated", "Book has been updated!")

            conn1 = sqlite3.connect("event_logs.db")
            cursor1 = conn1.cursor()
            cursor1.execute("""CREATE TABLE IF NOT EXISTS books_updated (
                            event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            book_id INTEGER,
                            book_title TEXT,
                            book_author TEXT,
                            book_pages INTEGER,
                            book_instances INTEGER,
                            event_by_admin TEXT,
                            event_date TEXT
                            )""")
            conn1.commit()
            cursor1.execute("INSERT INTO books_updated (book_id, book_title, book_author, book_pages, book_instances, event_by_admin, event_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        (book_id, book_title, book_author, book_pages, book_instances, event_by_admin, datetime.datetime.now()))
            conn1.commit()
            conn1.close()

        book_title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        pages_entry.delete(0, tk.END)
        instances_entry.delete(0, tk.END)

    else:
        messagebox.showerror("Reserved", "This book has been reserved for deletion by an admin and hence cannot be updated until it's unreserved!\n\nThere are two small buttons at the 'Delete Book' applet section down below.\nWhen yellow 'RD' button is clicked, it assigns an attribute to a book that makes it unable to be deleted, nor will its details update and the available instances of that book will reach down to zero.\n\nBut when the blue 'URD' button is clicked, the book is Unreserved and therefore, Unlocked!\n\nLogs are generated for each admin doing database-specific tasks and hence, once the values belonging to the database are overridden, they can be further monitored by managers and overwatch officers!")
        return

def exit_the_program():

    current_username = getpass.getuser()
    event_by_admin = current_username
    conn1 = sqlite3.connect("event_logs.db")
    cursor1 = conn1.cursor()
    cursor1.execute("INSERT INTO admin_enter_exit_log (admin, admin_exit_date) VALUES (?, ?)",
                (event_by_admin, datetime.datetime.now()))
    conn1.commit()
    conn1.close()
    try:
        conn.close()
        access_manager.destroy()
    except TclError:
        pass
    try:
        root.destroy()
        messagebox.showinfo("Exit Message", "Successfully exited the Library!")
    except TclError:
        messagebox.showinfo("Manipulation Notice", "Access Manager successfully closed but Main window was already dealt with by an admin!")

def add_user():
    username = username_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields must be filled in.")
        return

    if str(username) != "" and str(password) != "":
        user_add_cofirmation = messagebox.askyesno("User-Add Confirmation", "Are you sure you're going to add the following User?\nAlways double-check before you confirm!\n\nPlease note that you can always come back and Update the specific User identifying him/her with their unique Username from this applet.\n\n--CONFIRM AND CONTINUE?--")
        if user_add_cofirmation:
            pass
        else:
            return

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        cursor.execute("UPDATE users SET password=? WHERE id=?", (password, user[0]))
        conn.commit()
        messagebox.showinfo("Updated", "User has been updated.")
    else:
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        messagebox.showinfo("Added", "New user has been added.")

    current_username = getpass.getuser()
    event_by_admin = current_username

    conn1 = sqlite3.connect("event_logs.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""CREATE TABLE IF NOT EXISTS user_signup (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    password TEXT,
                    event_by_admin TEXT,
                    event_date TEXT
                    )""")
    conn1.commit()

    cursor1.execute("INSERT INTO user_signup (username, password, event_by_admin, event_date) VALUES (?, ?, ?, ?)",
                (username, password, event_by_admin, datetime.datetime.now()))
    conn1.commit()
    conn1.close()

    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

def retrieve_ids():
    username = username_entry_retrieve.get()
    title = book_title_entry_retrieve.get()

    if str(username) == "" and str(title) == "" :
        messagebox.showerror("NoEntry Error", "To retrieve IDs, please type into at least ONE field!")
        return

    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM books WHERE title=?", (title,))
    book = cursor.fetchone()

    user_id = user[0] if user else "User not found"
    book_id = book[0] if book else "Book not found"

    messagebox.showinfo("IDs", f"User ID: {user_id}\nBook ID: {book_id}")

    username_entry_retrieve.delete(0, tk.END)
    book_title_entry_retrieve.delete(0, tk.END)

def delete_book():
    book_id = book_id_entry_delete.get()

    if str(book_id) == "" :
        messagebox.showerror("Book Not Specified!!!", "Please provide us with a specified Book ID or retrieve it if you need to delete a book!\n\nPlease note that you always need the book ID anytime you want to delete a book and not its Title per se would do the trick for you alone!\n\nWe mandated this to force admins to think over their request and make sure everything's alright before making their decision firm!\n\nThanks for understanding the potential of this action!")
        return
    try:
        book_id = int(book_id)
    except (ValueError , TypeError):
        if str(book_id) != "" :
            messagebox.showerror("Book ID ValueType Error", "'Book ID' must be a Number! You can also retrieve it from the applet above!")
            return
        else:
            pass

    if str(book_id) != "" :
        delete_confirm = messagebox.askyesno("Confirm Book Deletion", "You're going to completely wipe a book from the database by its ID!\nUndertaking its consequences would be a bit speculative and pose risks as it could make a potentially unwanted change to the database!\nSure what you're really doing while reconsidering all the risks involved?\nIf Yes & have already Double-Checked everything, then ...\n\n--Hit Yes to PROCEED?--")
        if delete_confirm:
            pass
        else:
            return
    
    cursor.execute("SELECT reserved_deletion FROM books WHERE id=?", (book_id,))
    reserved_deletion = cursor.fetchone()
    if reserved_deletion is None:
        reserved_deletion = str(reserved_deletion)
    else:
        reserved_deletion = list(reserved_deletion)
    if "Reserved" not in reserved_deletion:

        borrowed_by_user = False
        cursor.execute("SELECT borrowed_ids FROM users")
        rows = cursor.fetchall()
        for row in str(rows):
            row1 = list(row)
            for i in row1:
                i = str(i)
            if str(book_id) == i:
                borrowed_by_user = True
        if borrowed_by_user:
            last_check = messagebox.askyesno("Already Borrowed", "This book is currently borrowed by a User or Users!\nIt's highly recommended to wait before the book is returned. You can skip this by using that small 'RD' button and lock the book so no one would be able to borrow nor delete it!\n\nBut if you wish otherwise; however, as a consequence, you'll need to free the user MANUALLY after they have returned the book or paid off their debt.\n\nAre you sure you're going to Delete the book now?")
            if last_check:
                pass
            else:
                return

        current_username = getpass.getuser()
        event_by_admin = current_username
        cursor.execute("SELECT title FROM books WHERE id=?", (book_id,))
        book_title_tuple = cursor.fetchone()
        book_title = book_title_tuple[0] if book_title_tuple else None

        conn1 = sqlite3.connect("event_logs.db")
        cursor1 = conn1.cursor()
        cursor1.execute("""CREATE TABLE IF NOT EXISTS deleted_books (
                        event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        book_title TEXT,
                        book_id INTEGER,
                        event_by_admin TEXT,
                        event_date TEXT
                        )""")
        conn1.commit()

        cursor1.execute("INSERT INTO deleted_books (book_title, book_id, event_by_admin, event_date) VALUES (?, ?, ?, ?)",
                    (book_title, book_id, event_by_admin, datetime.datetime.now()))
        conn1.commit()
        conn1.close()

        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        conn.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Deleted", "Book has been deleted.")
        elif str(book_id) != "" :
            messagebox.showerror("Error", "Book not found.")

        book_id_entry_delete.delete(0, tk.END)

    else:
        messagebox.showerror("Book Reserved!", "You cannot delete this book since it has been reserved!\nUse 'RD' and 'URD' small buttons below to Reserve or UnReserve books for deletion.")
        return

def borrow_book():
    username = username_entry_borrow.get()
    password = password_entry_borrow.get()
    book_id = book_id_entry_borrow.get()
    days = days_entry_borrow.get()

    try:
        book_id = int(book_id)
    except (ValueError , TypeError):
        if str(book_id) != "" :
            messagebox.showerror("Book ID ValueType Error", "'Book ID' must be a Number! You can also retrieve it.")
            return
        else:
            pass
    try:
        days = int(days)
    except (ValueError , TypeError):
        if str(days) != "" :
            messagebox.showerror("Days ValueType Error", "'Number of Days' must be a Number!\n\n*** Also keep in mind you're never allowed to borrow a book for more than 15 days! ***")
            return
        else:
            pass

    if username == "" or password == "" or str(book_id) == "" or str(days) == "":
        messagebox.showerror("Error", "All fields must be filled in.")
        return
    
    if days > 15:

        messagebox.showerror("Days Error", "Days exceeded the allowed limit!\nBear in mind that no more than 15 days could be maxing out the cap.")
        return
    else:
        pass

    if str(username) != "" and str(password) != "" and str(book_id) != "" and str(days) != "":
        borrow_confirmation = messagebox.askyesno("Borrow Confirmation", "It seems as though an admin is attmepting to borrow a specific book for a User!\nPrepare for a Double Check & ...\n\n--PROCEED?--")
        if borrow_confirmation:
            pass
        else:
            return

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password))
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
        messagebox.showinfo(
            "Unavailable", "Apologies, This book is just currently not physically available in our library.\nPlease come back later!")
        return

    borrowed_ids.append(str(book_id))
    borrowed_ids_str = ",".join(borrowed_ids)

    cursor.execute("SELECT days_remaining FROM users WHERE username=?", (username,))
    days_remaining_tuple = cursor.fetchone()
    days_remaining = days_remaining_tuple[0] if days_remaining_tuple else None

    borrowed_ids_string = str(borrowed_ids).split(",")

    try:
        days_remaining = int(days_remaining)
    except (TypeError , ValueError):
        pass

    if len(borrowed_ids_string) < 3:

        cursor.execute("UPDATE users SET borrowed_ids=?, date_borrowed=? WHERE id=?",
                    (borrowed_ids_str, datetime.datetime.now(), user[0]))
        if days_remaining is None or str(days_remaining) == "user_exempt" or str(days_remaining) == "":
            cursor.execute("UPDATE users SET days_remaining=? WHERE id=?", (days, user[0]))
        else:
            pass
        
        try:
            days_remaining = int(days_remaining)
            if days_remaining is None or int(days_remaining) < days:
                cursor.execute("UPDATE users SET days_remaining=? WHERE id=?", (days, user[0]))
        except (TypeError , ValueError):
            pass

        cursor.execute("UPDATE books SET instances=? WHERE id=?", (instances - 1, book[0]))
        conn.commit()
    else:
        messagebox.showerror("Limit Exceeded", "To fight off abuse, Each user can only borrow up to 2 books in a row & NO MORE than the specified limit!\nReturn one book to free up space for the other!")
        return

    cursor.execute("SELECT id FROM users WHERE username=?", (username,))
    user_id_tuple = cursor.fetchone()
    user_id = user_id_tuple[0] if user_id_tuple else None
    try:
        user_id = int(user_id)
    except (TypeError , ValueError):
        pass
    cursor.execute("SELECT title FROM books WHERE id=?", (book_id,))
    book_title_tuple = cursor.fetchone()
    book_title = book_title_tuple[0] if book_title_tuple else None
    days_period = days
    current_username = getpass.getuser()
    event_by_admin = current_username

    conn1 = sqlite3.connect("event_logs.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""CREATE TABLE IF NOT EXISTS borrowed_books_by_users (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT,
                    book_id INTEGER,
                    book_title TEXT,
                    days_period INTEGER,
                    event_by_admin TEXT,
                    event_date TEXT
                    )""")
    conn1.commit()

    cursor1.execute("INSERT INTO borrowed_books_by_users (user_id, username, book_id, book_title, days_period, event_by_admin, event_date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (user_id, username, book_id, book_title, days_period, event_by_admin, datetime.datetime.now()))
    conn1.commit()
    conn1.close()

    messagebox.showinfo("Borrowed", "Book has been borrowed successfully!")

    username_entry_borrow.delete(0, tk.END)
    password_entry_borrow.delete(0, tk.END)
    book_id_entry_borrow.delete(0, tk.END)
    days_entry_borrow.delete(0, tk.END)

def return_book():
    username = username_entry_return.get()
    password = password_entry_return.get()
    book_id = book_id_entry_return.get()

    try:
        book_id = int(book_id)
    except (ValueError , TypeError):
        if str(book_id) != "" :
            messagebox.showerror("Book ID error", "'Book ID' must be a Number! You can also retrieve it.")
            return
        else:
            pass

    if username == "" or password == "" or str(book_id) == "":
        messagebox.showerror("Error", "All fields must be filled in.")
        return

    if str(username) != "" and str(password) != "" and str(book_id) != "":
        return_confirmation = messagebox.askyesno("Give-back Confirmation", "An admin's attempting to return a book on behalf of a user which can assign to them a free badge or something!\n\n--PROCEED?--")
        if return_confirmation:
            pass
        else:
            return

    cursor.execute(
        "SELECT * FROM users WHERE username=? AND password=?", (username, password))
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
        messagebox.showerror("Error", "Specified User has not borrowed this book.")
        return

    cursor.execute("SELECT reserved_deletion FROM books WHERE id=?", (book_id,))
    reserved_deletion = cursor.fetchone()
    if reserved_deletion is None:
        reserved_deletion = str(reserved_deletion)
    else:
        reserved_deletion = list(reserved_deletion)
        for i in reserved_deletion:
            i = str(i)
    not_reserved = False
    if i != "Reserved":
        not_reserved = True

    borrowed_ids.remove(str(book_id))
    borrowed_ids_str = ",".join(borrowed_ids)

    cursor.execute("UPDATE users SET borrowed_ids=? WHERE id=?", (borrowed_ids_str, user[0]))
    if not_reserved:
        cursor.execute("UPDATE books SET instances=? WHERE id=?",
                    (book[4] + 1, book[0]))
    else:
        messagebox.showinfo("Null Returned Successfully!", "User has returned their debt, but book was not returned to our database because the book had been flagged as 'Reserved'.")

    if len(borrowed_ids) == 0:
        cursor.execute("UPDATE users SET days_remaining='user_exempt' WHERE id=?", (user[0],))

    conn.commit()

    current_username = getpass.getuser()
    event_by_admin = current_username
    cursor.execute("SELECT title FROM books WHERE id=?", (book_id,))
    book_title_tuple = cursor.fetchone()
    book_title = book_title_tuple[0] if book_title_tuple else None

    if not_reserved:
        rd = "True"
    else:
        rd = "False"

    conn1 = sqlite3.connect("event_logs.db")
    cursor1 = conn1.cursor()
    cursor1.execute("""CREATE TABLE IF NOT EXISTS returned_books (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    book_title TEXT,
                    book_id INTEGER,
                    reserved_state TEXT,
                    event_by_admin TEXT,
                    event_date TEXT
                    )""")
    conn1.commit()
    cursor1.execute("INSERT INTO returned_books (username, book_title, book_id, reserved_state, event_by_admin, event_date) VALUES (?, ?, ?, ?, ?, ?)",
                (username, book_title, book_id, rd, event_by_admin, datetime.datetime.now()))
    conn1.commit()
    conn1.close()

    if not_reserved:
        messagebox.showinfo("Returned", "Book has been returned successfully.")

    username_entry_return.delete(0, tk.END)
    password_entry_return.delete(0, tk.END)
    book_id_entry_return.delete(0, tk.END)

def rd():
    book_id = book_id_entry_delete.get()

    try:
        book_id = int(book_id)
    except (ValueError , TypeError):
        messagebox.showerror("Error", "Please input a Number!\n\nHint: by using this button you're going to Lock a book and prevent it from being deleted! After you confirm, the number of available instances of the specified book will reach down to zero!")
        return
    confirmation = messagebox.askyesno("Confirmation Message", "By using this feature the number of available instances of the following book will reach '0'\n\n---SUBMIT & Proceed?---")
    if confirmation:
        pass
    else:
        return
    cursor.execute("SELECT reserved_deletion FROM books where id=?", (book_id,))
    reserved_deletion = cursor.fetchone()
    if reserved_deletion:
        try:
            reserved_deletion = list(reserved_deletion)
            for i in reserved_deletion:
                i = str(i)
            if i != "Reserved":
                cursor.execute("UPDATE books SET instances=?, reserved_deletion=? WHERE id=?", (0, "Reserved", book_id))
                conn.commit()
                messagebox.showinfo("Success!", "Book has been Reserved Successfully!")

                cursor.execute("SELECT title FROM books WHERE id=?", (book_id,))
                book_title = cursor.fetchone()
                if book_title is None:
                    book_title = str(book_title)
                else:
                    book_title = list(book_title)
                    for i in book_title:
                        i = str(i)
                current_username = getpass.getuser()
                event_by_admin = current_username
                conn1 = sqlite3.connect("event_logs.db")
                cursor1 = conn1.cursor()
                cursor1.execute("""CREATE TABLE IF NOT EXISTS reserved_deletion_log (
                                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                reserved_book_title TEXT,
                                reserved_book_id INTEGER,
                                event_by_admin TEXT,
                                event_date TEXT
                                )""")
                conn1.commit()

                cursor1.execute("INSERT INTO reserved_deletion_log (reserved_book_title, reserved_book_id, event_by_admin, event_date) VALUES (?, ?, ?, ?)",
                            (i, book_id, event_by_admin, datetime.datetime.now()))
                conn1.commit()
                conn1.close()
                book_id_entry_delete.delete(0, tk.END)
            else:
                messagebox.showerror("Already Reserved!", "Book deletion ALREADY Reserved!")
                return
        except sqlite3.OperationalError:
            messagebox.showerror("Invalid Input!", "The given Book ID is not Valid!")
            return
    else:
        messagebox.showerror("Unavailable", "Book not Available!")
    
def urd():
    book_id = book_id_entry_delete.get()

    try:
        book_id = int(book_id)
    except (ValueError , TypeError):
        messagebox.showerror("Error", "Please input a Number!\n\nHint: By using this button, you will unlock a book from deletion and Hence it will be deleted!")
        return
    confirmation = messagebox.askyesno("Confirmation Message", "You're going to Unlock the following book from being deleted!\n\n---SUBMIT & Proceed?---")
    if confirmation:
        pass
    else:
        return
    cursor.execute("SELECT reserved_deletion FROM books where id=?", (book_id,))
    reserved_deletion = cursor.fetchone()
    if reserved_deletion:
        try:
            reserved_deletion = list(reserved_deletion)
            for i in reserved_deletion:
                i = str(i)
            if i == "Reserved":
                cursor.execute("UPDATE books SET reserved_deletion=? WHERE id=?", ("", book_id))
                conn.commit()
                messagebox.showinfo("Success!", "Book has been UnReserved Successfully!\n\nDon't forget to update the Number of Instances for this book later!\nSimply use the 'Add Book' Applet above & Good Luck!")

                cursor.execute("SELECT title FROM books WHERE id=?", (book_id,))
                book_title = cursor.fetchone()
                if book_title is None:
                    book_title = str(book_title)
                else:
                    book_title = list(book_title)
                    for i in book_title:
                        i = str(i)
                current_username = getpass.getuser()
                event_by_admin = current_username
                conn1 = sqlite3.connect("event_logs.db")
                cursor1 = conn1.cursor()
                cursor1.execute("""CREATE TABLE IF NOT EXISTS unreserved_deletion_log (
                                event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                unreserved_book_title TEXT,
                                unreserved_book_id INTEGER,
                                event_by_admin TEXT,
                                event_date TEXT
                                )""")
                conn1.commit()

                cursor1.execute("INSERT INTO unreserved_deletion_log (unreserved_book_title, unreserved_book_id, event_by_admin, event_date) VALUES (?, ?, ?, ?)",
                            (i, book_id, event_by_admin, datetime.datetime.now()))
                conn1.commit()
                conn1.close()
                book_id_entry_delete.delete(0, tk.END)
            else:
                messagebox.showerror("Already UnReserved!", "Book deletion ALREADY UnReserved!")
                return
        except sqlite3.OperationalError:
            messagebox.showerror("Invalid Input!", "The given Book ID is not Valid!")
            return
    else:
        messagebox.showerror("Unavailable", "Book not Available!")

def insert_to():
    title = book_title_entry.get()
    if title == "":
        messagebox.showerror("Title Not Addressed", "To use this feature, you need to type at least a valid Book Title!\n\nHint: This feature allows you to modify Book details with more convenience and without requiring you to type every single entry again so this way you can simply read over the details and change only what has to be updated.\nAll in All, its function aims to ensure higher precision and an optimal time management!")
        return
    try:
        if title:
            query = "SELECT author, pages, instances FROM books WHERE title=?"
            cursor.execute(query, (title,))
            fetched = cursor.fetchall()
            if fetched is None:
                fetched = str(fetched)
            else:
                fetched = list(fetched)
                for i in fetched:
                    i = list(tuple(i))
                author_entry.delete(0, tk.END)
                author_entry.insert(tk.END, str(i[0]))
                pages_entry.delete(0, tk.END)
                pages_entry.insert(tk.END, str(i[1]))
                instances_entry.delete(0, tk.END)
                instances_entry.insert(tk.END, str(i[2]))
        else:
            messagebox.showerror("error", "Seems local database is raw and fresh. Therefore, no sorta books currently exists in it!")
            return
    except UnboundLocalError:
        messagebox.showerror("error", "Invalid Book Title! There could be a reason that this book is yet not available in the local database!")
        return

custom_font = Font(family="Helvetica", size=24, weight="bold")
label50 = tk.Label(root, text="$$$$$$$$ $$$$$$$$$$ $$$$$$$", font=custom_font, fg="#000000", bg="#000000")

frame_header = tk.Frame(root,bg="#000000")
frame_header.grid(column=0, row=1)
frame_header.config(height=100,width=50)

label50.pack(in_=frame_header)

custom_font = Font(family="Helvetica", size=24, weight="bold")
label51 = tk.Label(root, text="$$$$$$$$ $$$$$$$$$$ $$$$$$$", font=custom_font, fg="#000000", bg="#000000")

frame_header = tk.Frame(root,bg="#000000")
frame_header.grid(column=0, row=2)
frame_header.config(height=40,width=50)

label51.pack

custom_font = Font(family="small fonts", size=24, weight="bold")
label51 = tk.Label(root, text="$Library Management System$ \u23CE", font=custom_font, fg="yellow", bg="#000000")
label51.place(relx=0.51, rely=0, anchor=tk.N)

frame1 = tk.Frame(root, bg="#67e081")
frame1.config(height=150, width=300)
frame1.config(relief="ridge")
frame1.grid(column=0, row=3)

frame2 = tk.Frame(root, bg="#67e081")
frame2.config(height=150, width=300)
frame2.config(relief="ridge")
frame2.grid(column=0, row=4, pady=(37, 0))

frame3 = tk.Frame(root, bg="#67e081")
frame3.config(height=350, width=300)
frame3.config(relief="ridge")
frame3.grid(column=1, row=4, padx=48, pady=(37, 0))

frame4 = tk.Frame(root, bg="#67e081")
frame4.config(height=350, width=300)
frame4.config(relief="ridge")
frame4.grid(column=1, row=5, sticky="S")

frame5 = tk.Frame(root, bg="#67e081")
frame5.config(height=350, width=300)
frame5.config(relief="ridge")
frame5.grid(column=1, row=3)

frame6 = tk.Frame(root, bg="#67e081")
frame6.config(height=350, width=300)
frame6.config(relief="ridge")
frame6.grid(column=0, row=5, pady=(37, 0))

book_title_label = tk.Label(
    frame1, background="#7bdfe0", text="Book Title :", width="16")
book_title_label.grid(column=0, row=0)
book_title_entry = tk.Entry(frame1)
book_title_entry.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
book_title_entry.grid(column=1, row=0)

author_label = tk.Label(frame1, background="#7bdfe0",
                        text="Author :", width="16")
author_label.grid(column=0, row=1)
author_entry = tk.Entry(frame1)
author_entry.configure(bg="peru", fg="darkblue", justify="center", font="arial 13 bold")
author_entry.grid(column=1, row=1)

pages_label = tk.Label(frame1, background="#7bdfe0",
                       text="Number of Pages :", width="16")
pages_label.grid(column=0, row=2)
pages_entry = tk.Entry(frame1)
pages_entry.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
pages_entry.grid(column=1, row=2)

instances_label = tk.Label(
    frame1, background="#7bdfe0", text="Number of Instances:", width="16")
instances_label.grid(column=0, row=3)
instances_entry = tk.Entry(frame1)
instances_entry.configure(bg="peru", fg="darkblue", justify="center", font="arial 13 bold")
instances_entry.grid(column=1, row=3)

add_book_button = tk.Button(
    frame1, background="green", text="Add/Update Book", command=add_book, fg="white", relief="ridge")
add_book_button.grid(column=1, row=4)

update_button = tk.Button(frame1, text="Modify/prep", command=insert_to)
update_button.configure(font="arial 8 bold", pady=0, background="purple", relief="ridge", fg="yellow", width=10)
update_button.place(relx=0.24, rely=0.79, anchor=tk.N)

username_label = tk.Label(frame2, background="#7bdfe0",
                          text="Username:", width=16)
username_label.grid(column=0, row=0)
username_entry = tk.Entry(frame2)
username_entry.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
username_entry.grid(column=1, row=0)

password_label = tk.Label(frame2, background="#7bdfe0",
                          text="Password :", width=16)
password_label.grid(column=0, row=1)
password_entry = tk.Entry(frame2)
password_entry.configure(bg="peru", fg="darkblue", justify="center", font="arial 13 bold", show="*")
password_entry.grid(column=1, row=1)

add_user_button = tk.Button(
    frame2, background="green", text="Add User", command=add_user, fg="white", relief="ridge")
add_user_button.grid(column=1, row=2)

username_label_retrieve = tk.Label(
    frame3, background="#7bdfe0", text="Username :", width="16")
username_label_retrieve.grid(column=0, row=0)
username_entry_retrieve = tk.Entry(frame3)
username_entry_retrieve.configure(bg="peru", fg="darkblue", justify="center", font="arial 13 bold")
username_entry_retrieve.grid(column=1, row=0)

book_title_label_retrieve = tk.Label(
    frame3, background="#7bdfe0", text="Book Title :", width="16")
book_title_label_retrieve.grid(column=0, row=1)
book_title_entry_retrieve = tk.Entry(frame3)
book_title_entry_retrieve.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
book_title_entry_retrieve.grid(column=1, row=1)

retrieve_ids_button = tk.Button(
    frame3, background="green", text="Retrieve IDs", command=retrieve_ids, fg="white", relief="ridge")
retrieve_ids_button.grid(column=1, row=2)

book_id_label_delete = tk.Label(
    frame4, background="#7bdfe0", text="Book ID :", width=16)
book_id_label_delete.grid(column=0, row=0)
book_id_entry_delete = tk.Entry(frame4)
book_id_entry_delete.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
book_id_entry_delete.grid(column=1, row=0)

reserve_deletion_button = tk.Button(frame4, text="RD", command=rd)
reserve_deletion_button.configure(font="arial 7 bold", pady=0, background="yellow", relief="ridge")
reserve_deletion_button.place(relx=0.36, rely=0.57, anchor=tk.N)

division = tk.Label(frame4, background="#67e081", fg="#000000", text="|", font="impact 12 bold")
division.place(relx=0.23, rely=0.47, anchor=tk.N)

unreserve_deletion_button = tk.Button(frame4, text="URD", command=urd)
unreserve_deletion_button.configure(font="arial 7 bold", pady=0, background="#0000ff", fg="yellow", relief="ridge")
unreserve_deletion_button.place(relx=0.1, rely=0.57, anchor=tk.N)

delete_book_button = tk.Button(
    frame4, background="green", text="Delete Book", command=delete_book, fg="white", relief="ridge")
delete_book_button.grid(column=1, row=1)

username_label_borrow = tk.Label(
    frame5, background="#7bdfe0", text="Username :", width="16")
username_label_borrow.grid(column=0, row=0)
username_entry_borrow = tk.Entry(frame5)
username_entry_borrow.configure(bg="peru", fg="darkblue", justify="center", font="arial 13 bold")
username_entry_borrow.grid(column=1, row=0)

password_label_borrow = tk.Label(
    frame5, background="#7bdfe0", text="Password :", width="16")
password_label_borrow.grid(column=0, row=1)
password_entry_borrow = tk.Entry(frame5)
password_entry_borrow.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold", show="*")
password_entry_borrow.grid(column=1, row=1)

book_id_label_borrow = tk.Label(
    frame5, background="#7bdfe0", text="Book ID :", width="16")
book_id_label_borrow.grid(column=0, row=2)
book_id_entry_borrow = tk.Entry(frame5)
book_id_entry_borrow.configure(bg="peru", fg="darkblue", justify="center", font="arial 13 bold")
book_id_entry_borrow.grid(column=1, row=2)

days_label_borrow = tk.Label(
    frame5, background="#7bdfe0", text="Number of Days :", width="16")
days_label_borrow.grid(column=0, row=3)
days_entry_borrow = tk.Entry(frame5)
days_entry_borrow.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
days_entry_borrow.grid(column=1, row=3)

borrow_book_button = tk.Button(
    frame5, background="green", text="Borrow Book", command=borrow_book, fg="white", relief="ridge")
borrow_book_button.grid(column=1, row=4)

username_label_return = tk.Label(
    frame6, background="#7bdfe0", text="Username :", width=16)
username_label_return.grid(column=0, row=0)
username_entry_return = tk.Entry(frame6)
username_entry_return.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
username_entry_return.grid(column=1, row=0)

password_label_return = tk.Label(
    frame6, background="#7bdfe0", text="Password :", width=16)
password_label_return.grid(column=0, row=1)
password_entry_return = tk.Entry(frame6)
password_entry_return.configure(bg="peru", fg="darkblue", justify="center", font="arial 13 bold", show="*")
password_entry_return.grid(column=1, row=1)

book_id_label_return = tk.Label(
    frame6, background="#7bdfe0", text="Book ID :", width=16)
book_id_label_return.grid(column=0, row=2)
book_id_entry_return = tk.Entry(frame6)
book_id_entry_return.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
book_id_entry_return.grid(column=1, row=2)

return_book_button = tk.Button(
    frame6, background="green", text="Return Book", command=return_book, fg="white", relief="ridge")
return_book_button.grid(column=1, row=3)

#Task_Manager
def run_update_database():
    subprocess.Popen(['python', 'Additional Complementary Tools/Check Charged Users/RUN THIS FIRST.py'])

def run_check_charged_users():
    subprocess.Popen(['python', 'Additional Complementary Tools/Check Charged Users/Check/Library_Management_System_Check_User_Charge_With_Username.py'])

def run_manually_free_user():
    subprocess.Popen(['python', 'Additional Complementary Tools/Free a User/Free.py'])

def run_library_monitor():
    subprocess.Popen(['python', 'Additional Complementary Tools/Library Monitor/Library_Supervisor.py'])

def run_show_treeview():
    subprocess.Popen(['python', 'Additional Complementary Tools/Show database/Show.py'])
def run_registry():
    subprocess.Popen(['python', 'Additional Complementary Tools/registry/registry.py'])

access_manager = tk.Tk()
access_manager.option_add("*Font", "terminal 14 bold")
access_manager.title("$$ Access Manager $$")
access_manager.geometry("550x550")
access_manager.configure(bg="#000000")
access_manager.resizable(False,False)
custom_font_2 = Font(family="arial", size=17)
label37 = tk.Label(access_manager, text="Use These Buttons to Access all Tools inside an All-in-One whole window: \u23CE", font=custom_font_2, fg="#ffff00", bg="#000000")
label37.pack()

space37 = tk.Label(access_manager, text="")
space37.configure(bg="#000000")
space38 = tk.Label(access_manager, text="")
space38.configure(bg="#000000")
space37.pack()
space39 = tk.Label(access_manager, text="")
space39.configure(bg="#000000")
space40 = tk.Label(access_manager, text="")
space40.configure(bg="#000000")
space41 = tk.Label(access_manager, text="")
space41.configure(bg="#000000")
space42 = tk.Label(access_manager, text="")
space42.configure(bg="#000000")
space43 = tk.Label(access_manager, text="")
space43.configure(bg="#000000")

update_database_button = tk.Button(access_manager, text="Update Database's Timezone!", background="#00ff00", foreground="darkblue", width=40, height=2, relief="ridge", command=run_update_database)
check_charged_users_button = tk.Button(access_manager, text="Check Charged Users", background="#00ff00", foreground="darkblue", width=40, height=2, relief="ridge", command=run_check_charged_users)
manually_free_user_button = tk.Button(access_manager, text="Manually Free a User", background="#00ff00", foreground="darkblue", width=40, height=2, relief="ridge", command=run_manually_free_user)
library_monitor_button = tk.Button(access_manager, text="Library Monitor", background="#00ff00", foreground="darkblue", width=40, height=2, relief="ridge", command=run_library_monitor)
show_treeview_button = tk.Button(access_manager, text="Show Treeview", background="#00ff00", foreground="darkblue", width=40, height=2, relief="ridge", command=run_show_treeview)
registry_button = tk.Button(access_manager, text="Register Books & Users", background="#00ff00", foreground="darkblue", width=40, height=2, relief="ridge", command=run_registry)
exit_button = tk.Button(access_manager, text="Exit", background="#ff0000", foreground="darkblue", width=8, relief="raised", font="calibri 14 bold", command=exit_the_program)

update_database_button.pack()
space39.pack()
check_charged_users_button.pack()
space40.pack()
manually_free_user_button.pack()
space41.pack()
library_monitor_button.pack()
space42.pack()
show_treeview_button.pack()
space38.pack()
registry_button.pack()
space43.pack()
exit_button.pack()

access_manager.mainloop()
root.mainloop()
conn.close()