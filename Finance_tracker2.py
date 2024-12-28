import json
import datetime
import tkinter as tk
from GUI import FinanceTrackerGUI


# Global list to store transactions
transaction = {}


# File handling functions

# function to load data from the JSONfile
def load_transactions(filename):
    global transaction # dictionary is made global to access outside the function

    try:
        with open(f"{filename}", "r") as file:
            transaction = json.load(file)
            return transaction

    except FileNotFoundError:
        print("Saved transaction file does not exist:Adding new transaction")
    except json.JSONDecodeError:
        print("Error decoding existing JSON file\n")


# funtion to save data to the JSON file
def save_transactions(filename):
    with open(f"{filename}", "w") as file:
        json.dump(transaction, file, indent=2)

#function to read bulk transactions
def read_bulk_transactions_from_file(filename):
    load_transactions("text.json")
    transactions = []  # Temporary list to store transactions

    with open(filename, 'r') as file:
        for data in file:
            transaction_from_file = data.strip().split(',')

            T_category = transaction_from_file[0].strip().lower()  # Transaction category
            T_amount = transaction_from_file[1].strip()  # Transaction amount
            T_date = transaction_from_file[2].strip()  # Transaction date
            T_status = transaction_from_file[3].strip() # Transaction status

            details = {"amount": int(T_amount), "date": T_date,"status":T_status}  # Create a dictionary with the transaction details

            if T_category in transaction:
                transaction[T_category].append(details)
            else:
                transaction[T_category] = [details]

            transactions.append(data)  # Add the transaction to the temporary list

    # Save transactions to JSON file
    save_transactions("transactions.json")

    # Truncate the file to clear its content
    with open(filename, 'w') as file:
        pass

    return transactions  # Return transactions


# function to error handle integer and float input
def user_input(data_type, message, error):
    while True:
        try:
            value = data_type(input(message))
            return value
        except ValueError:
            print(error)


# get information on user data on transactions
def add_transaction():
    # temporary list to add information
    temp_transactions = []

    while True:
        choice = input("Do you want to enter bulk transaction:(yes/no)").lower() #prompting the user to add bulk transction or not
        if choice == "yes":
            print("""Enter the bulk transactions in the "bulk_transactions.txt" text file 
                     according to the below format

                     transaction type,amount,date,income/expense

                     (eg:salary,230000,2023/03/03,income)

                  """)
            read_bulk_transactions_from_file("bulk_transaction.txt")
            break
        elif choice == "no":
            while True:
                category = input("Category of the transaction:")
                if category == "":
                    print("Invalid Input:enter a category")
                else:
                    break
            #error handling the amount
            amount = user_input(int, "Enter the amount: ", "Invalid input. Please enter an integer.")

            #Error handling to check if user has properly enterd income or expense
            while True:
                type = input("Type of transaction (Income or Expense):").lower()
                if type == "income" or type == "expense":
                    break
                else:
                    print("Invalid Input")
            #Error handling the date to check for proper format
            while True:
                date = input("Enter the date YYYY/MM/DD: ")
                if date == " ":
                    print("Invalid input:Enter a date")
                else:
                    try:
                        temp_date = datetime.datetime.strptime(date, "%Y/%m/%d")
                        format_date = temp_date.strftime("%Y/%m/%d")
                        break
                    except ValueError:
                        print("Invalid input:please enter format")

            #appending the data into temporary list
            temp_transactions.append(category)
            temp_transactions.append(amount)
            temp_transactions.append(format_date)
            temp_transactions.append(type)

            load_transactions("transactions.json")

            #capturing the keys of the dictionary
            for keys in transaction.keys():

                if keys == temp_transactions[0]: #checking if the key is similar to the transacton type

                    transaction[keys].append({
                        "amount": temp_transactions[1],
                        "date": temp_transactions[2],
                        "status": temp_transactions[3]
                    })

                    save_transactions("transactions.json")
                    temp_transactions.clear() #clearing the temporary list


                elif keys != temp_transactions[0]:
                    transaction[temp_transactions[0]] = []
                    transaction[temp_transactions[0]].append({
                        "amount": temp_transactions[1],
                        "date": temp_transactions[2],
                        "status": temp_transactions[3]
                    })
                save_transactions("transactions.json")
                temp_transactions.clear()

            break
        else:
            print("Invalid Input:Please enter yes or no")

#functiont to veiw transactions
def view_transaction():

    # Create a root window for the GUI
    root = tk.Tk()

    # Create an instance of the FinanceTrackerGUI class
    app = FinanceTrackerGUI(root)

    # Display transactions using the GUI
    app.display_transactions(transaction)

    # Start the GUI main loop
    root.mainloop()

    

