import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime

# --- 1. PREMIUM PAGE CONFIG ---
st.set_page_config(
    page_title="Visiontech Mundada | Elegant Portal",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE ELEGANT LIGHT UI STYLE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); color: #2d3436; }
    h1 { font-weight: 800; letter-spacing: -1.5px; color: #0984e3; margin-bottom: 10px; }
    h2, h3 { color: #2d3436; font-weight: 600; }
    [data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e1e4e8; }
    div[data-testid="stMetric"] { background: #ffffff; border: 1px solid #e1e4e8; border-radius: 20px; padding: 25px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); transition: all 0.3s ease; }
    div[data-testid="stMetric"]:hover { transform: translateY(-5px); box-shadow: 0 15px 35px rgba(9, 132, 227, 0.15); border-color: #0984e3; }
    [data-testid="stMetricValue"] > div { color: #0984e3 !important; font-weight: 800; }
    div.stForm { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 25px; border: 1px solid #ffffff; padding: 40px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); margin-top: 20px; }
    .stButton>button { background: linear-gradient(135deg, #0984e3 0%, #00cec9 100%); color: white; border: none; padding: 15px; border-radius: 12px; font-weight: 700; transition: all 0.4s ease; box-shadow: 0 4px 15px rgba(9, 132, 227, 0.3); width: 100%; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(9, 132, 227, 0.4); }
    .elegant-footer { text-align: center; padding: 40px; color: #636e72; font-size: 14px; letter-spacing: 0.5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SUPABASE CONNECTION ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"

@st.cache_resource
def get_supabase():
    return create_client(URL, KEY)

supabase = get_supabase()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3; font-size: 28px;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align: center; color: #636e72; font-weight: 600; margin-bottom: 30px;'>OPERATIONS PORTAL</div>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", [
        "🏠 Dashboard", 
        "📝 Master Registration", 
        "🏗️ Site Data Entry", 
        "💸 Finance Ledger"
    ])
    st.divider()
    st.info(f"User: Mayur Patil\n\nDate: {datetime.now().strftime('%d-%m-%Y')}")

# --- 5. DASHBOARD PAGE (LIVE ANALYTICS) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    
    # Fetch Data for Metrics
    res = supabase.table("site_data").select("po_amt, received_amt, team_billing, team_paid_amt").execute()
    
    if res.data:
        df = pd.DataFrame(res.data)
        total_po = df['po_amt'].sum()
        total_rec = df['received_amt'].sum()
        total_bill = df['team_billing'].sum()
        total_paid = df['team_paid_amt'].sum()
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total PO Value", f"₹ {total_po:,.0f}")
        m2.metric("Total Received", f"₹ {total_rec:,.0f}")
        m3.metric("Client Pending", f"₹ {total_po - total_rec:,.0f}")
        m4.metric("Team Payable", f"₹ {total_bill - total_paid:,.0f}")
        
        st.divider()
        st.subheader("Collection vs Target")
        progress = (total_rec / total_po) if total_po > 0 else 0
        st.progress(progress)
        st.write(f"Overall Collection Efficiency: **{progress*100:.1f}%**")
    else:
        st.info("Start by registering sites to see live metrics.")

# --- 6. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Client Master", "🛠️ Team Master"])
    
    with tab1:
        with st.form("client_master_form", clear_on_submit=True):
            st.subheader("Add New Client")
            cn = st.text_input("Client/Company Name")
            cp = st.text_input("Contact Person")
            if st.form_submit_button("Register Client"):
                if cn:
                    supabase.table("client_master").insert({"client_name": cn, "contact_person": cp}).execute()
                    st.success(f"Client {cn} Added!")
                else: st.error("Name is required")

    with tab2:
        with st.form("team_master_form", clear_on_submit=True):
            st.subheader("Add New Team")
            tn = st.text_input("Team/Agency Name")
            tl = st.text_input("Team Leader")
            if st.form_submit_button("Register Team"):
                if tn:
                    supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute()
                    st.success(f"Team {tn} Added!")
                else: st.error("Name is required")

# --- 7. SITE DATA ENTRY (RESTORED ALL COLUMNS) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registration</h1>", unsafe_allow_html=True)
    
    # Fetch Dropdown Data
    c_res = supabase.table("client_master").select("client_name").execute()
    t_res = supabase.table("team_master").select("team_name").execute()
    clients = [c['client_name'] for c in c_res.data] if c_res.data else []
    teams = [t['team_name'] for t in t_res.data] if t_res.data else []

    with st.form("site_entry_full", clear_on_submit=True):
        st.subheader("📍 Site & Project Basics")
        c1, c2, c3 = st.columns(3)
        p_id = c1.text_input("Project ID")
        s_id = c2.text_input("Site ID")
        s_name = c3.selectbox("Client Name (From Master)", ["Select Client"] + clients)
        
        c4, c5, c6 = st.columns(3)
        cluster = c4.text_input("Cluster")
        work_desc = c5.text_area("Work Description", height=65)
        proj_amt = c6.number_input("Project Amount", min_value=0.0)

        st.divider()
        st.subheader("📑 PO & Team Assignment")
        c7, c8, c9 = st.columns(3)
        po_no = c7.text_input("PO No")
        po_amt = c8.number_input("PO Amount", min_value=0.0)
        status = c9.selectbox("Status", ["Planning", "Execution", "WCC Process", "Closed"])

        c10, c11, c12 = st.columns(3)
        team_sel = c10.selectbox("Assigned Team", ["Select Team"] + teams)
        t_bill = c11.number_input("Team Billing", min_value=0.0)
        t_paid = c12.number_input("Team Paid Amt", min_value=0.0)

        st.divider()
        st.subheader("💳 WCC & Finance")
        c13, c14, c15 = st.columns(3)
        wcc_no = c13.text_input("WCC No.")
        wcc_amt = c14.number_input("WCC Amt", min_value=0.0)
        rec_amt = c15.number_input("Received Amt", min_value=0.0)

        if st.form_submit_button("🚀 SYNC COMPLETE DATA"):
            if s_id != "" and s_name != "Select Client":
                entry = {
                    "project_id": p_id, "site_id": s_id, "site_name": s_name,
                    "cluster": cluster, "work_description": work_desc, "project_amt": proj_amt,
                    "po_no": po_no, "po_amt": po_amt, "site_status": status,
                    "team_name": team_sel, "team_billing": t_bill, "team_paid_amt": t_paid,
                    "wcc_no": wcc_no, "wcc_amt": wcc_amt, "received_amt": rec_amt
                }
                supabase.table("site_data").insert(entry).execute()
                st.success(f"Site {s_id} Synced Successfully!")
            else: st.error("Site ID and Client Name are mandatory!")

# --- 8. FINANCE LEDGER (FULL FORM) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    
    with st.form("finance_ledger_form", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        payer = f1.text_input("Received From (Payer)")
        payee = f2.text_input("Paid To (Payee)")
        fdate = f3.date_input("Date", datetime.now())
        
        st.divider()
        f4, f5 = st.columns(2)
        ramt = f4.number_input("Received Amount (+)", min_value=0.0)
        pamt = f5.number_input("Paid Amount (-)", min_value=0.0)
        
        remarks = st.text_input("Transaction Note")
        
        if st.form_submit_button("📝 LOG TRANSACTION"):
            fdata = {"received_from": payer, "paid_to": payee, "transaction_date": str(fdate), "received_amt": ramt, "paid_amount": pamt}
            supabase.table("finance").insert(fdata).execute()
            st.success("Transaction Logged!")

st.markdown("<div class='elegant-footer'>Visiontech Automation © 2026 • Mundada Portal</div>", unsafe_allow_html=True)
