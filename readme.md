# Tax Liability Calculator

This Python program calculates the tax liability for a married couple based on their combined yearly salary and the number of children they have.

The program assumes you are married and filing jointly, it also assumes you are taking the standard deduction of $29,200 for the 2024 tax year.


## How it works

The program takes three inputs:

1. The husband's yearly salary
2. The wife's yearly salary
3. The number of children they have

The program then calculates the total salary by adding the husband's and wife's salaries. It subtracts a standard deduction of $29,200 from the total salary.

The program calculates the tax based on the following tax brackets:

- 35% for incomes over $487,450
- 32% for incomes over $383,900
- 24% for incomes over $201,050
- 22% for incomes over $94,300
- 12% for incomes over $23,200
- 10% for incomes of $23,200 or less

The program also subtracts a child credit of $2,000 per child from the tax.

The program then returns the tax and the total salary after the standard deduction, both formatted as US currency.

## How to run the program

To run the program, simply execute the `tax.py` file in a Python environment.