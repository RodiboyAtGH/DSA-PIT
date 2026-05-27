import tkinter as tk
from tkinter import ttk, messagebox
import json

#DATA STORAGE
students = []
enrollment_queue = []

# LOGIN SYSTEM
USERNAME = "admin"
PASSWORD = "1234"

# COLLEGE AND PROGRAM DATA
college_programs = {

    "College of Information Technology and Computing": [
        "B.S. in Information Technology",
        "B.S. in Technology Communication Management",
        "B.S. in Data Science",
        "B.S. in Computer Science"
    ],

    "College of Engineering and Architecture": [
        "B.S. in Architecture",
        "B.S. in Civil Engineering",
        "B.S. in Mechanical Engineering",
        "B.S. in Computer Engineering",
        "B.S. in Geodetic Engineering",
        "B.S. in Electrical Engineering",
        "B.S. in Electronics Engineering"
    ],

    "College of Technology": [
        "B.S. in Autotronics",
        "B.S. in Electro-Mechanical Technology (IA)",
        "B.S. in Electro-Mechanical Technology (MR)",
        "B.S. in Electronics Technology (ES)",
        "B.S. in Electronics Technology (MST)",
        "B.S. in Electronics Technology (TN)",
        "B.S. in Energy Systems & Management (EMCM)",
        "B.S. in Energy Systems & Management (PSDE)",
        "B.S. in Manufacturing Engineering Technology",
        "Bachelor of Technology, Operations, & Management"
    ],

    "College of Science and Mathematics": [
        "B.S. in Applied Mathematics",
        "B.S. in Applied Physics",
        "B.S. in Chemistry",
        "B.S. in Environmental Science",
        "B.S. in Food Technology"
    ],

    "College of Science Technology and Education": [
        "Bachelor in Secondary Education Major in Science",
        "Bachelor in Secondary Education Major in Mathematics",
        "Bachelor in Technology and Livelihood Education",
        "Bachelor in Technical-Vocational Teacher Education"
    ],

    "College of Medicine": [
        "Doctor of Medicine"
    ],

    "Senior High School": [
        "STEM",
        "ABM",
        "HUMSS",
        "TVL"
    ]
}

# FUNCTIONS
def save_to_file():
    with open("students.json", "w") as file:
        json.dump(students, file)

def load_from_file():
    global students

    try:
        with open("students.json", "r") as file:
            students = json.load(file)
            display_students(students)

    except:
        students = []

# UPDATE PROGRAM DROPDOWN
def update_programs(event):
    selected_college = college_combo.get()

    if selected_college in college_programs:
        # Update Program dropdown
        program_combo["values"] = college_programs[selected_college]
        program_combo.set("")

        # Update Year Level dropdown based on College/SHS
        if selected_college == "Senior High School":
            year_combo["values"] = ["Grade 11", "Grade 12"]
        else:
            year_combo["values"] = ["1st Year", "2nd Year", "3rd Year", "4th Year"]
        
        year_combo.set("")

# DISPLAY STUDENTS
def display_students(data):

    student_list.delete(*student_list.get_children())

    for student in data:

        student_list.insert("", tk.END, values=(

            student["id"],
            student["name"],
            student["college"],
            student["course"],
            student["year"]
        ))

# ADD STUDENT
def add_student():

    sid = id_entry.get()
    name = name_entry.get()

    college = college_combo.get()

    course = program_combo.get()

    year = year_combo.get()

    if sid == "" or name == "" or college == "" or course == "" or year == "":
        messagebox.showerror("Error", "Complete all fields!")
        return

    student = {

        "id": sid,
        "name": name,
        "college": college,
        "course": course,
        "year": year
    }

    students.append(student)

    enrollment_queue.append(name)

    display_students(students)

    update_queue()

    save_to_file()

    clear_fields()

    messagebox.showinfo("Success", "Student added successfully!")

# SEARCH STUDENT
def search_student():

    keyword = search_entry.get().lower()
    results = []

    for student in students:

        if keyword in student["name"].lower():

            results.append(student)

    display_students(results)

# UPDATE STUDENT
def update_student():

    selected = student_list.focus()
    if not selected:

        messagebox.showerror("Error", "Select a student first!")
        return
    
    # CHECK DUPLICATE ID
    for student in students:
        if student["id"] == id:
            messagebox.showerror("Duplicate Error", "Student ID already exists!")
            return

    values = student_list.item(selected, "values")

    old_id = values[0]

    for student in students:

        if student["id"] == old_id:

            student["id"] = id_entry.get()

            student["name"] = name_entry.get()

            student["college"] = college_combo.get()

            student["course"] = program_combo.get()

            student["year"] = year_combo.get()

    display_students(students)

    save_to_file()

    clear_fields()

    messagebox.showinfo("Updated", "Student record updated!")

