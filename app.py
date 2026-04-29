import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Mundada | Full Portal", layout="wide")

# --- 2. ELEGANT STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); }
    h1 { font-weight: 800; color: #0984e3; }
    div.stForm { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 20px; padding: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); }
    .stButton>button { background: linear-gradient(135deg, #0984e3 0%, #00cec9 100%); color: white; border-radius: 10px; font-weight: 700; border: none; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. CONNECTION ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"

@st.cache_resource
def get_supabase():
    return create_client(URL, KEY)

supabase = get_supabase()

# --- 4. NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MENU", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.divider()
    st.info("User: Mayur Patil")

# --- 5. DASHBOARD ---
if page == "🏠 Dashboard":
    st.header("Project Intelligence")
    st.write("Dashboard metrics live soon.")

# --- 6. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.header("Master Database")
    t1, t2 = st.tabs(["Client Master", "Team Master"])
    with t1:
        with st.form("c_reg"):
            c_n = st.text_input("New Client Name")
            if st.form_submit_button("Add Client"):
                supabase.table("client_master").insert({"client_name": c_n}).execute()
                st.success("Client Registered!")
    with t2:
        with st.form("t_reg"):
            t_n = st.text_input("New Team Name")
            if st.form_submit_button("Add Team"):
                supabase.table("team_master").insert({"team_name": t_n}).execute()
                st.success("Team Registered!")

# --- 7. SITE DATA ENTRY (ALL COLUMNS RESTORED) ---
elif page == "🏗️ Site Data Entry":
    st.header("Complete Site Registry")
    
    # Data Fetch for Dropdowns
    clients = supabase.table("client_master").select("client_name").execute()
    teams = supabase.table("team_master").select("team_name").execute()
    client_list = [c['client_name'] for c in clients.data] if clients.data else []
    team_list = [t['team_name'] for t in teams.data] if teams.data else []

    with st.form("full_site_form", clear_on_submit=True):
        st.subheader("📍 Site Details")
        c1, c2, c3 = st.columns(3)
        p_id = c1.text_input("Project ID")
        s_id = c2.text_input("Site ID")
        s_name = c3.selectbox("Client / Site Name", client_list)
        
        c4, c5, c6 = st.columns(3)
        cluster = c4.text_input("Cluster")
        work_desc = c5.text_area("Work Description", height=65)
        proj_amt = c6.number_input("Project Amt", min_value=0.0)

        st.divider()
        st.subheader("📑 PO & Team Assignment")
        c7, c8, c9 = st.columns(3)
        po_no = c7.text_input("PO No")
        po_amt = c8.number_input("PO Amt", min_value=0.0)
        s_status = c9.selectbox("Site Status", ["Pending", "Work in Progress", "WCC Done", "Closed"])

        c10, c11, c12 = st.columns(3)
        team_sel = c10.selectbox("Team Name", team_list)
        team_bill = c11.number_input("Team Billing", min_value=0.0)
        team_paid = c12.number_input("Team Paid Amt", min_value=0.0)

        st.divider()
        st.subheader("💳 WCC & Received Details")
        c13, c14, c15 = st.columns(3)
        wcc_no = c13.text_input("WCC No.")
        wcc_amt = c14.number_input("WCC Amt", min_value=0.0)
        rec_amt = c15.number_input("Received Amt", min_value=0.0)

        if st.form_submit_button("🚀 SYNC COMPLETE DATA"):
            data = {
                "project_id": p_id, "site_id": s_id, "site_name": s_name,
                "cluster": cluster, "work_description": work_desc, "project_amt": proj_amt,
                "po_no": po_no, "po_amt": po_amt, "site_status": s_status,
                "team_name": team_sel, "team_billing": team_bill, "team_paid_amt": team_paid,
                "wcc_no": wcc_no, "wcc_amt": wcc_amt, "received_amt": rec_amt
            }
            supabase.table("site_data").insert(data).execute()
            st.success(f"Site {s_id} Fully Synced!")

# --- 8. FINANCE ---
elif page == "💸 Finance Ledger":
    st.header("Finance Center")
    with st.form("fin"):
        st.write("Finance form ready.")
        st.form_submit_button("Save")

st.markdown("<div style='text-align: center; padding: 20px; color: gray;'>Visiontech Automation © 2026</div>", unsafe_allow_html=True)
