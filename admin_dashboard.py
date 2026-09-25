import tkinter as tk
from tkinter import messagebox
import subprocess
import sys
import os

# Project folder ka path
base_dir = os.path.dirname(os.path.abspath(__file__))


# ---------------- FUNCTIONS ----------------

def open_add_job():
    subprocess.Popen([
        sys.executable,
        os.path.join(base_dir, "admin.py")
    ])


def open_manage_jobs():
    subprocess.Popen([
        sys.executable,
        os.path.join(base_dir, "manage_jobs.py")
    ])


def open_manage_applications():
    subprocess.Popen([
        sys.executable,
        os.path.join(base_dir, "admin_applications.py")
    ])


def exit_dashboard():
    root.destroy()


# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Admin Dashboard")
root.geometry("500x480")
root.resizable(False, False)
root.configure(bg="#f4f7fb")


# ---------------- HEADER ----------------

header = tk.Frame(root, bg="#184E8D", height=100)
header.pack(fill="x")

tk.Label(
    header,
    text="ADMIN DASHBOARD",
    font=("Arial", 24, "bold"),
    fg="white",
    bg="#1565c0"
).pack(pady=(20, 5))

tk.Label(
    header,
    text="Online Job Portal",
    font=("Arial", 11),
    fg="white",
    bg="#1565c0"
).pack()


# ---------------- BUTTON FRAME ----------------

button_frame = tk.Frame(root, bg="#f4f7fb")
button_frame.pack(pady=35)


# ADD NEW JOB

tk.Button(
    button_frame,
    text="ADD NEW JOB",
    font=("Arial", 13, "bold"),
    bg="#1976d2",
    fg="white",
    width=28,
    height=2,
    bd=0,
    cursor="hand2",
    command=open_add_job
).pack(pady=8)


# MANAGE JOBS

tk.Button(
    button_frame,
    text="MANAGE JOBS",
    font=("Arial", 13, "bold"),
    bg="#1976d2",
    fg="white",
    width=28,
    height=2,
    bd=0,
    cursor="hand2",
    command=open_manage_jobs
).pack(pady=8)


# MANAGE APPLICATIONS

tk.Button(
    button_frame,
    text="MANAGE APPLICATIONS",
    font=("Arial", 13, "bold"),
    bg="#0C457F",
    fg="white",
    width=28,
    height=2,
    bd=0,
    cursor="hand2",
    command=open_manage_applications
).pack(pady=8)


# EXIT

tk.Button(
    button_frame,
    text="EXIT",
    font=("Arial", 12, "bold"),
    bg="#d32f2f",
    fg="white",
    width=28,
    height=2,
    bd=0,
    cursor="hand2",
    command=exit_dashboard
).pack(pady=8)


# ---------------- RUN ----------------

root.mainloop()