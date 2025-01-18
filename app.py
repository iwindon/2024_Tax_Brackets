from flask import Flask, request, render_template, flash, redirect, url_for
import locale
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Configure logging
logging.basicConfig(level=logging.INFO)

def calculate_tax(salary, salary2, num_children, filing_status):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    standard_deduction = 30000 if filing_status == 'married' else 15000
    child_credit = 2000 * num_children

    if filing_status == 'married':
        total_salary = salary + salary2
        taxable_income = total_salary - standard_deduction
    else:
        total_salary = salary
        taxable_income = total_salary - standard_deduction

    if filing_status == 'single':
        tax_brackets = [
            (626350, 0.37),
            (250525, 0.35),
            (197300, 0.32),
            (103350, 0.24),
            (48475, 0.22),
            (11925, 0.12),
            (0, 0.10)
        ]
    elif filing_status == 'married':
        tax_brackets = [
            (751600, 0.37),
            (501050, 0.35),
            (394600, 0.32),
            (206700, 0.24),
            (96950, 0.22),
            (23850, 0.12),
            (0, 0.10)
        ]
    tax = 0

    for i in range(len(tax_brackets)-1):
        if taxable_income > tax_brackets[i][0]:
            tax += (taxable_income - tax_brackets[i][0]) * tax_brackets[i][1]
            taxable_income = tax_brackets[i][0]
    tax += taxable_income * tax_brackets[-1][1]
    tax -= child_credit

    final_salary_after_taxes = total_salary - tax

    return locale.currency(tax, grouping=True), locale.currency(final_salary_after_taxes, grouping=True)

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
            tax, final_salary_after_taxes = calculate_tax(salary, salary2, num_children, filing_status)
            return render_template('result.html', tax=tax, final_salary_after_taxes=final_salary_after_taxes)
        else:
            flash('Invalid input. Please enter valid numbers and ensure the number of dependents is between 0 and 3.')
            return redirect(url_for('index'))
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)

