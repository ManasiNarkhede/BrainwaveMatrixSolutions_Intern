import tkinter as tk
from tkinter import messagebox, simpledialog
import random
from account import Account

class ATMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NavBharat ATM")
        self.root.geometry("400x600")

        # Create a frame for logo at the top
        self.logo_frame = tk.Frame(self.root, bg="#f8f9fa")
        self.logo_frame.pack(side="top", fill="x")

        # Load and resize the logo 
        self.logo_image = tk.PhotoImage(file=r"D:\Brainwave Matrix Solutions Internship\Task-1\images\logo.png")  
        self.resized_logo = self.logo_image.subsample(3, 3)  
        self.label_logo = tk.Label(self.logo_frame, image=self.resized_logo, bg="#f8f9fa")
        self.label_logo.pack(pady=10)

        # Create a canvas for the background image
        self.canvas = tk.Canvas(self.root, width=1000, height=600, bg="#f8f9fa")
        self.canvas.pack(fill="both", expand=True)

        # Load and set the background image
        self.background_image = tk.PhotoImage(file=r"D:\Brainwave Matrix Solutions Internship\Task-1\images\atm.png")  
        self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        
        # Create the main content frame
        self.main_frame = tk.Frame(self.canvas, bg="white", bd=10, relief="groove")
        self.main_frame.place(relx=0.5, rely=0.4, anchor="center")

        # ATM System Data
        self.accounts = {}
        self.current_account = None

        # Show the welcome screen first
        self.create_welcome_screen()

    def create_welcome_screen(self):
        """Create the main welcome screen."""
        self.clear_screen()

        # Welcome Title
        self.label_welcome = tk.Label(self.main_frame, text="Welcome to NavBharat ATM", font=("Arial", 24, "bold"), bg="white")
        self.label_welcome.pack(pady=20)

        # Tagline
        self.label_tagline = tk.Label(self.main_frame, text="Secure. Swift. Simple", font=("Arial", 16, "italic"), bg="white")
        self.label_tagline.pack(pady=10)

        # Insert Card Button 
        self.button_insert_card = tk.Button(self.main_frame, text="Insert Card", font=("Arial", 14), bg="#468faf", fg="white", command=self.simulate_card_insertion)  
        self.button_insert_card.pack(pady=20)

        # Cardless Transactions Button
        self.button_cardless_transaction = tk.Button(self.main_frame, text="Cardless Transactions", font=("Arial", 14), bg="#468faf", fg="white", command=self.create_cardless_transaction_screen)  
        self.button_cardless_transaction.pack(pady=10)

        # Exit Button
        self.button_exit = tk.Button(self.main_frame, text="Exit", font=("Arial", 14), bg="#c9184a", fg="white", command=self.root.quit)  
        self.button_exit.pack(pady=10)

    def simulate_card_insertion(self):
        """Simulate the card reading process with a random account number."""
        self.clear_screen()

        # Display "Please wait" message
        self.label_wait = tk.Label(self.main_frame, text="Please wait while the card is read...", font=("Arial", 16), bg="white")
        self.label_wait.pack(pady=20)

        # Wait for 5 seconds to simulate card reading
        self.root.update()
        self.root.after(5000, self.generate_random_account)

    def generate_random_account(self):
        """Generate a random account number and move to PIN entry."""
        account_number = str(random.randint(100000, 999999))

        # Create a default account if not present
        if account_number not in self.accounts:
            self.accounts[account_number] = Account(account_number, "1234", balance=5000.00)

        # Set the current account
        self.current_account = self.accounts[account_number]

        # Display the card inserted message
        self.clear_screen()
        self.label_card_inserted = tk.Label(self.main_frame, text="Leave your card inserted during the entire transaction.", font=("Arial", 16, "bold"), bg="white")
        self.label_card_inserted.pack(pady=20)

        # Proceed to PIN entry after showing the message
        self.root.update()
        self.root.after(3000, self.create_pin_entry_screen)

    def create_pin_entry_screen(self):
        """Create the PIN entry screen."""
        self.clear_screen()

        self.label_pin_entry = tk.Label(self.main_frame, text="Enter PIN", font=("Arial", 24, "bold"), bg="white")
        self.label_pin_entry.pack(pady=20)

        # PIN Label and Entry
        self.label_pin = tk.Label(self.main_frame, text="PIN:", bg="white")
        self.label_pin.pack(pady=10)
        self.entry_pin = tk.Entry(self.main_frame, show="*")
        self.entry_pin.pack(pady=10)

        # Instruction to use 1234 as pin
        self.label_hint = tk.Label(self.main_frame, text="(Use PIN 1234)", font=("Arial", 12, "italic"), bg="white")
        self.label_hint.pack(pady=5)

        # Login Button
        self.button_login = tk.Button(self.main_frame, text="Login", font=("Arial", 14), bg="#02c39a", fg="white", command=self.login_with_pin)  
        self.button_login.pack(pady=20)

    def login_with_pin(self):
        """Handle PIN entry and check for correctness."""
        entered_pin = self.entry_pin.get()

        # Check if the entered PIN matches the default PIN "1234"
        if entered_pin == "1234":
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Incorrect PIN. Please try again.")

    def create_main_menu(self):
        """Create the main ATM menu screen."""
        self.clear_screen()

        self.label_welcome = tk.Label(self.main_frame, text=f"Welcome, Customer ({self.current_account.account_number})", font=("Arial", 18, "bold"), bg="white")
        self.label_welcome.pack(pady=20)

        # Buttons for each action
        self.button_balance = tk.Button(self.main_frame, text="Check Balance", font=("Arial", 14), bg="#64dfdf", fg="white", command=self.show_balance)  
        self.button_balance.pack(pady=10)

        self.button_deposit = tk.Button(self.main_frame, text="Deposit Money", font=("Arial", 14), bg="#48bfe3", fg="white", command=self.deposit_money)  
        self.button_deposit.pack(pady=10)

        self.button_withdraw = tk.Button(self.main_frame, text="Withdraw Money", font=("Arial", 14), bg="#5390d9", fg="white", command=self.withdraw_money)  
        self.button_withdraw.pack(pady=10)

        self.button_history = tk.Button(self.main_frame, text="Transaction History", font=("Arial", 14), bg="#6930c3", fg="white", command=self.show_transaction_history)  
        self.button_history.pack(pady=10)

        self.button_logout = tk.Button(self.main_frame, text="Logout", font=("Arial", 14), bg="#c9184a", fg="white", command=self.logout)  
        self.button_logout.pack(pady=10)

    def deposit_money(self):
        """Prompt user to enter deposit amount and update account."""
        amount = self.get_amount("Enter amount to deposit:")
        if amount:
            if self.current_account.deposit(amount):
                messagebox.showinfo("Success", f"Successfully deposited: ₹{amount:.2f}")
                self.show_balance()  
            else:
                messagebox.showerror("Error", "Invalid deposit amount.")

    def withdraw_money(self):
        """Prompt user to enter withdrawal amount and update account."""
        amount = self.get_amount("Enter amount to withdraw:")
        if amount:
            if self.current_account.withdraw(amount):
                messagebox.showinfo("Success", f"Successfully withdrew: ₹{amount:.2f}")
                self.show_balance()  
            else:
                messagebox.showerror("Error", "Invalid withdrawal amount or insufficient funds.")


    def show_balance(self):
        """Display the current balance."""
        balance = self.current_account.get_balance()
        messagebox.showinfo("Balance", f"Your balance is: ₹{balance:.2f}")

    def show_transaction_history(self):
        """Display transaction history."""
        history = self.current_account.get_transaction_history()
        history_message = "\n".join(history) if history else "No transactions available."
        messagebox.showinfo("Transaction History", history_message)

    def logout(self):
        """Logout the user and return to the welcome screen."""
        self.current_account = None
        self.create_welcome_screen()

    def create_cardless_transaction_screen(self):
        """Create the cardless transaction screen."""
        self.clear_screen()

        self.label_cardless = tk.Label(self.main_frame, text="Cardless Transactions", font=("Arial", 24, "bold"), bg="white")
        self.label_cardless.pack(pady=20)

        # Login Button
        self.button_login_account = tk.Button(self.main_frame, text="Login", font=("Arial", 14), bg="#02c39a", fg="white", command=self.show_login_form)  
        self.button_login_account.pack(pady=10)

        # Create Account Button
        self.button_create_account = tk.Button(self.main_frame, text="Create Account", font=("Arial", 14), bg="#028090", fg="white", command=self.show_create_account_form)  
        self.button_create_account.pack(pady=10)

        # Back Button
        self.button_back = tk.Button(self.main_frame, text="Back to Main Menu", font=("Arial", 14), bg="#c9184a", fg="white", command=self.create_welcome_screen)  
        self.button_back.pack(pady=10)

    def show_login_form(self):
        """Show the login form for existing accounts."""
        self.clear_screen()

        self.label_login = tk.Label(self.main_frame, text="Login", font=("Arial", 24, "bold"), bg="white")
        self.label_login.pack(pady=20)

        # Input fields for logging in
        self.label_login_account_number = tk.Label(self.main_frame, text="Account Number:", bg="white")
        self.label_login_account_number.pack(pady=5)
        self.entry_login_account_number = tk.Entry(self.main_frame)
        self.entry_login_account_number.pack(pady=5)

        self.label_login_pin = tk.Label(self.main_frame, text="PIN:", bg="white")
        self.label_login_pin.pack(pady=5)
        self.entry_login_pin = tk.Entry(self.main_frame, show="*")
        self.entry_login_pin.pack(pady=5)

        # Login button
        self.button_login_account = tk.Button(self.main_frame, text="Login", font=("Arial", 14), bg="#02c39a", fg="white", command=self.login_account)
        self.button_login_account.pack(pady=10)

        # Back Button
        self.button_back = tk.Button(self.main_frame, text="Back", font=("Arial", 14), bg="#c9184a", fg="white", command=self.create_cardless_transaction_screen)  
        self.button_back.pack(pady=10)

    def show_create_account_form(self):
        """Show the form to create a new account."""
        self.clear_screen()

        self.label_create_account = tk.Label(self.main_frame, text="Create Account", font=("Arial", 24, "bold"), bg="white")
        self.label_create_account.pack(pady=20)

        # Input fields for creating an account
        self.label_first_name = tk.Label(self.main_frame, text="First Name:", bg="white")
        self.label_first_name.pack(pady=5)
        self.entry_first_name = tk.Entry(self.main_frame)
        self.entry_first_name.pack(pady=5)

        self.label_last_name = tk.Label(self.main_frame, text="Last Name:", bg="white")
        self.label_last_name.pack(pady=5)
        self.entry_last_name = tk.Entry(self.main_frame)
        self.entry_last_name.pack(pady=5)

        self.label_age = tk.Label(self.main_frame, text="Age:", bg="white")
        self.label_age.pack(pady=5)
        self.entry_age = tk.Entry(self.main_frame)
        self.entry_age.pack(pady=5)

        self.label_pin = tk.Label(self.main_frame, text="Set a PIN:", bg="white")
        self.label_pin.pack(pady=5)
        self.entry_pin = tk.Entry(self.main_frame, show="*")
        self.entry_pin.pack(pady=5)

        # Create account button
        self.button_create_account = tk.Button(self.main_frame, text="Create Account", font=("Arial", 14), bg="#02c39a", fg="white", command=self.create_account)
        self.button_create_account.pack(pady=10)

        # Back Button
        self.button_back = tk.Button(self.main_frame, text="Back", font=("Arial", 14), bg="#F44336", fg="white", command=self.create_cardless_transaction_screen)  
        self.button_back.pack(pady=10)

    def create_account(self):
        """Create a new account."""
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        age = self.entry_age.get()
        pin = self.entry_pin.get()

        # Check if age is a valid number and greater than 18
        try:
            age = int(age)
            if age < 18:
                messagebox.showerror("Error", "Age must be 18 or older to create an account.")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid age.")
            return

        if first_name and last_name and pin:
            account_number = str(random.randint(100000, 999999))
            self.accounts[account_number] = Account(account_number, pin)
            messagebox.showinfo("Account Created", f"Account created successfully!\nAccount Number: {account_number}")

            # Wait for 2 seconds and return to cardless transactions
            self.root.after(1000, self.create_cardless_transaction_screen)  # Go back after 2 seconds
            self.clear_account_creation_fields()  # Clear fields after creating an account
        else:
            messagebox.showerror("Error", "All fields must be filled.")

    def clear_account_creation_fields(self):
        """Clear the fields for account creation."""
        self.entry_first_name.delete(0, tk.END)
        self.entry_last_name.delete(0, tk.END)
        self.entry_age.delete(0, tk.END)
        self.entry_pin.delete(0, tk.END)

    def login_account(self):
        """Login to an existing account."""
        account_number = self.entry_login_account_number.get()
        pin = self.entry_login_pin.get()

        if account_number in self.accounts and self.accounts[account_number].pin == pin:
            self.current_account = self.accounts[account_number]
            self.create_main_menu()
        else:
            messagebox.showerror("Error", "Invalid Account Number or PIN.")
            self.clear_login_fields()  # Clear fields after unsuccessful login

    def clear_login_fields(self):
        """Clear the fields for login."""
        self.entry_login_account_number.delete(0, tk.END)
        self.entry_login_pin.delete(0, tk.END)

    def get_amount(self, prompt):
        """Prompt the user to enter an amount."""
        amount_str = simpledialog.askstring("Input", prompt)
        try:
            return float(amount_str)
        except (ValueError, TypeError):
            messagebox.showerror("Error", "Invalid amount entered.")
            return None

    def clear_screen(self):
        """Clear the main frame."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
