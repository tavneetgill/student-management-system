import random
import string
import tkinter
from tkinter import *
from datetime import date
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter import messagebox

from PIL import Image,ImageTk
import os
from tkinter.ttk import Combobox
import openpyxl, xlrd
from openpyxl import Workbook
import pathlib
from tkinter.ttk import Treeview


#=================================================SQL Connectivity=========================================================
#import libraries
import mysql.connector
from mysql.connector import Error
import pandas as pd

def create_server_connection(host,user,password,port):
    connection= None
    try:
        connection=mysql.connector.connect(host=host,user=user,password=password,port=port)
        print("MySQL Database Connection successful!")
    except Error as err:
        print(f"Error:'{err}'")
    return connection

pw="tavneet2"
db="studentData"
connection=create_server_connection("127.0.0.1","root",pw,3307)

def create_database(connection,query):
    cursor=connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        if err.errno == 1007:  # Check for specific error: Can't create database; database exists
            print("Database already exists.")
        else :
            print(f"Error:'{err}'")
create_database_query= "Create database studentData"
create_database(connection,create_database_query)

#Connect to database
def create_db_conection(host,user,password,port,dbname):
    connection=None
    try:
        connection=mysql.connector.connect(host=host,user=user,password=password,port=port,database=dbname)
        print("MySQl database connection successful")
    except Error as err:
        print(f"Error:'{err}'")
    return connection

#Execute sql queries
def execute_query(connection,query,values=None):
    cursor=connection.cursor()
    try:
        if values is not None:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        connection.commit()
        print("Query was successful")
    except Error as err:
        print(f"Error:'{err}'")

create_student_table="""
create table student(
Registration_no int primary key ,
Full_Name varchar(30) not null,
DOB date,
Gender varchar(30),
Class int,
Religion varchar(30),
Skills varchar(30)
);
"""
create_parent_table="""
create table Parents(
Student_no int primary key AUTO_INCREMENT,
FatherName varchar(30) not null,
MotherName varchar(30),
FatherOccupation varchar(30),
MotherOccupation varchar(30)
);
"""
create_user_students_table ="""
CREATE TABLE user_students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    student_id INT,
    FOREIGN KEY (user_id) REFERENCES logindata(id),
    FOREIGN KEY (student_id) REFERENCES student(Registration_No)
);
"""
update = """
ALTER TABLE student
MODIFY COLUMN DOB varchar(100),
MODIFY COLUMN Religion varchar(100),
MODIFY COLUMN Skills varchar(100)
"""

auto_increment_query = """
ALTER TABLE student
MODIFY COLUMN Registration_No INT AUTO_INCREMENT
"""
#connect to database
connection=create_db_conection("127.0.0.1","root",pw,3307,db)
execute_query(connection,create_student_table)
execute_query(connection,update)
execute_query(connection, auto_increment_query)
execute_query(connection, create_parent_table)
execute_query(connection, create_user_students_table)

#=============================================================================================================

#==========================================================Login Part===================================================

root = Tk()
root.title('Login')
root.geometry('925x500+170+100')
root.configure(bg='#fff')
root.resizable(False, False)

def user_exists(username):
    try:
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='tavneet2',
            database='studentdata',
            port=3307
        )

        cursor = connection.cursor()
        query = "SELECT * FROM logindata WHERE username=%s"
        cursor.execute(query, (username,))
        user_data = cursor.fetchone()
        cursor.close()
        connection.close()

        if user_data:
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return False

def login():
    username = user.get()
    password = code.get()
    if not user_exists(username):
        messagebox.showerror("Error", "User does not exist.")
    else:
        try:
            connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='tavneet2',
                database='studentdata',
                port=3307
            )

            cursor = connection.cursor()
            query = "SELECT password FROM logindata WHERE username=%s"
            cursor.execute(query, (username,))
            correct_password = cursor.fetchone()
            cursor.close()

            if correct_password and password == correct_password[0]:
                messagebox.showinfo("Success", "Logged in successfully!")
                student(username)
                # Fetch students associated with the logged-in user
                students = fetch_all(username)
                for stu in students:
                    print(stu)  # Display or use the student information as needed

            else:
                messagebox.showerror("Error", "Password is incorrect.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Database error. Please try again later.")

