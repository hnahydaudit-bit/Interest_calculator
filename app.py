import streamlit as st
from datetime import date


st.set_page_config(page_title="GST Interest Calculator", page_icon="💸", layout="centered")

st.title("💸 GST Interest Calculator")
st.caption("Calculate delayed-payment interest on IGST, CGST, and SGST.")

with st.container(border=True):
    col1, col2 = st.columns(2)

    with col1:
        due_date = st.date_input("Due date", value=date.today())
        payment_date = st.date_input("Payment date", value=date.today())

    with col2:
        annual_rate = st.number_input(
            "Annual interest rate (%)",
            min_value=0.0,
            max_value=100.0,
            value=18.0,
            step=0.1,
            help="Example: use 18 for 18% per annum.",
        )

st.subheader("Tax details")
tax_col1, tax_col2, tax_col3 = st.columns(3)

with tax_col1:
    igst = st.number_input("IGST (₹)", min_value=0.0, value=0.0, step=100.0)
with tax_col2:
    cgst = st.number_input("CGST (₹)", min_value=0.0, value=0.0, step=100.0)
with tax_col3:
    sgst = st.number_input("SGST (₹)", min_value=0.0, value=0.0, step=100.0)


def calculate_interest(amount: float, rate_percent: float, days: int) -> float:
    """Simple interest for delayed payment based on annual rate."""
    return amount * (rate_percent / 100) * (days / 365)


delay_days = (payment_date - due_date).days
chargeable_days = max(delay_days, 0)

if delay_days < 0:
    st.warning("Payment date is before due date. No interest is charged.")

igst_interest = calculate_interest(igst, annual_rate, chargeable_days)
cgst_interest = calculate_interest(cgst, annual_rate, chargeable_days)
sgst_interest = calculate_interest(sgst, annual_rate, chargeable_days)

total_tax = igst + cgst + sgst
total_interest = igst_interest + cgst_interest + sgst_interest
grand_total = total_tax + total_interest

st.subheader("Result")
res1, res2, res3 = st.columns(3)
res1.metric("Delay days", f"{chargeable_days}")
res2.metric("Total tax (₹)", f"{total_tax:,.2f}")
res3.metric("Total interest (₹)", f"{total_interest:,.2f}")

with st.expander("Interest breakdown"):
    st.write(f"IGST interest: ₹{igst_interest:,.2f}")
    st.write(f"CGST interest: ₹{cgst_interest:,.2f}")
    st.write(f"SGST interest: ₹{sgst_interest:,.2f}")

st.success(f"Grand total payable: ₹{grand_total:,.2f}")

st.caption(
    "Formula used: Interest = Tax amount × (Annual rate / 100) × (Delay days / 365)"
)
