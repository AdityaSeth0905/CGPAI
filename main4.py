import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
import mysql.connector
from PIL import Image, ImageTk


# Create the Tkinter window
window = ctk.CTk()
window.title("NebulaSource")

# Variable to track whether the "Database" button has been clicked
database_button_clicked = False
navigation_bar = None  # Store the navigation bar frame
data = None

# Function to handle login with MySQL verification
def login():
    global navigation_bar
    username = username_entry.get()
    password = password_entry.get()

    if verify_user(username, password):
        messagebox.showinfo("Login", "Login Successful")
        messagebox.showinfo("Login Successful!", "Welcome " + username + " to the NebulaSource Server")
        clear_login_screen()
        create_navigation_bar()
    else:
        messagebox.showerror("Login", "Login Failed")

# Function to verify username and password against MySQL database
def verify_user(username, password):
    try:
        # Connect to your MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="8882187203",
            database="CIIE"  # Update with your database name
        )

        # Create a cursor object to execute SQL queries
        cursor = db_connection.cursor()

        # Prepare a query to check the username and password
        query = "SELECT * FROM members WHERE username = %s AND password = %s"
        user_data = (username, password)

        # Execute the query
        cursor.execute(query, user_data)

        # Fetch the result (it should return one row if the username and password are correct)
        result = cursor.fetchone()

        # Close the cursor and the database connection
        cursor.close()
        db_connection.close()

        if result:
            return result  # User is verified
        else:
            return None  # User is not verified

    except mysql.connector.Error as e:
        print("Error:", e)
        return None

# Function to create the navigation bar
def create_navigation_bar():
    global navigation_bar
    # Create a navigation bar
    nav_frame = tk.Frame(window, bg="black")
    nav_frame.pack(side="top", fill="x")

    profile_button = tk.Button(nav_frame, text="Profile", font=("Helvetica", 15), command=show_profile)
    profile_button.pack(side="left", padx=10)

    database_button = tk.Button(nav_frame, text="Database", font=("Helvetica", 15), command=handle_database_button)
    database_button.pack(side="left", padx=10)

    navigation_bar = nav_frame  # Store the navigation bar frame

# Function to display user's profile
def show_profile():
    user_data = verify_user(username_entry.get(), password_entry.get())
    if user_data:
        user_profile_window = tk.Toplevel()
        user_profile_window.title("User Profile")

        # Retrieve user data
        username, fname, lname, profile_picture = user_data

        # Display profile picture
        profile_image = Image.open(profile_picture)
        profile_image = profile_image.resize((100, 100), Image.BILINEAR)
        profile_photo = ImageTk.PhotoImage(profile_image)
        profile_picture_label = tk.Label(user_profile_window, image=profile_photo)
        profile_picture_label.photo = profile_photo  # Keep a reference to the image
        profile_picture_label.pack(pady=10)

        # Display username and full name
        username_label = tk.Label(user_profile_window, text=f"Username: {username}", font=("Helvetica", 14))
        username_label.pack()
        full_name_label = tk.Label(user_profile_window, text=f"Full Name: {fname} {lname}", font=("Helvetica", 14))
        full_name_label.pack()

        # Fetch and display other details from the database
        other_details = get_user_details(username)
        for detail in other_details:
            detail_label = tk.Label(user_profile_window, text=detail, font=("Helvetica", 12))
            detail_label.pack()

# Function to retrieve user details from the database
def get_user_details(username):
    try:
        # Connect to your MySQL database
        db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="8882187203",
            database="CIIE"  # Update with your database name
        )

        # Create a cursor object to execute SQL queries
        cursor = db_connection.cursor()

        # Prepare a query to retrieve user details
        query = "SELECT detail FROM user_details WHERE username = %s"
        cursor.execute(query, (username,))

        # Fetch all the details
        details = [row[0] for row in cursor.fetchall()]

        # Close the cursor and the database connection
        cursor.close()
        db_connection.close()

        return details

    except mysql.connector.Error as e:
        print("Error:", e)
        return []

# Function to connect to the database and retrieve data
def connect_to_database():
    try:
        # Connect to your MySQL database
        db_connection = mysql.connector.connect(
            host="localhost", 
            user="root",  
            passwd="8882187203",
            database="ciie"
        )

        # Create a cursor object to execute SQL queries
        cursor = db_connection.cursor()

        # Execute an SQL query to retrieve data
        cursor.execute("SELECT * FROM members")

        # Fetch all the data from the query result
        data = cursor.fetchall()

        # Close the cursor and the database connection
        cursor.close()
        db_connection.close()

        return data

    except mysql.connector.Error as e:
        print("Error:", e)
        return None

# Function to handle the "Database" button click
def handle_database_button():
    global database_button_clicked
    if not database_button_clicked:
        database_button_clicked = True
        show_database_viewer()

# Function to switch to the database viewer
def show_database_viewer():
    global data
    clear_login_screen()
    data = connect_to_database()

    if data:
        # Create a Treeview widget to display the data
        tree = ttk.Treeview(window, columns=list(range(len(data[0]))), show="headings")
        tree.pack()

        # Add column headings
        for i, col in enumerate(data[0]):
            tree.heading(i, text=col)
            tree.column(i, width=100)

        # Add data rows
        for row in data[1:]:
            tree.insert("", "end", values=row)
        
        # Calculate the size of the window based on data size
        window.geometry(f"{len(data[0]) * 100}x{len(data) * 20}")

# Function to clear the login screen
def clear_login_screen():
    image_label.pack_forget()
    image_label.pack_forget()
    image_label.pack_forget()
    image_label.pack_forget()
    username_label.pack_forget()
    username_entry.pack_forget()
    password_label.pack_forget()
    password_entry.pack_forget()
    login_button.pack_forget()

# Load and resize the image using BILINEAR filter
image = Image.open("CIIELOGOWhite.png")
image = image.resize((400, 300), Image.BILINEAR)
photo = ImageTk.PhotoImage(image)

# Create a label to display the image
image_label = tk.Label(window, image=photo, bg="black")
image_label.pack(pady=20)

# Create labels and entry widgets for username and password with a black background
username_label = tk.Label(window, text="Username:", bg="black", fg="white", font=("Helvetica", 20))
username_label.pack(pady=10)

username_entry = tk.Entry(window, font=("Helvetica", 20), bg="black", fg="white")
username_entry.pack(pady=10)

password_label = tk.Label(window, text="Password:", bg="black", fg="white", font=("Helvetica", 20))
password_label.pack(pady=10)

password_entry = tk.Entry(window, show="*", font=("Helvetica", 20), bg="black", fg="white")
password_entry.pack(pady=10)

# Create a login button with the custom font
login_button = tk.Button(window, text="Login", command=login, font=("Helvetica", 20))
login_button.pack(pady=10)

# Start the main event loop
window.mainloop()