def signup():
    username = user.get()
    password = code.get()
    if user_exists(username):
        messagebox.showerror("Error", "User already exists.")
    else:
        try:
            connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='tavneet2',
                database='studentdata',
                port=3307
            )
            cursor = connection.cursor()
            query = "INSERT INTO logindata (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("Success", "Signed up successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Database error. Please try again later.")


#Fetch data
def fetch_all(username):
                try:
                    connection = mysql.connector.connect(
                        host='127.0.0.1',
                        user='root',
                        password='tavneet2',
                        database='studentdata',
                        port=3307
                    )

                    cursor = connection.cursor()

                    # Get the user ID using their username
                    query = "SELECT id FROM logindata WHERE username=%s"
                    cursor.execute(query, (username,))
                    user_id = cursor.fetchone()[0]

                    # Fetch all students associated with the user using the user_students table
                    query = "SELECT s.* FROM student s JOIN user_students us ON s.Registration_No = us.student_id WHERE us.user_id=%s"
                    cursor.execute(query, (user_id,))
                    students = cursor.fetchall()

                    cursor.close()
                    connection.close()

                    return students
                except mysql.connector.Error as err:
                    print(f"Error: {err}")
                    return []


def student(logged_in_username):
    background = "#06283D"
    framebg = "#EDEDED"
    framefg = "#06283D"

    root = Tk()
    root.title("Student Registration System")
    root.geometry("1250x650+0+0")
    root.config(bg=background)

    file = pathlib.Path('Student_data.xlsx')

    # Exit window
    def Exit():
        root.destroy()

    # Clear
    def Clear():
        Name.set('')
        DOB.set('')
        Religion.set('')
        Skill.set('')
        f_Name.set('')
        m_Name.set('')
        F_occupation.set('')
        m_occupation.set('')
        Class.set("Select Class")
        saveButton.config(state='normal')

    # Save
    def Save():
        username = user.get()
        R1 = Registration.get()
        N1 = name_entry.get()
        C1 = Class.get()
        try:
            G1 = gender
        except:
            messagebox.showerror("Error", "Select Gender!")

        D2 = DOB_entry.get()
        D1 = Date.get()
        Re1 = religion_entry.get()
        S1 = skill_entry.get()
        fathername = f_entry.get()
        mothername = m_entry.get()
        F1 = FO_entry.get()
        M1 = MO_entry.get()


        if N1=="" or C1=="Select Class" or D2=="" or Re1=="" or S1=="" or fathername=="" or mothername=="" or F1=="" or M1=="":
            messagebox.showerror("error","Few Data is missing!")
        else:

            connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='tavneet2',
                database='studentdata',
                port=3307
            )

            cursor = connection.cursor()

            # Get the user ID using their username
            query = "SELECT id FROM logindata WHERE username=%s"
            cursor.execute(query, (username,))
            user_id = cursor.fetchone()[0]
            insert_student_query = "INSERT INTO `student` (`Full_Name`,`Class`,`DOB`,`Gender`,`Religion`,`Skills`) VALUES(%s,%s,%s,%s,%s,%s)"
            cursor.execute(insert_student_query, (N1, C1, D2, G1, Re1, S1,))
            print((user_id,N1, C1, D2, G1, Re1, S1,))
            student_id = cursor.lastrowid
            insert_query2 = "INSERT INTO `parents` (`FatherName`,`MotherName`,`FatherOccupation`,`MotherOccupation`) VALUES(%s,%s,%s,%s)"
            vals2 = (fathername, mothername, F1, M1)
            execute_query(connection, insert_query2, vals2)
            associate_query = "INSERT INTO user_students (user_id, student_id) VALUES (%s, %s)"
            aq = (user_id, student_id)
            execute_query(connection, associate_query, aq)

            connection.commit()
            cursor.close()
            connection.close()

            messagebox.showinfo("info", "Successfully data entered!")

            Clear()



    #Update
    # Update
    def update(radio):
        R1 = reg_entry.get()
        N1 = name_entry.get()
        C1 = Class.get()
        selection(radio)
        D2 = DOB_entry.get()
        D1 = Date.get()
        Re1 = religion_entry.get()
        S1 = skill_entry.get()
        fathername = f_entry.get()
        mothername = m_entry.get()
        F1 = FO_entry.get()
        M1 = MO_entry.get()

        connection = create_db_conection("127.0.0.1", "root", pw, 3307, db)
        cursor = connection.cursor()
        update_student_query = """
                        UPDATE `student`
                        SET `Full_Name` = %s,
                            `Class` = %s,
                            `DOB` = %s,
                            `Gender` = %s,
                            `Religion` = %s,
                            `Skills` = %s
                        WHERE `Registration_no` = %s
                    """
        vals = (N1, C1, D2, gender, Re1, S1, R1)
        execute_query(connection, update_student_query, vals)

        update_parent_query = """
                        UPDATE `Parents`
                        SET `FatherName` = %s,
                            `MotherName` = %s,
                            `FatherOccupation` = %s,
                            `MotherOccupation` = %s
                        WHERE `Student_no` = %s
                    """
        vals2 = (fathername, mothername, F1, M1, R1)
        execute_query(connection, update_parent_query, vals2)

        connection.close()
        messagebox.showinfo("info", "Successfully data updated!")


    # gender
    def selection(radio):
        global gender
        if radio == 1:
            gender = "Male"
        else:
            gender = "Female"


    # Show total records
    def openNewWindow():
        username = user.get()
        newWindow = Toplevel(root)
        newWindow.title("Student Records")
        newWindow.geometry("1000x400")

        # Create a Treeview widget
        tree = ttk.Treeview(newWindow)
        tree['show']='headings'

        s=ttk.Style(newWindow)
        s.theme_use("clam")

        s.configure(".",font=("Helvetica",11))
        s.configure("Treeview.Heading",foreground='black',font=("Helvetica",11,"bold"))
        tree["columns"] = ("Registration No", "Full Name", "Class", "DOB", "Gender", "Religion", "Skills")
        tree.tag_configure("evenrow", background="#f2f2f2")
        tree.tag_configure("oddrow", background="#ffffff")

        tree.column("Registration No",width=150,minwidth=150,anchor=tkinter.CENTER)
        tree.column("Full Name",width=100,minwidth=100,anchor=tkinter.CENTER)
        tree.column("DOB",width=100,minwidth=100,anchor=tkinter.CENTER)
        tree.column("Gender",width=150,minwidth=150,anchor=tkinter.CENTER)
        tree.column("Class",width=100,minwidth=100,anchor=tkinter.CENTER)
        tree.column("Religion",width=100,minwidth=100,anchor=tkinter.CENTER)
        tree.column("Skills",width=250,minwidth=250,anchor=tkinter.CENTER)

        tree.heading("Registration No", text="Registration No")
        tree.heading("Full Name", text="Full Name")
        tree.heading("DOB", text="DOB")
        tree.heading("Gender", text="Gender")
        tree.heading("Class", text="Class")
        tree.heading("Religion", text="Religion")
        tree.heading("Skills", text="Skills")

        # Add data to the Treeview
        i=0
        students = fetch_all(username)
        for student in students:
            tree.insert("",i, text="", values=(student[0],student[1],student[2],student[3],student[4],student[5],student[6]))
            i=i+1

        # Add a scrollbar to the Treeview
        scrollbar = Scrollbar(newWindow, orient="vertical")
        hsb=Scrollbar(newWindow, orient="horizontal")
        hsb.configure(command=tree.xview())
        scrollbar.configure(command=tree.yview())
        tree.configure(xscroll=hsb.set)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)
        hsb.pack(side=BOTTOM, fill=X)

        # Pack the Treeview
        tree.pack(fill="both", expand=True)

    # ===================================UI Design======================================================================
    # top frames
    Label(root, text='Username: '+logged_in_username, width=0, height=1, bg="#08344f",fg='white', anchor='e',font='arial 10 bold').pack(side=TOP, fill=X)
    Label(root, text='Student Registration', width=0, height=2, bg="#0b4b73", fg='#fff', font='arial 20 bold').pack(
        side=TOP, fill=X)


    # Registration and Date
    Label(root, text="Registration No:", font='arial 13', fg=framebg, bg=background).place(x=30, y=100)
    Label(root, text='Date:', font="arial 13", fg=framebg, bg=background).place(x=500, y=100)
    Registration = IntVar()
    Date = StringVar()
    reg_entry = Entry(root, textvariable=Registration, width=15, font='arial 10')
    reg_entry.place(x=160, y=100)


    today = date.today()
    d1 = today.strftime("%d/%m/%Y")
    date_entry = Label(root, text=d1, width=15, font='arial 10')
    date_entry.place(x=550, y=100)


    # Student Details
    obj = LabelFrame(root, text="Student's Details", font=20, bd=2, width=900, bg=framebg, fg=framefg, height=250,
                     relief=GROOVE)
    obj.place(x=30, y=150)

    Label(root, text="Full Name:", font="arial 13", bg=framebg, fg=framefg).place(x=40, y=220)
    Label(root, text="Date of Birth:", font="arial 13", bg=framebg, fg=framefg).place(x=40, y=270)
    Label(root, text="Gender:", font="arial 13", bg=framebg, fg=framefg).place(x=40, y=320)

    Label(root, text="Class:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=220)
    Label(root, text="Religion:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=270)
    Label(root, text="Skills:", font="arial 13", bg=framebg, fg=framefg).place(x=500, y=320)

    Name = StringVar()
    name_entry = Entry(obj, textvariable=Name, width=20, font="arial 10")
    name_entry.place(x=160, y=50)

    DOB = StringVar()
    DOB_entry = Entry(obj, textvariable=DOB, width=20, font="arial 10")
    DOB_entry.place(x=160, y=100)

    radio=IntVar()

    R1 = Radiobutton(obj, text="Male", variable=radio, value=1, bg=framebg, fg=framefg, command=lambda: selection(radio))
    R1.place(x=150, y=150)

    R2 = Radiobutton(obj, text="Female", variable=radio, value=2, bg=framebg, fg=framefg, command=lambda: selection(radio))
    R2.place(x=200, y=150)

    Religion = StringVar()
    religion_entry = Entry(obj, textvariable=Religion, width=20, font="arial 10")
    religion_entry.place(x=630, y=100)

    Skill = StringVar()
    skill_entry = Entry(obj, textvariable=Skill, width=20, font="arial 10")
    skill_entry.place(x=630, y=150)

    Class = Combobox(obj, values=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], font='Roboto 10', width=17, state='r')
    Class.place(x=630, y=50)
    Class.set("Select Class")

    # Parents Details
    obj2 = LabelFrame(root, text="Parent's Details", font=20, bd=2, width=900, bg=framebg, fg=framefg, height=210,
                      relief=GROOVE)
    obj2.place(x=30, y=430)

    Label(obj2, text="Father's Name:", font='arial 13', bg=framebg, fg=framefg).place(x=30, y=50)
    Label(obj2, text="Occupation:", font='arial 13', bg=framebg, fg=framefg).place(x=30, y=100)

    f_Name = StringVar()
    f_entry = Entry(obj2, textvariable=f_Name, width=20, font='arial 10')
    f_entry.place(x=160, y=50)

    F_occupation = StringVar()
    FO_entry = Entry(obj2, textvariable=F_occupation, width=20, font='arial 10')
    FO_entry.place(x=160, y=100)

    Label(obj2, text="Mother's Name:", font='arial 13', bg=framebg, fg=framefg).place(x=500, y=50)
    Label(obj2, text="Occupation:", font='arial 13', bg=framebg, fg=framefg).place(x=500, y=100)

    m_Name = StringVar()
    m_entry = Entry(obj2, textvariable=m_Name, width=20, font='arial 10')
    m_entry.place(x=630, y=50)

    m_occupation = StringVar()
    MO_entry = Entry(obj2, textvariable=m_occupation, width=20, font='arial 10')
    MO_entry.place(x=630, y=100)

    # button
    Button(root, text="Show Records", width=19, height=2, font='arial 12 bold', bg='lightblue',
           command=openNewWindow).place(x=1000, y=150)
    saveButton = Button(root, text="Save", width=19, height=2, font='arial 12 bold', bg='lightblue', command=Save)
    saveButton.place(x=1000, y=250)
    Button(root, text="Reset", width=19, height=2, font='arial 12 bold', bg='lightblue', command=Clear).place(x=1000,
                                                                                                              y=350)
    Button(root, text="Exit", width=19, height=2, font='arial 12 bold', bg='lightblue', command=Exit).place(x=1000,
                                                                                                            y=450)
    Button(root, text="Update", width=19, height=2, font='arial 12 bold', bg='lightblue', command=lambda:update(radio)).place(x=1000,
                                                                                                              y=550)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")
def generate_reset_token():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=20))

