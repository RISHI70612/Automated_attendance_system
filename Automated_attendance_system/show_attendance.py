import pandas as pd
from glob import glob
import os
import tkinter as tk
import csv

# Placeholder for actual text-to-speech implementation
def text_to_speech(text):
    print(text)

def calculate_attendance(subject):
    if subject == "":
        t = 'Please enter the subject name.'
        text_to_speech(t)
    else:
        directory_path = os.path.join("Attendance", subject)
        if os.path.exists(directory_path):
            filenames = glob(os.path.join(directory_path, f"{subject}*.csv"))
            df = [pd.read_csv(f) for f in filenames]

            if len(df) > 0:
                combined_df = pd.concat(df, ignore_index=True)

                grouped_df = combined_df.groupby("Enrollment")["Name"].apply(list).reset_index()

                new_csv_path = os.path.join(directory_path, "attendance.csv")
                grouped_df.to_csv(new_csv_path, index=False)

                newdf = df[0]  # Initialize newdf with the first DataFrame
                for i in range(1, len(df)):
                    newdf = newdf.merge(df[i], how="outer")
                newdf.fillna(0, inplace=True)
                newdf["Attendance"] = 0
                for i in range(len(newdf)):
                    newdf["Attendance"].iloc[i] = str(int(round(newdf.iloc[i, 2:-1].mean() * 100))) + '%'
                newdf.to_csv(new_csv_path, index=False)

                root = tk.Tk()
                root.title(f"Attendance of {subject}")
                root.configure(background="black")
                with open(new_csv_path) as file:
                    reader = csv.reader(file)
                    r = 0

                    for col in reader:
                        c = 0
                        for row in col:
                            label = tk.Label(
                                root,
                                width=12,  # Adjust the width as needed
                                height=1,
                                fg="yellow",
                                font=("times", 15, " bold "),
                                bg="black",
                                text=row,
                                relief=tk.RIDGE,
                            )
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                t = f"No CSV files found for '{subject}'."
                text_to_speech(t)
        else:
            t = f"Attendance directory for '{subject}' does not exist."
            text_to_speech(t)

def open_attendance_directory(subject_entry):
    directory_path = os.path.join("Attendance", subject_entry.get())
    if os.path.exists(directory_path):
        os.startfile(directory_path)
    else:
        t = f"Attendance directory for '{subject_entry.get()}' does not exist."
        text_to_speech(t)

def subjectchoose(text_to_speech):
    subject_window = tk.Tk()
    subject_window.title("Subject Selection")
    subject_window.geometry("400x200")
    subject_window.configure(background="black")

    label = tk.Label(
        subject_window,
        text="Enter Subject:",
        bg="black",
        fg="yellow",
        font=("arial", 15),
    )
    label.pack(pady=20)

    subject_entry = tk.Entry(
        subject_window,
        bg="black",
        fg="yellow",
        font=("times", 20, "bold"),
    )
    subject_entry.pack()

    submit_button = tk.Button(
        subject_window,
        text="View Attendance",
        command=lambda: calculate_attendance(subject_entry.get()),
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        relief=tk.RIDGE,
       
    )
    submit_button.pack(pady=20)

    check_sheets_button = tk.Button(
        subject_window,
        text="Check Sheets",
        command=lambda: open_attendance_directory(subject_entry),
        bd=7,
        font=("times new roman", 15),
        bg="black",
        fg="yellow",
        relief=tk.RIDGE,
    )
    check_sheets_button.pack()

    subject_window.mainloop()
