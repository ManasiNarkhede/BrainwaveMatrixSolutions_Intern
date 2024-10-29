    selected_index = self.sales_listbox.curselection()
        if selected_index:
            product_name = self.sales_listbox.get(selected_index).split(" - ")[0].split(": ")[1].strip()
            print(f"Deleting product: {product_name}")  # Debug print statement

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
