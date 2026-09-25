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


# ---------------- LOAD APPLICATIONS ----------------

def load_applications():

    for item in applications_list.get_children():
        applications_list.delete(item)

    try:

        connection = connect_database()
        cursor = connection.cursor()

        query = """
        SELECT
            applications.application_id,
            users.name,
            users.email,
            jobs.company_name,
            jobs.job_title,
            applications.application_date,
            applications.status
        FROM applications
        JOIN users
            ON applications.user_id = users.user_id
        JOIN jobs
            ON applications.job_id = jobs.job_id
        ORDER BY applications.application_id DESC
        """

        cursor.execute(query)

        applications = cursor.fetchall()

        for application in applications:
            applications_list.insert(
                "",
                tk.END,
                values=application
            )

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ---------------- UPDATE STATUS ----------------

def update_status():

    selected = applications_list.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select an application!"
        )

        return

    application_id = applications_list.item(
        selected[0]
    )["values"][0]

    new_status = status_combo.get()

    if new_status == "":

        messagebox.showwarning(
            "Warning",
            "Please select a status!"
        )

        return

    try:

        connection = connect_database()
        cursor = connection.cursor()

        query = """
        UPDATE applications
        SET status = %s
        WHERE application_id = %s
        """

        cursor.execute(
            query,
            (new_status, application_id)
        )

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Application status updated successfully!"
        )

        cursor.close()
        connection.close()

        load_applications()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("Online Job Portal - Application Management")

root.geometry("1150x700")

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
    text="APPLICATION MANAGEMENT",
    font=("Arial", 24, "bold"),
    bg="#1f4e78",
    fg="white"
)

title_label.pack(pady=15)


subtitle_label = tk.Label(
    header,
    text="Review and update job applications",
    font=("Arial", 12),
    bg="#1f4e78",
    fg="white"
)

subtitle_label.pack()


# ---------------- PAGE TITLE ----------------

page_title = tk.Label(
    root,
    text="All Job Applications",
    font=("Arial", 18, "bold")
)

page_title.pack(pady=18)


# ---------------- TABLE FRAME ----------------

table_frame = tk.Frame(root)

table_frame.pack(
    padx=20,
    pady=5
)


columns = (
    "Application ID",
    "Name",
    "Email",
    "Company",
    "Job Title",
    "Applied Date",
    "Status"
)


applications_list = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=16
)


column_widths = {
    "Application ID": 110,
    "Name": 130,
    "Email": 220,
    "Company": 130,
    "Job Title": 160,
    "Applied Date": 120,
    "Status": 120
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


# ---------------- STATUS SECTION ----------------

status_frame = tk.Frame(root)

status_frame.pack(pady=18)


status_label = tk.Label(
    status_frame,
    text="Select New Status:",
    font=("Arial", 11, "bold")
)

status_label.pack(
    side=tk.LEFT,
    padx=10
)


status_combo = ttk.Combobox(
    status_frame,
    values=[
        "Pending",
        "Selected",
        "Rejected"
    ],
    state="readonly",
    width=20,
    font=("Arial", 11)
)

status_combo.pack(
    side=tk.LEFT,
    padx=10
)


# ---------------- UPDATE BUTTON ----------------

update_button = tk.Button(
    root,
    text="UPDATE STATUS",
    width=25,
    height=2,
    font=("Arial", 11, "bold"),
    bg="#1f4e78",
    fg="white",
    command=update_status
)

update_button.pack(pady=5)


# ---------------- FOOTER ----------------

footer = tk.Label(
    root,
    text="Online Job Portal | Admin Application Management",
    font=("Arial", 9),
    fg="gray"
)

footer.pack(
    side="bottom",
    pady=10
)


# ---------------- LOAD DATA ----------------

load_applications()


root.mainloop()