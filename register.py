
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys


# ================= LOGIN PAGE =================

def open_login():
    root.destroy()
    subprocess.Popen([sys.executable, "login.py"])


# ================= REGISTER USER =================

def register_user():

    name = name_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()
    qualification = qualification_entry.get().strip()
    skills = skills_entry.get().strip()

    if name == "" or email == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Name, Email and Password are required!"
        )
        return

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Payal@2302",
            database="online_job_portal"
        )

        cursor = connection.cursor()

        query = """
        INSERT INTO users
        (name, email, password, qualification, skills)
        VALUES (%s, %s, %s, %s, %s)
        """

        values = (
            name,
            email,
            password,
            qualification,
            skills
        )

        cursor.execute(query, values)
        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Registration Successful!\nPlease login to continue."
        )

        # Close Registration Page
        root.destroy()

        # Open Login Page
        subprocess.Popen([sys.executable, "login.py"])

    except mysql.connector.Error as error:

        # Duplicate email handling
        if "Duplicate entry" in str(error):
            messagebox.showwarning(
                "Already Registered",
                "This email is already registered!\nPlease login."
            )
        else:
            messagebox.showerror(
                "Error",
                f"Registration failed!\n{error}"
            )


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("Online Job Portal - Registration")
root.geometry("600x750")
root.resizable(False, False)
root.configure(bg="#f4f6f8")


# ================= HEADER =================

header = tk.Frame(
    root,
    bg="#1f4e79",
    height=95
)

header.pack(fill="x")


tk.Label(
    header,
    text="ONLINE JOB PORTAL",
    font=("Arial", 23, "bold"),
    bg="#1f4e79",
    fg="white"
).pack(pady=(18, 3))


tk.Label(
    header,
    text="Create your account to find your dream job",
    font=("Arial", 10),
    bg="#1f4e79",
    fg="white"
).pack()


# ================= FORM CARD =================

form = tk.Frame(
    root,
    bg="white",
    padx=40,
    pady=18
)

form.pack(
    padx=60,
    pady=18,
    fill="x"
)


# ================= TITLE =================

tk.Label(
    form,
    text="Create Your Account",
    font=("Arial", 19, "bold"),
    bg="white",
    fg="#1f4e79"
).pack(pady=(0, 2))


tk.Label(
    form,
    text="Register as a Job Seeker",
    font=("Arial", 9),
    bg="white",
    fg="#666666"
).pack(pady=(0, 12))


# ================= FULL NAME =================

tk.Label(
    form,
    text="Full Name",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333",
    anchor="w"
).pack(fill="x")


name_entry = tk.Entry(
    form,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

name_entry.pack(
    fill="x",
    ipady=5,
    pady=(3, 8)
)


# ================= EMAIL =================

tk.Label(
    form,
    text="Email Address",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333",
    anchor="w"
).pack(fill="x")


email_entry = tk.Entry(
    form,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

email_entry.pack(
    fill="x",
    ipady=5,
    pady=(3, 8)
)


# ================= PASSWORD =================

tk.Label(
    form,
    text="Password",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333",
    anchor="w"
).pack(fill="x")


password_entry = tk.Entry(
    form,
    font=("Arial", 10),
    show="*",
    relief="solid",
    bd=1
)

password_entry.pack(
    fill="x",
    ipady=5,
    pady=(3, 8)
)


# ================= QUALIFICATION =================

tk.Label(
    form,
    text="Qualification",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333",
    anchor="w"
).pack(fill="x")


qualification_entry = tk.Entry(
    form,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

qualification_entry.pack(
    fill="x",
    ipady=5,
    pady=(3, 8)
)


# ================= SKILLS =================

tk.Label(
    form,
    text="Skills",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333",
    anchor="w"
).pack(fill="x")


skills_entry = tk.Entry(
    form,
    font=("Arial", 10),
    relief="solid",
    bd=1
)

skills_entry.pack(
    fill="x",
    ipady=5,
    pady=(3, 14)
)


# ================= REGISTER BUTTON =================

register_button = tk.Button(
    form,
    text="REGISTER",
    font=("Arial", 11, "bold"),
    bg="#1f4e79",
    fg="white",
    activebackground="#163a5c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=register_user
)

register_button.pack(
    fill="x",
    ipady=8
)


# ================= LOGIN OPTION =================

tk.Label(
    form,
    text="Already registered?",
    font=("Arial", 9),
    bg="white",
    fg="#666666"
).pack(
    pady=(12, 3)
)


login_button = tk.Button(
    form,
    text="LOGIN",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#1f4e79",
    activebackground="white",
    activeforeground="#163a5c",
    relief="flat",
    cursor="hand2",
    command=open_login
)

login_button.pack(
    fill="x",
    ipady=5
)


# ================= FOOTER =================

tk.Label(
    root,
    text="Online Job Portal • Job Seeker Registration",
    font=("Arial", 9),
    bg="#f4f6f8",
    fg="#777777"
).pack(
    pady=8
)


# ================= START =================

root.mainloop()