#function to update the transactions
def update_transaction():


    choice = ""
    load_transactions("transactions.json")
    if len(transaction) == 0:
        print("Invalid input:Add a transaction to update")
        return
    else:
        print(json.dumps(transaction, indent=4))

        while True:
            choice = input("Enter the transaction type to be update:")

            #getting the transactions under the user choice
            transaction_info = transaction.get(choice)
            if transaction_info == "":
                print("Invalid input:Please enter a transaction type")
            else:
                #displaying the transactions as groups
                for i in range(len(transaction_info)):
                    print(f"group{i + 1}:", transaction_info[i])
                    print()
                while True:

                    #Taking the user in[ut on the uopdate group
                    update_group = user_input(int, "Enter the transaction group: ", "Invalid input. Please enter an integer.")
                    if 1 <= update_group <= len(transaction_info):
                        while True:

                            #updating the amount
                            update_value = input("Enter the value to be updated(Eg:amount):")
                            if update_value == "amount":
                                updated_amount = user_input(int, "Enter the amount: ",
                                                            "Invalid input. Please enter an integer.")
                                transaction_info[0][update_value] = updated_amount

                                transaction[choice]=transaction_info

                                save_transactions("transactions.json")

                                break
                            #updating the date
                            elif update_value == "date":
                                while True:
                                    updated_date = input("Enter the updated date YYYY/MM/DD: ")
                                    try:
                                        temp_date = datetime.datetime.strptime(updated_date, "%Y/%m/%d")
                                        format_date = temp_date.strftime("%Y/%m/%d")
                                        break
                                    except ValueError:
                                        print("please enter format")
                                transaction_info[0][update_value] = format_date
                                transaction[choice] = transaction_info

                                save_transactions("transactions.json")
                                break
                             #updating thes status
                            elif update_value == "status":
                                updated_status= (input("Enter the type(Income or Expense):")).lower()
                                if updated_status == "income" or updated_status == "expense":
                                    transaction_info[0][update_value] = updated_status
                                    transaction[choice] = transaction_info

                                    save_transactions("transactions.json")
                                    break
                                else:
                                    print("Invalid input:please enter income or expense")
                            else:
                                print("Invalid value to update ")
                        break
                    else:
                        print("Invalid input:Enter a valid transaction group")
                break

#function to delete transctions
def delete_transaction():
    load_transactions("transactions.json")

    if len(transaction) == 0:
        print("Invalid input:Add a transaction to delete")
        return
    else:
        print(json.dumps(transaction, indent=4))

        while True:
            choice = input("Enter the transaction type to be update:")

            transaction_info = transaction.get(choice)
            if transaction_info == "":
                print("Invalid input:Please enter a transaction type")
            else:

                for i in range(len(transaction_info)):
                    print(f"group{i + 1}:", transaction_info[i])
                    print()
                while True:

                    #getting the user input to delete the transaction
                    transaction_remove = user_input(int, "Enter the transaction group: ","Invalid input. Please enter an integer.")
                    if 1 <= transaction_remove <= len(transaction_info):
                        del transaction_info[transaction_remove - 1]
                        save_transactions("transactions.json")

                    #checking wether the user want to continue delete transactions
                    while True:
                        continue_delete = input("Do you wish to continue delete transactions(Yes/No):").lower()
                        if continue_delete == "yes":
                            delete_transaction()
                        elif continue_delete == "no":
                            print("transactions are deleted")

                            break
                        else:
                            print("Invalid input:Enter a valid transaction group")
                        break
                    break
                break

#trnasction to display the summary
def display_summary():

    load_transactions("transactions.json")
    if len(transaction) == 0:
        print("Invalid input:Add a transaction to get the summary")
        return
    else:

        total_expense = 0
        total_income = 0
        # check transaction is income or expense within index
        for keys in transaction:# capture the keys from the dictionary

            for values in transaction[keys]:#capture the coreponding values of the keys

                # checking weather the status is income or expense
                if (values["status"]) == "income":
                    total_income = total_income + (values["amount"])
                    continue
                elif (values["status"]) == "expense":
                    total_expense = total_expense + (values["amount"])
                    continue
                else:
                    continue
                break
        print(f"\nTotal Income is : {total_income}")
        print(f"Total Expense is : {total_expense}")
        profit = total_income - total_expense
        if profit > 0:
            print(f"\nYour net income (profit) is : {profit}")
        else:
            print(f"\nYour net loss (loss) is : {profit}")


def main_menu():
    load_transactions("transactions.json")
    while True:
        print("""
        Personal Finance Tracker
        1. Add Transaction
        2. View Transactions
        3. Update Transaction
        4. Delete Transaction
        5. Display Summary
        6. Exit
                    """)
        choice = input("Enter your choice: ")

        if choice == "1":
            add_transaction()
        elif choice == "2":
            view_transaction()
        elif choice == "3":
            update_transaction()
        elif choice == "4":
            delete_transaction()
        elif choice == "5":
            display_summary()
        elif choice == "6":
            print("Program ended")
            break
        else:
            print("Invalid input:try again")


if __name__ == "__main__":
    main_menu()


