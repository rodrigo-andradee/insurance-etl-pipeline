# Insurance ETL Pipeline - Internal Lookup Tool

import streamlit as st
import pandas as pd

# --- Page config ---
st.set_page_config(page_title="Insurance Lookup Tool", page_icon="🛡️", layout="wide")

# --- Load data ---
@st.cache_data
def load_data():
    fact_claims   = pd.read_parquet("data/fact_claims")
    dim_customers = pd.read_parquet("data/dim_customers")
    dim_policies  = pd.read_parquet("data/dim_policies")
    dim_agents    = pd.read_parquet("data/dim_agents")
    return fact_claims, dim_customers, dim_policies, dim_agents

fact_claims, dim_customers, dim_policies, dim_agents = load_data()

# --- Helper functions ---
def format_marital(val):
    return "Married" if val == "Y" else "Single"

def format_employment(val):
    return "Employed" if val == "Y" else "Unemployed"

# --- Title ---
st.title("🛡️ Insurance Internal Lookup Tool")
st.markdown("Internal tool for claims and fraud risk analysis.")
st.divider()

# --- Customer directory ---
with st.expander("📋 View all available Customer IDs"):
    st.dataframe(
        dim_customers[["CUSTOMER_ID", "CUSTOMER_NAME", "CITY", "STATE"]].sort_values("CUSTOMER_ID"),
        use_container_width=True
    )

st.divider()

# --- Search ---
st.subheader("🔍 Search Customer")

search_type = st.radio("Search by:", ["Customer ID", "Customer Name"], horizontal=True)

customer = pd.DataFrame()

if search_type == "Customer ID":
    customer_id = st.text_input("Enter Customer ID (e.g. A00003822)")
    if customer_id:
        customer = dim_customers[dim_customers["CUSTOMER_ID"] == customer_id]

else:
    all_names = sorted(dim_customers["CUSTOMER_NAME"].dropna().unique().tolist())
    selected_name = st.selectbox("Start typing a customer name:", [""] + all_names)
    if selected_name:
        customer = dim_customers[dim_customers["CUSTOMER_NAME"] == selected_name]

if not customer.empty:
    customer_id = customer["CUSTOMER_ID"].values[0]
    claims = fact_claims[fact_claims["CUSTOMER_ID"] == customer_id]

    # --- Customer Info ---
    st.subheader("👤 Customer Information")
    col1, col2, col3 = st.columns(3)
    col1.metric("Name", customer["CUSTOMER_NAME"].values[0])
    col2.metric("Age", customer["AGE"].values[0])
    col3.metric("City", customer["CITY"].values[0])

    col4, col5, col6 = st.columns(3)
    col4.metric("Marital Status", format_marital(customer["MARITAL_STATUS"].values[0]))
    col5.metric("Employment", format_employment(customer["EMPLOYMENT_STATUS"].values[0]))
    col6.metric("Social Class", customer["SOCIAL_CLASS"].values[0])

    st.divider()

    # --- Claims History ---
    st.subheader("📋 Claims History")
    if claims.empty:
        st.info("No claims found for this customer.")
    else:
        st.dataframe(claims[[
            "TRANSACTION_ID", "POLICY_NUMBER", "CLAIM_AMOUNT",
            "CLAIM_STATUS", "INCIDENT_SEVERITY", "LOSS_DT",
            "fraud_indicator", "risk_level"
        ]], use_container_width=True)

        st.divider()

        # --- Fraud Risk Assessment ---
        st.subheader("⚠️ Fraud Risk Assessment")
        fraud_claims = claims[claims["fraud_indicator"] == 1]

        if fraud_claims.empty:
            st.success("✅ No suspicious claims detected for this customer.")
        else:
            st.error(f"🚨 {len(fraud_claims)} suspicious claim(s) detected!")
            for _, row in fraud_claims.iterrows():
                with st.expander(f"Claim {row['TRANSACTION_ID']}"):
                    st.write(f"**Claim Amount:** ${row['CLAIM_AMOUNT']:,.2f}")
                    st.write(f"**Incident Severity:** {row['INCIDENT_SEVERITY']}")
                    st.write(f"**Any Injury:** {'Yes' if row['ANY_INJURY'] == 1 else 'No'}")
                    st.write(f"**Police Report Available:** {'Yes' if row['POLICE_REPORT_AVAILABLE'] == 1 else 'No'}")
                    st.write(f"**Risk Level:** {row['risk_level']}")

elif search_type == "Customer ID" and "customer_id" in dir() and customer_id:
    st.warning("Customer not found. Please check the ID.")