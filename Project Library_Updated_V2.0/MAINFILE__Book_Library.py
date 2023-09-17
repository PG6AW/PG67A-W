import tkinter as tk
from tkinter import messagebox , TclError
import sqlite3
import datetime
from tkinter.font import Font
import subprocess


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
    except ValueError:
        if str(pages) != "" :
            messagebox.showerror("Book Pages ValueType Error", "Value for 'Number of Pages' must be Numerical!")
            return
        else:
            pass
    try:
        instances = int(instances)
    except ValueError:
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
        
    cursor.execute("SELECT * FROM books WHERE title=?", (title,))
    book = cursor.fetchone()

    if book:
        cursor.execute(
            "UPDATE books SET pages=?, instances=? WHERE id=?", (pages, instances, book[0]))
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

def exit_the_program():
    try:
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
        messagebox.showerror("Book Not Specified!!!", "Please provide us with a specified Book ID or retrieve it if you need to delete a book!\n\nPlease note that you always need the book ID anytime you want to delete a book and not its Title per se would do the trick for you alone!\n\nWe mandated this to force admins to double-check their request and make sure everything's alright before making their decision firm!\n\nThanks for understanding the potential of this action!")
        return
    try:
        book_id = int(book_id)
    except ValueError:
        if str(book_id) != "" :
            messagebox.showerror("Book ID ValueType Error", "'Book ID' must be a Number! You can also retrieve it from the applet above!")
            return
        else:
            pass

    if str(book_id) != "" :
        delete_confirm = messagebox.askyesno("Confirm Book Deletion", "You're going to completely purge a book from the database by its ID!\nUndertaking its consequences would be a bit speculative and pose risks as it could make an unwanted change to the database!\nSure what you're really doing while reconsidering all the risks involved?\nIf Yes & have already Double-Checked everything, then ...\n\n--PROCEED?--")
        if delete_confirm:
            pass
        else:
            return

    cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()

    if cursor.rowcount > 0:
        messagebox.showinfo("Deleted", "Book has been deleted.")
    elif str(book_id) != "" :
        messagebox.showerror("Error", "Book not found.")

    book_id_entry_delete.delete(0, tk.END)

def borrow_book():
    username = username_entry_borrow.get()
    password = password_entry_borrow.get()
    book_id = book_id_entry_borrow.get()
    days = days_entry_borrow.get()

    try:
        book_id = int(book_id)
    except ValueError:
        if str(book_id) != "" :
            messagebox.showerror("Book ID ValueType Error", "'Book ID' must be a Number! You can also retrieve it.")
            return
        else:
            pass
    try:
        days = int(days)
    except ValueError:
        if str(days) != "" :
            messagebox.showerror("Days ValueType Error", "'Number of Days' must be a Number!")
            return
        else:
            pass

    if username == "" or password == "" or str(book_id) == "" or str(days) == "":
        messagebox.showerror("Error", "All fields must be filled in.")
        return

    if str(username) != "" and str(password) != "" and str(book_id) != "" and str(days) != "":
        borrow_confirmation = messagebox.askyesno("Borrow Confirmation", "It seems as though an admin's attmepting to borrow a user a specific Book!\nPrepare for a Double Check & ...\n\n--PROCEED?--")
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
            "Unavailable", "This book is not available in the library.")
        return

    borrowed_ids.append(str(book_id))
    borrowed_ids_str = ",".join(borrowed_ids)

    cursor.execute("UPDATE users SET borrowed_ids=?, days_remaining=?, date_borrowed=? WHERE id=?",
                   (borrowed_ids_str, days, datetime.datetime.now(), user[0]))
    cursor.execute("UPDATE books SET instances=? WHERE id=?", (instances - 1, book[0]))
    conn.commit()

    messagebox.showinfo("Borrowed", "Book has been borrowed successfully.")

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
    except ValueError:
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

    borrowed_ids.remove(str(book_id))
    borrowed_ids_str = ",".join(borrowed_ids)

    cursor.execute("UPDATE users SET borrowed_ids=? WHERE id=?", (borrowed_ids_str, user[0]))
    cursor.execute("UPDATE books SET instances=? WHERE id=?",
                   (book[4] + 1, book[0]))

    if len(borrowed_ids) == 0:
        cursor.execute("UPDATE users SET days_remaining='user_exempt' WHERE id=?", (user[0],))

    conn.commit()

    messagebox.showinfo("Returned", "Book has been returned successfully.")

    username_entry_return.delete(0, tk.END)
    password_entry_return.delete(0, tk.END)
    book_id_entry_return.delete(0, tk.END)

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
    frame1, background="#E7717D", text="Add Book", command=add_book)
add_book_button.grid(column=1, row=4)

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
password_entry.configure(bg="peru", fg="darkblue", justify="center", font="arial 13 bold")
password_entry.grid(column=1, row=1)

add_user_button = tk.Button(
    frame2, background="#E7717D", text="Add User", command=add_user)
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
    frame3, background="#E7717D", text="Retrieve IDs", command=retrieve_ids)
retrieve_ids_button.grid(column=1, row=2)

book_id_label_delete = tk.Label(
    frame4, background="#7bdfe0", text="Book ID :", width=16)
book_id_label_delete.grid(column=0, row=0)
book_id_entry_delete = tk.Entry(frame4)
book_id_entry_delete.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
book_id_entry_delete.grid(column=1, row=0)

delete_book_button = tk.Button(
    frame4, background="#E7717D", text="Delete Book", command=delete_book)
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
password_entry_borrow.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
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
    frame5, background="#E7717D", text="Borrow Book", command=borrow_book)
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
password_entry_return.configure(bg="peru", fg="darkblue", justify="center", font="arial 13 bold")
password_entry_return.grid(column=1, row=1)

book_id_label_return = tk.Label(
    frame6, background="#7bdfe0", text="Book ID :", width=16)
book_id_label_return.grid(column=0, row=2)
book_id_entry_return = tk.Entry(frame6)
book_id_entry_return.configure(bg="saddle brown", fg="#ffffff", justify="center", font="arial 13 bold")
book_id_entry_return.grid(column=1, row=2)

return_book_button = tk.Button(
    frame6, background="#E7717D", text="Return Book", command=return_book)
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

def run_show_listboxes():
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
show_listboxes_button = tk.Button(access_manager, text="Show Listboxes", background="#00ff00", foreground="darkblue", width=40, height=2, relief="ridge", command=run_show_listboxes)
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
show_listboxes_button.pack()
space38.pack()
registry_button.pack()
space43.pack()
exit_button.pack()

access_manager.mainloop()
root.mainloop()
