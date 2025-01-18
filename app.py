from flask import Flask, request, render_template
import locale

app = Flask(__name__)

def calculate_tax(salary, salary2, num_children, filing_status):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    standard_deduction = 29200 if filing_status == 'married' else 14600
    child_credit = 2000 * num_children

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filing_status = request.form['filing_status']
        salary = float(request.form['salary'])
        salary2 = float(request.form['salary2']) if filing_status == 'married' else 0
        num_children = int(request.form['num_children'])
        tax, total_salary = calculate_tax(salary, salary2, num_children, filing_status)
        return render_template('result.html', tax=tax, total_salary=total_salary)
    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True)
