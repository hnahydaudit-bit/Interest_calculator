# Interest_calculator

codex/create-interest-calculator-for-gst-f1nf1o
Simple Streamlit app with two GST utilities:

- **Interest Calculator** for delayed-payment interest
- **Late Fee Calculator** for delayed filing fee

## Inputs supported

### Interest Calculator

Simple Streamlit app to calculate GST delayed-payment interest using:

main
- Due date
- Payment date
- Annual interest rate
- Tax components: IGST, CGST, SGST

codex/create-interest-calculator-for-gst-f1nf1o
### Late Fee Calculator
- Due date
- Filing date
- Late fee per day for CGST and SGST
  - Standard dropdown options: `10`, `25`, `50`, `100`
  - Manual value entry


 main
## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Interest formula

`Interest = Tax amount × (Annual rate / 100) × (Delay days / 365)`
codex/create-interest-calculator-for-gst-f1nf1o

## Late fee formula

- `CGST late fee = CGST per-day fee × Late days`
- `SGST late fee = SGST per-day fee × Late days`

 main
