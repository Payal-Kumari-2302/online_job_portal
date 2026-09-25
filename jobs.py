import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
import subprocess
import sys
from datetime import date


# ---------------- LOGGED-IN USER ----------------

if len(sys.argv) > 1:
    logged_in_email = sys.argv[1]
else:
    logged_in_email = ""


# ---------------- DATABASE ----------------

def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Payal@2302",
        database="online_job_portal"
    )


# ---------------- LOAD JOBS ----------------

def load_jobs(search_text=""):

    for item in jobs_list.get_children():
        jobs_list.delete(item)

    try:
        connection = connect_database()
        cursor = connection.cursor()

        if search_text == "":
            query = """
            SELECT job_id, company_name, job_title,
                   location, salary,
                   apply_start_date, apply_end_date
            FROM jobs
            ORDER BY job_id DESC
            """
            cursor.execute(query)

        else:
            query = """
            SELECT job_id, company_name, job_title,
                   location, salary,
                   apply_start_date, apply_end_date
            FROM jobs
            WHERE job_title LIKE %s
               OR company_name LIKE %s
               OR location LIKE %s
            ORDER BY job_id DESC
            """

            value = "%" + search_text + "%"

            cursor.execute(
                query,
                (value, value, value)
            )

        jobs = cursor.fetchall()

        for job in jobs:

            start_date = (
                job[5].strftime("%d-%m-%Y")
                if job[5]
                else ""
            )

            end_date = (
                job[6].strftime("%d-%m-%Y")
                if job[6]
                else ""
            )

            jobs_list.insert(
                "",
                tk.END,
                values=(
                    job[0],
                    job[1],
                    job[2],
                    job[3],
                    job[4],
                    start_date,
                    end_date
                )
            )

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ---------------- SEARCH ----------------

def search_jobs():

    search_text = search_entry.get().strip()

    load_jobs(search_text)


# ---------------- JOB DETAILS ----------------

def show_job_details():

    selected = jobs_list.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a job!"
        )
        return

    job_id = jobs_list.item(
        selected[0]
    )["values"][0]

    try:

        connection = connect_database()
        cursor = connection.cursor()

        query = """
        SELECT company_name, job_title, location,
               salary, skills_required, description,
               apply_start_date, apply_end_date
        FROM jobs
        WHERE job_id = %s
        """

        cursor.execute(
            query,
            (job_id,)
        )

        job = cursor.fetchone()

        cursor.close()
        connection.close()

        if job:

            start_date = (
                job[6].strftime("%d-%m-%Y")
                if job[6]
                else "Not specified"
            )

            end_date = (
                job[7].strftime("%d-%m-%Y")
                if job[7]
                else "Not specified"
            )

            details = f"""
Company: {job[0]}

Job Title: {job[1]}

Location: {job[2]}

Salary: {job[3]}

Required Skills: {job[4]}

Apply Start Date: {start_date}

Apply End Date: {end_date}

Description:
{job[5]}
"""

            messagebox.showinfo(
                "Job Details",
                details
            )

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ---------------- CHECK APPLICATION DATE ----------------

def check_application_date(job_id):

    try:

        connection = connect_database()
        cursor = connection.cursor()

        query = """
        SELECT apply_start_date, apply_end_date
        FROM jobs
        WHERE job_id = %s
        """

        cursor.execute(
            query,
            (job_id,)
        )

        job = cursor.fetchone()

        cursor.close()
        connection.close()

        if not job:
            return False, "Job not found!"

        start_date = job[0]
        end_date = job[1]
        today = date.today()

        # Application has not started
        if start_date and today < start_date:

            start_text = start_date.strftime("%d-%m-%Y")

            return False, (
                f"Applications will start from {start_text}."
            )

        # Application has expired
        if end_date and today > end_date:

            end_text = end_date.strftime("%d-%m-%Y")

            return False, (
                f"Application deadline was {end_text}."
            )

        return True, ""

    except mysql.connector.Error as error:

        return False, str(error)


# ---------------- APPLY BUTTON STATUS ----------------

