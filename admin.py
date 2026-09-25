import tkinter as tk
from tkinter import messagebox
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


# ================= ADD JOB =================

def add_job():

    company = company_entry.get().strip()
    title = title_entry.get().strip()
    location = location_entry.get().strip()
    salary = salary_entry.get().strip()
    skills = skills_entry.get().strip()
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()
    description = description_text.get("1.0", tk.END).strip()

    # Required fields
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
            "Please enter dates in DD-MM-YYYY format.\n\n"
            "Example: 15-09-2026"
        )
        return

    # Insert into database
    try:

        connection = connect_database()
        cursor = connection.cursor()

        query = """
        INSERT INTO jobs
        (
            company_name,
            job_title,
            location,
            salary,
            skills_required,
            description,
            apply_start_date,
            apply_end_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
                end
            )
        )

        connection.commit()

        cursor.close()
        connection.close()

        messagebox.showinfo(
            "Success",
            "Job Added Successfully!"
        )

        # Clear form
        company_entry.delete(0, tk.END)
        title_entry.delete(0, tk.END)
        location_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)
        skills_entry.delete(0, tk.END)
        start_date_entry.delete(0, tk.END)
        end_date_entry.delete(0, tk.END)
        description_text.delete("1.0", tk.END)

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Database Error",
            str(error)
        )


# ================= MAIN WINDOW =================

root = tk.Tk()

root.title("Online Job Portal - Add Job")
root.geometry("650x700")
root.resizable(False, False)
root.configure(bg="#f4f6f8")


# ================= HEADER =================

header = tk.Frame(
    root,
    bg="#1f4e78",
    height=100
)

header.pack(fill="x")

tk.Label(
    header,
    text="ADMIN PANEL",
    font=("Arial", 22, "bold"),
    bg="#1f4e78",
    fg="white"
).pack(pady=(18, 4))

tk.Label(
    header,
    text="Add New Job",
    font=("Arial", 11),
    bg="#1f4e78",
    fg="white"
).pack()


# ================= FORM CARD =================

card = tk.Frame(
    root,
    bg="white",
    padx=35,
    pady=20
)

card.pack(
    padx=45,
    pady=20,
    fill="both"
)


# ================= TITLE =================

tk.Label(
    card,
    text="Job Details",
    font=("Arial", 18, "bold"),
    bg="white",
    fg="#1f4e78"
).grid(
    row=0,
    column=0,
    columnspan=2,
    pady=(0, 15)
)


# ================= LABEL STYLE =================

label_style = {
    "font": ("Arial", 10, "bold"),
    "bg": "white",
    "fg": "#333333"
}


# ================= COMPANY =================

tk.Label(
    card,
    text="Company Name",
    **label_style
).grid(
    row=1,
    column=0,
    sticky="w",
    pady=6
)

company_entry = tk.Entry(
    card,
    width=38,
    font=("Arial", 10)
)

company_entry.grid(
    row=1,
    column=1,
    padx=(20, 0),
    pady=6,
    ipady=4
)


# ================= JOB TITLE =================

tk.Label(
    card,
    text="Job Title",
    **label_style
).grid(
    row=2,
    column=0,
    sticky="w",
    pady=6
)

title_entry = tk.Entry(
    card,
    width=38,
    font=("Arial", 10)
)

title_entry.grid(
    row=2,
    column=1,
    padx=(20, 0),
    pady=6,
    ipady=4
)


# ================= LOCATION =================

tk.Label(
    card,
    text="Location",
    **label_style
).grid(
    row=3,
    column=0,
    sticky="w",
    pady=6
)

location_entry = tk.Entry(
    card,
    width=38,
    font=("Arial", 10)
)

location_entry.grid(
    row=3,
    column=1,
    padx=(20, 0),
    pady=6,
    ipady=4
)


# ================= SALARY =================

tk.Label(
    card,
    text="Salary",
    **label_style
).grid(
    row=4,
    column=0,
    sticky="w",
    pady=6
)

salary_entry = tk.Entry(
    card,
    width=38,
    font=("Arial", 10)
)

salary_entry.grid(
    row=4,
    column=1,
    padx=(20, 0),
    pady=6,
    ipady=4
)


# ================= SKILLS =================

tk.Label(
    card,
    text="Required Skills",
    **label_style
).grid(
    row=5,
    column=0,
    sticky="w",
    pady=6
)

skills_entry = tk.Entry(
    card,
    width=38,
    font=("Arial", 10)
)

skills_entry.grid(
    row=5,
    column=1,
    padx=(20, 0),
    pady=6,
    ipady=4
)


# ================= START DATE =================

tk.Label(
    card,
    text="Apply Start Date",
    **label_style
).grid(
    row=6,
    column=0,
    sticky="w",
    pady=6
)

start_date_entry = tk.Entry(
    card,
    width=38,
    font=("Arial", 10)
)

start_date_entry.grid(
    row=6,
    column=1,
    padx=(20, 0),
    pady=6,
    ipady=4
)


# ================= END DATE =================

tk.Label(
    card,
    text="Apply End Date",
    **label_style
).grid(
    row=7,
    column=0,
    sticky="w",
    pady=6
)

end_date_entry = tk.Entry(
    card,
    width=38,
    font=("Arial", 10)
)

end_date_entry.grid(
    row=7,
    column=1,
    padx=(20, 0),
    pady=6,
    ipady=4
)


# ================= DESCRIPTION =================

tk.Label(
    card,
    text="Job Description",
    **label_style
).grid(
    row=8,
    column=0,
    sticky="nw",
    pady=6
)

description_text = tk.Text(
    card,
    width=38,
    height=4,
    font=("Arial", 10)
)

description_text.grid(
    row=8,
    column=1,
    padx=(20, 0),
    pady=6
)


# ================= ADD BUTTON =================

tk.Button(
    root,
    text="ADD JOB",
    width=25,
    height=2,
    font=("Arial", 11, "bold"),
    bg="#1f4e78",
    fg="white",
    activebackground="#163a5c",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=add_job
).pack(
    pady=5,
    ipady=3
)


# ================= FOOTER =================

tk.Label(
    root,
    text="BCA Mini Project | Online Job Portal",
    font=("Arial", 8),
    bg="#f4f6f8",
    fg="#777777"
).pack(
    side="bottom",
    pady=7
)


# ================= START =================

root.mainloop()