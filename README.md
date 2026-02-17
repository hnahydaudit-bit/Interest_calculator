# Interest_calculator

Simple Streamlit app to calculate GST delayed-payment interest using:

- Due date
- Payment date
- Annual interest rate
- Tax components: IGST, CGST, SGST

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Interest formula

`Interest = Tax amount × (Annual rate / 100) × (Delay days / 365)`
