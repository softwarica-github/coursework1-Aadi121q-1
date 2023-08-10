import unittest
import tkinter as tk
import tkinter.font as tkFont
import mysql.connector
from tkinter import Frame, Label, Entry, Button, messagebox

# MySQL database configuration
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "Aadi_@1a1",
    "database": "atm_console"
}

class cardHolder:
    def __init__(self, cardNum, pin, firstname, lastname, balance):
        self.cardNum = cardNum
        self.pin = pin
        self.firstname = firstname
        self.lastname = lastname
        self.balance = balance

    def get_firstname(self):
        return self.firstname

    def get_balance(self):
        return self.balance

    def set_balance(self, balance):
        self.balance = balance

class cardHolderApp:
    def __init__(self, root):
        self.root = root
        self.current_user = cardHolder("", "", "", "", "")

        # Create the login frame
        self.login_frame = Frame(root)
        self.login_frame.grid(row=0, column=0, padx=50, pady=50)

        self.custom_font = tkFont.Font(family="Helvetica", size=12)

        self.welcome_label = Label(self.login_frame, text="Welcome to the Card Holder App!")
        self.welcome_label.config(font=(self.custom_font, 14, "bold"), pady=10)
        self.welcome_label.grid(row=0, column=0, columnspan=2)

        self.debit_label = Label(self.login_frame, text="Debit Card Number:")
        self.debit_label.config(font=self.custom_font, pady=5)
        self.debit_label.grid(row=1, column=0, sticky="e")

        self.debit_entry = Entry(self.login_frame)
        self.debit_entry.config(font=self.custom_font)
        self.debit_entry.grid(row=1, column=1, padx=5, pady=5)

        self.pin_label = Label(self.login_frame, text="PIN:")
        self.pin_label.config(font=self.custom_font, pady=5)
        self.pin_label.grid(row=2, column=0, sticky="e")

        self.pin_entry = Entry(self.login_frame, show="*")
        self.pin_entry.config(font=self.custom_font)
        self.pin_entry.grid(row=2, column=1, padx=5, pady=5)

        self.login_button = Button(self.login_frame, text="Login", command=lambda: self.update_main_frame(self.login()))
        self.login_button.config(font=self.custom_font, padx=10)
        self.login_button.grid(row=3, column=0, columnspan=2, pady=5)

        # Create the main frame
        self.main_frame = Frame(root)
        self.main_frame.grid(row=0, column=0, padx=50, pady=50)
        self.main_frame.grid_remove()

        self.welcome_label = Label(self.main_frame, text="Welcome " + self.current_user.get_firstname() + ",")
        self.welcome_label.config(font=(self.custom_font, 14, "bold"), pady=10)
        self.welcome_label.grid(row=0, column=0, columnspan=2)

        self.deposit_label = Label(self.main_frame, text="Deposit Amount:")
        self.deposit_label.config(font=self.custom_font, pady=5)
        self.deposit_label.grid(row=1, column=0, sticky="e")

        self.deposit_entry = Entry(self.main_frame)
        self.deposit_entry.config(font=self.custom_font)
        self.deposit_entry.grid(row=1, column=1, padx=5, pady=5)

        self.deposit_button = Button(self.main_frame, text="Deposit", command=self.deposit)
        self.deposit_button.config(font=self.custom_font, padx=10)
        self.deposit_button.grid(row=2, column=0, columnspan=2, pady=5)

        self.withdraw_label = Label(self.main_frame, text="Withdraw Amount:")
        self.withdraw_label.config(font=self.custom_font, pady=5)
        self.withdraw_label.grid(row=3, column=0, sticky="e")

        self.withdraw_entry = Entry(self.main_frame)
        self.withdraw_entry.config(font=self.custom_font)
        self.withdraw_entry.grid(row=3, column=1, padx=5, pady=5)

        self.withdraw_button = Button(self.main_frame, text="Withdraw", command=self.withdraw)
        self.withdraw_button.config(font=self.custom_font, padx=10)
        self.withdraw_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.show_balance_button = Button(self.main_frame, text="Show Balance", command=self.check_balance)
        self.show_balance_button.config(font=self.custom_font, padx=10)
        self.show_balance_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.balance_label = Label(self.main_frame, text="")
        self.balance_label.config(font=self.custom_font, pady=10)
        self.balance_label.grid(row=6, column=0, columnspan=2)

        self.exit_button = Button(self.main_frame, text="Exit", command=root.quit)
        self.exit_button.config(font=self.custom_font, padx=10)
        self.exit_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(6, weight=1)

        self.root.geometry("400x400")
        self.root.minsize(300, 250)

        self.root.mainloop()

    def login(self):
        card_number = self.debit_entry.get().strip()
        pin = self.pin_entry.get().strip()

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            query = "SELECT * FROM card_holders WHERE cardNum = %s AND pin = %s"
            cursor.execute(query, (card_number, pin))
            matched_user = cursor.fetchone()

            cursor.close()
            conn.close()
            return matched_user
        except mysql.connector.Error as e:
            print("Error connecting to MySQL: ", e)
            messagebox.showerror("Error", "Error connecting to the database.")
            return None

    def update_main_frame(self, user_data):
        if user_data is not None:
            self.current_user = cardHolder(*user_data)
            self.welcome_label.config(text="Welcome " + self.current_user.get_firstname() + ",")
            self.login_frame.grid_remove()
            self.main_frame.grid()
            messagebox.showinfo("Login Successful", "Welcome, " + self.current_user.get_firstname() + "!")
        else:
            self.current_user = None
            self.login_frame.grid()
            self.main_frame.grid_remove()

    def deposit(self):
        if self.current_user is None:
            messagebox.showerror("Not Logged In", "Please log in before making a deposit.")
            return

        try:
            deposit_amount = float(self.deposit_entry.get())
            self.current_user.set_balance(self.current_user.get_balance() + deposit_amount)
            self.balance_label.config(text="Your new balance is: $" + str(self.current_user.get_balance()))
            messagebox.showinfo("Deposit", "Deposit successful! Your new balance is: $" + str(self.current_user.get_balance()))
            self.deposit_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid input")

    def withdraw(self):
        if self.current_user is None:
            messagebox.showerror("Not Logged In", "Please log in before making a withdrawal.")
            return

        try:
            withdraw_amount = float(self.withdraw_entry.get())
            if self.current_user.get_balance() < withdraw_amount:
                self.balance_label.config(text="Insufficient balance.")
                messagebox.showerror("Withdrawal", "Insufficient balance!")
            else:
                self.current_user.set_balance(self.current_user.get_balance() - withdraw_amount)
                self.balance_label.config(text="You are good to go!!! Thank you :)")
                messagebox.showinfo("Withdrawal", "Withdrawal successful! Your new balance is: $" + str(self.current_user.get_balance()))
            self.withdraw_entry.delete(0, 'end')
        except ValueError:
            messagebox.showerror("Invalid Input", "Invalid input")

    def check_balance(self):
        if self.current_user is None:
            messagebox.showerror("Not Logged In", "Please log in to check your balance.")
            return

        messagebox.showinfo("Balance", "Your current balance is: $" + str(self.current_user.get_balance()))

