import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import messagebox, Label
from PIL import Image, ImageTk
from utilities import get_products, get_sales, get_low_stock_products

class Dashboard(tk.Frame):
    def __init__(self, master, content_area, show_inventory, show_sales, show_dashboard, logout):
        super().__init__(master)
        self.master = master
        self.configure(bg="#f0f0f0")  
        self.content_area = content_area

        # Dashboard frame to the left
        self.pack(side="left", fill="y")

        # Create a frame for navigation buttons
        self.nav_frame = tk.Frame(self, bg="alice blue")
        self.nav_frame.pack(side=tk.TOP, fill=tk.X)

        # Create navigation buttons
        self.create_nav_button("Dashboard", self.nav_frame, show_dashboard, "#a9d6e5")
        self.create_nav_button("Inventory", self.nav_frame, show_inventory, "#61a5c2")
        self.create_nav_button("Sales", self.nav_frame, show_sales, "#2c7da0" )
        self.create_nav_button("Logout", self.nav_frame, logout, "#014f86")

    def clear_content_area(self):
        # Clear the content area for new content
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def create_nav_button(self, text, frame, command, color):
        button = tk.Button(frame, text=text, command=command, width=20, padx=10, pady=10, bg=color)
        button = tk.Button(frame, text=text, command=command, width=20, padx=10, pady=10, bg=color)
        button = tk.Button(frame, text=text, command=command, width=20, padx=10, pady=10, bg=color)
        button = tk.Button(frame, text=text, command=command, width=20, padx=10, pady=10, bg=color)
        button.pack(pady=5)

    def show_visualization_image(self, image_path, frame):
        # Load and resize the image for the chart
        img = Image.open(image_path)
        img = img.resize((300, 200))  
        img_tk = ImageTk.PhotoImage(img)

        # Create a label to display the image
        label = Label(frame, image=img_tk)
        label.image = img_tk  
        label.pack(side="left", padx=5)

    def show_dashboard(self):
        self.clear_content_area()
        tk.Label(self.content_area, text="Welcome to the Dashboard!", font=("Helvetica", 16), bg="alice blue").pack(pady=20)
        
        # Create the main visualization frame
        visualization_frame = tk.Frame(self.content_area, bg="alice blue")
        visualization_frame.pack(expand=True, fill="both")

        # Create a chart frame to hold the charts
        chart_frame = tk.Frame(visualization_frame, bg="#f0f0f0")
        chart_frame.pack(pady=10)

        # Fetch data and check if there are any products or sales
        products = get_products()
        sales = get_sales()
        low_stock_products = get_low_stock_products()

        if not products:
            messagebox.showinfo("No Products", "No products found in the inventory.")
            return
        if not sales:
            messagebox.showinfo("No Sales", "No sales data found.")

        # Plot 1: Product Distribution (bar chart)
        product_names = [product[1] for product in products]
        quantities = [product[2] for product in products]
        plt.figure(figsize=(5, 4))
        plt.bar(product_names, quantities, color='#dee2ff')
        plt.xlabel("Products")
        plt.ylabel("Quantity")
        plt.title("Product Distribution")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('product_distribution.png')
        plt.close()

        # Plot 2: Sales Summary (bar chart)
        product_ids = [sale[1] for sale in sales]
        sale_quantities = [sale[2] for sale in sales]
        plt.figure(figsize=(5, 4))
        plt.bar(product_ids, sale_quantities, color='#c2f8cb')
        plt.xlabel("Product IDs")
        plt.ylabel("Quantity Sold")
        plt.title("Sales Summary")
        plt.tight_layout()
        plt.savefig('sales_summary.png')
        plt.close()

        # Use the method from the Dashboard instance to display images
        self.show_visualization_image('product_distribution.png', chart_frame)
        self.show_visualization_image('sales_summary.png', chart_frame)

        # Display low stock alert if needed
        if low_stock_products:
            low_stock_names = [product[1] for product in low_stock_products]
            low_stock_message = "Low Stock Alert for: " + ", ".join(low_stock_names)
            messagebox.showwarning("Low Stock Alert", low_stock_message)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Inventory Management System")
    content_area = tk.Frame(root)
    content_area.pack(fill="both", expand=True)

    # dashboard = Dashboard(root, content_area, show_inventory, show_sales, show_dashboard, logout)
    dashboard = Dashboard(root, content_area, lambda: None, lambda: None, lambda: None, lambda: None)
    root.mainloop()
