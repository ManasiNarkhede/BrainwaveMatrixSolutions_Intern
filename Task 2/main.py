import tkinter as tk
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from utilities import *
from inventory import Inventory
from dashboard import Dashboard
from sales import Sales

class InventoryApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Inventory Management System")
        self.current_user = None
        
        # Set the background color for the main window
        self.master.configure(bg="#f0f8ff")  

        # Create a title label
        title_label = tk.Label(self.master, text="Inventory Management System", font=("Helvetica", 24, "bold"), bg="#f0f8ff", fg="#003049")
        title_label.pack(pady=10)

        # Create Content_area
        self.content_area = tk.Frame(self.master, bg="#f0f8ff")  
        self.content_area.pack(fill="both", expand=True)

        # Initialize the main frame
        self.main_frame = Frame(self.master, bg="#f0f8ff")  
        self.main_frame.pack(fill="both", expand=True)

        # Login frame
        tk.Label(self.content_area, text="Login Page", font=("Helvetica", 16), bg="#f0f8ff").pack(pady=20)
        self.frame_login = tk.Frame(self.content_area, bg="#f0f8ff")  
        self.frame_login.pack(pady=(20, 10), padx=20)

        # UI elements for the login frame
        tk.Label(self.frame_login, text="Username:", bg="#e6f7ff").pack()
        self.username_entry = Entry(self.frame_login)
        self.username_entry.pack()

        tk.Label(self.frame_login, text="Password:", bg="#e6f7ff").pack()
        self.password_entry = Entry(self.frame_login, show='*')
        self.password_entry.pack()

        tk.Button(self.frame_login, text="Login", command=self.login, bg="#b5e48c").pack(pady=5)
        tk.Button(self.frame_login, text="Register", command=self.register, bg="#57cc99").pack(pady=5)

        # Place the image
        self.bottom_image = PhotoImage(file="D:/Brainwave Matrix Solutions Internship/Task-2/images/background.png") 
        self.bottom_image_label = tk.Label(self.frame_login, image=self.bottom_image, bg="#f0f0f0")
        self.bottom_image_label.pack(side=tk.BOTTOM, pady=10) 

        # Initialize the Dashboard 
        self.frame_dashboard = None

        # Navigation Buttons 
        self.frame_navigation = tk.Frame(self.master, bg="#f0f0f0")  
        self.frame_navigation.pack(side=tk.LEFT, fill=tk.Y)

        # Initialize the Inventory (but do not display it yet)
        self.frame_inventory = None
        self.sales_frame = None

    def clear_content_area(self):
        # Clear the content area for new content
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login_user(username, password):
            self.current_user = username
            self.frame_login.pack_forget()  # Hide login frame
            
            # Create an instance of the Dashboard class
            self.frame_dashboard = Dashboard(
                self.master,
                self.content_area,
                show_inventory=self.show_inventory,
                show_sales=self.show_sales,
                show_dashboard=self.show_dashboard,
                logout=self.logout
            )
            self.frame_dashboard.pack(side=tk.LEFT, padx=10, fill=tk.Y)  # Show dashboard frame
            self.frame_dashboard.show_dashboard()  # Call the show_dashboard method

        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if username and password:
            register_user(username, password)
            messagebox.showinfo("Registration Success", "User registered successfully!")
        else:
            messagebox.showwarning("Input Error", "Please enter a username and password.")

    def logout(self):
        self.current_user = None
        if self.frame_dashboard is not None:
            self.frame_dashboard.pack_forget()  
            self.frame_dashboard = None
            
        # Hide the inventory frame if it exists
        if self.frame_inventory is not None:
            self.frame_inventory.pack_forget()  
            self.frame_inventory = None 

        # Hide the sales frame if it exists
        if self.frame_sales is not None:
            self.frame_sales.pack_forget()  
            self.frame_sales = None 
            
        # Clear the content area
        self.clear_content_area()

        # Display the login frame 
        tk.Label(self.content_area, text="Logged out successfully", font=("Helvetica", 16), bg="#f0f8ff").pack(pady=20)
        self.frame_login = tk.Frame(self.content_area, bg="#f0f8ff")  # Light Blue
        self.frame_login.pack(pady=(20, 10), padx=20)

        tk.Label(self.frame_login, text="Username:", bg="#e6f7ff").pack()
        self.username_entry = Entry(self.frame_login)
        self.username_entry.pack()

        tk.Label(self.frame_login, text="Password:", bg="#e6f7ff").pack()
        self.password_entry = Entry(self.frame_login, show='*')
        self.password_entry.pack()

        tk.Button(self.frame_login, text="Login", command=self.login, bg="#b5e48c").pack(pady=5)
        tk.Button(self.frame_login, text="Register", command=self.register, bg="#57cc99").pack(pady=5)

        self.bottom_image = PhotoImage(file="D:/Brainwave Matrix Solutions Internship/Task-2/images/background.png")  # Change to your bottom image path
        self.bottom_image_label = tk.Label(self.frame_login, image=self.bottom_image, bg="#f0f0f0")
        self.bottom_image_label.pack(side=tk.BOTTOM, pady=10) 

    def show_dashboard(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Welcome to the Dashboard!", font=("Helvetica", 16),bg="#f0f0f0").pack(pady=20)
        
        # Create the main visualization frame
        visualization_frame = tk.Frame(self.content_area, bg="#f0f8ff")
        visualization_frame.pack(expand=True, fill="both")

        # Create a chart frame to hold the charts
        chart_frame = tk.Frame(visualization_frame, bg="#f0f8ff")
        chart_frame.pack(pady=10)

        # Fetch data to check if there are any products or sales
        products = get_products()
        sales = get_sales()
        low_stock_products = get_low_stock_products()

        if not products:
            messagebox.showinfo("No Products", "No products found in the inventory.")
            return
        if not sales:
            messagebox.showinfo("No Sales", "No sales data found.")

        # Plot 1: Product Distribution 
        product_names = [product[1] for product in products]
        quantities = [product[2] for product in products]
        plt.figure(figsize=(5, 4))
        plt.bar(product_names, quantities, color='lightblue')
        plt.xlabel("Products")
        plt.ylabel("Quantity")
        plt.title("Product Distribution")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('product_distribution.png')
        plt.close()

        # Plot 2: Sales Summary 
        product_ids = [sale[1] for sale in sales]
        sale_quantities = [sale[2] for sale in sales]
        plt.figure(figsize=(5, 4))
        plt.bar(product_ids, sale_quantities, color='lightgreen')
        plt.xlabel("Product IDs")
        plt.ylabel("Quantity Sold")
        plt.title("Sales Summary")
        plt.tight_layout()
        plt.savefig('sales_summary.png')
        plt.close()

        # Dashboard instance to display images
        self.frame_dashboard.show_visualization_image('product_distribution.png', chart_frame)
        self.frame_dashboard.show_visualization_image('sales_summary.png', chart_frame)

        # Display low stock alert if needed
        if low_stock_products:
            low_stock_names = [product[1] for product in low_stock_products]
            low_stock_message = "Low Stock Alert for: " + ", ".join(low_stock_names)
            messagebox.showwarning("Low Stock Alert", low_stock_message)

    def show_inventory(self):     
        self.clear_content_area()
                
        if self.frame_inventory is None:  
            self.frame_inventory = Inventory(self.master, self.content_area)

        self.frame_inventory.pack(fill="both", expand=True)  # Show inventory frame

    def show_sales(self):
        self.clear_content_area()
        self.frame_sales = Sales(self.master, self.content_area)
        self.frame_sales.pack(fill="both", expand=True)

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
