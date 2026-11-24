# ==============================================================================
# Project Title       : ATM Transaction Sequence Simulation (Desktop GUI Edition)
# Case Study Number   : 13
# Course              : Introduction to Python Programming
# Description         : An interactive Desktop GUI simulation of the ATM Terminal
#                       built using Python's standard tkinter library.
# ==============================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ATMApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Citizens State Bank - ATM Terminal (Case Study 13)")
        self.root.geometry("820x680")
        self.root.minsize(760, 620)
        self.root.configure(bg="#0f172a")

        # Business Logic Constants
        self.INITIAL_BALANCE = 1000.00
        self.WITHDRAWAL_LIMIT = 500.00

        # Account State Variables
        self.current_balance = self.INITIAL_BALANCE
        self.total_deposit_amount = 0.00
        self.total_withdrawal_amount = 0.00
        self.total_deposit_count = 0
        self.total_withdrawal_count = 0
        self.transaction_history = []

        self.setup_ui()
        self.update_display()

    def setup_ui(self):
        # Header Frame
        header = tk.Frame(self.root, bg="#1e293b", pady=12, padx=20)
        header.pack(fill="x")

        title_lbl = tk.Label(
            header,
            text="CITIZENS STATE BANK - ATM TERMINAL",
            font=("Segoe UI", 16, "bold"),
            fg="#10b981",
            bg="#1e293b"
        )
        title_lbl.pack(anchor="w")

        sub_lbl = tk.Label(
            header,
            text="Case Study 13 • Transaction Sequence Simulator",
            font=("Segoe UI", 10),
            fg="#94a3b8",
            bg="#1e293b"
        )
        sub_lbl.pack(anchor="w")

        # Main Content Frame
        main_frame = tk.Frame(self.root, bg="#0f172a", padx=20, pady=15)
        main_frame.pack(fill="both", expand=True)

        # Upper HUD Cards
        hud_frame = tk.Frame(main_frame, bg="#0f172a")
        hud_frame.pack(fill="x", pady=(0, 15))

        self.card_bal = self.create_hud_card(hud_frame, "CURRENT BALANCE", "$1,000.00", "#10b981")
        self.card_bal.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.card_limit = self.create_hud_card(hud_frame, "WITHDRAWAL LIMIT", "$500.00", "#38bdf8")
        self.card_limit.pack(side="left", fill="x", expand=True, padx=4)

        self.card_count = self.create_hud_card(hud_frame, "TRANSACTIONS", "0", "#f59e0b")
        self.card_count.pack(side="left", fill="x", expand=True, padx=(8, 0))

        # Middle Grid: Left Actions & Right History List
        content_grid = tk.Frame(main_frame, bg="#0f172a")
        content_grid.pack(fill="both", expand=True)

        # Left Action Panel
        action_box = tk.LabelFrame(
            content_grid,
            text=" ATM OPERATIONS ",
            font=("Segoe UI", 11, "bold"),
            fg="#e2e8f0",
            bg="#1e293b",
            padx=15,
            pady=15
        )
        action_box.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Amount Entry Field
        amt_lbl = tk.Label(action_box, text="Transaction Amount ($):", font=("Segoe UI", 10, "bold"), fg="#cbd5e1", bg="#1e293b")
        amt_lbl.pack(anchor="w", pady=(0, 4))

        self.amount_var = tk.StringVar()
        self.amt_entry = tk.Entry(
            action_box,
            textvariable=self.amount_var,
            font=("Consolas", 15, "bold"),
            bg="#0f172a",
            fg="#f8fafc",
            insertbackground="#10b981",
            relief="flat",
            highlightthickness=1,
            highlightbackground="#475569"
        )
        self.amt_entry.pack(fill="x", ipady=6, pady=(0, 15))
        self.amt_entry.focus()

        # Operational Buttons
        btn_deposit = tk.Button(
            action_box,
            text="[1] Deposit Funds",
            font=("Segoe UI", 10, "bold"),
            bg="#059669",
            fg="white",
            activebackground="#047857",
            relief="flat",
            cursor="hand2",
            command=self.handle_deposit
        )
        btn_deposit.pack(fill="x", ipady=8, pady=4)

        btn_withdraw = tk.Button(
            action_box,
            text="[2] Withdraw Funds",
            font=("Segoe UI", 10, "bold"),
            bg="#0284c7",
            fg="white",
            activebackground="#0369a1",
            relief="flat",
            cursor="hand2",
            command=self.handle_withdraw
        )
        btn_withdraw.pack(fill="x", ipady=8, pady=4)

        btn_balance = tk.Button(
            action_box,
            text="[3] Check Account Balance",
            font=("Segoe UI", 10),
            bg="#334155",
            fg="#f1f5f9",
            activebackground="#475569",
            relief="flat",
            cursor="hand2",
            command=self.handle_check_balance
        )
        btn_balance.pack(fill="x", ipady=6, pady=4)

        btn_summary = tk.Button(
            action_box,
            text="[5] Exit & Generate Final Summary",
            font=("Segoe UI", 10, "bold"),
            bg="#e11d48",
            fg="white",
            activebackground="#be123c",
            relief="flat",
            cursor="hand2",
            command=self.handle_summary
        )
        btn_summary.pack(fill="x", ipady=8, pady=(15, 4))

        # Right History Listbox
        hist_box = tk.LabelFrame(
            content_grid,
            text=" TRANSACTION AUDIT LOG ",
            font=("Segoe UI", 11, "bold"),
            fg="#e2e8f0",
            bg="#1e293b",
            padx=10,
            pady=10
        )
        hist_box.pack(side="right", fill="both", expand=True)

        scrollbar = tk.Scrollbar(hist_box)
        scrollbar.pack(side="right", fill="y")

        self.history_listbox = tk.Listbox(
            hist_box,
            font=("Consolas", 9),
            bg="#0f172a",
            fg="#e2e8f0",
            selectbackground="#334155",
            selectforeground="#38bdf8",
            relief="flat",
            yscrollcommand=scrollbar.set
        )
        self.history_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.history_listbox.yview)

        # Status / Message Banner
        self.status_var = tk.StringVar(value="Ready. Welcome to Citizens State Bank ATM.")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Segoe UI", 9),
            fg="#94a3b8",
            bg="#020617",
            padx=15,
            pady=6,
            anchor="w"
        )
        status_bar.pack(fill="x", side="bottom")

    def create_hud_card(self, parent, title, initial_val, color):
        frame = tk.Frame(parent, bg="#1e293b", padx=15, pady=10, highlightthickness=1, highlightbackground="#334155")
        lbl_title = tk.Label(frame, text=title, font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#1e293b")
        lbl_title.pack(anchor="w")
        lbl_val = tk.Label(frame, text=initial_val, font=("Consolas", 14, "bold"), fg=color, bg="#1e293b")
        lbl_val.pack(anchor="w", pady=(2, 0))
        frame.val_label = lbl_val
        return frame

    def update_display(self):
        self.card_bal.val_label.config(text=f"${self.current_balance:,.2f}")
        self.card_count.val_label.config(text=str(len(self.transaction_history)))
        self.amount_var.set("")
        self.amt_entry.focus()

    def get_parsed_amount(self):
        val_str = self.amount_var.get().strip()
        if not val_str:
            messagebox.showerror("Input Error", "Please enter a transaction amount.")
            return None
        try:
            amt = float(val_str)
            return amt
        except ValueError:
            messagebox.showerror("Invalid Input", "Transaction amount must be a valid numeric quantity.")
            return None

    def handle_deposit(self):
        amount = self.get_parsed_amount()
        if amount is None:
            return

        if amount <= 0:
            messagebox.showerror("Transaction Rejected", "Deposit amount must be greater than $0.00.")
            self.status_var.set("Rejected: Deposit amount must be greater than $0.00.")
            return

        self.current_balance += amount
        self.total_deposit_amount += amount
        self.total_deposit_count += 1

        log_entry = f"Deposit    | +${amount:>7.2f} | Balance: ${self.current_balance:>8.2f}"
        self.transaction_history.append(log_entry)
        self.history_listbox.insert("end", f"[{len(self.transaction_history)}] {log_entry}")
        self.history_listbox.see("end")

        self.status_var.set(f"Success: Deposited ${amount:.2f}. Updated Balance: ${self.current_balance:.2f}")
        messagebox.showinfo("Deposit Confirmed", f"${amount:.2f} deposited successfully.\nNew Balance: ${self.current_balance:.2f}")
        self.update_display()

    def handle_withdraw(self):
        amount = self.get_parsed_amount()
        if amount is None:
            return

        if amount <= 0:
            messagebox.showerror("Transaction Rejected", "Withdrawal amount must be greater than $0.00.")
            self.status_var.set("Rejected: Withdrawal amount must be greater than $0.00.")
            return

        if amount > self.WITHDRAWAL_LIMIT:
            messagebox.showerror("Transaction Rejected", f"Exceeds maximum limit of ${self.WITHDRAWAL_LIMIT:.2f} per transaction.")
            self.status_var.set(f"Rejected: Requested ${amount:.2f} exceeds limit of ${self.WITHDRAWAL_LIMIT:.2f}.")
            return

        if amount > self.current_balance:
            messagebox.showerror("Transaction Rejected", f"Insufficient funds.\nAvailable: ${self.current_balance:.2f}\nRequested: ${amount:.2f}")
            self.status_var.set(f"Rejected: Insufficient funds (Available: ${self.current_balance:.2f}).")
            return

        self.current_balance -= amount
        self.total_withdrawal_amount += amount
        self.total_withdrawal_count += 1

        log_entry = f"Withdrawal | -${amount:>7.2f} | Balance: ${self.current_balance:>8.2f}"
        self.transaction_history.append(log_entry)
        self.history_listbox.insert("end", f"[{len(self.transaction_history)}] {log_entry}")
        self.history_listbox.see("end")

        self.status_var.set(f"Success: Withdrew ${amount:.2f}. Remaining Balance: ${self.current_balance:.2f}")
        messagebox.showinfo("Withdrawal Confirmed", f"${amount:.2f} dispensed successfully.\nRemaining Balance: ${self.current_balance:.2f}")
        self.update_display()

    def handle_check_balance(self):
        msg = f"Account Inquiry:\n\nAvailable Balance: ${self.current_balance:.2f}\nPer-Transaction Limit: ${self.WITHDRAWAL_LIMIT:.2f}"
        self.status_var.set(f"Balance Inquiry: ${self.current_balance:.2f}")
        messagebox.showinfo("Account Balance", msg)

    def handle_summary(self):
        net_change = self.total_deposit_amount - self.total_withdrawal_amount
        summary_text = (
            "==================================================\n"
            "          FINAL ATM TRANSACTION SUMMARY           \n"
            "==================================================\n"
            f"Initial Starting Balance  : ${self.INITIAL_BALANCE:.2f}\n"
            f"Total Deposits ({self.total_deposit_count:>2})       : +${self.total_deposit_amount:.2f}\n"
            f"Total Withdrawals ({self.total_withdrawal_count:>2})    : -${self.total_withdrawal_amount:.2f}\n"
            f"Net Balance Adjustment    : ${net_change:+.2f}\n"
            f"Final Ending Balance      : ${self.current_balance:.2f}\n"
            "--------------------------------------------------\n"
            f"Total Transactions Logged : {len(self.transaction_history)}\n"
            "==================================================\n\n"
            "Thank you for banking with Citizens State Bank. Goodbye!"
        )

        confirm = messagebox.askyesno("Exit Confirmation", summary_text + "\n\nWould you like to close the ATM session?")
        if confirm:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ATMApp(root)
    root.mainloop()
