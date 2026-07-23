from flask import Flask, request, render_template, flash
import locale
import logging

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flashing messages

# Configure logging
logging.basicConfig(level=logging.INFO)

# Set locale for currency formatting
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except locale.Error:
    # Windows often does not have this locale string installed.
    pass

FILING_STATUSES = {
    'single': {
        'label': 'Single',
        'standard_deduction': 16100,
        'requires_second_salary': False,
        'brackets': [
            (12400, 0.10),
            (50400, 0.12),
            (105700, 0.22),
            (201775, 0.24),
            (256225, 0.32),
            (640600, 0.35),
            (None, 0.37),
        ],
    },
    'married_joint': {
        'label': 'Married Filing Jointly',
        'standard_deduction': 32200,
        'requires_second_salary': True,
        'brackets': [
            (24800, 0.10),
            (100800, 0.12),
            (211400, 0.22),
            (403550, 0.24),
            (512450, 0.32),
            (768700, 0.35),
            (None, 0.37),
        ],
    },
    'married_separate': {
        'label': 'Married Filing Separately',
        'standard_deduction': 16100,
        'requires_second_salary': False,
        'brackets': [
            (12400, 0.10),
            (50400, 0.12),
            (105700, 0.22),
            (201775, 0.24),
            (256225, 0.32),
            (384350, 0.35),
            (None, 0.37),
        ],
    },
    'head_household': {
        'label': 'Head of Household',
        'standard_deduction': 24150,
        'requires_second_salary': False,
        'brackets': [
            (17700, 0.10),
            (67600, 0.12),
            (105700, 0.22),
            (201775, 0.24),
            (256225, 0.32),
            (640600, 0.35),
            (None, 0.37),
        ],
    },
    'qualifying_surviving_spouse': {
        'label': 'Qualifying Surviving Spouse',
        'standard_deduction': 32200,
        'requires_second_salary': False,
        'brackets': [
            (24800, 0.10),
            (100800, 0.12),
            (211400, 0.22),
            (403550, 0.24),
            (512450, 0.32),
            (768700, 0.35),
            (None, 0.37),
        ],
    },
}

# Custom filter for currency formatting
@app.template_filter('currency')
def currency_filter(value):
    try:
        return f"${float(value):,.2f}"
    except (TypeError, ValueError):
        return '$0.00'

def parse_currency(value):
    cleaned = (value or '').replace(',', '').replace('$', '').strip()
    return float(cleaned)


def calculate_tax(salary, salary2, num_children, filing_status):
    status = FILING_STATUSES[filing_status]
    standard_deduction = status['standard_deduction']
    total_salary = salary + salary2
    taxable_income = max(0.0, total_salary - standard_deduction)

    gross_tax = 0.0
    tax_breakdown = []
    lower_bound = 0.0

    for cap, rate in status['brackets']:
        upper_bound = taxable_income if cap is None else min(taxable_income, cap)
        taxed_amount = max(0.0, upper_bound - lower_bound)

        if taxed_amount > 0:
            bracket_tax = taxed_amount * rate
            gross_tax += bracket_tax
            tax_breakdown.append(
                {
                    'lower': lower_bound,
                    'upper': upper_bound,
                    'rate': rate,
                    'taxed_amount': taxed_amount,
                    'tax': bracket_tax,
                }
            )

        if cap is None or taxable_income <= cap:
            break
        lower_bound = float(cap)

    child_credit = 2200 * num_children
    tax_liability = max(0.0, gross_tax - child_credit)
    final_salary_after_taxes = total_salary - tax_liability

    return {
        'filing_status_label': status['label'],
        'total_income': total_salary,
        'standard_deduction': standard_deduction,
        'taxable_income': taxable_income,
        'gross_tax': gross_tax,
        'child_credit': child_credit,
        'tax_liability': tax_liability,
        'final_salary_after_taxes': final_salary_after_taxes,
        'tax_breakdown': tax_breakdown,
    }

def validate_inputs(salary, salary2, num_children, filing_status):
    errors = []

    if filing_status not in FILING_STATUSES:
        return None, ['Invalid filing status selected.']

    status = FILING_STATUSES[filing_status]

    try:
        salary = parse_currency(salary)
        if salary < 0:
            errors.append('Salary cannot be negative.')
    except ValueError:
        errors.append('Primary salary must be a valid number.')
        salary = 0.0

    try:
        salary2 = parse_currency(salary2) if salary2 else 0.0
        if salary2 < 0:
            errors.append('Second salary cannot be negative.')
    except ValueError:
        errors.append('Second salary must be a valid number.')
        salary2 = 0.0

    if status['requires_second_salary'] and salary2 == 0:
        errors.append('Second salary is required for Married Filing Jointly.')

    try:
        num_children = int(num_children)
        if num_children < 0:
            errors.append('Number of qualifying children cannot be negative.')
    except ValueError:
        errors.append('Number of qualifying children must be a whole number.')
        num_children = 0

    if errors:
        return None, errors

    return (salary, salary2, num_children), []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        filing_status = request.form.get('filing_status', 'single')
        salary = request.form.get('salary', '')
        salary2 = request.form.get('salary2', '')
        num_children = request.form.get('num_children', '0')

        form_data = {
            'filing_status': filing_status,
            'salary': salary,
            'salary2': salary2,
            'num_children': num_children,
        }

        validated_inputs, errors = validate_inputs(salary, salary2, num_children, filing_status)
        if validated_inputs:
            salary, salary2, num_children = validated_inputs
            result = calculate_tax(salary, salary2, num_children, filing_status)
            return render_template('result.html', result=result)
        else:
            for error in errors:
                flash(error)
            return render_template('form.html', form_data=form_data, filing_statuses=FILING_STATUSES)
    return render_template('form.html', form_data={}, filing_statuses=FILING_STATUSES)

if __name__ == '__main__':
    app.run(debug=True)