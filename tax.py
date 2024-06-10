import locale

def calculate_tax(husband_salary, wife_salary, num_children):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    standard_deduction = 29200
    child_credit = 2000 * num_children
    total_salary = husband_salary + wife_salary - standard_deduction
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

print("This program calculates the tax liability for 2024.")
print("Please enter the numbers without commas or dollar signs.")
husband_salary = float(input("Enter the husband's yearly salary: "))
wife_salary = float(input("Enter the wife's yearly salary: "))
num_children = int(input("Enter the number of children: "))
tax, total_salary = calculate_tax(husband_salary, wife_salary, num_children)
print(f"The tax liability for 2024 is estimated to be: {tax}")