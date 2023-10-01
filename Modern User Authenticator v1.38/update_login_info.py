import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import getpass
import subprocess
import datetime
import ctypes


conn = sqlite3.connect("accounts.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS register (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT,
               gender TEXT,
               birth_year INTEGER,
               birth_month TEXT,
               birth_day INTEGER,
               email TEXT,
               username TEXT UNIQUE,
               password TEXT,
               event_by_admin TEXT,
               register_date TEXT
)
""")
conn.commit()

conn = sqlite3.connect("accounts.db")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS cache (username TEXT)""")
conn.commit()
cursor.execute("SELECT username FROM cache")
cross_username = cursor.fetchone()
if cross_username is None:
    pass
else:
    cross_username = list(cross_username)
    for cross in cross_username:
        cross = str(cross)
conn.commit()
cursor.execute("DELETE FROM cache")
conn.commit()

def change():
    username = username_entry.get()
    old_password = old_password_entry.get()
    name = name_entry.get()
    gender = selected_button.get()
    birth_year = year_menu.get()
    birth_month = month_menu.get()
    birth_day = day_menu.get()
    email = email_entry.get()
    new_password = new_password_entry.get()
    confirm_password = confirm_new_password_entry.get()

    if username == "" or old_password == "" or name == "" or email == "" or new_password == "" or confirm_password == "":
        messagebox.showerror("Error", "Please fill in all fields!")
        return
    
    if gender == "" or str(gender) == "None" or gender == None:
        messagebox.showerror("Error", "Please choose your gender pronoun!")
        return

    if birth_year == "YEAR":
        messagebox.showerror("Error", "Please select your Year of Birth!")
        return
    
    if birth_month == "MONTH":
        messagebox.showerror("Error", "Please select your Month of Birth!")
        return
    
    if birth_day == "DAY":
        messagebox.showerror("Error", "Please select your Day of Birth!")
        return

    try:
        birth_year = int(birth_year)
    except(ValueError , TypeError):
        pass

    try:
        birth_day = int(birth_day)
    except(ValueError , TypeError):
        pass

    conn = sqlite3.connect("accounts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM register")
    usernames = cursor.fetchall()
    if usernames is None:
        usernames = str(usernames)
    else:
        usernames = list(usernames)
    if (f"('{username}',)") in str(usernames):
        pass
    else:
        messagebox.showerror("Invalid Username", "Usernames are UNIQUE values, meaning they cannot change.\nAnd the Username you have provided, doesn't exist in the local database!\n\nMake sure everything's alright before you confirm the submission!")
        return

    ambiguous_char = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", '"', "'", "|", "{", "}", "[", "]", ":", ";", "/", "?", ",", ".", ">", "<"]
    num_char = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    lower_case_char = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    upper_case_char = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    ambiguous_check = []
    num_check = []
    lower_case_char_check = []
    upper_case_char_check = []

    if len(new_password) < 8:
        messagebox.showerror("error", "Password is too short!\nPassphrase must be at least 8 characters long!")
        return
    else:
        for amb in ambiguous_char:
            if amb in new_password:
                ambiguous_check.append("1")
            else:
                pass
        if len(ambiguous_check) > 0:
            for num in num_char:
                if num in new_password:
                    num_check.append("1")
                else:
                    pass
            if len(num_check) > 2:
                for lower in lower_case_char:
                    if lower in new_password:
                        lower_case_char_check.append("1")
                    else:
                        pass
                if len(lower_case_char_check) > 2:
                    for upper in upper_case_char:
                        if upper in new_password:
                            upper_case_char_check.append("1")
                        else:
                            pass
                    if len(upper_case_char_check) > 0:
                        pass
                    else:
                        messagebox.showerror("error", "You should at least include 1 upper case letter in your password!")
                        return
                else:
                    messagebox.showerror("error", "You should at least include 3 different lower case letters in your password!")
                    return
            else:
                messagebox.showerror("error", "You should at least include 3 different numbers in your password!")
                return
        else:
            messagebox.showerror("error", "You should at least include 1 ambiguous character in your password!")
            return
        if new_password != confirm_password:
            messagebox.showerror("Cfrm-P-N-M Error!", "PASSWORDS DO NOT MATCH! PLEASE CONFIRM YOUR PASSWORD FIRST!")
            return
        else:
            pass

    cursor.execute("SELECT password FROM register WHERE username=?", (username,))
    correct_password = cursor.fetchone()
    if correct_password is None:
        correct_password = str(correct_password)
    else:
        correct_password = list(correct_password)
        for i in correct_password:
            i = str(i)
    if old_password == i:
        if str(old_password) == str(new_password):
            messagebox.showerror("Identical Passwords!", "New password and old password should not be identical!\nChoose something new as your new password!")
            return
        else:
            pass
        confirm = messagebox.askyesno("Confirmation", "YOU HAVE BEEN AUTHENTICATED!\nDo you confirm the changes you are making to your account?\nAlways double-check before you proceed. Do this specially for your password since it's the only key to accessing your account!\n\n__PROCEED?__")
        if confirm:
            username_entry.delete(0, tk.END)
            old_password_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            selected_button.set(None)
            year_menu.set("YEAR")
            month_menu.set("MONTH")
            day_menu.set("DAY")
            email_entry.delete(0, tk.END)
            new_password_entry.delete(0, tk.END)
            confirm_new_password_entry.delete(0, tk.END)
            pass
        else:
            return

        cursor.execute("UPDATE register SET name=?, gender=?, birth_year=?, birth_month=?, birth_day=?, email=?, password=?", (name, gender, birth_year, birth_month, birth_day, email, new_password))
        conn.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS updated_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    new_password TEXT,
                    changed_name TEXT,
                    corrected_gender TEXT,
                    corrected_birth_year INTEGER,
                    corrected_birth_month TEXT,
                    corrected_birth_day INTEGER,
                    changed_email TEXT,
                    event_by_admin TEXT,
                    commit_date TEXT
        )
        """)
        conn.commit()
        current_username = getpass.getuser()
        event_by_admin = current_username
        cursor.execute("INSERT INTO updated_logs (username, new_password, changed_name, corrected_gender, corrected_birth_year, corrected_birth_month, corrected_birth_day, changed_email, event_by_admin, commit_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (username, new_password, name, gender, birth_year, birth_month, birth_day, email, event_by_admin, datetime.datetime.now()))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success!", "Successfully updated your details including your name and password!\n\nYou are now being redirected to the Login window shortly...")
        subprocess.Popen(['python', 'login.py'])
        window2.destroy()
    else:
        messagebox.showerror("Error", "Sounds like you don't remember your password!\nWithout your old password there is no way to change your details, nor can you access the library app.\n\nIf for any reason you need to recover your account, reach out to managers ASAP!")
        return

def real_time_password_status_label():
    password = new_password_entry.get()
    old_password = old_password_entry.get()
    confirm_password = confirm_new_password_entry.get()

    ambiguous_char = ["`", "~", "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "=", '"', "'", "|", "{", "}", "[", "]", ":", ";", "/", "?", ",", ".", ">", "<"]
    num_char = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
    lower_case_char = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    upper_case_char = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    ambiguous_check = []
    num_check = []
    lower_case_char_check = []
    upper_case_char_check = []

    ambiguous_perplexity = []
    num_perplexity = []
    lower_case_perplexity = []
    upper_case_perplexity = []
    for char in password:
        if char in ambiguous_char:
            if len(num_perplexity) == 0 and len(upper_case_perplexity) == 0:
                ambiguous_perplexity.append(1)
            elif len(num_perplexity) > 0 or len(upper_case_perplexity) > 0:
                ambiguous_perplexity.append(2)
                num_perplexity.clear()
        if char in num_char:
            if len(ambiguous_perplexity) == 0 and len(lower_case_perplexity) == 0:
                num_perplexity.append(1)
            elif len(ambiguous_perplexity) > 0 or len(lower_case_perplexity) > 0:
                num_perplexity.append(2)
                lower_case_perplexity.clear()
        if char in lower_case_char:
            if len(num_perplexity) == 0 and len(upper_case_perplexity) == 0:
                lower_case_perplexity.append(1)
            elif len(num_perplexity) > 0 or len(upper_case_perplexity) > 0:
                lower_case_perplexity.append(2)
                upper_case_perplexity.clear()
        if char in upper_case_char:
            if len(ambiguous_perplexity) == 0 and len(lower_case_perplexity) == 0:
                upper_case_perplexity.append(1)
            elif len(ambiguous_perplexity) > 0 or len(lower_case_perplexity) > 0:
                upper_case_perplexity.append(2)
                ambiguous_perplexity.clear()

    perplexity_level = "low"
    if 2 in ambiguous_perplexity:
        perplexity_level = "medium"
    if 2 in upper_case_perplexity:
        perplexity_level = "medium"
    if 2 in lower_case_perplexity:
        perplexity_level = "medium"
    if 2 in num_perplexity:
        perplexity_level = "medium"
    if (2 in ambiguous_perplexity) and (2 in lower_case_perplexity):
        perplexity_level = "high"
    if (2 in upper_case_perplexity) and (2 in num_perplexity):
        perplexity_level = "high"
    if (2 in ambiguous_perplexity) and (2 in num_perplexity):
        perplexity_level = "high"
    if (2 in upper_case_perplexity) and (2 in lower_case_perplexity):
        perplexity_level = "high"
    if (2 in lower_case_perplexity) and (2 in num_perplexity):
        perplexity_level = "high"
    if (2 in ambiguous_perplexity) and (2 in upper_case_perplexity):
        perplexity_level = "high"

    if len(password) == 0:
        stat = "Waiting for you ..."
    elif len(password) < 4:
        stat = "Weakest Passphrase ever!"
    elif len(password) < 8:
        stat = "Passphrase is quite Poor!"
    else:
        for amb in ambiguous_char:
            if amb in password:
                ambiguous_check.append("1")
            else:
                pass
        if len(ambiguous_check) > 0:
            for num in num_char:
                if num in password:
                    num_check.append("1")
                else:
                    pass
            if len(num_check) > 2:
                for lower in lower_case_char:
                    if lower in password:
                        lower_case_char_check.append("1")
                    else:
                        pass
                if len(lower_case_char_check) > 2:
                    for upper in upper_case_char:
                        if upper in password:
                            upper_case_char_check.append("1")
                        else:
                            pass
                    if len(upper_case_char_check) > 0:
                        stat = "Passphrase strength is Fair!"
                        if len(password) > 15 and len(num_check) > 4 and len(lower_case_char_check) > 6 and len(upper_case_char_check) > 1 and len(ambiguous_check) > 1:
                            stat = "Passphrase strength is Average!"
                        if len(password) > 21 and len(upper_case_char_check) > 2 and len(num_check) > 7 and len(lower_case_char_check) > 8 and len(ambiguous_check) > 1 and (perplexity_level == "medium" or perplexity_level == "high"):
                            stat = "Passphrase strength is Good!"
                        if len(password) > 35 and len(ambiguous_check) > 4 and len(upper_case_char_check) > 7 and len(lower_case_char_check) > 12 and len(num_check) > 8 and (perplexity_level == "medium" or perplexity_level == "high"):
                            stat = "Noice! Passphrase strength is now Great!"
                        if len(password) > 45 and len(ambiguous_check) > 7 and len(upper_case_char_check) > 9 and len(lower_case_char_check) > 15 and len(num_check) > 9 and (perplexity_level == "high"):
                            stat = "Great Job! The Passphrase is now Consolidated!"
                        if len(password) > 50 and len(ambiguous_check) > 9 and len(upper_case_char_check) > 11 and len(num_check) > 9 and len(lower_case_char_check) > 17 and (perplexity_level == "high"):
                            stat = "Excellent! This Passphrase is Fortified!"
                        if str(password) == str(old_password):
                            stat = "New password shouldn't be the same as the old one!"
                    else:
                        stat = "Passphrase is still Weak!"
                else:
                    stat = "Passphrase is still Weak!"
            else:
                stat = "Passphrase is still Weak!"
        else:
            stat = "Passphrase is still Weak!"

    if password != confirm_password and (stat == "Passphrase strength is Average!" or stat == "Passphrase strength is Fair!" or stat == "Passphrase strength is Good!" or stat == "Noice! Passphrase strength is now Great!" or stat == "Excellent! This Passphrase is Fortified!" or stat == "Great Job! The Passphrase is now Consolidated!"):
        stat_label.place(relx=0.5, rely=0.948, anchor=tk.N)
        stat = "PASSWORDS DO NOT MATCH!\nEventhough you may have almost passed some strict security measures,\nBUT PLEASE CONFIRM YOUR PASSWORD FIRST!"
    else:
        stat_label.place(relx=0.5, rely=0.978, anchor=tk.N)
        pass
    status_label.set(stat)

show_it = "no"
def show_entry_text():
    global show_it
    if show_it != "yes":
        old_password_entry.configure(show="")
        show_pass_button.configure(text="Hide", bg="#333333", fg="white")
        show_it = "yes"
    elif show_it == "yes":
        old_password_entry.configure(show="*")
        show_pass_button.configure(text="Show", bg="red", fg="yellow")
        show_it = "no"

show_it_2 = "no"
def show_entry_text_2():
    global show_it_2
    if show_it_2 != "yes":
        new_password_entry.configure(show="")
        show_pass_button_2.configure(text="Hide", bg="#333333", fg="white")
        show_it_2 = "yes"
    elif show_it_2 == "yes":
        new_password_entry.configure(show="*")
        show_pass_button_2.configure(text="Show", bg="red", fg="yellow")
        show_it_2 = "no"

show_it_3 = "no"
def show_entry_text_3():
    global show_it_3
    if show_it_3 != "yes":
        confirm_new_password_entry.configure(show="")
        show_pass_button_3.configure(text="Hide", bg="#333333", fg="white")
        show_it_3 = "yes"
    elif show_it_3 == "yes":
        confirm_new_password_entry.configure(show="*")
        show_pass_button_3.configure(text="Show", bg="red", fg="yellow")
        show_it_3 = "no"

def back():
    confirm = messagebox.askyesno("Confirmation", "Back to Login page?")
    if confirm:
        conn.close()
        subprocess.Popen(['python', 'login.py'])
        window2.destroy()
    else:
        return

def check_caps_lock():
    keyboard_state = ctypes.windll.user32.GetKeyState(0x14)
    caps_lock_state = keyboard_state & 0x0001 != 0
    
    if caps_lock_state:
        caps_lock_label_left.configure(fg="red", text="CapsLock On!")
        caps_lock_label_right.configure(fg="red", text="CapsLock On!")
        caps_lock_label_left_2.configure(fg="red", text="CapsLock On!")
        caps_lock_label_right_2.configure(fg="red", text="CapsLock On!")
    else:
        caps_lock_label_left.configure(fg="#333333", text="")
        caps_lock_label_right.configure(fg="#333333", text="")
        caps_lock_label_left_2.configure(fg="#333333", text="")
        caps_lock_label_right_2.configure(fg="#333333", text="")
    window2.after(1000, check_caps_lock)

window2 = tk.Tk()
window2.configure(bg="#333333")
window2.geometry("560x950")
window2.title("Update Details")
window2.resizable(False, False)

main_label = tk.Label(window2, text="Commit Changes ", font="impact 17 italic", bg="orange")
username_label = tk.Label(window2, text="Enter your UNIQUE Username: ", font="arial 15 bold", bg="yellow")
username_entry = tk.Entry(window2, font="arial 20 italic", justify="center", width=34, fg="darkblue", relief="ridge", bg="#999999")
old_password_label = tk.Label(window2, text="Enter your Old Password: ", font="arial 15 bold", bg="yellow")
old_password_entry = tk.Entry(window2, font="arial 20 italic", justify="center", width=34, fg="darkblue", relief="ridge", show="*", bg="#999999")
name_label = tk.Label(window2, text="Enter your updated Name & Last Name: ", font="arial 15 bold", bg="yellow")
name_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=39, fg="purple", relief="ridge", bg="lightblue")
email_label = tk.Label(window2, text="Enter your updated Email: ", font="arial 15 bold", bg="yellow")
email_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=39, fg="purple", relief="ridge", bg="lightblue")
new_password_label = tk.Label(window2, text="Enter your New Password: ", font="arial 15 bold", bg="yellow")
new_password_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=39, fg="darkgreen", relief="ridge", show="*", bg="lightblue")
confirm_new_password_label = tk.Label(window2, text="Confirm the New Password: ", font="arial 15 bold", bg="yellow")
confirm_new_password_entry = tk.Entry(window2, font="arial 17 italic", justify="center", width=39, fg="darkgreen", relief="ridge", show="*", bg="lightblue")
dropdowns_frame = tk.LabelFrame(window2, text="Choose your Date of Birth:", bg="#333333", fg="yellow", bd=3, highlightbackground="#00ff00", highlightthickness=1, font="arial 14 bold", width=230, pady=12, labelanchor="n")

month_menu = ttk.Combobox(dropdowns_frame, width=6, justify="center")
style2 = ttk.Style(dropdowns_frame)
style2.configure('TMenubutton', background='lightgreen')
months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
month_menu['values'] = (months)
month_menu.set("MONTH")
month_menu.configure(style='TMenubutton', font="arial 12 bold", foreground="darkgreen")
month_menu.state(['readonly'])
month_menu.pack(side="left", padx=45)

day_menu = ttk.Combobox(dropdowns_frame, width=4, justify="center")
style2 = ttk.Style(dropdowns_frame)
style2.configure('TMenubutton', background='lightgreen')
days = [int(day) for day in range(1, 32)]
day_menu['values'] = (days)
day_menu.set("DAY")
day_menu.configure(style='TMenubutton', font="arial 12 bold", foreground="darkgreen")
day_menu.state(['readonly'])
day_menu.pack(side="left", padx=45)

year_menu = ttk.Combobox(dropdowns_frame, width=4, justify="center")
style2 = ttk.Style(dropdowns_frame)
style2.configure('TMenubutton', background='lightgreen')
years = [int(year) for year in range(1870, 2024)]
year_menu['values'] = (years)
year_menu.set("YEAR")
year_menu.configure(style='TMenubutton', font="arial 12 bold", foreground="darkgreen")
year_menu.state(['readonly'])
year_menu.pack(side="left", padx=45)

style1 = ttk.Style()
style1.configure("Graphical.TRadiobutton", indicatorsize=25, background="#333333", foreground="orange", font="impact 15 italic")
radiobutton_frame = tk.LabelFrame(window2, text="You'd rather be referred to as:", bg="#333333", fg="yellow", bd=3, highlightbackground="#00ff00", highlightthickness=1, font="arial 18 bold", width=230, pady=2, labelanchor="n")
selected_button = tk.StringVar()
radio_button1 = ttk.Radiobutton(radiobutton_frame, text="He", variable=selected_button, value="Male", style="Graphical.TRadiobutton")
radio_button1.pack(side="left", padx=49)
radio_button2 = ttk.Radiobutton(radiobutton_frame, text="She", variable=selected_button, value="Female", style="Graphical.TRadiobutton")
radio_button2.pack(side="left", padx=49)
radio_button3 = ttk.Radiobutton(radiobutton_frame, text="They", variable=selected_button, value="N/A", style="Graphical.TRadiobutton")
radio_button3.pack(side="left", padx=49)

caps_lock_label_left = tk.Label(window2, text="", bg="#333333", fg="#333333", font="arial 11 bold", height=1, width=11)
caps_lock_label_right = tk.Label(window2, text="", bg="#333333", fg="#333333", font="arial 11 bold", height=1, width=11)
caps_lock_label_left_2 = tk.Label(window2, text="", bg="#333333", fg="#333333", font="arial 11 bold", height=1, width=11)
caps_lock_label_right_2 = tk.Label(window2, text="", bg="#333333", fg="#333333", font="arial 11 bold", height=1, width=11)
caps_lock_label_left.place(relx=0.15, rely=0.481, anchor=tk.N)
caps_lock_label_right.place(relx=0.85, rely=0.481, anchor=tk.N)
caps_lock_label_left_2.place(relx=0.145, rely=0.58, anchor=tk.N)
caps_lock_label_right_2.place(relx=0.855, rely=0.58, anchor=tk.N)
check_caps_lock()

submit_button = tk.Button(window2, text="Submit Changes!", font="arial 15 bold", bg="blue", fg="yellow", relief="raised", command=change)
back_button = tk.Button(window2, text="< - Back to Login", font="arial 15 bold", bg="darkblue", fg="yellow", relief="ridge", command=back)
show_pass_button = tk.Button(window2, text="Show", command=show_entry_text, font="arial 8 bold", bg="red", fg="yellow", width=4, relief="groove")
show_pass_button.place(relx=0.913, rely=0.237, anchor=tk.N)
show_pass_button_2 = tk.Button(window2, text="Show", command=show_entry_text_2, font="arial 8 bold", bg="red", fg="yellow", width=4, relief="groove")
show_pass_button_2.place(relx=0.913, rely=0.528, anchor=tk.N)
show_pass_button_3 = tk.Button(window2, text="Show", command=show_entry_text_3, font="arial 8 bold", bg="red", fg="yellow", width=4, relief="groove")
show_pass_button_3.place(relx=0.913, rely=0.625, anchor=tk.N)

try:
    username_entry.delete(0, tk.END)
    username_entry.insert(tk.END, cross)
except NameError:
    pass

status_label = tk.StringVar()
stat_label = tk.Label(window2, textvariable=status_label, bg="#333333", fg="#00ff00", font="lotus 9 italic")
new_password_entry.bind('<KeyRelease>', lambda event: real_time_password_status_label())
confirm_new_password_entry.bind('<KeyRelease>', lambda event: real_time_password_status_label())
stat_label.place(relx=0.5, rely=0.978, anchor=tk.N)

main_label.pack(pady=18)
username_label.pack(pady=10)
username_entry.pack(pady=5)
old_password_label.pack(pady=10)
old_password_entry.pack(pady=5)
name_label.pack(pady=10)
name_entry.pack(pady=5)
email_label.pack(pady=10)
email_entry.pack(pady=5)
new_password_label.pack(pady=10)
new_password_entry.pack(pady=5)
confirm_new_password_label.pack(pady=10)
confirm_new_password_entry.pack(pady=5)
radiobutton_frame.pack(padx=20, pady=20)
dropdowns_frame.pack(padx=20, pady=0)
submit_button.place(relx=0.695, rely=0.898, anchor=tk.N)
back_button.place(relx=0.29, rely=0.898, anchor=tk.N)

window2.mainloop()
conn.close()