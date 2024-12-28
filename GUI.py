import tkinter as tk
from tkinter import ttk
import json
from tkinter import messagebox


class FinanceTrackerGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("Personal Finance Tracker")
        self.root.geometry("500x500")

        self.transactions = self.load_transactions("transactions.json")
        self.create_widgets()

    def create_widgets(self):
        global mytree,search_entry,search_var


        # Frame for table and scrollbar


        frame = tk.Frame(self.root, borderwidth=2, relief="ridge")
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Treeview for displaying transactions
        mytree = ttk.Treeview(frame)

        # Vertical Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=mytree.yview)
        scrollbar.pack(side="right", fill="y")

        # Configure Treeview to use the scrollbar
        mytree.configure(yscrollcommand=scrollbar.set)



        # Initialize columns
        mytree["columns"] = ("type", "amount", "date", "status")

        # Hide the default index column
        mytree["show"] = "headings"

        # Format columns
        mytree.column("#0", width=0, stretch=tk.NO)  #Hiding the default column
        mytree.column("type", anchor="w", width=120)
        mytree.column("amount", anchor="center", width=120)
        mytree.column("date", anchor="center", width=120)
        mytree.column("status", anchor="center", width=120)

        # Headings for the columns

        mytree.heading("#0", text="", anchor="w")
        mytree.heading("type", text="type", anchor="w", command=lambda: self.sort_by_column("type", False))
        mytree.heading("amount", text="amount", anchor="center", command=lambda: self.sort_by_column("amount", False))
        mytree.heading("date", text="date", anchor="center", command=lambda: self.sort_by_column("date", False))
        mytree.heading("status", text="status", anchor="center", command=lambda: self.sort_by_column("status", False))

        # Scrollbar for the Treeview



        mytree.pack(fill="both", expand=True)#

        # Search bar and button

        search_label = tk.LabelFrame(frame, text="", font=("Helvetica", "8"))
        search_label.pack(padx=5, pady=5)

        self.search_var = tk.StringVar() # The data entered im the entry feild is stored
        search_entry = tk.Entry(search_label, textvariable=self.search_var)
        search_entry.grid(row=0, column=0, padx=5, pady=5)

        search_button = tk.Button(search_label, text="Search", command=self.search_transactions)#calling the search function with the button click
        search_button.grid(row=0, column=1, padx=5, pady=5)

        refresh_button = tk.Button(frame, text="Refresh", command=self.refresh_transactions)#transactions are refreshed by calling the refresh function
        refresh_button.pack(padx=10, pady=10)


    # Loading the JSON file
    def load_transactions(self, filename):

        try:
            with open(f"{filename}", "r") as file:
                transactions = json.load(file)
                return transactions

        except FileNotFoundError:
            messagebox.showinfo("Error", "The file is not found")
        except json.JSONDecodeError:
            messagebox.showinfo("Error", "Error decoding existing JSON file.")

    # Function to display the data in the treeveiw
    def display_transactions(self, transactions):

        # Add transactions to the treeview
        count = 0

        # for loop to get the keys and values from the dictionary
        for keys in transactions:
            for values in transactions[keys]:
                count += 1
                mytree.insert(parent="", index="end", iid=count, text="",
                              values=(keys, values["amount"], values["date"], values["status"]))
                mytree.pack()



    # function to search data in the treeveiw
    def search_transactions(self):

        data_tree = self.search_var.get().lower()

        found = False  # Flag to check if any match is found

        # deleting the data in the treeveiw
        for record in mytree.get_children():
            mytree.delete(record)

        # variable to keep the count of the iterations
        count = 0

        # for loop to get the keys and values from the dictionary
        for key, value_list in self.transactions.items():
            for value in value_list:

                # Entering the data to the treeveiw if the searched data exist in the dictionary
                if data_tree in str(value["date"]).lower() or \
                        data_tree in str(value["amount"]).lower() or \
                        data_tree in str(value["status"]).lower() or \
                        data_tree in key.lower():
                    count += 1
                    mytree.insert(parent="", index="end", iid=count, text="",
                                  values=(key, value["amount"], value["date"], value["status"]))
                    found = True  # Set the flag to True if a match is found
        if not found:
            messagebox.showinfo("Error", "The value is not in the database. Please try again.")

    #functrion to refresh the treeveiw after searching
    def refresh_transactions(self):
        # Clear the Treeview
        for record in mytree.get_children():
            mytree.delete(record)

        # Insert all transactions back
        self.display_transactions(self.transactions)

    #sort data in each of the column in the treeveiw
    def sort_by_column(self, col, reverse=False):
        # Get all the values in the column
        data = [(mytree.set(child, col), child) for child in mytree.get_children('')]

        # Sort the data
        data.sort(reverse=reverse)

        for index, (val, child) in enumerate(data):
            mytree.move(child, '', index)

        # Reverse the sorting order for next time
        mytree.heading(col, command=lambda _col=col: self.sort_by_column(_col, not reverse))


def main():
    root = tk.Tk()
    app = FinanceTrackerGUI(root) # Calling the class
    app.display_transactions(app.transactions)
    root.mainloop()


if __name__ == "__main__":
    main()
