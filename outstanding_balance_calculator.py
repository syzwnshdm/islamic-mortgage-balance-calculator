

import math
import argparse
import sys

def get_float_input(prompt):
    """Prompts the user for a float value and handles invalid input."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_int_input(prompt):
    """Prompts the user for an integer value and handles invalid input."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def calculate_outstanding_balance(principal, annual_rate, term_years, payments_made):
    """
    Calculates the monthly payment and outstanding balance of a loan.

    Args:
        principal (float): The original loan amount.
        annual_rate (float): The annual interest rate (as a percentage, e.g., 4.5).
        term_years (int): The total loan term in years.
        payments_made (int): The number of payments already made.

    Returns:
        (float, float): A tuple containing the monthly payment and the outstanding balance.
                         Returns (0, 0) if the loan is already paid off.
    """
    if principal <= 0:
        return 0, 0

    monthly_rate = (annual_rate / 100) / 12
    total_payments = term_years * 12

    if payments_made >= total_payments:
        return 0, 0 # Loan is fully paid

    # Calculate monthly payment (M) using the formula:
    # M = P * [r(1+r)^n] / [(1+r)^n - 1]
    if monthly_rate > 0:
        numerator_m = monthly_rate * ((1 + monthly_rate) ** total_payments)
        denominator_m = ((1 + monthly_rate) ** total_payments) - 1
        monthly_payment = principal * (numerator_m / denominator_m)
    else: # Handle zero interest case
        monthly_payment = principal / total_payments


    # Calculate outstanding balance (B) using the formula:
    # B = P * [(1+r)^n - (1+r)^p] / [(1+r)^n - 1]
    if monthly_rate > 0:
        numerator_b = ((1 + monthly_rate) ** total_payments) - ((1 + monthly_rate) ** payments_made)
        denominator_b = ((1 + monthly_rate) ** total_payments) - 1
        balance = principal * (numerator_b / denominator_b)
    else: # Handle zero interest case
        balance = principal - (monthly_payment * payments_made)


    return monthly_payment, balance

def main():
    """Main function to run the calculator."""
    parser = argparse.ArgumentParser(
        description="Islamic Mortgage Outstanding Balance Calculator (EPR-based)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Example usage:\n"
                 "python outstanding_balance_calculator.py --principal 500000 --epr 4.5 --term 30 --paid 60"
    )
    parser.add_argument("-p", "--principal", type=float, help="The original principal amount.")
    parser.add_argument("-e", "--epr", type=float, help="The current annual Effective Profit Rate (EPR) in %.")
    parser.add_argument("-t", "--term", type=int, help="The total loan term in years.")
    parser.add_argument("-d", "--paid", type=int, help="The number of monthly payments already made.")
    args = parser.parse_args()

    # If command-line arguments are provided, use them. Otherwise, enter interactive mode.
    if args.principal and args.epr and args.term and args.paid:
        principal_amount = args.principal
        epr = args.epr
        loan_term_years = args.term
        payments_made = args.paid
        print("--- Calculating from command-line arguments ---")
    elif len(sys.argv) > 1:
        parser.print_help()
        sys.exit(1)
    else:
        print("--- Islamic Mortgage Outstanding Balance Calculator (EPR-based) ---")
        print("This tool calculates your outstanding balance based on the Effective Profit Rate (EPR).\n")
        principal_amount = get_float_input("Enter the original principal amount: ")
        epr = get_float_input("Enter the current annual Effective Profit Rate (EPR) in % (e.g., 4.75): ")
        loan_term_years = get_int_input("Enter the total loan term in years (e.g., 30): ")
        payments_made = get_int_input("Enter the number of monthly payments already made: ")
        print("\nCalculating...")

    monthly_payment, outstanding_balance = calculate_outstanding_balance(
        principal_amount, epr, loan_term_years, payments_made
    )

    if outstanding_balance > 0:
        principal_paid_off = principal_amount - outstanding_balance
        print("\n--- Results ---")
        print(f"Estimated Monthly Payment (based on EPR): ${monthly_payment:,.2f}")
        print(f"Outstanding Balance (based on EPR): ${outstanding_balance:,.2f}")
        print(f"Amount Paid Off from Principal: ${principal_paid_off:,.2f}")
        print("\nDisclaimer: This is an estimate for informational purposes. Always refer to official bank statements.")
    else:
        print("\nBased on your input, this loan appears to be fully paid off.")


if __name__ == "__main__":
    main()
