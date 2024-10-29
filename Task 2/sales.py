import tkinter as tk
from tkinter import messagebox, END
from utilities import connect_db  

class Sales(tk.Frame):
    def __init__(self, master, content_area):
        super().__init__(content_area, bg="#f0f8ff")  
        self.sales_data = []  # Initialize empty sales data list

        # Create a label for "Sales" 
        tk.Label(self, text="Sales", font=("Helvetica", 16), bg="#e6f7ff").pack(pady=10)

        # Create a form frame 
        self.form_frame = tk.Frame(self, bg="#f0f8ff")  
        self.form_frame.pack(side="top", anchor="n", pady=10, padx=10)

        # Create the sales form within form_frame
        self.create_sales_form()

        # Create the sales listbox 
        self.sales_listbox = tk.Listbox(self, width=70, height=6, bg="#ffffff")  
        self.sales_listbox.pack(pady=10, padx=10)  
        self.sales_listbox.bind("<<ListboxSelect>>", self.on_sales_select)

        # Pack this Sales frame in the content area
        self.pack(fill="both", expand=True)
        self.load_sales()

    def create_sales_form(self):
        # Sales form in form_frame with input boxes
        tk.Label(self.form_frame, text="Product Name:", bg="#f0f8ff").pack(side="top", anchor="w", padx=5, pady=2)
        self.product_name_entry = tk.Entry(self.form_frame, width=30)
        self.product_name_entry.pack(padx=5, pady=2)

        tk.Label(self.form_frame, text="Quantity Sold:", bg="#f0f8ff").pack(side="top", anchor="w", padx=5, pady=2)
        self.quantity_entry = tk.Entry(self.form_frame, width=30)
        self.quantity_entry.pack(padx=5, pady=2)

        tk.Label(self.form_frame, text="Sale Price:", bg="#f0f8ff").pack(side="top", anchor="w", padx=5, pady=2)
        self.sale_price_entry = tk.Entry(self.form_frame, width=30)
        self.sale_price_entry.pack(padx=5, pady=2)

        # Buttons for sales management 
        button_frame = tk.Frame(self.form_frame)
        button_frame.pack(fill="x", pady=5)
        tk.Button(button_frame, text="Add Sale", command=self.add_sale, bg="#06a77d", fg="#fff").pack(side="left", padx=5)  # Green button
        tk.Button(button_frame, text="Update Sale", command=self.update_sale, bg="#119da4", fg="#fff").pack(side="left", padx=5)  # Orange button
        tk.Button(button_frame, text="Delete Sale", command=self.delete_sale, bg="#dd2d4a",  fg="#fff").pack(side="left", padx=5)  # Red button

    def clear_sales_form(self):
        self.product_name_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.sale_price_entry.delete(0, END)

    def load_sales(self):
        self.sales_listbox.delete(0, END)

        # Use the connect_db function to get the connection
        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Fetch sales data from the database
            cursor.execute("SELECT product_name, quantity, sale_price FROM sales")
            sales = cursor.fetchall()

            # Populate the listbox with sales data
            for sale in sales:
                self.sales_listbox.insert(END, f"Product: {sale[0]} - Quantity: {sale[1]}, Price: {sale[2]}")
        
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

        finally:
            cursor.close()  
            conn.close()    

    def add_sale(self):
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        sale_price = self.sale_price_entry.get()

        if product_name and quantity.isdigit() and sale_price.replace('.', '', 1).isdigit():
            conn = connect_db()
            cursor = conn.cursor()

            try:
                query = """
                    INSERT INTO sales (product_name, quantity, sale_price)
                    VALUES (%s, %s, %s)
                """
                cursor.execute(query, (product_name, int(quantity), float(sale_price)))
                conn.commit()

                # Load updated sales data into the listbox
                self.load_sales()
                self.clear_sales_form()
                messagebox.showinfo("Success", "Sale added successfully!")
            
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

            finally:
                cursor.close()
                conn.close()

        else:
            messagebox.showerror("Input Error", "Please provide valid data.")

    def on_sales_select(self, event):
        selected_index = self.sales_listbox.curselection()
        if selected_index:  
            sale_data = self.sales_listbox.get(selected_index).split(" - ")
            
            # Handle different parsing scenarios 
            if len(sale_data) == 2:
                product_name = sale_data[0]
                details = sale_data[1].split(", ")
                
                quantity, price = None, None
                for detail in details:
                    if "Quantity:" in detail:
                        quantity = detail.split(": ")[1]
                    elif "Price:" in detail:
                        price = detail.split(": ")[1]
                
                # Update entries only if parsed values are available
                self.product_name_entry.delete(0, END)
                self.product_name_entry.insert(0, product_name)

                if quantity:
                    self.quantity_entry.delete(0, END)
                    self.quantity_entry.insert(0, quantity)

                if price:
                    self.sale_price_entry.delete(0, END)
                    self.sale_price_entry.insert(0, price)
            else:
                messagebox.showerror("Error", "Unable to parse selected sale item.")

    def update_sale(self):
        selected_index = self.sales_listbox.curselection()
        if selected_index:
            product_name = self.product_name_entry.get()
            quantity = self.quantity_entry.get()
            sale_price = self.sale_price_entry.get()

            if product_name and quantity.isdigit() and sale_price.replace('.', '', 1).isdigit():
                conn = connect_db()
                cursor = conn.cursor()
                try:
                    query = """
                        UPDATE sales 
                        SET quantity = %s, sale_price = %s 
                        WHERE product_name = %s
                    """
                    cursor.execute(query, (int(quantity), float(sale_price), product_name))
                    conn.commit()
                    self.load_sales()  # Refresh the listbox
                    self.clear_sales_form()
                    messagebox.showinfo("Success", "Sale updated successfully!")
                except Exception as e:
                    messagebox.showerror("Database Error", f"An error occurred: {e}")
                finally:
                    cursor.close()
                    conn.close()
            else:
                messagebox.showerror("Input Error", "Please provide valid data.")
        else:
            messagebox.showwarning("Selection Error", "Please select a sale to update.")

    def delete_sale(self):
        selected_index = self.sales_listbox.curselection()
        if selected_index:
            product_name = self.sales_listbox.get(selected_index).split(" - ")[0].split(": ")[1].strip()
            print(f"Deleting product: {product_name}")  

            conn = connect_db()
            cursor = conn.cursor()
            try:
                query = "DELETE FROM sales WHERE product_name = %s"
                cursor.execute(query, (product_name,))
                conn.commit()
                self.load_sales()  # Refresh the listbox
                self.clear_sales_form()
                messagebox.showinfo("Success", "Sale deleted successfully!")
            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")
            finally:
                cursor.close()
                conn.close()
        else:
            messagebox.showwarning("Selection Error", "Please select a sale to delete.")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("800x600")  
    content_area = tk.Frame(root)
    content_area.pack(fill="both", expand=True)
    
    Sales(master=root, content_area=content_area)  
    
    root.mainloop() 