# DELETE STUDENT
def delete_student():

    selected = student_list.focus()

    if not selected:

        messagebox.showerror("Error", "Select a student first!")
        return

    values = student_list.item(selected, "values")

    sid = values[0]

    for student in students:

        if student["id"] == sid:
            students.remove(student)
            break

    display_students(students)
    save_to_file()
    messagebox.showinfo("Deleted", "Student deleted!")

# SORT STUDENTS
def sort_students():

    sorted_students = sorted(students, key=lambda x: x["name"])
    display_students(sorted_students)

# ==========================================
# SELECT RECORD
# ==========================================

def select_record(event):
    selected = student_list.focus()
    
    # Safety check in case empty space is clicked
    if not selected:
        return 

    values = student_list.item(selected, "values")

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)

    id_entry.insert(0, values[0])
    name_entry.insert(0, values[1])

    college_combo.set(values[2])

    # Adjust Program values based on selected record's college
    program_combo["values"] = college_programs.get(values[2], [])
    program_combo.set(values[3])

    # Adjust Year values based on selected record's college
    if values[2] == "Senior High School":
        year_combo["values"] = ["Grade 11", "Grade 12"]
    else:
        year_combo["values"] = ["1st Year", "2nd Year", "3rd Year", "4th Year"]

    year_combo.set(values[4])

# CLEAR FIELDS
def clear_fields():

    id_entry.delete(0, tk.END)
    name_entry.delete(0, tk.END)
    college_combo.set("")
    program_combo.set("")
    year_combo.set("")

# ENROLLMENT QUEUE
def update_queue():

    queue_box.delete(0, tk.END)
    for person in enrollment_queue:
        queue_box.insert(tk.END, person)

def serve_student():

    if enrollment_queue:

        served = enrollment_queue.pop(0)
        update_queue()
        messagebox.showinfo("Now Serving", served)

# LOGIN FUNCTION
def login():

    user = username_entry.get()
    pw = password_entry.get()

    if user == USERNAME and pw == PASSWORD:

        login_window.destroy()
        open_main_system()

    else:

        messagebox.showerror(
            "Login Failed",
            "Invalid username or password!"
        )

