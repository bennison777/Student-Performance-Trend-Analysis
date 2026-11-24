# ==============================================================================
# Project Title       : ATM Transaction Sequence Simulation
# Case Study Number   : 13
# Course              : Introduction to Python Programming
# Description         : A menu-driven ATM transaction simulation for a single
#                       bank account, demonstrating control structures, loops,
#                       lists, and basic I/O without functions or classes.
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. INITIAL SYSTEM CONFIGURATION & STATE VARIABLES
# ------------------------------------------------------------------------------
INITIAL_BALANCE = 1000.00       # Starting account balance in dollars
WITHDRAWAL_LIMIT = 500.00      # Maximum allowed withdrawal per transaction

current_balance = INITIAL_BALANCE
total_deposit_amount = 0.00
total_withdrawal_amount = 0.00
total_deposit_count = 0
total_withdrawal_count = 0

# List to record transaction audit strings
transaction_history = []

is_running = True

# ------------------------------------------------------------------------------
# 2. MAIN APPLICATION LOOP (MENU-DRIVEN INTERACTION)
# ------------------------------------------------------------------------------
print("==================================================")
print("     WELCOME TO THE CITIZENS STATE BANK ATM       ")
print("==================================================")
print("Account Initialized with Balance : $" + "{:.2f}".format(current_balance))
print("Per-Transaction Withdrawal Limit : $" + "{:.2f}".format(WITHDRAWAL_LIMIT))
print("==================================================")

while is_running:
    print("\n----------------- ATM MAIN MENU ------------------")
    print("1. Deposit Funds")
    print("2. Withdraw Funds")
    print("3. Check Account Balance")
    print("4. View Transaction History")
    print("5. Exit & Generate Final Summary")
    print("--------------------------------------------------")
    
    user_choice = input("Enter your choice (1-5): ").strip()
    
    # --------------------------------------------------------------------------
    # OPTION 1: DEPOSIT FUNDS
    # --------------------------------------------------------------------------
    if user_choice == "1":
        print("\n--- DEPOSIT FUNDS ---")
        deposit_input = input("Enter amount to deposit ($): ")
        deposit_amount = float(deposit_input)
        
        # Validation: Amount must be strictly positive
        if deposit_amount <= 0:
            print("Transaction Rejected: Deposit amount must be greater than $0.00.")
        else:
            current_balance = current_balance + deposit_amount
            total_deposit_amount = total_deposit_amount + deposit_amount
            total_deposit_count = total_deposit_count + 1
            
            # Format and record the transaction log entry
            log_entry = "Deposit     | Amount: +$" + "{:.2f}".format(deposit_amount) + " | Balance: $" + "{:.2f}".format(current_balance)
            transaction_history.append(log_entry)
            
            print("Transaction Successful: Deposited $" + "{:.2f}".format(deposit_amount))
            print("Updated Balance: $" + "{:.2f}".format(current_balance))
            
    # --------------------------------------------------------------------------
    # OPTION 2: WITHDRAW FUNDS
    # --------------------------------------------------------------------------
    elif user_choice == "2":
        print("\n--- WITHDRAW FUNDS ---")
        withdrawal_input = input("Enter amount to withdraw ($): ")
        withdrawal_amount = float(withdrawal_input)
        
        # Validation 1: Amount must be strictly positive
        if withdrawal_amount <= 0:
            print("Transaction Rejected: Withdrawal amount must be greater than $0.00.")
        # Validation 2: Amount must not exceed the per-transaction limit
        elif withdrawal_amount > WITHDRAWAL_LIMIT:
            print("Transaction Rejected: Exceeds maximum limit of $" + "{:.2f}".format(WITHDRAWAL_LIMIT) + " per transaction.")
        # Validation 3: Amount must not exceed the available balance
        elif withdrawal_amount > current_balance:
            print("Transaction Rejected: Insufficient funds.")
            print("Available Balance: $" + "{:.2f}".format(current_balance) + " | Requested: $" + "{:.2f}".format(withdrawal_amount))
        else:
            current_balance = current_balance - withdrawal_amount
            total_withdrawal_amount = total_withdrawal_amount + withdrawal_amount
            total_withdrawal_count = total_withdrawal_count + 1
            
            # Format and record the transaction log entry
            log_entry = "Withdrawal  | Amount: -$" + "{:.2f}".format(withdrawal_amount) + " | Balance: $" + "{:.2f}".format(current_balance)
            transaction_history.append(log_entry)
            
            print("Transaction Successful: Withdrew $" + "{:.2f}".format(withdrawal_amount))
            print("Updated Balance: $" + "{:.2f}".format(current_balance))
            
    # --------------------------------------------------------------------------
    # OPTION 3: CHECK ACCOUNT BALANCE
    # --------------------------------------------------------------------------
    elif user_choice == "3":
        print("\n--- ACCOUNT BALANCE INQUIRY ---")
        print("Current Available Balance: $" + "{:.2f}".format(current_balance))
        print("Per-Transaction Withdrawal Limit: $" + "{:.2f}".format(WITHDRAWAL_LIMIT))
        
    # --------------------------------------------------------------------------
    # OPTION 4: VIEW TRANSACTION HISTORY
    # --------------------------------------------------------------------------
    elif user_choice == "4":
        print("\n--- TRANSACTION HISTORY LOG ---")
        if len(transaction_history) == 0:
            print("No transactions recorded in this session yet.")
        else:
            print("No. | Type        | Details")
            print("--------------------------------------------------")
            item_number = 1
            for record in transaction_history:
                print(str(item_number) + ".  | " + record)
                item_number = item_number + 1
            print("--------------------------------------------------")
            print("Total Transactions Logged: " + str(len(transaction_history)))
            
    # --------------------------------------------------------------------------
    # OPTION 5: EXIT & GENERATE FINAL TRANSACTION SUMMARY
    # --------------------------------------------------------------------------
    elif user_choice == "5":
        print("\n==================================================")
        print("          FINAL ATM TRANSACTION SUMMARY           ")
        print("==================================================")
        print("Initial Starting Balance  : $" + "{:.2f}".format(INITIAL_BALANCE))
        print("Total Successful Deposits : " + str(total_deposit_count) + " (Sum: $" + "{:.2f}".format(total_deposit_amount) + ")")
        print("Total Successful Withdraws: " + str(total_withdrawal_count) + " (Sum: $" + "{:.2f}".format(total_withdrawal_amount) + ")")
        print("Net Balance Adjustment    : $" + "{:.2f}".format(total_deposit_amount - total_withdrawal_amount))
        print("Final Ending Balance      : $" + "{:.2f}".format(current_balance))
        print("--------------------------------------------------")
        print("AUDIT TRAIL:")
        if len(transaction_history) == 0:
            print("No transactions executed during this session.")
        else:
            audit_index = 1
            for record in transaction_history:
                print("  [" + str(audit_index) + "] " + record)
                audit_index = audit_index + 1
        print("==================================================")
        print("Thank you for banking with Citizens State Bank. Goodbye!")
        print("==================================================")
        
        # Terminate the loop
        is_running = False
        
    # --------------------------------------------------------------------------
    # INVALID MENU CHOICE
    # --------------------------------------------------------------------------
    else:
        print("Invalid Selection: '" + user_choice + "' is not a recognized option.")
        print("Please enter a numeric option between 1 and 5.")
