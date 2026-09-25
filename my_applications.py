import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector


# ---------------- DATABASE ----------------

def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Payal@2302",
        database="online_job_portal"
    )


# ---------------- SHOW APPLICATIONS ----------------

def show_applications():

    email = email_entry.get().strip()

    if email == "":
        messagebox.showwarning(
            "Warning",
            "Please enter your registered email!"
        )
        return

    for item in applications_list.get_children():
        applications_list.delete(item)

    try:

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT user_id FROM users WHERE email = %s",
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            messagebox.showerror(
                "Error",
                "This email is not registered!"
            )

            cursor.close()
            connection.close()
            return

        user_id = user[0]

        query = """
        SELECT
            jobs.company_name,
            jobs.job_title,
            jobs.location,
            applications.application_date,
            applications.status
        FROM applications
        JOIN jobs
            ON applications.job_id = jobs.job_id
        WHERE applications.user_id = %s
        ORDER BY applications.application_date DESC
        """

        cursor.execute(
            query,
            (user_id,)
        )

        applications = cursor.fetchall()

        for application in applications:

            applications_list.insert(
                "",
                tk.END,
                values=application
            )

        if not applications:

            messagebox.showinfo(
                "Applications",
                "You have not applied for any job yet."
            )

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("Online Job Portal - My Applications")

root.geometry("1000x650")

root.resizable(False, False)


# ---------------- HEADER ----------------

header = tk.Frame(
    root,
    bg="#1f4e78",
    height=110
)

header.pack(
    fill="x"
)


title_label = tk.Label(
    header,
    text="MY APPLICATIONS",
    font=("Arial", 24, "bold"),
    bg="#1f4e78",
    fg="white"
)

title_label.pack(pady=15)


subtitle_label = tk.Label(
    header,
    text="Track your job applications and status",
    font=("Arial", 12),
    bg="#1f4e78",
    fg="white"
)

subtitle_label.pack()


# ---------------- EMAIL SECTION ----------------

email_frame = tk.Frame(root)

email_frame.pack(pady=25)


email_label = tk.Label(
    email_frame,
    text="Registered Email:",
    font=("Arial", 11, "bold")
)

email_label.pack(
    side=tk.LEFT,
    padx=8
)


email_entry = tk.Entry(
    email_frame,
    width=40,
    font=("Arial", 11)
)

email_entry.pack(
    side=tk.LEFT,
    padx=8
)

email_entry.insert(
    0,
    "jaiswalpayal0403@gmail.com"
)


# ---------------- SHOW BUTTON ----------------

show_button = tk.Button(
    root,
    text="SHOW MY APPLICATIONS",
    width=25,
    height=2,
    font=("Arial", 10, "bold"),
    bg="#1f4e78",
    fg="white",
    command=show_applications
)

show_button.pack(
    pady=5
)


# ---------------- TABLE ----------------

table_frame = tk.Frame(root)

table_frame.pack(
    padx=25,
    pady=25
)


columns = (
    "Company",
    "Job Title",
    "Location",
    "Applied Date",
    "Status"
)


applications_list = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=14
)


column_widths = {
    "Company": 170,
    "Job Title": 200,
    "Location": 160,
    "Applied Date": 150,
    "Status": 150
}


for column in columns:

    applications_list.heading(
        column,
        text=column
    )

    applications_list.column(
        column,
        width=column_widths[column],
        anchor="center"
    )


applications_list.pack(
    side=tk.LEFT
)


# ---------------- SCROLLBAR ----------------

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=applications_list.yview
)

scrollbar.pack(
    side=tk.RIGHT,
    fill="y"
)


applications_list.configure(
    yscrollcommand=scrollbar.set
)


# ---------------- FOOTER ----------------

footer = tk.Label(
    root,
    text="Online Job Portal | BCA Mini Project",
    font=("Arial", 9),
    fg="gray"
)

footer.pack(
    side="bottom",
    pady=10
)
root.mainloop()