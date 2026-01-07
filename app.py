from flask import Flask, request, render_template, flash, redirect, url_for
import locale
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set locale for currency formatting
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Custom filter for currency formatting
@app.template_filter('currency')
def currency_filter(value):
    return locale.currency(value, grouping=True)

def calculate_tax(salary, salary2, num_children, filing_status):
    standard_deduction = 32200 if filing_status == 'married' else 16100
    child_credit = 2200 * num_children

    if filing_status == 'married':
        total_salary = salary + salary2
        taxable_income = total_salary - standard_deduction
    else:
        total_salary = salary
        taxable_income = total_salary - standard_deduction

    if filing_status == 'single':
        tax_brackets = [
            (640600, 0.37),
            (256225, 0.35),
            (201775, 0.32),
            (105700, 0.24),
            (50400, 0.22),
            (12400, 0.12),
            (0, 0.10)
        ]
    elif filing_status == 'married':
        tax_brackets = [
            (768700, 0.37),
            (512450, 0.35),
            (403550, 0.32),
            (211400, 0.24),
            (100800, 0.22),
            (24800, 0.12),
            (0, 0.10)
        ]
    tax = 0
    tax_breakdown = []

    for i in range(len(tax_brackets)-1):
        if taxable_income > tax_brackets[i][0]:
            amount = (taxable_income - tax_brackets[i][0]) * tax_brackets[i][1]
            tax += amount
            tax_breakdown.append((tax_brackets[i][0], tax_brackets[i][1], amount))
            taxable_income = tax_brackets[i][0]
    amount = taxable_income * tax_brackets[-1][1]
    tax += amount
    tax_breakdown.append((tax_brackets[-1][0], tax_brackets[-1][1], amount))
    tax -= child_credit

    final_salary_after_taxes = total_salary - tax

    return locale.currency(tax, grouping=True), locale.currency(final_salary_after_taxes, grouping=True), tax_breakdown

def validate_inputs(salary, salary2, num_children):
    try:
        salary = float(salary)
        if salary2:
            salary2 = float(salary2)
        num_children = int(num_children)
        if num_children < 0 or num_children > 3:
            return None
        return salary, salary2, num_children
    except ValueError:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filing_status = request.form['filing_status']
        salary = request.form['salary']
        salary2 = request.form['salary2'] if filing_status == 'married' else 0
        num_children = request.form['num_children']

        validated_inputs = validate_inputs(salary, salary2, num_children)
        if validated_inputs:
            salary, salary2, num_children = validated_inputs
            tax, final_salary_after_taxes, tax_breakdown = calculate_tax(salary, salary2, num_children, filing_status)
            return render_template('result.html', tax=tax, final_salary_after_taxes=final_salary_after_taxes, tax_breakdown=tax_breakdown)
        else:
            flash('Invalid input. Please enter valid numbers and ensure the number of dependents is between 0 and 3.')
            return redirect(url_for('index'))
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)