def send_reset_email(email, reset_token):
    # In this function, you would typically send an email to the provided email address.
    # Since we cannot send actual emails here, we'll just show a message box with the reset token.
    messagebox.showinfo("Reset Password", f"Reset Token: {reset_token}")


def forgot_password():
    username = user.get()

    if not user_exists(username):
        messagebox.showerror("Error", "User does not exist.")
    else:
        reset_token = generate_reset_token()

        # Store the reset token in the database (You need to add a new table for this purpose)
        try:
            connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='tavneet2',
                database='studentdata',
                port=3307
            )

            cursor = connection.cursor()
            query = "INSERT INTO password_reset_tokens (username, reset_token) VALUES (%s, %s) "
            cursor.execute(query, (username, reset_token))
            connection.commit()
            cursor.close()
            connection.close()
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Database error. Please try again later.")

        send_reset_email(username, reset_token)
        password_reset(username)

def password_reset(username):
    # This function should be triggered when the user clicks on the link in the email or the application opens the reset password page.
    # You'll need to create a new tkinter window to handle the password reset page.
    # In that window, ask the user to enter their reset token and new password.
    # Verify the reset token from the database, and if it's valid, update the user's password.

    reset_window = tk.Toplevel(root)
    reset_window.title("Password Reset")
    reset_window.geometry("300x200")
    center_window(reset_window, 300, 200)

    reset_token_label = tk.Label(reset_window, text="Enter Reset Token:")
    reset_token_label.pack(pady=5)
    reset_token_entry = tk.Entry(reset_window)
    reset_token_entry.pack(pady=5)

    new_password_label = tk.Label(reset_window, text="Enter New Password:")
    new_password_label.pack(pady=5)
    new_password_entry = tk.Entry(reset_window, show="*")
    new_password_entry.pack(pady=5)


    def reset_password(username):
        reset_token = reset_token_entry.get()
        new_password = new_password_entry.get()

        try:
            connection = mysql.connector.connect(
                host='127.0.0.1',
                user='root',
                password='tavneet2',
                database='studentdata',
                port=3307
            )
            cursor = connection.cursor()
            query = "SELECT * FROM password_reset_tokens WHERE reset_token=%s AND username=%s"
            cursor.execute(query, (reset_token,username))
            token_data = cursor.fetchone()
            cursor.close()

            if not token_data:
                messagebox.showerror("Error", "Invalid or expired reset token.")
            else:
                cursor = connection.cursor()
                query = "UPDATE logindata SET password=%s WHERE username=%s"
                cursor.execute(query, (new_password, username))
                cursor.close()

                cursor = connection.cursor()
                query = "DELETE FROM password_reset_tokens WHERE username=%s"
                cursor.execute(query, (username,))
                cursor.close()

                connection.commit()
                connection.close()

                messagebox.showinfo("Success", "Password reset successful!")
                reset_window.destroy()

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", "Database error. Please try again later.")

    reset_button = ttk.Button(reset_window, text="Reset Password", command=lambda: reset_password(username), style='Rounded.TButton')

    reset_button.pack(pady=5)