def update_apply_button(event=None):

    selected = jobs_list.selection()

    if not selected:
        apply_button.config(
            text="APPLY FOR JOB",
            state="disabled"
        )
        return

    job_id = jobs_list.item(
        selected[0]
    )["values"][0]

    try:

        connection = connect_database()
        cursor = connection.cursor()

        query = """
        SELECT apply_start_date, apply_end_date
        FROM jobs
        WHERE job_id = %s
        """

        cursor.execute(
            query,
            (job_id,)
        )

        job = cursor.fetchone()

        cursor.close()
        connection.close()

        if not job:

            apply_button.config(
                text="JOB NOT FOUND",
                state="disabled"
            )

            return

        start_date = job[0]
        end_date = job[1]
        today = date.today()

        # Start date is in future
        if start_date and today < start_date:

            apply_button.config(
                text="APPLICATION NOT STARTED",
                state="disabled"
            )

        # End date has passed
        elif end_date and today > end_date:

            apply_button.config(
                text="APPLICATION EXPIRED",
                state="disabled"
            )

        # Application is active
        else:

            apply_button.config(
                text="APPLY FOR JOB",
                state="normal"
            )

    except mysql.connector.Error:

        apply_button.config(
            text="APPLY FOR JOB",
            state="disabled"
        )


# ---------------- APPLY FOR JOB ----------------

def apply_for_job():

    selected = jobs_list.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a job first!"
        )

        return

    job_id = jobs_list.item(
        selected[0]
    )["values"][0]

    email = logged_in_email

    if email == "":

        messagebox.showwarning(
            "Warning",
            "Please login first!"
        )

        return

    # Check application date
    allowed, message = check_application_date(job_id)

    if not allowed:

        messagebox.showwarning(
            "Application Closed",
            message
        )

        return

    try:

        connection = connect_database()
        cursor = connection.cursor()

        # Find logged-in user
        cursor.execute(
            """
            SELECT user_id
            FROM users
            WHERE email = %s
            """,
            (email,)
        )

        user = cursor.fetchone()

        if not user:

            messagebox.showerror(
                "Error",
                "User is not registered!"
            )

            cursor.close()
            connection.close()

            return

        user_id = user[0]

        # Check duplicate application
        cursor.execute(
            """
            SELECT application_id
            FROM applications
            WHERE user_id = %s
              AND job_id = %s
            """,
            (user_id, job_id)
        )

        already_applied = cursor.fetchone()

        if already_applied:

            messagebox.showwarning(
                "Already Applied",
                "You have already applied for this job!"
            )

            cursor.close()
            connection.close()

            return

        # Insert application
        query = """
        INSERT INTO applications
        (user_id, job_id, application_date, status)
        VALUES (%s, %s, CURDATE(), 'Pending')
        """

        cursor.execute(
            query,
            (user_id, job_id)
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Job Application Submitted Successfully!"
        )

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ---------------- MY APPLICATIONS ----------------

def open_my_applications():

    root.destroy()

    subprocess.Popen(
        [
            sys.executable,
            "my_applications.py",
            logged_in_email
        ]
    )


# ---------------- LOGOUT ----------------

def logout():

    root.destroy()

    subprocess.Popen(
        [
            sys.executable,
            "login.py"
        ]
    )


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("Online Job Portal - Available Jobs")
root.geometry("1100x780")
root.resizable(False, False)
root.configure(bg="#f4f6f8")


# ---------------- HEADER ----------------

header = tk.Frame(
    root,
    bg="#1f4e78",
    height=100
)

header.pack(fill="x")


title_label = tk.Label(
    header,
    text="ONLINE JOB PORTAL",
    font=("Arial", 24, "bold"),
    bg="#1f4e78",
    fg="white"
)

title_label.pack(pady=12)


subtitle_label = tk.Label(
    header,
    text="Find your next career opportunity",
    font=("Arial", 12),
    bg="#1f4e78",
    fg="white"
)

subtitle_label.pack()


# ---------------- SEARCH SECTION ----------------

search_title = tk.Label(
    root,
    text="Search Available Jobs",
    font=("Arial", 16, "bold"),
    bg="#f4f6f8",
    fg="#333333"
)

search_title.pack(pady=(20, 8))


search_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

search_frame.pack(pady=5)


search_entry = tk.Entry(
    search_frame,
    width=45,
    font=("Arial", 12),
    relief="solid",
    bd=1
)

