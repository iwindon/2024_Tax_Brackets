from flask import Flask, request, render_template
import locale

app = Flask(__name__)

def calculate_tax(salary, salary2, num_children, filing_status):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    standard_deduction = 29200 if filing_status == 'married' else 14600
    child_credit = 2000 * num_children

    if filing_status == 'married':
        total_salary = salary + salary2
        taxable_income = total_salary - standard_deduction
    else:
        total_salary = salary
        taxable_income = total_salary - standard_deduction

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
        if taxable_income > tax_brackets[i][0]:
            tax += (taxable_income - tax_brackets[i][0]) * tax_brackets[i][1]
            taxable_income = tax_brackets[i][0]
    tax += taxable_income * tax_brackets[-1][1]
    tax -= child_credit

    final_salary_after_taxes = total_salary - tax

    return locale.currency(tax, grouping=True), locale.currency(final_salary_after_taxes, grouping=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filing_status = request.form['filing_status']
        salary = float(request.form['salary'])
        salary2 = float(request.form['salary2']) if filing_status == 'married' else 0
        num_children = int(request.form['num_children'])
        tax, final_salary_after_taxes = calculate_tax(salary, salary2, num_children, filing_status)
        return render_template('result.html', tax=tax, final_salary_after_taxes=final_salary_after_taxes)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
