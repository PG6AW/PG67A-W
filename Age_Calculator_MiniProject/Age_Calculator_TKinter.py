#Calculate patient's age from solar or gregorian
#TKinter GUI
#Useful for hospitals

import tkinter as tk
from tkinter import messagebox
import datetime

def from_solar():
    solar_birth = birth_year_entry.get()
    if solar_birth == "":
        messagebox.showerror("error", "Please fill in the field!")
        return
    try:
        solar_birth = int(solar_birth)
    except (ValueError , TypeError):
        messagebox.showerror("Invalid Input", "Solar birth date must be a number representing a year!")
        return

    year = ""
    timedate = datetime.datetime.now()
    timedate = str(timedate)
    year = timedate[0] + timedate[1] + timedate[2] + timedate[3]
    solar_to_greg = solar_birth + 621
    greg_birth = solar_to_greg
    if int(greg_birth) > int(year):
        messagebox.showerror("Invalid Year", "This solar year hasn't come yet!\nAre you guys living in future or sth? If so,\n\nThen tell me how you travel in time?")
        return
    age = int(year) - int(greg_birth)
    if age > 110:
        ask = messagebox.askyesno("SUS!", f"Are you sure {age} is the correct age for your patient? Seems like it could be a mistake! Or your patient is lucky enough to have lived {age} years!\n\nDouble-Check if you had inputted or mistakenly requested solar or gregorian!\n\nSince you had requested 'SOLAR' this time!")
        if ask:
            pass
        else:
            return
    messagebox.showinfo("info", f"The patient is {age} years old!")

def from_greg():
    greg_birth = birth_year_entry.get()
    if greg_birth == "":
        messagebox.showerror("error", "Please fill in the field!")
        return
    try:
        greg_birth = int(greg_birth)
    except (ValueError , TypeError):
        messagebox.showerror("Invalid Input", "Gregorian birth date must be a number representing a year!")
        return

    year = ""
    timedate = datetime.datetime.now()
    timedate = str(timedate)
    year = timedate[0] + timedate[1] + timedate[2] + timedate[3]
    if int(year) < int(greg_birth):
        messagebox.showerror("Invalid Year", "This gregorian year hasn't come yet!\nAre you guys living in future or sth? If so,\n\nThen tell me how you travel in time?")
        return
    age = int(year) - int(greg_birth)
    if age > 110:
        ask = messagebox.askyesno("SUS!", f"Are you sure {age} is the correct age for your patient? Seems like it could be a mistake! Or your patient is lucky enough to have lived {age} years!\n\nDouble-Check if you had inputted or mistakenly requested solar or gregorian!\n\nSince you had requested 'GREGORIAN' this time!")
        if ask:
            pass
        else:
            return
    messagebox.showinfo("info", f"The patient is {age} years old!")

root = tk.Tk()
root.title("Age Calculator")
root.configure(bg="blue")
root.geometry("570x200")
root.resizable(False, False)

buttons_frame = tk.Frame(root, bg="blue")
birth_year_label = tk.Label(root, text="Enter patient's Birth Year in gregorian or solar:", font="arial 18 bold", bg="blue", fg="yellow")
birth_year_entry = tk.Entry(root, width=30, font="arial 18 italic", justify="center", bg="lightblue", fg="blue")
greg_submit = tk.Button(buttons_frame, text="From Gregorian", command=from_greg, relief="groove", bg="lightgreen", fg="darkblue", font="arial 9 bold")
solar_submit = tk.Button(buttons_frame, text="From Solar", command=from_solar, relief="groove", bg="lightgreen", fg="darkblue", font="arial 9 bold")

birth_year_label.pack(pady=15)
birth_year_entry.pack(pady=15)
greg_submit.pack(side="left", padx=45)
solar_submit.pack(side="left", padx=45)
buttons_frame.pack(pady=15)
root.mainloop()