# Tax Liability Calculator

This Python program calculates the tax liability based on the filing status, yearly salary, and the number of children.

The program supports two filing statuses: 'single' and 'married'. For 'single', it assumes you are taking the standard deduction of $14,600 for the 2024 tax year. For 'married', it assumes you are filing jointly and taking the standard deduction of $29,200.

## How it works

The program takes different inputs based on the filing status:

If you are filing as 'single':
1. Your yearly salary
2. How many dependants they have

If you are filing as 'married':
1. The first spouse's yearly salary
2. The second spouse's yearly salary
3. The number of dependants they have

The program then calculates the total salary. For 'single', it subtracts the standard deduction of $14,600 from the salary. For 'married', it adds the two salaries and subtracts the standard deduction of $29,200.

The program calculates the tax based on the following tax brackets:

For 'single':
- 35% for incomes over $243,725
- 32% for incomes over $191,950
- 24% for incomes over $100,525
- 22% for incomes over $47,150
- 12% for incomes over $11,600
- 10% for incomes of $11,600 or less

For 'married':
- 35% for incomes over $487,450
- 32% for incomes over $383,900
- 24% for incomes over $201,050
- 22% for incomes over $94,300
- 12% for incomes over $23,200
- 10% for incomes of $23,200 or less

For 'married', the program also subtracts a child credit of $2,000 per child from the tax.

The program then returns the tax and the total salary after the standard deduction, both formatted as US currency.

## How to run the program

To run the program, simply execute the `tax.py` file in a Python environment.