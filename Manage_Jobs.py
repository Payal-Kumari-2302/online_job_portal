import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime


# ================= DATABASE =================

def connect_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Payal@2302",
        database="online_job_portal"
    )


# ================= LOAD JOBS =================

def load_jobs():

    # Clear table
    for item in job_table.get_children():
        job_table.delete(item)

    try:
        connection = connect_database()
        cursor = connection.cursor()

        query = """
        SELECT job_id,
               company_name,
               job_title,
               location,
               salary,
               skills_required,
               apply_start_date,
               apply_end_date
        FROM jobs
        ORDER BY job_id DESC
        """

        cursor.execute(query)

        jobs = cursor.fetchall()

        for job in jobs:

            start_date = (
                job[6].strftime("%d-%m-%Y")
                if job[6]
                else ""
            )

            end_date = (
                job[7].strftime("%d-%m-%Y")
                if job[7]
                else ""
            )

            job_table.insert(
                "",
                tk.END,
                values=(
                    job[0],
                    job[1],
                    job[2],
                    job[3],
                    job[4],
                    job[5],
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


# ================= EDIT JOB =================

def edit_job():

    selected = job_table.selection()

    if not selected:
        messagebox.showwarning(
            "Warning",
            "Please select a job first!"
        )
        return

    job_id = job_table.item(
        selected[0],
        "values"
    )[0]

    try:

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT company_name,
                   job_title,
                   location,
                   salary,
                   skills_required,
                   description,
                   apply_start_date,
                   apply_end_date
            FROM jobs
            WHERE job_id = %s
            """,
            (job_id,)
        )

        job = cursor.fetchone()

        cursor.close()
        connection.close()

        if not job:
            messagebox.showerror(
                "Error",
                "Job not found!"
            )
            return

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )
        return


    # ================= EDIT WINDOW =================

    edit_window = tk.Toplevel(root)

    edit_window.title("Edit Job")
    edit_window.geometry("550x650")
    edit_window.resizable(False, False)
    edit_window.configure(bg="#f4f6f8")


    # ================= HEADER =================

    tk.Label(
        edit_window,
        text="EDIT JOB",
        font=("Arial", 20, "bold"),
        bg="#1f4e78",
        fg="white"
    ).pack(
        fill="x",
        pady=(0, 15),
        ipady=12
    )


    # ================= FORM =================

    form = tk.Frame(
        edit_window,
        bg="white",
        padx=30,
        pady=15
    )

    form.pack(
        padx=30,
        pady=10,
        fill="both",
        expand=True
    )


    # ================= FIELDS =================

    fields = [
        ("Company Name", job[0]),
        ("Job Title", job[1]),
        ("Location", job[2]),
        ("Salary", job[3]),
        ("Required Skills", job[4])
    ]

    entries = {}


    for row, (label, value) in enumerate(fields):

        tk.Label(
            form,
            text=label,
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#333333"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            pady=6
        )

        entry = tk.Entry(
            form,
            width=32,
            font=("Arial", 10)
        )

        entry.insert(
            0,
            value or ""
        )

        entry.grid(
            row=row,
            column=1,
            padx=(15, 0),
            pady=6,
            ipady=3
        )

        entries[label] = entry


    # ================= START DATE =================

    tk.Label(
        form,
        text="Apply Start Date",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#333333"
    ).grid(
        row=5,
        column=0,
        sticky="w",
        pady=6
    )

    start_entry = tk.Entry(
        form,
        width=32,
        font=("Arial", 10)
    )

    if job[6]:
        start_entry.insert(
            0,
            job[6].strftime("%d-%m-%Y")
        )

    start_entry.grid(
        row=5,
        column=1,
        padx=(15, 0),
        pady=6,
        ipady=3
    )


    # ================= END DATE =================

    tk.Label(
        form,
        text="Apply End Date",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#333333"
    ).grid(
        row=6,
        column=0,
        sticky="w",
        pady=6
    )

    end_entry = tk.Entry(
        form,
        width=32,
        font=("Arial", 10)
    )

    if job[7]:
        end_entry.insert(
            0,
            job[7].strftime("%d-%m-%Y")
        )

    end_entry.grid(
        row=6,
        column=1,
        padx=(15, 0),
        pady=6,
        ipady=3
    )


    # ================= DESCRIPTION =================

    tk.Label(
        form,
        text="Job Description",
        font=("Arial", 10, "bold"),
        bg="white",
        fg="#333333"
    ).grid(
        row=7,
        column=0,
        sticky="nw",
        pady=6
    )

    description_text = tk.Text(
        form,
        width=32,
        height=5,
        font=("Arial", 10)
    )

    description_text.insert(
        "1.0",
        job[5] or ""
    )

    description_text.grid(
        row=7,
        column=1,
        padx=(15, 0),
        pady=6
    )


    # ================= SAVE CHANGES =================

    def save_changes():

        company = entries["Company Name"].get().strip()
        title = entries["Job Title"].get().strip()
        location = entries["Location"].get().strip()
        salary = entries["Salary"].get().strip()
        skills = entries["Required Skills"].get().strip()

        start_date = start_entry.get().strip()
        end_date = end_entry.get().strip()

        description = description_text.get(
            "1.0",
            tk.END
        ).strip()


        if company == "" or title == "":
            messagebox.showwarning(
                "Warning",
                "Company Name and Job Title are required!"
            )
            return


        # Date validation

        try:

            start = datetime.strptime(
                start_date,
                "%d-%m-%Y"
            ).date()

            end = datetime.strptime(
                end_date,
                "%d-%m-%Y"
            ).date()

            if end < start:

                messagebox.showwarning(
                    "Invalid Date",
                    "End Date cannot be before Start Date!"
                )
                return

        except ValueError:

            messagebox.showwarning(
                "Invalid Date",
                "Please use DD-MM-YYYY format.\n\n"
                "Example: 15-09-2026"
            )
            return


        # ================= UPDATE DATABASE =================

        try:

            connection = connect_database()
            cursor = connection.cursor()

            query = """
            UPDATE jobs
            SET company_name = %s,
                job_title = %s,
                location = %s,
                salary = %s,
                skills_required = %s,
                description = %s,
                apply_start_date = %s,
                apply_end_date = %s
            WHERE job_id = %s
            """

            cursor.execute(
                query,
                (
                    company,
                    title,
                    location,
                    salary,
                    skills,
                    description,
                    start,
                    end,
                    job_id
                )
            )

            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Job Updated Successfully!"
            )

            edit_window.destroy()

            load_jobs()

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Database Error",
                str(error)
            )


    # ================= SAVE BUTTON =================

    tk.Button(
        edit_window,
        text="SAVE CHANGES",
        width=22,
        height=2,
        font=("Arial", 10, "bold"),
        bg="#1f4e78",
        fg="white",
        activebackground="#163a5c",
        activeforeground="white",
        relief="flat",
        cursor="hand2",
        command=save_changes
    ).pack(
        pady=10,
        ipady=2
    )


# ================= DELETE JOB =================

def delete_job():

    selected = job_table.selection()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Please select a job first!"
        )
        return


    values = job_table.item(
        selected[0],
        "values"
    )

    job_id = values[0]
    company = values[1]
    title = values[2]


    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete this job?\n\n"
        f"Company: {company}\n"
        f"Job: {title}"
    )

    if not confirm:
        return


    try:

        connection = connect_database()
        cursor = connection.cursor()

        cursor.execute(
            "DELETE FROM jobs WHERE job_id = %s",
            (job_id,)
        )

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Job Deleted Successfully!"
        )

        load_jobs()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("Online Job Portal - Manage Jobs")
root.geometry("1050x600")
root.resizable(False, False)
root.configure(bg="#f4f6f8")


# ================= HEADER =================

header = tk.Frame(
    root,
    bg="#1f4e78",
    height=90
)

header.pack(fill="x")


tk.Label(
    header,
    text="MANAGE JOBS",
    font=("Arial", 22, "bold"),
    bg="#1f4e78",
    fg="white"
).pack(pady=(16, 3))


tk.Label(
    header,
    text="View, edit and delete job opportunities",
    font=("Arial", 10),
    bg="#1f4e78",
    fg="white"
).pack()


# ================= MAIN CARD =================

card = tk.Frame(
    root,
    bg="white",
    padx=20,
    pady=15
)

card.pack(
    padx=35,
    pady=20,
    fill="both",
    expand=True
)


# ================= TABLE TITLE =================

tk.Label(
    card,
    text="Available Jobs",
    font=("Arial", 16, "bold"),
    bg="white",
    fg="#1f4e78"
).pack(
    anchor="w",
    pady=(0, 10)
)


# ================= TABLE FRAME =================

table_frame = tk.Frame(
    card,
    bg="white"
)

table_frame.pack(
    fill="both",
    expand=True
)


# ================= TABLE =================

columns = (
    "ID",
    "Company",
    "Job Title",
    "Location",
    "Salary",
    "Skills",
    "Start Date",
    "End Date"
)


job_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    height=12
)


# Headings

for column in columns:

    job_table.heading(
        column,
        text=column
    )


# Column widths

job_table.column(
    "ID",
    width=45,
    anchor="center"
)

job_table.column(
    "Company",
    width=120
)

job_table.column(
    "Job Title",
    width=180
)

job_table.column(
    "Location",
    width=110
)

job_table.column(
    "Salary",
    width=110
)

job_table.column(
    "Skills",
    width=180
)

job_table.column(
    "Start Date",
    width=100,
    anchor="center"
)

job_table.column(
    "End Date",
    width=100,
    anchor="center"
)


# Scrollbar

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=job_table.yview
)

job_table.configure(
    yscrollcommand=scrollbar.set
)


job_table.pack(
    side="left",
    fill="both",
    expand=True
)

scrollbar.pack(
    side="right",
    fill="y"
)


# ================= BUTTON FRAME =================

button_frame = tk.Frame(
    card,
    bg="white"
)

button_frame.pack(
    pady=15
)


# ================= EDIT BUTTON =================

tk.Button(
    button_frame,
    text="EDIT SELECTED JOB",
    width=22,
    height=2,
    font=("Arial", 10, "bold"),
    bg="#1f4e78",
    fg="white",
    activebackground="#163a5c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=edit_job
).pack(
    side="left",
    padx=10
)


# ================= DELETE BUTTON =================

tk.Button(
    button_frame,
    text="DELETE SELECTED JOB",
    width=22,
    height=2,
    font=("Arial", 10, "bold"),
    bg="#c0392b",
    fg="white",
    activebackground="#922b21",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=delete_job
).pack(
    side="left",
    padx=10
)


# ================= LOAD DATA =================

load_jobs()


# ================= START =================

root.mainloop()
