import streamlit as st
from datetime import date


codex/create-interest-calculator-for-gst-f1nf1o
st.set_page_config(page_title="GST Calculator", page_icon="💸", layout="centered")

st.title("💸 GST Interest & Late Fee Calculator")
st.caption("Simple calculator for GST delayed-payment interest and return-filing late fee.")

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
 main


def calculate_interest(amount: float, rate_percent: float, days: int) -> float:
    """Simple interest for delayed payment based on annual rate."""
    return amount * (rate_percent / 100) * (days / 365)


 codex/create-interest-calculator-for-gst-f1nf1o
def get_chargeable_days(start_date: date, end_date: date) -> int:
    """Return delay days; negatives are capped at zero."""
    return max((end_date - start_date).days, 0)


def per_day_fee_input(label: str, key_prefix: str) -> float:
    """Input control that supports standard slab selection or manual fee entry."""
    mode = st.radio(
        f"{label} per day selection",
        options=["Standard", "Manual"],
        horizontal=True,
        key=f"{key_prefix}_mode",
        label_visibility="collapsed",
    )

    if mode == "Standard":
        return float(
            st.selectbox(
                f"{label} per day (₹)",
                options=[10, 25, 50, 100],
                index=1,
                key=f"{key_prefix}_standard",
            )
        )

    return st.number_input(
        f"{label} per day (₹)",
        min_value=0.0,
        value=25.0,
        step=1.0,
        key=f"{key_prefix}_manual",
    )


interest_tab, late_fee_tab = st.tabs(["Interest Calculator", "Late Fee Calculator"])

with interest_tab:
    with st.container(border=True):
        col1, col2 = st.columns(2)

        with col1:
            due_date = st.date_input("Due date", value=date.today(), key="interest_due")
            payment_date = st.date_input("Payment date", value=date.today(), key="interest_payment")

        with col2:
            annual_rate = st.number_input(
                "Annual interest rate (%)",
                min_value=0.0,
                max_value=100.0,
                value=18.0,
                step=0.1,
                help="Example: use 18 for 18% per annum.",
                key="interest_rate",
            )

    st.subheader("Tax details")
    tax_col1, tax_col2, tax_col3 = st.columns(3)

    with tax_col1:
        igst = st.number_input("IGST (₹)", min_value=0.0, value=0.0, step=100.0, key="igst")
    with tax_col2:
        cgst = st.number_input("CGST (₹)", min_value=0.0, value=0.0, step=100.0, key="cgst")
    with tax_col3:
        sgst = st.number_input("SGST (₹)", min_value=0.0, value=0.0, step=100.0, key="sgst")

    delay_days = (payment_date - due_date).days
    chargeable_days = get_chargeable_days(due_date, payment_date)

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

with late_fee_tab:
    with st.container(border=True):
        lf_col1, lf_col2 = st.columns(2)
        with lf_col1:
            late_fee_due_date = st.date_input("Due date", value=date.today(), key="lf_due")
        with lf_col2:
            filing_date = st.date_input("Filing date", value=date.today(), key="lf_filing")

    st.subheader("Late fee per day")
    fee_col1, fee_col2 = st.columns(2)
    with fee_col1:
        cgst_fee_per_day = per_day_fee_input("CGST", "lf_cgst")
    with fee_col2:
        sgst_fee_per_day = per_day_fee_input("SGST", "lf_sgst")

    late_days_raw = (filing_date - late_fee_due_date).days
    late_days = get_chargeable_days(late_fee_due_date, filing_date)

    if late_days_raw < 0:
        st.warning("Filing date is before due date. No late fee is charged.")

    cgst_late_fee = cgst_fee_per_day * late_days
    sgst_late_fee = sgst_fee_per_day * late_days
    total_late_fee = cgst_late_fee + sgst_late_fee

    st.subheader("Late fee output")
    out1, out2, out3 = st.columns(3)
    out1.metric("Late days", f"{late_days}")
    out2.metric("CGST late fee (₹)", f"{cgst_late_fee:,.2f}")
    out3.metric("SGST late fee (₹)", f"{sgst_late_fee:,.2f}")

    st.success(f"Total late fee payable: ₹{total_late_fee:,.2f}")

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
 main
