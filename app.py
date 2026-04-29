import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIG & STYLE ---
st.set_page_config(page_title="Mundada | Visiontech", layout="wide")

# Custom CSS for Professional Look
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; background-color: #007bff; color: white; font-weight: bold; }
    .stTextInput>div>div>input, .stNumberInput>div>div>input { border-radius: 8px; }
    .footer { position: fixed; bottom: 0; width: 100%; text-align: center; color: gray; font-size: 12px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE CONNECTION ---
# Note: Humne URL se /rest/v1/ nikaal diya hai connection fix karne ke liye
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"

try:
    supabase: Client = create_client(URL, KEY)
except Exception as e:
    st.error(f"Supabase Connection Failed: {e}")

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🏗️ Mundada Mgmt")
    st.divider()
    page = st.radio("Navigation", ["📊 Dashboard", "📝 Site Data Entry", "💰 Finance Ledger"])
    st.divider()
    st.info("Logistics & Ops Portal\n\nUser: Mayur Patil")

# --- 4. DASHBOARD PAGE ---
if page == "📊 Dashboard":
    st.header("Visiontech - Mundada Overview")
    
    # Static Metrics (Inko baad mein live queries se connect kar sakte hain)
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric("Total Sites", "0")
    with c2: st.metric("PO Value", "₹ 0.00")
    with c3: st.metric("Client Received", "₹ 0.00")
    with c4: st.metric("Team Balance", "₹ 0.00")
    
    st.divider()
    st.write("Recent Activity will appear here.")

# --- 5. SITE DATA PAGE ---
elif page == "📝 Site Data Entry":
    st.header("New Site Entry - VIS Mundada")
    
    with st.form("site_form", clear_on_submit=True):
        # Section A: Project & Description
        st.subheader("📍 Site & Project Details")
        a1, a2, a3 = st.columns(3)
        project_id = a1.text_input("Project ID")
        site_id = a2.text_input("Site ID")
        site_name = a3.text_input("Site Name")
        
        a4, a5, a6 = st.columns(3)
        cluster = a4.text_input("Cluster")
        work_desc = a5.text_area("Work Description", height=70)
        project_amt = a6.number_input("Project Amt", min_value=0.0, step=1000.0)

        st.divider()

        # Section B: PO & Team
        st.subheader("📑 PO & Team Assignment")
        b1, b2, b3 = st.columns(3)
        po_no = b1.text_input("PO No")
        po_amt = b2.number_input("PO Amt", min_value=0.0)
        site_status = b3.selectbox("Site Status", ["Pending", "Material Dispatched", "Work in Progress", "WCC Done", "Closed"])
        
        b4, b5, b6 = st.columns(3)
        team_name = b4.text_input("Team Name")
        team_billing = b5.number_input("Team Billing", min_value=0.0)
        team_paid = b6.number_input("Team Paid Amt", min_value=0.0)
        # Note: Team Balance is auto-calculated in Supabase

        st.divider()

        # Section C: WCC & Finance
        st.subheader("💳 Client Billing (WCC)")
        c1, c2, c3 = st.columns(3)
        wcc_no = c1.text_input("WCC No.")
        wcc_amt = c2.number_input("WCC Amt", min_value=0.0)
        received_amt = c3.number_input("Received Amt", min_value=0.0)
        # Note: Balance Amt is auto-calculated in Supabase

        # Form Submit Button
        submit_btn = st.form_submit_button("Submit to Supabase")
        
        if submit_btn:
            if not site_id:
                st.warning("Site ID is mandatory!")
            else:
                data = {
                    "project_id": project_id,
                    "site_id": site_id,
                    "site_name": site_name,
                    "cluster": cluster,
                    "work_description": work_desc,
                    "project_amt": project_amt,
                    "po_no": po_no,
                    "po_amt": po_amt,
                    "site_status": site_status,
                    "team_name": team_name,
                    "team_billing": team_billing,
                    "team_paid_amt": team_paid,
                    "wcc_no": wcc_no,
                    "wcc_amt": wcc_amt,
                    "received_amt": received_amt
                }
                
                try:
                    response = supabase.table("site_data").insert(data).execute()
                    st.success(f"✅ Data for Site {site_id} successfully saved!")
                except Exception as e:
                    st.error(f"Failed to save data: {e}")

# --- 6. FINANCE PAGE ---
elif page == "💰 Finance Ledger":
    st.header("Financial Transactions")
    
    with st.form("finance_form", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        rec_from = f1.text_input("Received From")
        paid_to = f2.text_input("Paid To")
        trans_date = f3.date_input("Date", datetime.now())
        
        f4, f5 = st.columns(2)
        rec_amt = f4.number_input("Received Amt", min_value=0.0)
        paid_amt = f5.number_input("Paid Amount", min_value=0.0)
        
        if st.form_submit_button("Record Transaction"):
            fin_data = {
                "received_from": rec_from,
                "paid_to": paid_to,
                "transaction_date": str(trans_date),
                "received_amt": rec_amt,
                "paid_amount": paid_amt
            }
            try:
                supabase.table("finance").insert(fin_data).execute()
                st.success("Transaction recorded successfully!")
            except Exception as e:
                st.error(f"Error: {e}")

# Footer
st.markdown('<div class="footer">Visiontech Automation System © 2026</div>', unsafe_allow_html=True)