img = PhotoImage(file='login.png')
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='Sign In', fg='#57a1f8', bg='white', font=('Microsoft YaHei UI Light', 23, 'bold'))
heading.place(x=100, y=5)


def on_enter(e):
    user.delete(0, 'end')


def on_leave(e):
    name = user.get()
    if name == '':
        user.insert(0, 'Username')


user = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
user.place(x=30, y=80)
user.insert(0, 'Username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=107)


def on_enter(e):
    code.delete(0, 'end')


def on_leave(e):
    name = code.get()
    if name == '':
        code.insert(0, 'Password')


code = Entry(frame, width=25, fg='black', border=0, bg="white", font=('Microsoft YaHei UI Light', 11))
code.place(x=30, y=150)
code.insert(0, 'Password')
code.bind('<FocusIn>', on_enter)
code.bind('<FocusOut>', on_leave)

Frame(frame, width=295, height=2, bg="black").place(x=25, y=177)

Button(frame, width=39, pady=7, text='Sign In', bg='#57a1f8', border=0, command=login).place(x=35, y=204)

label = Label(frame, text="Don't have an account?", fg='black', bg='white', font=('Microsoft YaHei UI Light', 9))
label.place(x=75, y=270)

sign_up = Button(frame, width=6, text='Sign Up', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=signup)
sign_up.place(x=215, y=270)
forget_pass= Button(frame, width=20, text='Forget Password?', border=0, bg='white', cursor='hand2', fg='#57a1f8', command=forgot_password)
forget_pass.place(x=100, y=300)


root.mainloop()