class TestCardHolderApp(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = cardHolderApp(self.root)
        self.app.grid(row=0, column=0, padx=50, pady=50)
        self.app.grid_remove()

    def tearDown(self):
        self.root.destroy()

    def test_login_successful(self):
        card_number = "1234567890123456"
        pin = "1234"

        # Mock database connection and fetch the user data
        with unittest.mock.patch('mysql.connector.connect') as mock_connect:
            mock_cursor = mock_connect.return_value.cursor.return_value
            mock_cursor.fetchone.return_value = ("TestFirstName", "TestLastName", 100.0)

            # Simulate user input
            self.app.debit_entry.insert(0, card_number)
            self.app.pin_entry.insert(0, pin)

            # Trigger the login function
            self.app.login()

            # Check if the main frame is visible and the welcome message is correct
            self.assertTrue(self.app.main_frame.winfo_ismapped())
            self.assertEqual(self.app.welcome_label.cget("text"), "Welcome TestFirstName,")

    def test_login_invalid_credentials(self):
        card_number = "9876543210987654"
        pin = "4321"

        # Mock database connection and return None for invalid credentials
        with unittest.mock.patch('mysql.connector.connect') as mock_connect:
            mock_cursor = mock_connect.return_value.cursor.return_value
            mock_cursor.fetchone.return_value = None

            # Simulate user input
            self.app.debit_entry.insert(0, card_number)
            self.app.pin_entry.insert(0, pin)

            # Trigger the login function
            self.app.login()

            # Check if the login frame is still visible and an error message is shown
            self.assertTrue(self.app.login_frame.winfo_ismapped())
            self.assertEqual(self.app.welcome_label.cget("text"), "Welcome to the Card Holder App!")
            self.assertTrue(messagebox.showerror.called_with("Invalid Credentials", "Invalid card number or PIN."))

if __name__ == "__main__":
    unittest.main()