# MAIN SYSTEM
def open_main_system():

    global root
    global id_entry
    global name_entry
    global college_combo
    global program_combo
    global year_combo
    global student_list
    global search_entry
    global queue_box

    root = tk.Tk()
    root.title("Student Record Management System")
    root.geometry("1200x700")
    
    # main window background
    root.configure(bg="#111844")

    # INPUT FRAME 
    input_frame = tk.Frame(root, bg="#111844")
    input_frame.pack(pady=10)

    student_info_frame = tk.Frame(
        root,
        bg="#AEADA6"
    )
    student_info_frame.pack(pady=10)
    student_info_frame.pack_propagate(False)

    # STUDENT ID
    tk.Label(
        student_info_frame, 
        text="Student ID", 
        bg="#AEADA6", 
        fg="black"
    ).grid(row=0, column=0)

    id_entry = tk.Entry(
        student_info_frame, 
        width=50, 
        bg="white")
    id_entry.grid(row=0, column=1)

    # NAME
    tk.Label(student_info_frame, 
        text="Name", 
        bg="#AEADA6", 
        fg="black"
    ).grid(row=1, column=0)

    name_entry = tk.Entry( 
        student_info_frame, 
        width=50, 
        bg="white")
    name_entry.grid(row=1, column=1)

    # COLLEGE
    tk.Label(
        student_info_frame, 
        text="College", 
        bg="#AEADA6", 
        fg="black"
    ).grid(row=2, column=0)

    college_combo = ttk.Combobox(
        student_info_frame,
        width=47,
        values=list(college_programs.keys())
    )
    college_combo.grid(row=2, column=1)
    college_combo.bind("<<ComboboxSelected>>", update_programs)

    # PROGRAM
    tk.Label(
        student_info_frame, 
        text="Program", 
        bg="#AEADA6", 
        fg="black"
    ).grid(row=3, column=0)

    program_combo = ttk.Combobox(student_info_frame, width=47)
    program_combo.grid(row=3, column=1)

    # YEAR LEVEL
    tk.Label(
        student_info_frame, 
        text="Year Level", 
        bg="#AEADA6", 
        fg="black"
    ).grid(row=4, column=0)

    year_combo = ttk.Combobox(
        student_info_frame,
        width=47,
        values=[
            "1st Year",
            "2nd Year",
            "3rd Year",
            "4th Year"
        ]
    )
    year_combo.grid(row=4, column=1)
    
    # BUTTON FRAME
    button_frame = tk.Frame(root, bg="#111844")
    button_frame.pack(pady=10)

    # BUTTONS
    tk.Button(
        button_frame,
        text="Add Student",
        width=15,
        bg="#FAE251",
        fg="black",
        command=add_student
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Update Student",
        width=15,
        bg="#FAE251",
        fg="black",
        command=update_student
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete Student",
        width=15,
        bg="#FAE251",
        fg="black",
        command=delete_student
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        button_frame,
        text="Sort A-Z",
        width=15,
        bg="#FAE251",
        fg="black",
        command=sort_students
    ).grid(row=0, column=3, padx=5)

    # SEARCH FRAME
    search_frame = tk.Frame(root, bg="#111844")
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search Name", bg="#111844", fg="white").pack(side=tk.LEFT)

    search_entry = tk.Entry(search_frame, width=40, bg="white")
    search_entry.pack(side=tk.LEFT)

    tk.Button(
        search_frame,
        text="Search",
        bg="gold",
        fg="black",
        command=search_student
    ).pack(side=tk.LEFT, padx=5)

    # TABLE 
    columns = (
        "ID",
        "Name",
        "College",
        "Program",
        "Year"
    )

    student_list = ttk.Treeview(
        root,
        columns=columns,
        show="headings",
        height=12
    )

    for col in columns:
        student_list.heading(col, text=col)
        student_list.column(col, width=220)

    student_list.pack(pady=10)
    student_list.bind("<ButtonRelease-1>", select_record)

    # QUEUE SYSTEM FRAME
    queue_frame = tk.Frame(root, bg="#111844")
    queue_frame.pack(pady=10)

    tk.Label(
        queue_frame,
        text="Enrollment Queue",
        bg="#111844",
        fg="white"
    ).pack()

    queue_box = tk.Listbox(queue_frame, width=50, bg="white")
    queue_box.pack()

    tk.Button(
        queue_frame,
        text="Serve Student",
        bg="#FAE251",
        fg="black",
        command=serve_student
    ).pack(pady=5)

    load_from_file()

    root.mainloop()

# LOGIN WINDOW
login_window = tk.Tk()
login_window.title("Admin Login")
login_window.geometry("500x600")
login_window.configure(bg="#111844")

# LOGO
photo = tk.PhotoImage(file="ustp.png")
photo = photo.subsample(2, 2)

logo_label = tk.Label(
    login_window,
    image=photo,
    bg="#FAE251"
)
logo_label.pack(pady=15)

# LOGIN BOX
login_frame = tk.Frame(
    login_window,
    bg="#AEADA6",
    width=300,
    height=360
)

login_frame.pack(pady=5)
login_frame.pack_propagate(False)

# TITLE
title_label = tk.Label(
    login_frame,
    text="Enter \nAccount Details",
    font=("Times New Roman", 18, "bold"),
    bg="#AEADA6",
    fg="#111844"
)
title_label.pack(pady=10)

# FORM BOX
form_frame = tk.Frame(
    login_frame,
    bg="WhiteSmoke",
    padx=20,
    pady=10
)
form_frame.pack(pady=10)

# USERNAME
tk.Label(
    form_frame,
    text="Username",
    font=("Arial", 12,"italic"),
    bg="WhiteSmoke",
    fg="black"
).pack(anchor="w", pady=(5, 0))

username_entry = tk.Entry(
    form_frame,
    width=30,
)

username_entry.pack(pady=10, ipady=10)

# PASSWORD
tk.Label(
    form_frame,
    text="Password",
    font=("Arial", 12,"italic"),
    bg="WhiteSmoke",
    fg="black"
).pack(anchor="w", pady=(5, 0))

password_entry = tk.Entry(
    form_frame,
    show="*",
    width=30,
)

password_entry.pack(pady=5, ipady=5)

# LOGIN BUTTON
tk.Button(
    form_frame,
    text="Login",
    width=20,
    bg="#FAE251",
    fg="#111844",
    font=("Arial", 11, "italic", "bold"),
    command=login
).pack(pady=15)

login_window.mainloop()
