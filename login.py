
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys


# ---------------- OPEN REGISTRATION ----------------

def open_registration():

    root.destroy()

    subprocess.Popen(
        [sys.executable, "register.py"]
    )


# ---------------- LOGIN FUNCTION ----------------

def login_user():

    email = email_entry.get().strip()
    password = password_entry.get()

    if email == "" or password == "":
        messagebox.showwarning(
            "Warning",
            "Please enter Email and Password!"
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
        SELECT user_id, name
        FROM users
        WHERE email = %s AND password = %s
        """

        cursor.execute(
            query,
            (email, password)
        )

        user = cursor.fetchone()

        cursor.close()
        connection.close()

        if user:

            messagebox.showinfo(
                "Login Successful",
                f"Welcome, {user[1]}!"
            )

            root.destroy()

            # Open Jobs Page with logged-in user's email
            subprocess.Popen(
                [sys.executable, "jobs.py", email]
            )

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Email or Password!"
            )

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()

root.title("Online Job Portal - Login")
root.geometry("550x560")
root.resizable(False, False)

root.configure(
    bg="#f4f6f8"
)


# ---------------- HEADER ----------------

header = tk.Frame(
    root,
    bg="#1f4e78",
    height=110
)

header.pack(
    fill="x"
)

title = tk.Label(
    header,
    text="ONLINE JOB PORTAL",
    font=("Arial", 24, "bold"),
    bg="#1f4e78",
    fg="white"
)

title.pack(pady=(22, 5))


header_subtitle = tk.Label(
    header,
    text="Login to find and apply for jobs",
    font=("Arial", 11),
    bg="#1f4e78",
    fg="white"
)

header_subtitle.pack()


# ---------------- LOGIN CARD ----------------

card = tk.Frame(
    root,
    bg="white",
    padx=40,
    pady=25
)

card.pack(
    padx=55,
    pady=25,
    fill="x"
)


# ---------------- CARD TITLE ----------------

tk.Label(
    card,
    text="Welcome Back",
    font=("Arial", 20, "bold"),
    bg="white",
    fg="#1f4e78"
).pack(
    pady=(0, 20)
)


# ---------------- EMAIL ----------------

tk.Label(
    card,
    text="Email Address",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333",
    anchor="w"
).pack(
    fill="x"
)

email_entry = tk.Entry(
    card,
    font=("Arial", 11),
    relief="solid",
    bd=1
)

email_entry.pack(
    fill="x",
    ipady=6,
    pady=(5, 14)
)


# ---------------- PASSWORD ----------------

tk.Label(
    card,
    text="Password",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#333333",
    anchor="w"
).pack(
    fill="x"
)

password_entry = tk.Entry(
    card,
    font=("Arial", 11),
    show="*",
    relief="solid",
    bd=1
)

password_entry.pack(
    fill="x",
    ipady=6,
    pady=(5, 18)
)


# ---------------- LOGIN BUTTON ----------------

login_button = tk.Button(
    card,
    text="LOGIN",
    font=("Arial", 11, "bold"),
    bg="#1f4e78",
    fg="white",
    activebackground="#163a5c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=login_user
)

login_button.pack(
    fill="x",
    ipady=8
)


# ---------------- REGISTER LINK ----------------

tk.Label(
    card,
    text="Don't have an account?",
    font=("Arial", 9),
    bg="white",
    fg="#666666"
).pack(
    pady=(18, 5)
)


register_button = tk.Button(
    card,
    text="CREATE NEW ACCOUNT",
    font=("Arial", 10, "bold"),
    bg="white",
    fg="#1f4e78",
    activebackground="white",
    activeforeground="#163a5c",
    relief="solid",
    bd=1,
    cursor="hand2",
    command=open_registration
)

register_button.pack(
    fill="x",
    ipady=6
)


# ---------------- FOOTER ----------------

footer = tk.Label(
    root,
    text="Online Job Portal • BCA Mini Project",
    font=("Arial", 9),
    bg="#f4f6f8",
    fg="#777777"
)

footer.pack(
    pady=8
)


root.mainloop()