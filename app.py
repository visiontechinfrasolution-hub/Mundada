import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

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
    div.stForm { background: rgba(255, 255, 255, 0.7); backdrop-filter: blur(15px); border-radius: 25px; border: 1px solid #ffffff; padding: 40px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.08); margin-top: 20px; }
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

# --- 3. HELPER FUNCTION FOR EXCEL ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# --- 4. SIDEBAR NAVIGATION ---
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
    st.info(f"User: Mayur Patil")

# --- 5. DASHBOARD ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        res = supabase.table("site_data").select("po_amt, received_amt, team_billing, team_paid_amt, wcc_amt").execute()
        if res.data:
            df = pd.DataFrame(res.data)
            st.markdown("### 📍 Project Summary")
            c1_1, c1_2 = st.columns(2)
            c1_1.metric("Total Site Count", f"{len(df)}")
            c1_2.metric("Total PO Amt", f"₹ {df['po_amt'].sum():,.0f}")
            st.divider()
            st.markdown("### 👥 Team & Vendor Status")
            c2_1, c2_2, c2_3 = st.columns(3)
            c2_1.metric("Total Team Billing", f"₹ {df['team_billing'].sum():,.0f}")
            c2_2.metric("Total Team Paid", f"₹ {df['team_paid_amt'].sum():,.0f}")
            c2_3.metric("Total Team Balance", f"₹ {(df['team_billing'].sum() - df['team_paid_amt'].sum()):,.0f}", delta_color="inverse")
            st.divider()
            st.markdown("### 💳 Client Recovery (WCC)")
            c3_1, c3_2, c3_3 = st.columns(3)
            c3_1.metric("Total WCC Amt", f"₹ {df['wcc_amt'].sum():,.0f}")
            c3_2.metric("Total Received Amt", f"₹ {df['received_amt'].sum():,.0f}")
            c3_3.metric("Total Balance", f"₹ {(df['wcc_amt'].sum() - df['received_amt'].sum()):,.0f}")
        else: st.info("No data available.")
    except Exception as e: st.error(f"Dashboard Error: {e}")

# --- 6. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["👥 Client Master", "🛠️ Team Master"])
    
    with t1:
        with st.form("client_form", clear_on_submit=True):
            cn = st.text_input("New Client Name")
            cp = st.text_input("Contact Person")
            if st.form_submit_button("Register Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn, "contact_person": cp}).execute()
                st.success("Client Registered!")
        st.divider()
        c_data = supabase.table("client_master").select("*").execute()
        if c_data.data:
            df_c = pd.DataFrame(c_data.data).drop(columns=['id'], errors='ignore')
            search_c = st.text_input("🔍 Search Client Records")
            if search_c: df_c = df_c[df_c.astype(str).apply(lambda x: x.str.contains(search_c, case=False)).any(axis=1)]
            st.dataframe(df_c, use_container_width=True)
            st.download_button("📥 Download Excel", data=to_excel(df_c), file_name="Client_Master.xlsx")

    with t2:
        with st.form("team_form", clear_on_submit=True):
            tn = st.text_input("New Team Name")
            tl = st.text_input("Team Leader")
            if st.form_submit_button("Register Team"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute()
                st.success("Team Registered!")
        st.divider()
        t_data = supabase.table("team_master").select("*").execute()
        if t_data.data:
            df_t = pd.DataFrame(t_data.data).drop(columns=['id'], errors='ignore')
            search_t = st.text_input("🔍 Search Team Records")
            if search_t: df_t = df_t[df_t.astype(str).apply(lambda x: x.str.contains(search_t, case=False)).any(axis=1)]
            st.dataframe(df_t, use_container_width=True)
            st.download_button("📥 Download Excel", data=to_excel(df_t), file_name="Team_Master.xlsx")

# --- 7. SITE DATA ENTRY ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registration</h1>", unsafe_allow_html=True)
    c_res = supabase.table("client_master").select("client_name").execute()
    t_res = supabase.table("team_master").select("team_name").execute()
    client_list = [c['client_name'] for c in c_res.data] if c_res.data else []
    team_list = [t['team_name'] for t in t_res.data] if t_res.data else []

    with st.form("site_entry_form", clear_on_submit=True):
        r1_1, r1_2, r1_3 = st.columns(3)
        p_id, s_id, client = r1_1.text_input("Project ID"), r1_2.text_input("Site ID"), r1_3.selectbox("Client Name", ["Select"] + client_list)
        r2_1, r2_2, r2_3 = st.columns(3)
        cluster, work_desc, p_amt = r2_1.text_input("Cluster"), r2_2.text_area("Work Description", height=65), r2_3.number_input("Project Amt", min_value=0.0)
        st.divider()
        r3_1, r3_2, r3_3 = st.columns(3)
        po_no, po_amt, status = r3_1.text_input("PO No"), r3_2.number_input("PO Amt", min_value=0.0), r3_3.selectbox("Status", ["Planning", "WIP", "WCC Done", "Closed"])
        r4_1, r4_2, r4_3 = st.columns(3)
        team, t_bill, t_paid = r4_1.selectbox("Assigned Team", ["Select"] + team_list), r4_2.number_input("Team Billing", min_value=0.0), r4_3.number_input("Team Paid Amt", min_value=0.0)
        st.divider()
        r5_1, r5_2, r5_3 = st.columns(3)
        wcc_n, wcc_a, rec_a = r5_1.text_input("WCC No."), r5_2.number_input("WCC Amt", min_value=0.0), r5_3.number_input("Received Amt", min_value=0.0)
        if st.form_submit_button("🚀 SYNC TO CLOUD"):
            if s_id and client != "Select":
                data = {"project_id": p_id, "site_id": s_id, "site_name": client, "cluster": cluster, "work_description": work_desc, "project_amt": p_amt, "po_no": po_no, "po_amt": po_amt, "site_status": status, "team_name": team, "team_billing": t_bill, "team_paid_amt": t_paid, "wcc_no": wcc_n, "wcc_amt": wcc_a, "received_amt": rec_a}
                supabase.table("site_data").insert(data).execute()
                st.success("Site Recorded!")
            else: st.error("Site ID and Client mandatory.")
    
    st.divider()
    st.subheader("📂 Registered Site Records")
    s_data = supabase.table("site_data").select("*").execute()
    if s_data.data:
        df_s = pd.DataFrame(s_data.data).drop(columns=['id'], errors='ignore')
        search_s = st.text_input("🔍 Search Site Database")
        if search_s: df_s = df_s[df_s.astype(str).apply(lambda x: x.str.contains(search_s, case=False)).any(axis=1)]
        st.dataframe(df_s, use_container_width=True)
        st.download_button("📥 Download Database Excel", data=to_excel(df_s), file_name="Site_Database.xlsx")

# --- 8. FINANCE LEDGER ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    
    # Fetch data for dropdowns
    c_res = supabase.table("client_master").select("client_name").execute()
    t_res = supabase.table("team_master").select("team_name").execute()
    client_list = [c['client_name'] for c in c_res.data] if c_res.data else []
    team_list = [t['team_name'] for t in t_res.data] if t_res.data else []

    with st.form("finance_form", clear_on_submit=True):
        f1, f2, f3 = st.columns(3)
        # Dropdown for Client (Received From)
        fr = f1.selectbox("Received From (Client)", ["Select Client"] + client_list)
        # Dropdown for Team (Paid To)
        to = f2.selectbox("Paid To (Team)", ["Select Team"] + team_list)
        dt = f3.date_input("Date", datetime.now())
        
        f4, f5 = st.columns(2)
        ra = f4.number_input("Received Amt", min_value=0.0)
        pa = f5.number_input("Paid Amt", min_value=0.0)
        
        if st.form_submit_button("Record Transaction"):
            if fr != "Select Client" and to != "Select Team":
                f_data = {"received_from": fr, "paid_to": to, "transaction_date": str(dt), "received_amt": ra, "paid_amount": pa}
                supabase.table("finance").insert(f_data).execute()
                st.success("Transaction Logged!")
            else:
                st.error("Please select both Client and Team.")
            
    st.divider()
    st.subheader("💰 Transaction Ledger")
    f_res = supabase.table("finance").select("*").execute()
    if f_res.data:
        df_f = pd.DataFrame(f_res.data).drop(columns=['id'], errors='ignore')
        search_f = st.text_input("🔍 Search Transaction History")
        if search_f:
            df_f = df_f[df_f.astype(str).apply(lambda x: x.str.contains(search_f, case=False)).any(axis=1)]
        st.dataframe(df_f, use_container_width=True)
        st.download_button("📥 Download Ledger Excel", data=to_excel(df_f), file_name="Finance_Ledger.xlsx")

st.markdown("<div class='elegant-footer'>Visiontech Automation © 2026</div>", unsafe_allow_html=True)
