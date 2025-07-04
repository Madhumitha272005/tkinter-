from tkinter import *
from tkinter import messagebox, ttk
import pymysql
import matplotlib.pyplot as plt

# DB Connection
def get_connection_localDB():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='Madhu@2005',
        db='job_application',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )

root = Tk()
root.title('Login Page')
root.geometry('925x500+300+200')
root.configure(bg="#fff")
root.resizable(False, False)

def signin():
    username = user.get()
    password = code.get()
    if username == 'admin' and password == '1234':
        open_application_form()
    else:
        messagebox.showerror("Invalid", "Invalid username or password")

# Login UI
img = PhotoImage(file=r"C:\\Users\\Madhumitha\\OneDrive\\Desktop\\robotkutty.png")
Label(root, image=img, bg='white').place(x=50, y=50)

frame = Frame(root, width=350, height=350, bg="white")
frame.place(x=480, y=70)

heading = Label(frame, text='LOGIN', fg='#57a1f8', bg='white', font=('Times new roman', 24, 'bold'))
heading.place(x=100, y=5)

def on_enter(e): user.delete(0, 'end')
def on_leave(e): 
    if user.get() == '': user.insert(0, 'username')

user = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Times new roman', 14))
user.place(x=30, y=80)
user.insert(0, 'username')
user.bind('<FocusIn>', on_enter)
user.bind('<FocusOut>', on_leave)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=107)

def on_enter_pw(e): code.delete(0, 'end')
def on_leave_pw(e): 
    if code.get() == '': code.insert(0, 'password')

code = Entry(frame, width=25, fg='black', border=0, bg='white', font=('Times new roman', 14))
code.place(x=30, y=150)
code.insert(0, 'password')
code.bind('<FocusIn>', on_enter_pw)
code.bind('<FocusOut>', on_leave_pw)
Frame(frame, width=295, height=2, bg='black').place(x=25, y=177)

Button(frame, width=39, pady=7, text='LOGIN', bg='#57a1f8', fg='white', border=0, command=signin).place(x=35, y=204)

# Application Form
def open_application_form():
    app = Toplevel(root)
    app.title("Job Application Form")
    app.geometry('500x600')
    app.config(bg='white')

    Label(app, text="Job Application Form", font=('Times new roman', 20, 'bold'), bg='white').pack(pady=10)

    labels = ['Name', 'Age', 'Date of Birth (YYYY-MM-DD)', 'Gender', 'Email', 'Phone', 'Address', 'Skills', 'Experience']
    entries = {}

    y_pos = 60
    for label in labels:
        Label(app, text=label+":", font=('Times new roman', 12), bg='white').place(x=30, y=y_pos)
        if label == 'Gender':
            combo = ttk.Combobox(app, values=['Male', 'Female', 'Other'], font=('Times new roman', 12))
            combo.place(x=220, y=y_pos)
            entries[label] = combo
        else:
            entry = Entry(app, width=30, font=('Times new roman', 12))
            entry.place(x=220, y=y_pos)
            entries[label] = entry
        y_pos += 40

    # Submit function
    def submit_form():
        data = {field: entry.get().strip() for field, entry in entries.items()}
        try:
            conn = get_connection_localDB()
            with conn.cursor() as cursor:
                sql = """
                INSERT INTO applications (name, age, dob, gender, email, phone, address, skills, experience)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """
                cursor.execute(sql, (
                    data['Name'], data['Age'], data['Date of Birth (YYYY-MM-DD)'], data['Gender'],
                    data['Email'], data['Phone'], data['Address'], data['Skills'], data['Experience']
                ))
                conn.commit()
            messagebox.showinfo("Success", "Data saved to database!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
        finally:
            conn.close()

    # View function
    def view_data():
        try:
            conn = get_connection_localDB()
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM applications")
                records = cursor.fetchall()
            show_data_table(records)
            show_age_chart(records)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
        finally:
            conn.close()

    Button(app, text="Submit", bg='#57a1f8', fg='white', font=('Times new roman', 12),
           command=submit_form).place(x=200, y=y_pos+20)
    Button(app, text="View Data", bg='green', fg='white', font=('Times new roman', 12),
           command=view_data).place(x=280, y=y_pos+20)

# Show table
def show_data_table(records):
    table_win = Toplevel(root)
    table_win.title("Data Table")
    tree = ttk.Treeview(table_win, columns=('ID', 'Name', 'Age', 'DOB', 'Gender', 'Email', 'Phone', 'Address', 'Skills', 'Experience'),
                        show='headings')
    for col in tree['columns']:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    for row in records:
        tree.insert('', END, values=(
            row['id'], row['name'], row['age'], row['dob'], row['gender'], row['email'],
            row['phone'], row['address'], row['skills'], row['experience']
        ))
    tree.pack(fill=BOTH, expand=True)

# Simple chart (age distribution)
def show_age_chart(records):
    ages = [int(r['age']) for r in records if r['age']]
    if ages:
        plt.figure(figsize=(6,4))
        plt.hist(ages, bins=range(min(ages), max(ages)+2), color='skyblue', edgecolor='black')
        plt.title("Age Distribution")
        plt.xlabel("Age")
        plt.ylabel("Count")
        plt.show()
    else:
        messagebox.showinfo("No Data", "No age data to show chart")

root.mainloop()
