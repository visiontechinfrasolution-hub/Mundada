import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PAGE CONFIG & STYLING ---
st.set_page_config(
    page_title="Visiontech Mundada | Elegant Portal",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); color: #2d3436; }
    h1 { font-weight: 800; letter-spacing: -1.5px; color: #0984e3; margin-bottom: 10px; }
    h2, h3 { color: #2d3436; font-weight: 600; margin-top: 20px; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e1e4e8; }
    div[data-testid="stMetric"] { background: #ffffff; border: 1px solid #e1e4e8; border-radius: 20px; padding: 25px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    [data-testid="stMetricValue"] > div { color: #0984e3 !important; font-weight: 800; }
    div.stForm { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 25px; border: 1px solid #ffffff; padding: 40px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); }
    .stButton>button { background: linear-gradient(135deg, #0984e3 0%, #00cec9 100%); color: white; border: none; padding: 15px; border-radius: 12px; font-weight: 700; width: 100%; box-shadow: 0 4px 15px rgba(9, 132, 227, 0.3); }
    .elegant-footer { text-align: center; padding: 40px; color: #636e72; font-size: 14px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE CONNECTION ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"

@st.cache_resource
def get_supabase():
    return create_client(URL, KEY)

supabase = get_supabase()

# --- 3. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3; font-size: 28px;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", [
        "🏠 Dashboard", 
        "📝 Master Registration", 
        "🏗️ Site Data Entry", 
        "💸 Finance Ledger"
    ])
    st.divider()
    st.info(f"User: Mayur Patil\n\nSystem Time: {datetime.now().strftime('%H:%M')}")

# --- 4. DASHBOARD (3-LINE SMART LAYOUT) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    
    res = supabase.table("site_data").select("po_amt, received_amt, team_billing, team_paid_amt, wcc_amt").execute()
    
    if res.data:
        df = pd.DataFrame(res.data)
        
        # Line 1 Calculations
        site_count = len(df)
        total_po = df['po_amt'].sum()
        
        # Line 2 Calculations (Team)
        t_bill = df['team_billing'].sum()
        t_paid = df['team_paid_amt'].sum()
        t_bal = t_bill - t_paid
        
        # Line 3 Calculations (Client/WCC)
        t_wcc = df['wcc_amt'].sum()
        t_rec = df['received_amt'].sum()
        t_bal_client = t_wcc - t_rec

        # --- DISPLAY ---
        st.markdown("### 📍 Project Summary")
        c1_1, c1_2 = st.columns(2)
        c1_1.metric("Total Site Count", f"{site_count}")
        c1_2.metric("Total PO Amt", f"₹ {total_po:,.0f}")
        
        st.divider()
        st.markdown("### 👥 Team & Vendor Status")
        c2_1, c2_2, c2_3 = st.columns(3)
        c2_1.metric("Total Team Billing", f"₹ {t_bill:,.0f}")
        c2_2.metric("Total Team Paid", f"₹ {t_paid:,.0f}")
        c2_3.metric("Total Team Balance", f"₹ {t_bal:,.0f}", delta=f"Pending", delta_color="inverse")
        
        st.divider()
        st.markdown("### 💳 Client Recovery (WCC)")
        c3_1, c3_2, c3_3 = st.columns(3)
        c3_1.metric("Total WCC Amt", f"₹ {t_wcc:,.0f}")
        c3_2.metric("Total Received Amt", f"₹ {t_rec:,.0f}")
        c3_3.metric("Total Balance", f"₹ {t_bal_client:,.0f}", delta=f"Receivable")
    else:
        st.info("No data available. Please add sites in the registry.")

# --- 5. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["👥 Client Master", "🛠️ Team Master"])
    
    with t1:
        with st.form("client_form", clear_on_submit=True):
            cn = st.text_input("New Client Name")
            cp = st.text_input("Contact Person")
            if st.form_submit_button("Register Client"):
                if cn:
                    supabase.table("client_master").insert({"client_name": cn, "contact_person": cp}).execute()
                    st.success("Client Added!")

    with t2:
        with st.form("team_form", clear_on_submit=True):
            tn = st.text_input("New Team Name")
            tl = st.text_input("Team Leader")
            if st.form_submit_button("Register Team"):
                if tn:
                    supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute()
                    st.success("Team Added!")

# --- 6. SITE DATA ENTRY ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registration</h1>", unsafe_allow_html=True)
    
    c_res = supabase.table("client_master").select("client_name").execute()
    t_res = supabase.table("team_master").select("team_name").execute()
    client_list = [c['client_name'] for c in c_res.data] if c_res.data else []
    team_list = [t['team_name'] for t in t_res.data] if t_res.data else []

    with st.form("site_entry_form", clear_on_submit=True):
        st.subheader("📍 Basic Details")
        r1_1, r1_2, r1_3 = st.columns(3)
        p_id = r1_1.text_input("Project ID")
        s_id = r1_2.text_input("Site ID")
        client = r1_3.selectbox("Client Name", ["Select"] + client_list)
        
        r2_1, r2_2, r2_3 = st.columns(3)
        cluster = r2_1.text_input("Cluster")
        work_desc = r2_2.text_area("Work Description", height=65)
        p_amt = r2_3.number_input("Project Amt", min_value=0.0)

        st.divider()
        st.subheader("📑 PO & Team Details")
        r3_1, r3_2, r3_3 = st.columns(3)
        po_no = r3_1.text_input("PO No")
        po_amt = r3_2.number_input("PO Amt", min_value=0.0)
        status = r3_3.selectbox("Status", ["Planning", "WIP", "WCC Done", "Closed"])

        r4_1, r4_2, r4_3 = st.columns(3)
        team = r4_1.selectbox("Assigned Team", ["Select"] + team_list)
        t_bill = r4_2.number_input("Team Billing", min_value=0.0)
        t_paid = r4_3.number_input("Team Paid Amt", min_value=0.0)

        st.divider()
        st.subheader("💳 WCC & Finance")
        r5_1, r5_2, r5_3 = st.columns(3)
        wcc_n = r5_1.text_input("WCC No.")
        wcc_a = r5_2.number_input("WCC Amt", min_value=0.0)
        rec_a = r5_3.number_input("Received Amt", min_value=0.0)

        if st.form_submit_button("🚀 SYNC TO CLOUD"):
            if s_id and client != "Select":
                data = {
                    "project_id": p_id, "site_id": s_id, "site_name": client, "cluster": cluster,
                    "work_description": work_desc, "project_amt": p_amt, "po_no": po_no,
                    "po_amt": po_amt, "site_status": status, "team_name": team,
                    "team_billing": t_bill, "team_paid_amt": t_paid, "wcc_no": wcc_n,
                    "wcc_amt": wcc_a, "received_amt": rec_a
                }
                supabase.table("site_data").insert(data).execute()
                st.success("Site Recorded!")
            else: st.error("Site ID and Client mandatory.")

# --- 7. FINANCE LEDGER ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    with st.form("finance_form", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        fr = f1.text_input("Received From")
        to = f2.text_input("Paid To")
        dt = f3.date_input("Date", datetime.now())
        f4, f5 = st.columns(2)
        ra = f4.number_input("Received Amt", min_value=0.0)
        pa = f5.number_input("Paid Amt", min_value=0.0)
        if st.form_submit_button("Record Transaction"):
            f_data = {"received_from": fr, "paid_to": to, "transaction_date": str(dt), "received_amt": ra, "paid_amount": pa}
            supabase.table("finance").insert(f_data).execute()
            st.success("Logged!")

st.markdown("<div class='elegant-footer'>Visiontech Automation © 2026</div>", unsafe_allow_html=True)
