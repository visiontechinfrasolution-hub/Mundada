import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- AUTO INSTALL OPENPYXL FOR EXCEL UPLOAD ---
import subprocess
import sys
try:
    import openpyxl
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "openpyxl"])
    import openpyxl

# --- 1. PAGE CONFIG & LAVISH CLEAN STYLE ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; }
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 15px; padding: 20px; border-left: 5px solid #0ea5e9; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    .stButton>button { background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white !important; border-radius: 10px; font-weight: 700; }
    div.stForm { background: #ffffff; border-radius: 20px; border: 1px solid #e2e8f0; padding: 30px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
    .balance-box { padding: 15px; border-radius: 10px; background-color: #eff6ff; border: 1px solid #dbeafe; margin-top: 10px; color: #1e40af; font-weight: 600; }
    .section-header { color: #1e293b; font-weight: 700; margin: 25px 0 15px 0; font-size: 1.2rem; border-bottom: 1px solid #f1f5f9; padding-bottom: 5px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE CONNECTION ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"
supabase = create_client(URL, KEY)

# --- 3. HELPERS ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# --- 4. SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger", "👥 Team Ledger"], key="nav_page")
    st.info(f"User: Mayur Patil\nDate: 29-Apr-2026")

# --- 5. DASHBOARD ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        s_res = supabase.table("site_data").select("*").execute()
        f_res = supabase.table("finance").select("*").execute()
        if s_res.data:
            df_s = pd.DataFrame(s_res.data)
            df_f = pd.DataFrame(f_res.data) if f_res.data else pd.DataFrame(columns=['received_from', 'received_amt'])
            
            st.markdown("### 📍 Summary")
            c1, c2 = st.columns(2)
            c1.metric("Total Site Count", len(df_s))
            c2.metric("Total PO Amt", f"₹ {df_s['po_amt'].sum():,.0f}")
            
            st.divider()
            st.markdown("### 👥 Team Status")
            c2_1, c2_2, c2_3 = st.columns(3)
            t_bill, t_paid = df_s['team_billing'].sum(), df_s['team_paid_amt'].sum()
            c2_1.metric("Total Team Billing", f"₹ {t_bill:,.0f}")
            c2_2.metric("Total Team Paid", f"₹ {t_paid:,.0f}")
            c2_3.metric("Total Team Balance", f"₹ {t_bill - t_paid:,.0f}")
            
            st.divider()
            st.markdown("### 💳 WCC & Client Recovery")
            c3_1, c3_2, c3_3 = st.columns(3)
            wcc_tot, rec_tot = df_s['wcc_amt'].sum(), df_s['received_amt'].sum()
            c3_1.metric("Total WCC Amt", f"₹ {wcc_tot:,.0f}")
            c3_2.metric("Total Received Amt", f"₹ {rec_tot:,.0f}")
            c3_3.metric("WCC Pending Balance", f"₹ {wcc_tot - rec_tot:,.0f}")
    except: st.info("Dashboard loading...")

# --- 6. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["👥 Clients", "🛠️ Teams", "📁 Projects"])
    with tab1:
        with st.form("cl_reg"):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: 
                    supabase.table("client_master").insert({"client_name": cn}).execute()
                    st.success("Saved")
                    st.rerun()
        st.divider()
        st.subheader("👥 Registered Clients")
        c_res = supabase.table("client_master").select("*").execute()
        if c_res.data: st.dataframe(pd.DataFrame(c_res.data).drop(columns=['id'], errors='ignore'), use_container_width=True)
    with tab2:
        with st.form("tm_reg"):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save Team"):
                if tn: 
                    supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute()
                    st.success("Saved")
                    st.rerun()
        st.divider()
        st.subheader("🛠️ Registered Teams")
        t_res = supabase.table("team_master").select("*").execute()
        if t_res.data: st.dataframe(pd.DataFrame(t_res.data).drop(columns=['id'], errors='ignore'), use_container_width=True)
    with tab3:
        with st.form("pr_reg"):
            pn = st.text_input("Project Name")
            if st.form_submit_button("Save Project"):
                if pn:
                    # Is line par error tab aati hai jab Table database mein nahi hoti
                    supabase.table("project_master").insert({"project_name": pn}).execute()
                    st.success("Project Saved")
                    st.rerun()
        st.divider()
        st.subheader("📁 Registered Projects")
        try:
            p_res = supabase.table("project_master").select("*").execute()
            if p_res.data: st.dataframe(pd.DataFrame(p_res.data).drop(columns=['id'], errors='ignore'), use_container_width=True)
        except: st.warning("Please create 'project_master' table in Supabase SQL editor.")

# --- 7. SITE DATA ENTRY ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    if "edit_row_data" not in st.session_state: st.session_state.edit_row_data = None
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()
    
    t_res = supabase.table("team_master").select("team_name").execute()
    teams_list = ["Select"] + [t['team_name'] for t in t_res.data] if t_res.data else ["Select"]
    
    try:
        p_master = supabase.table("project_master").select("project_name").execute()
        projects_master_list = ["Select"] + [p['project_name'] for p in p_master.data] if p_master.data else ["Select"]
    except:
        projects_master_list = ["Select"]

    tc1, tc2, tc3, tc4 = st.columns([1, 1, 1.5, 2.5])
    if tc1.button("➕ New Site"): 
        st.session_state.edit_row_data = None
        st.rerun()
    if not df.empty: tc2.download_button("📥 Download", data=to_excel(df), file_name="Site_Data.xlsx")
    
    uploaded_file = tc3.file_uploader("📤 Bulk Upload", type=['xlsx'], label_visibility="collapsed")
    search = tc4.text_input("🔍 Search Database...", placeholder="Search Site ID, Project ID...")
    
    er = st.session_state.edit_row_data
    is_editing = er is not None
    
    with st.expander("📝 Project Details Form", expanded=True):
        with st.form("site_full_form", clear_on_submit=not is_editing):
            st.markdown('<div class="section-header">📍 1. Site Details</div>', unsafe_allow_html=True)
            sc1, sc2, sc3 = st.columns(3)
            
            p_val = er.get('project_name', 'Select') if is_editing else 'Select'
            p_idx = projects_master_list.index(p_val) if p_val in projects_master_list else 0
            sel_project = sc1.selectbox("Project", projects_master_list, index=p_idx)
            
            p_id = sc2.text_input("Project ID (Must be Unique) *", value=str(er['project_id']) if is_editing else "")
            s_id = sc3.text_input("Site ID", value=str(er['site_id']) if is_editing else "")
            
            sc4, sc5, sc6 = st.columns(3)
            s_nm = sc4.text_input("Site Name", value=str(er['site_name']) if is_editing else "")
            cluster = sc5.text_input("Cluster", value=str(er['cluster']) if is_editing else "")
            po_n = sc6.text_input("PO Number", value=str(er['po_no']) if is_editing else "")
            
            p_amt = st.number_input("Projected Amount", value=float(er['project_amt']) if is_editing and er['project_amt'] else 0.0)

            st.markdown('<div class="section-header">👥 2. Team Details</div>', unsafe_allow_html=True)
            tc1, tc2 = st.columns(2)
            t_idx = teams_list.index(er['team_name']) if is_editing and er['team_name'] in teams_list else 0
            t_name = tc1.selectbox("Team Name", teams_list, index=t_idx)
            
            st_list = ["Select", "Yet to Start", "WIP", "Completed"]
            s_idx = st_list.index(er['site_status']) if is_editing and er['site_status'] in st_list else 0
            status = tc2.selectbox("Site Status", st_list, index=s_idx)
            
            tc3, tc4 = st.columns(2)
            t_bill = tc3.number_input("Team Billing", value=float(er['team_billing']) if is_editing and er['team_billing'] else 0.0)
            t_paid = tc4.number_input("Team Paid Amount", value=float(er['team_paid_amt']) if is_editing and er['team_paid_amt'] else 0.0)
            
            st.markdown(f"<div class='balance-box'>Team Balance (Auto-calculated): ₹ {t_bill - t_paid:,.2f}</div>", unsafe_allow_html=True)

            st.markdown('<div class="section-header">📄 3. VIS Billing Details</div>', unsafe_allow_html=True)
            vc1, vc2 = st.columns(2)
            wcc_n = vc1.text_input("VIS Invoice No.", value=str(er['wcc_no']) if is_editing else "")
            vc3, vc4 = st.columns(2)
            wcc_a = vc3.number_input("VIS Bill Amount", value=float(er['wcc_amt']) if is_editing and er['wcc_amt'] else 0.0)
            r_amt = vc4.number_input("VIS Received Amt", value=float(er['received_amt']) if is_editing and er['received_amt'] else 0.0)
            
            st.markdown(f"<div class='balance-box'>VIS Balance (Auto-calculated): ₹ {wcc_a - r_amt:,.2f}</div>", unsafe_allow_html=True)
            
            if st.form_submit_button("💾 Save Project Data", use_container_width=True):
                data = {
                    "project_name": None if sel_project == "Select" else sel_project,
                    "project_id": p_id, "site_id": s_id, "site_name": s_nm, 
                    "cluster": cluster, "site_status": None if status == "Select" else status, 
                    "project_amt": p_amt, "po_no": po_n, "team_name": None if t_name == "Select" else t_name, 
                    "team_billing": t_bill, "team_paid_amt": t_paid, "wcc_no": wcc_n, 
                    "wcc_amt": wcc_a, "received_amt": r_amt
                }

                if is_editing: 
                    supabase.table("site_data").update(data).eq('id', er['id']).execute()
                    st.session_state.edit_row_data = None
                else: 
                    supabase.table("site_data").insert(data).execute()
                st.rerun()

    st.divider()
    if not df.empty:
        if search: df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        st.subheader("📋 Complete Site Database")
        edit_sel = st.selectbox("🎯 Select Project ID to EDIT", ["None"] + df['project_id'].tolist())
        if edit_sel != "None":
            st.session_state.edit_row_data = df[df['project_id'] == edit_sel].iloc[0].to_dict()
            st.rerun()
        st.dataframe(df.drop(columns=['id']), use_container_width=True)

# --- 8. FINANCE LEDGER ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    pay_type = st.radio("Select Payment Type", ["Payment Received", "Payment Paid"], horizontal=True, key="pay_type")
    
    s_res = supabase.table("site_data").select("project_id", "received_amt", "team_paid_amt", "team_billing").execute()
    projects = ["None"] + [s['project_id'] for s in s_res.data] if s_res.data else ["None"]
    
    f_all_res = supabase.table("finance").select("*").order("transaction_date", desc=True).execute()
    df_finance = pd.DataFrame(f_all_res.data) if f_all_res.data else pd.DataFrame()

    if pay_type == "Payment Received":
        c_res = supabase.table("client_master").select("client_name").execute()
        clients = ["Select"] + [c['client_name'] for c in c_res.data] if c_res.data else ["Select"]

        f_client = st.selectbox("Received From (Client)", clients)
        f_date = st.date_input("Date", datetime.now())
        f_amt = st.number_input("Received Amt", value=None)
        f_project = st.selectbox("Project ID", projects)
        
        if st.button("🚀 Submit Received Payment"):
            if f_client != "Select" and f_amt is not None:
                finance_data = {"received_from": f_client, "transaction_date": str(f_date), "received_amt": float(f_amt)}
                try:
                    supabase.table("finance").insert(finance_data).execute()
                    if f_project != "None":
                        current_row = next((item for item in s_res.data if item["project_id"] == f_project), None)
                        old_amt = float(current_row['received_amt']) if current_row and current_row['received_amt'] else 0.0
                        supabase.table("site_data").update({"received_amt": old_amt + float(f_amt)}).eq("project_id", f_project).execute()
                    st.success("Finance Ledger Updated!")
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    else:
        t_master_res = supabase.table("team_master").select("team_name").execute()
        teams_list = ["Select"] + [t['team_name'] for t in t_master_res.data] if t_master_res.data else ["Select"]
        p_team = st.selectbox("Paid To (Team Name)", teams_list)
        p_project = st.selectbox("Project ID", projects)
        
        if p_project != "None":
            site_info = next((item for item in s_res.data if item["project_id"] == p_project), None)
            if site_info:
                st.markdown(f"<div class='balance-box'>Balance: ₹ {float(site_info['team_billing']) - float(site_info['team_paid_amt']):,.0f}</div>", unsafe_allow_html=True)

        p_date = st.date_input("Date", datetime.now())
        p_amt = st.number_input("Paid Amt", value=None)
        
        if st.button("🚀 Submit Paid Payment"):
            if p_team != "Select" and p_amt is not None and p_project != "None":
                finance_data = {"received_from": p_team, "transaction_date": str(p_date), "paid_amount": float(p_amt)}
                try:
                    supabase.table("finance").insert(finance_data).execute()
                    current_row = next((item for item in s_res.data if item["project_id"] == p_project), None)
                    old_paid = float(current_row['team_paid_amt']) if current_row and current_row['team_paid_amt'] else 0.0
                    supabase.table("site_data").update({"team_paid_amt": old_paid + float(p_amt)}).eq("project_id", p_project).execute()
                    st.success("Payment recorded!")
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

# --- 9. TEAM LEDGER ---
elif page == "👥 Team Ledger":
    st.markdown("<h1>👥 Team Wise Billing & Balance</h1>", unsafe_allow_html=True)
    s_res = supabase.table("site_data").select("team_name", "team_billing", "team_paid_amt").execute()
    if s_res.data:
        df = pd.DataFrame(s_res.data)
        team_df = df.groupby('team_name', as_index=False).sum()
        team_df['Balance'] = team_df['team_billing'] - team_df['team_paid_amt']
        st.dataframe(team_df, use_container_width=True)
        st.download_button("📥 Download Report", data=to_excel(team_df), file_name="Team_Wise_Report.xlsx")
        
