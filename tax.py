import locale

def calculate_tax(salary, salary2, num_children, filing_status):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    standard_deduction = 29200 if filing_status == 'married' else 14600
    child_credit = 2000 * num_children if filing_status == 'married' else 0

    if filing_status == 'married':
        total_salary = salary + salary2 - standard_deduction
    else:
        total_salary = salary - standard_deduction

    if filing_status == 'single':
        tax_brackets = [
            (243725, 0.35),
            (191950, 0.32),
            (100525, 0.24),
            (47150, 0.22),
            (11600, 0.12),
            (0, 0.10)
        ]
    elif filing_status == 'married':
        tax_brackets = [
            (487450, 0.35),
            (383900, 0.32),
            (201050, 0.24),
            (94300, 0.22),
            (23200, 0.12),
            (0, 0.10)
        ]
    tax = 0

    for i in range(len(tax_brackets)-1):
        if total_salary > tax_brackets[i][0]:
            tax += (total_salary - tax_brackets[i][0]) * tax_brackets[i][1]
            total_salary = tax_brackets[i][0]
    tax += total_salary * tax_brackets[-1][1]
    return locale.currency(tax - child_credit, grouping=True), locale.currency(total_salary, grouping=True)

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a whole number.")

def get_filing_status():
    while True:
        status = input("Are you filing as 'single' or 'married'? ").lower()
        if status in ['single', 'married']:
            return status
        else:
            print("Invalid input. Please enter 'single' or 'married'.")

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter numbers only, no commas or dollar signs.")

print("This program calculates the tax liability for 2024.")
print("Please enter the numbers without commas or dollar signs.")
filing_status = get_filing_status()
salary = get_float_input("Enter the yearly salary: ")

if filing_status == 'married':
    salary2 = get_float_input("Enter the second yearly salary: ")
    num_children = get_int_input("Enter the number of children: ")
else:
    salary2 = 0
    num_children = 0

tax, total_salary = calculate_tax(salary, salary2, num_children, filing_status)
print(f"The tax liability for 2024 is estimated to be: {tax}")