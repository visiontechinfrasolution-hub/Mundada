import streamlit as st
from supabase import create_client, Client
import pandas as pd

# --- CONFIGURATION & UI STYLE ---
st.set_page_config(page_title="Mundada | Visiontech", layout="wide")

# Custom CSS for Visiontech Look
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    .stTextInput>div>div>input { border-radius: 5px; }
    [data-testid="stMetricValue"] { font-size: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- SUPABASE CONNECTION ---
# Replace with your VIS-MUNDADA credentials
URL = "YOUR_SUPABASE_URL"
KEY = "YOUR_SUPABASE_KEY"
supabase: Client = create_client(URL, KEY)

# --- NAVIGATION ---
with st.sidebar:
    st.image("https://www.google.com/s2/favicons?sz=64&domain=streamlit.io") # Logo placeholder
    st.title("Mundada Management")
    page = st.radio("Go to", ["📈 Dashboard", "🏗️ Site Data", "💰 Finance"])
    st.info("User: Mayur Patil")

# --- 1. DASHBOARD PAGE ---
if page == "📈 Dashboard":
    st.header("Visiontech - Mundada Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Sites", "0")
    col2.metric("Total PO Amt", "₹ 0")
    col3.metric("WCC Received", "₹ 0")
    col4.metric("Pending Balance", "₹ 0")

# --- 2. SITE DATA PAGE ---
elif page == "🏗️ Site Data":
    st.header("Site Data Entry")
    
    with st.container():
        with st.form("site_entry", clear_on_submit=True):
            # Section: Basic Details
            st.subheader("📍 Basic & Work Details")
            r1c1, r1c2, r1c3 = st.columns(3)
            project_id = r1c1.text_input("Project ID")
            site_id = r1c2.text_input("Site ID")
            site_name = r1c3.text_input("Site Name")
            
            r2c1, r2c2, r2c3 = st.columns(3)
            cluster = r2c1.text_input("Cluster")
            work_desc = r2c2.text_area("Work Description", height=68)
            project_amt = r2c3.number_input("Project Amt", min_value=0.0)

            st.divider()
            
            # Section: PO & Team
            st.subheader("📑 PO & Team Assignment")
            r3c1, r3c2, r3c3 = st.columns(3)
            po_no = r3c1.text_input("PO No")
            po_amt = r3c2.number_input("PO Amt", min_value=0.0)
            site_status = r3c3.selectbox("Site Status", ["Pending", "In Progress", "Completed", "WCC Done"])
            
            r4c1, r4c2, r4c3 = st.columns(3)
            team_name = r4c1.text_input("Team Name")
            team_billing = r4c2.number_input("Team Billing", min_value=0.0)
            team_paid = r4c3.number_input("Team Paid Amt", min_value=0.0)

            st.divider()

            # Section: WCC & Finance
            st.subheader("💳 WCC & Received Details")
            r5c1, r5c2, r5c3 = st.columns(3)
            wcc_no = r5c1.text_input("WCC No.")
            wcc_amt = r5c2.number_input("WCC Amt", min_value=0.0)
            received_amt = r5c3.number_input("Received Amt", min_value=0.0)

            if st.form_submit_button("Submit Data to VIS-MUNDADA"):
                data = {
                    "project_id": project_id, "site_id": site_id, "site_name": site_name,
                    "cluster": cluster, "work_description": work_desc, "project_amt": project_amt,
                    "po_no": po_no, "po_amt": po_amt, "site_status": site_status,
                    "team_name": team_name, "team_billing": team_billing, "team_paid_amt": team_paid,
                    "wcc_no": wcc_no, "wcc_amt": wcc_amt, "received_amt": received_amt
                }
                supabase.table("site_data").insert(data).execute()
                st.success("Data successfully synced!")

# --- 3. FINANCE PAGE ---
elif page == "💰 Finance":
    st.header("Financial Ledger")
    # Form for Finance table (Received From, Paid To, Date, etc.)
