import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from configparser import ConfigParser

# Read database connection information from config file
config = ConfigParser()
config.read('config.ini')
db_config = {
    'host': config.get('database', 'host'),
    'user': config.get('database', 'user'),
    'password': config.get('database', 'password'),
    'database': config.get('database', 'database')
}

# Create a database connection
def connect_to_db():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            return conn
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Connection error: {err}")
        return None

# Current user information
current_user = None

# Refresh user list in Treeview
def update_tree_view_users():
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM license_user")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    for user in users:
        status = "Active" if user['active'] else "Inactive"
        tree.insert("", tk.END, values=(user['id'], user['license'], user['username'], user['password'], status, user['max_server_count'], user['fk_su_modify'], user['modify_date'], user['fk_su_create'], user['create_date']))

# Refresh server list in Treeview
def update_tree_view_servers():
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.*, l.username, l.license
        FROM servers s
        LEFT JOIN license_user l ON s.fk_license_user = l.id
    """)
    servers = cursor.fetchall()
    cursor.close()
    conn.close()

    for server in servers:
        tree.insert("", tk.END, values=(
            server['id'], server['servername'], server['server_address'],
            server['fk_license_user'], server['username'], server['license'],
            server['fk_license_user_modify'], server['modify_date'],
            server['fk_license_user_create'], server['create_date']
        ))

# Add a new user
def add_license_user():
    new_license = entry_license.get()
    new_username = entry_username.get()
    new_password = entry_password.get()
    new_active = var_active.get()
    new_max_server_count = entry_max_server_count.get()

    if not new_license or not new_username or not new_password or not new_max_server_count:
        messagebox.showwarning("Missing Information", "Please fill in all fields.")
        return

    conn = connect_to_db()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO license_user (license, username, password, active, max_server_count, fk_su_create, create_date) VALUES (%s, %s, %s, %s, %s, %s, NOW())",
            (new_license, new_username, new_password, new_active, new_max_server_count, current_user['id'])
        )
        conn.commit()
        messagebox.showinfo("Success", "New user added successfully.")
        update_tree_view_users()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error while adding user: {err}")
    finally:
        cursor.close()
        conn.close()

# Manage users
def manage_license_users():
    def save_license_user():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Warning", "Please select a user to edit.")
            return

        user_id = tree.item(selected_item)["values"][0]
        new_license = entry_license.get()
        new_username = entry_username.get()
        new_password = entry_password.get()
        new_active = var_active.get()
        new_max_server_count = entry_max_server_count.get()

        if not new_license or not new_username or not new_password or not new_max_server_count:
            messagebox.showwarning("Missing Information", "Please fill in all fields.")
            return

        conn = connect_to_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "UPDATE license_user SET license=%s, username=%s, password=%s, active=%s, max_server_count=%s, fk_su_modify=%s, modify_date=NOW() WHERE id=%s",
                (new_license, new_username, new_password, new_active, new_max_server_count, current_user['id'], user_id)
            )
            conn.commit()
            messagebox.showinfo("Success", "User updated successfully.")
            update_tree_view_users()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error while updating user: {err}")
        finally:
            cursor.close()
            conn.close()

    # UI components for managing users
    clear_main_frame()
    main_frame.columnconfigure(1, weight=1)

    label_search = tk.Label(main_frame, text="Search User:")
    label_search.grid(row=0, column=0, padx=10, pady=10, sticky="e")
    entry_search = tk.Entry(main_frame)
    entry_search.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    entry_search.bind("<KeyRelease>", lambda event: search_users(entry_search.get()))

    columns = ("ID", "License", "Username", "Password", "Status", "Max Server Count", "Modified By", "Modification Date", "Created By", "Creation Date")
    global tree
    tree = ttk.Treeview(main_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
    tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    tree.bind("<<TreeviewSelect>>", on_tree_select_license_user)
    main_frame.grid_rowconfigure(1, weight=1)

    label_license = tk.Label(main_frame, text="License:")
    label_license.grid(row=2, column=0, padx=10, pady=5, sticky="e")
    global entry_license
    entry_license = tk.Entry(main_frame)
    entry_license.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    label_username = tk.Label(main_frame, text="Username:")
    label_username.grid(row=3, column=0, padx=10, pady=5, sticky="e")
    global entry_username
    entry_username = tk.Entry(main_frame)
    entry_username.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    label_password = tk.Label(main_frame, text="Password:")
    label_password.grid(row=4, column=0, padx=10, pady=5, sticky="e")
    global entry_password
    entry_password = tk.Entry(main_frame, show="*")
    entry_password.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    label_max_server_count = tk.Label(main_frame, text="Max Server Count:")
    label_max_server_count.grid(row=5, column=0, padx=10, pady=5, sticky="e")
    global entry_max_server_count
    entry_max_server_count = tk.Entry(main_frame)
    entry_max_server_count.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    global var_active
    var_active = tk.IntVar()
    check_active = tk.Checkbutton(main_frame, text="Active", variable=var_active)
    check_active.grid(row=6, column=1, padx=10, pady=5, sticky="w")

    button_add_user = tk.Button(main_frame, text="Add New User", command=add_license_user)
    button_add_user.grid(row=7, column=0, padx=10, pady=10)

    button_save_user = tk.Button(main_frame, text="Update User", command=save_license_user)
    button_save_user.grid(row=7, column=1, padx=10, pady=10)

    update_tree_view_users()

# Fill in user details after selection
def on_tree_select_license_user(event):
    selected_item = tree.selection()
    if selected_item:
        user_id = tree.item(selected_item)["values"][0]
        conn = connect_to_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM license_user WHERE id=%s", (user_id,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        entry_license.delete(0, tk.END)
        entry_license.insert(0, user['license'])
        entry_username.delete(0, tk.END)
        entry_username.insert(0, user['username'])
        entry_password.delete(0, tk.END)
        entry_password.insert(0, user['password'])
        entry_max_server_count.delete(0, tk.END)
        entry_max_server_count.insert(0, user['max_server_count'])
        var_active.set(user['active'])

# Search for users
def search_users(query):
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_to_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM license_user WHERE username LIKE %s", (f"%{query}%",))
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    for user in users:
        status = "Active" if user['active'] else "Inactive"
        tree.insert("", tk.END, values=(user['id'], user['license'], user['username'], user['password'], status, user['max_server_count'], user['fk_su_modify'], user['modify_date'], user['fk_su_create'], user['create_date']))

# Clear the main frame
def clear_main_frame():
    for widget in main_frame.winfo_children():
        widget.destroy()

# Change user
def change_user():
    messagebox.showinfo("Change User", "Logging out...")
    main_screen.destroy()
    start_login()

# Exit the application
def exit_application():
    result = messagebox.askyesno("Exit", "Are you sure you want to exit the application?")
    if result:
        main_screen.destroy()

# Open the main screen
def open_main_screen(user):
    global main_screen, current_user
    current_user = user
    main_screen = tk.Tk()
    main_screen.title("Boylam Mobile Report License Manager")
    main_screen.geometry("800x600")

    # Menu bar
    menu_bar = tk.Menu(main_screen)

    # User Operations Menu
    user_menu = tk.Menu(menu_bar, tearoff=0)
    user_menu.add_command(label="Manage Users", command=manage_license_users)
    menu_bar.add_cascade(label="User Operations", menu=user_menu)

    # Server Operations Menu
    server_menu = tk.Menu(menu_bar, tearoff=0)
    server_menu.add_command(label="Manage Servers", command=manage_servers)
    menu_bar.add_cascade(label="Server Operations", menu=server_menu)

    # Admin Operations Menu (only for root users)
    if user['root']:
        admin_menu = tk.Menu(menu_bar, tearoff=0)
        admin_menu.add_command(label="Manage Admins", command=manage_authorized_users)
        admin_menu.add_command(label="View Logs", command=view_logs)
        menu_bar.add_cascade(label="Admin Operations", menu=admin_menu)

    # Other Menus
    menu_bar.add_command(label="Change User", command=change_user)
    menu_bar.add_command(label="Exit", command=exit_application)

    # Add menu bar to main screen
    main_screen.config(menu=menu_bar)

    # Main frame
    global main_frame
    main_frame = tk.Frame(main_screen)
    main_frame.pack(fill=tk.BOTH, expand=True)

    main_screen.mainloop()

# Login process
def login():
    username = entry_username.get()
    password = entry_password.get()

    if not username or not password:
        messagebox.showwarning("Missing Information", "Please fill in all fields.")
        return

    conn = connect_to_db()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM su WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            if user['active']:
                messagebox.showinfo("Login Successful", "Login successful!")
                root.destroy()  # Close the login screen
                open_main_screen(user)  # Open the main screen
            else:
                messagebox.showerror("Unauthorized User", "This user is not active.")
        else:
            messagebox.showerror("Login Failed", "Incorrect username or password.")

# Login screen UI
def start_login():
    global root, entry_username, entry_password
    root = tk.Tk()
    root.title("Boylam Mobile Report License Manager")
    root.geometry("300x200")

    label_username = tk.Label(root, text="Username:")
    label_username.pack(pady=5)
    entry_username = tk.Entry(root)
    entry_username.pack(pady=5)

    label_password = tk.Label(root, text="Password:")
    label_password.pack(pady=5)
    entry_password = tk.Entry(root, show="*")
    entry_password.pack(pady=5)

    button_login = tk.Button(root, text="Login", command=login)
    button_login.pack(pady=20)

    root.mainloop()

# Start the application
start_login()
