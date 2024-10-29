import tkinter as tk
from tkinter import messagebox, StringVar, Listbox, PhotoImage
from utilities import *  

class Inventory(tk.Frame):
    def __init__(self, master, content_area):
        super().__init__(master, bg="#f0f8ff")
        self.master = master
        self.content_area = content_area
        self.products = []  # Example list to hold products

        self.low_stock_threshold = 5  # Define the low stock threshold

        # Create a frame to hold inventory widgets
        self.frame_inventory = tk.Frame(self.content_area, bg="#f0f8ff")  # Light blue background
        self.frame_inventory.pack(fill=tk.BOTH, expand=True)
    
        # Inventory Title Label
        self.inventory_title = tk.Label(self.frame_inventory, text="Inventory", font=("Helvetica", 20, "bold"), bg="#f0f8ff", fg="#333")
        self.inventory_title.pack(pady=10)
        
        # Summary Label
        self.summary_label = tk.Label(self.frame_inventory, text="Inventory Summary: Total Items: 0 | Total Value: ₹0.00", bg="#f0f8ff", fg="#333")
        self.summary_label.pack(pady=10)

        # Search Bar
        search_frame = tk.Frame(self.content_area, bg="#f0f8ff")
        search_frame.pack()

        tk.Label(search_frame, text="Search Product:", bg="#f0f8ff", fg="#333").pack(side=tk.LEFT, padx=5)  
        self.search_var = StringVar()
        self.search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)  
        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_product_list())

        # Sort Options
        self.sort_option = StringVar(value="Sort By")
        sort_options = ["ID", "Name", "Quantity", "Price"]
        self.sort_menu = tk.OptionMenu(search_frame, self.sort_option, *sort_options, command=lambda _: self.refresh_product_list())
        self.sort_menu.config(bg="#fff", fg="#333")
        self.sort_menu.pack(side=tk.LEFT, padx=5)

        # Filter Low Stock Checkbutton
        self.low_stock_only = tk.BooleanVar(value=False)
        self.low_stock_check = tk.Checkbutton(search_frame, text="Show Low Stock Only", variable=self.low_stock_only, command=self.refresh_product_list, bg="#f0f8ff", fg="#333")
        self.low_stock_check.pack(side=tk.LEFT, padx=5)

        # Listbox to display products
        self.product_list = Listbox(self.frame_inventory, width=80, bg="#fff", fg="#333")
        self.product_list.pack(padx=10, pady=10)

        # Scrollbar for the Listbox
        self.scrollbar = tk.Scrollbar(self.frame_inventory)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.product_list.yview)

        # Call to refresh the product list initially
        self.refresh_product_list()

        # Labels for input fields
        input_frame = tk.Frame(self.frame_inventory, bg="#f0f8ff")
        input_frame.pack(pady=5)

        tk.Label(input_frame, text="Product Name:", bg="#f0f8ff", fg="#333").pack(side=tk.LEFT, padx=5)
        self.product_name = tk.Entry(input_frame)
        self.product_name.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="Quantity:", bg="#f0f8ff", fg="#333").pack(side=tk.LEFT, padx=5)
        self.product_quantity = tk.Entry(input_frame)
        self.product_quantity.pack(side=tk.LEFT, padx=5)

        tk.Label(input_frame, text="Price:", bg="#f0f8ff", fg="#333").pack(side=tk.LEFT, padx=5)
        self.product_price = tk.Entry(input_frame)
        self.product_price.pack(side=tk.LEFT, padx=5)

        # Buttons
        button_frame = tk.Frame(self.frame_inventory, bg="#f0f8ff")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Add Product", command=self.add_product, bg="#06a77d", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Edit Product", command=self.show_edit_product_page, bg="#005c69", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Update Product", command=self.update_product, bg="#119da4", fg="#fff").pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Delete Product", command=self.delete_product, bg="#dd2d4a", fg="#fff").pack(side=tk.LEFT, padx=5)

    def add_product(self):
        name = self.product_name.get()
        quantity = self.product_quantity.get()
        price = self.product_price.get()

        if name == "":
            messagebox.showwarning("Warning", "Product name cannot be empty.")
            return

        try:
            quantity = int(quantity)
        except ValueError:
            messagebox.showwarning("Warning", "Quantity must be an integer.")
            return

        try:
            price = float(price)
        except ValueError:
            messagebox.showwarning("Warning", "Price must be a number.")
            return

        add_product(name, quantity, price)
        messagebox.showinfo("Success", "Product added successfully!")
        self.refresh_product_list()

    def show_edit_product_page(self):
        selected_product = self.product_list.curselection()
        if selected_product:
            product_details = self.product_list.get(selected_product).split('|')
            self.product_name.delete(0, tk.END)
            self.product_name.insert(0, product_details[1].split(":")[1].strip())
            self.product_quantity.delete(0, tk.END)
            self.product_quantity.insert(0, product_details[2].split(":")[1].strip())
            self.product_price.delete(0, tk.END)
            self.product_price.insert(0, product_details[3].split(":")[1].strip().replace('₹', ''))
        else:
            messagebox.showwarning("Selection Error", "Please select a product to edit.")

    def update_product(self):
        selected_product = self.product_list.curselection()
        if selected_product:
            product_id = int(self.product_list.get(selected_product).split('|')[0].split(':')[1].strip())
            name = self.product_name.get()
            quantity = int(self.product_quantity.get())
            price = float(self.product_price.get())
            update_product(product_id, name, quantity, price)
            self.refresh_product_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a product to update.")

    def delete_product(self):
        selected_product = self.product_list.curselection()
        if selected_product:
            product_id = int(self.product_list.get(selected_product).split('|')[0].split(':')[1].strip())
            delete_product(product_id)
            self.refresh_product_list()
        else:
            messagebox.showwarning("Selection Error", "Please select a product to delete.")

    def refresh_product_list(self):
        # Clear the current product list display
        self.product_list.delete(0, tk.END)
        products = get_products()  # Fetch products from the database

        # Apply search filter
        search_term = self.search_var.get().lower()
        products = [p for p in products if search_term in p[1].lower()]

        # Apply low stock filter
        if self.low_stock_only.get():
            products = [p for p in products if p[2] < self.low_stock_threshold]

        # Sort products based on selected option
        sort_by = self.sort_option.get()
        if sort_by == "Name":
            products.sort(key=lambda x: x[1].lower())
        elif sort_by == "Quantity":
            products.sort(key=lambda x: x[2])
        elif sort_by == "Price":
            products.sort(key=lambda x: x[3])

        # Populate the product list with formatted data
        total_items = 0
        total_value = 0.0
        for product in products:
            total_items += product[2]
            total_value += product[2] * float(product[3])  # Convert to float
            low_stock_warning = " (Low Stock)" if product[2] < self.low_stock_threshold else ""
            self.product_list.insert(tk.END, f"ID: {product[0]} | Name: {product[1]} | Quantity: {product[2]}{low_stock_warning} | Price: ₹{float(product[3]):.2f}")

        # Update summary label with the inventory summary
        self.summary_label.config(text=f"Inventory Summary: Total Items: {total_items} | Total Value: ₹{total_value:.2f}")

    def update_inventory_summary(self, products):
        if not products:
            total_items = 0
            total_value = 0.0
        else:
            total_items = sum(product[2] for product in products)
            total_value = sum(product[2] * product[3] for product in products)

        self.summary_label.config(text=f"Inventory Summary: Total Items: {total_items} | Total Value: ₹{total_value:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Inventory Management System")
    root.configure(bg="#f0f8ff")  
    app = Inventory(root, content_area=root)
    app.pack(fill=tk.BOTH, expand=True)
    root.mainloop()