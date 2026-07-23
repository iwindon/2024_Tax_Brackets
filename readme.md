# Tax Liability Calculator

This Flask app estimates 2026 federal income tax liability based on filing status, income, and qualifying children.

## Supported filing statuses

1. Single
2. Married Filing Jointly
3. Married Filing Separately
4. Head of Household
5. Qualifying Surviving Spouse

## How it works

1. Reads income inputs from the form.
2. Applies the standard deduction for the selected filing status.
3. Calculates tax progressively through the configured 2026 brackets.
4. Applies child tax credit of $2,000 per qualifying child.
5. Floors tax liability at $0.00 (no negative liability).

## Key assumptions

1. This is an estimate for regular federal income tax only.
2. Uses standard deduction only (no itemized deductions).
3. Does not include additional taxes (self-employment, NIIT, AMT, etc.).
4. Child tax credit is modeled as non-refundable in this estimator.
5. Brackets are based on the 2026 values configured in the app.

## How to run the program

1. Create and activate your virtual environment.
2. Install dependencies from requirements.txt.
3. Run:

```bash
python app.py
```

4. Open the local Flask URL shown in your terminal.