search_entry.pack(
    side=tk.LEFT,
    padx=8,
    ipady=5
)


search_button = tk.Button(
    search_frame,
    text="SEARCH",
    width=12,
    font=("Arial", 10, "bold"),
    bg="#1f4e78",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=search_jobs
)

search_button.pack(
    side=tk.LEFT,
    ipady=5
)


# ---------------- JOB TABLE ----------------

table_frame = tk.Frame(
    root,
    bg="white"
)

table_frame.pack(
    padx=25,
    pady=18
)


columns = (
    "Job ID",
    "Company",
    "Job Title",
    "Location",
    "Salary",
    "Start Date",
    "End Date"
)


jobs_list = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=13
)


for column in columns:

    jobs_list.heading(
        column,
        text=column
    )


jobs_list.column(
    "Job ID",
    width=70,
    anchor="center"
)

jobs_list.column(
    "Company",
    width=145,
    anchor="center"
)

jobs_list.column(
    "Job Title",
    width=175,
    anchor="center"
)

jobs_list.column(
    "Location",
    width=125,
    anchor="center"
)

jobs_list.column(
    "Salary",
    width=120,
    anchor="center"
)

jobs_list.column(
    "Start Date",
    width=120,
    anchor="center"
)

jobs_list.column(
    "End Date",
    width=120,
    anchor="center"
)


jobs_list.pack(
    side=tk.LEFT
)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=jobs_list.yview
)

scrollbar.pack(
    side=tk.RIGHT,
    fill="y"
)


jobs_list.configure(
    yscrollcommand=scrollbar.set
)


# When a job is selected, update Apply button
jobs_list.bind(
    "<<TreeviewSelect>>",
    update_apply_button
)


# ---------------- DETAILS BUTTON ----------------

details_button = tk.Button(
    root,
    text="VIEW JOB DETAILS",
    width=22,
    height=2,
    font=("Arial", 10, "bold"),
    bg="#1f4e78",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=show_job_details
)

details_button.pack(pady=5)


# ---------------- LOGGED-IN EMAIL ----------------

email_label = tk.Label(
    root,
    text="Logged-in Email",
    font=("Arial", 11, "bold"),
    bg="#f4f6f8",
    fg="#333333"
)

email_label.pack(pady=(10, 3))


email_entry = tk.Entry(
    root,
    width=42,
    font=("Arial", 11),
    relief="solid",
    bd=1,
    state="readonly"
)

email_entry.pack(
    ipady=4
)


# Show logged-in email
email_entry.config(state="normal")

email_entry.insert(
    0,
    logged_in_email
)

email_entry.config(
    state="readonly"
)


# ---------------- APPLY BUTTON ----------------

apply_button = tk.Button(
    root,
    text="APPLY FOR JOB",
    width=22,
    height=2,
    font=("Arial", 10, "bold"),
    bg="#1f4e78",
    fg="white",
    relief="flat",
    cursor="hand2",
    state="disabled",
    command=apply_for_job
)

apply_button.pack(
    pady=8
)


# ---------------- BOTTOM BUTTONS ----------------

bottom_frame = tk.Frame(
    root,
    bg="#f4f6f8"
)

bottom_frame.pack(
    pady=5
)


my_applications_button = tk.Button(
    bottom_frame,
    text="MY APPLICATIONS",
    width=20,
    height=2,
    font=("Arial", 10, "bold"),
    bg="#1f4e78",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=open_my_applications
)

my_applications_button.pack(
    side=tk.LEFT,
    padx=10
)


logout_button = tk.Button(
    bottom_frame,
    text="LOGOUT",
    width=15,
    height=2,
    font=("Arial", 10, "bold"),
    bg="#555555",
    fg="white",
    relief="flat",
    cursor="hand2",
    command=logout
)

logout_button.pack(
    side=tk.LEFT,
    padx=10
)


# ---------------- FOOTER ----------------

footer = tk.Label(
    root,
    text="BCA Mini Project | Online Job Portal",
    font=("Arial", 9),
    bg="#f4f6f8",
    fg="#777777"
)

footer.pack(
    side="bottom",
    pady=8
)


# ---------------- LOAD JOBS ----------------

load_jobs()


root.mainloop()