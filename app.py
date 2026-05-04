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

# --- 1. PAGE CONFIG & ATTRACTIVE COLORFUL STYLE ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; }
    
    /* UNIVERSAL DARK BORDER FOR ALL INPUTS */
    div[data-baseweb="input"], div[data-baseweb="select"], div[data-baseweb="textarea"], .stNumberInput div {
        border: 2px solid #1e293b !important;
        border-radius: 8px !important;
    }

    /* SPECIFIC DARK BORDER FOR NUMBER INPUTS (RED DARK) */
    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        border: 2px solid #b91c1c !important;
        border-radius: 8px !important;
    }

    /* Dark text for visibility */
    input, textarea, div[role="button"] {
        color: #0f172a !important;
        font-weight: 600 !important;
    }

    /* Systematic Popup Styling */
    div[data-testid="stDialog"] div[role="dialog"] {
        border-radius: 20px;
        padding: 20px;
        background-color: #ffffff;
        border: 3px solid #0ea5e9;
    }

    /* Add New Site Button (Red Style) */
    .stButton > button[key="add_new_btn"] {
        background: linear-gradient(135deg, #ef4444 0%, #991b1b 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px 24px !important;
        font-weight: 800 !important;
        border: none !important;
        box-shadow: 0 4px 15px rgba(239, 68, 68, 0.3);
    }

    /* Section Headers - Colorful */
    .section-header-1 { color: #0284c7; font-weight: 800; margin-top: 20px; font-size: 1.3rem; border-left: 5px solid #0284c7; padding-left: 10px; background: #f0f9ff; }
    .section-header-2 { color: #7c3aed; font-weight: 800; margin-top: 20px; font-size: 1.3rem; border-left: 5px solid #7c3aed; padding-left: 10px; background: #f5f3ff; }
    .section-header-3 { color: #059669; font-weight: 800; margin-top: 20px; font-size: 1.3rem; border-left: 5px solid #059669; padding-left: 10px; background: #ecfdf5; }
    
    .balance-box { padding: 12px; border-radius: 10px; background-color: #1e293b; color: #ffffff; font-weight: 700; margin-top: 15px; border: 2px solid #0ea5e9; text-align: center; }
    
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 15px; padding: 20px; border: 2px solid #e2e8f0; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
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
            
            c1, c2 = st.columns(2)
            c1.metric("Total Site Count", len(df_s))
            c2.metric("Total PO Amt", f"₹ {df_s['po_amt'].sum():,.0f}")
            
            st.divider()
            c2_1, c2_2, c2_3 = st.columns(3)
            t_bill, t_paid = df_s['team_billing'].sum(), df_s['team_paid_amt'].sum()
            c2_1.metric("Total Team Billing", f"₹ {t_bill:,.0f}")
            c2_2.metric("Total Team Paid", f"₹ {t_paid:,.0f}")
            c2_3.metric("Total Team Balance", f"₹ {t_paid - t_bill:,.0f}")
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
        t_res = supabase.table("team_master").select("*").execute()
        if t_res.data: st.dataframe(pd.DataFrame(t_res.data).drop(columns=['id'], errors='ignore'), use_container_width=True)
    with tab3:
        with st.form("pr_reg"):
            pn = st.text_input("Project Name")
            if st.form_submit_button("Save Project"):
                if pn:
                    try:
                        supabase.table("project_master").insert({"project_name": pn}).execute()
                        st.success("Project Saved")
                        st.rerun()
                    except Exception as e: st.error(f"Error: {e}")
        st.divider()
        try:
            p_res = supabase.table("project_master").select("*").execute()
            if p_res.data: st.dataframe(pd.DataFrame(p_res.data).drop(columns=['id'], errors='ignore'), use_container_width=True)
        except: st.warning("Project Master table loading...")

# --- 7. SITE DATA ENTRY (FORCED CALCULATION FIX & NEW LAYOUT) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    
    @st.dialog("📝 Project Details Form", width="large")
    def open_popup_form(edit_data=None):
        is_editing = edit_data is not None
        er = edit_data if is_editing else {}
        
        t_res = supabase.table("team_master").select("team_name").execute()
        teams_list = ["Select"] + [t['team_name'] for t in t_res.data] if t_res.data else ["Select"]
        p_master = supabase.table("project_master").select("project_name").execute()
        projects_master_list = ["Select"] + [p['project_name'] for p in p_master.data] if p_master.data else ["Select"]

        st.markdown('<div class="section-header-1">📍 1. Site Details</div>', unsafe_allow_html=True)
        sc1, sc2, sc3 = st.columns(3)
        p_val = er.get('project_name', 'Select')
        sel_project = sc1.selectbox("Project", projects_master_list, index=projects_master_list.index(p_val) if p_val in projects_master_list else 0)
        p_id = sc2.text_input("Project ID (Must be Unique) *", value=str(er.get('project_id', '')))
        s_id = sc3.text_input("Site ID", value=str(er.get('site_id', '')))
        
        sc4, sc5, sc6 = st.columns(3)
        s_nm = sc4.text_input("Site Name", value=str(er.get('site_name', '')))
        cluster = sc5.text_input("Cluster", value=str(er.get('cluster', '')))
        po_n = sc6.text_input("PO Number", value=str(er.get('po_no', '')))
        
        p_amt = st.number_input("Projected Amount", value=float(er['project_amt']) if is_editing and er.get('project_amt') is not None else None, placeholder="Enter amount")
        w_desc = st.text_area("Work Description", value=str(er.get('work_description', '')), placeholder="Enter full work details here...")

        st.markdown('<div class="section-header-2">👥 2. Team Details</div>', unsafe_allow_html=True)
        tc1, tc2 = st.columns(2)
        t_name_val = er.get('team_name', 'Select')
        t_name = tc1.selectbox("Team Name", teams_list, index=teams_list.index(t_name_val) if t_name_val in teams_list else 0)
        st_list = ["Select", "Pending", "Yet to Start", "WIP", "Completed"]
        status_val = er.get('site_status', 'Select')
        status = tc2.selectbox("Site Status", st_list, index=st_list.index(status_val) if status_val in st_list else 0)
        
        tc3, tc4 = st.columns(2)
        t_bill = tc3.number_input("Team Billing", value=float(er['team_billing']) if is_editing and er.get('team_billing') is not None else None, placeholder="Enter amount")
        t_paid = tc4.number_input("Team Paid Amount", value=float(er['team_paid_amt']) if is_editing and er.get('team_paid_amt') is not None else None, placeholder="Enter amount")
        
        calc_t_bill = t_bill if t_bill is not None else 0.0
        calc_t_paid = t_paid if t_paid is not None else 0.0
        st.markdown(f"<div class='balance-box'>Team Balance (Auto-calculated): ₹ {calc_t_paid - calc_t_bill:,.2f}</div>", unsafe_allow_html=True)

        st.markdown('<div class="section-header-3">📄 3. VIS Billing Details</div>', unsafe_allow_html=True)
        vc1, vc2 = st.columns(2)
        wcc_n = vc1.text_input("VIS Invoice No.", value=str(er.get('wcc_no', '')))
        r_amt = vc2.number_input("VIS Received Amt", value=float(er['received_amt']) if is_editing and er.get('received_amt') is not None else None, placeholder="Enter amount")
        
        wcc_a = st.number_input("VIS Bill Amount", value=float(er['wcc_amt']) if is_editing and er.get('wcc_amt') is not None else None, placeholder="Enter amount")
        
        calc_wcc_a = wcc_a if wcc_a is not None else 0.0
        calc_r_amt = r_amt if r_amt is not None else 0.0
        st.markdown(f"<div class='balance-box'>VIS Balance (Auto-calculated): ₹ {calc_wcc_a - calc_r_amt:,.2f}</div>", unsafe_allow_html=True)
        
        st.write("")
        if st.button("🚀 SAVE PROJECT DATA", use_container_width=True):
            data = {
                "project_name": None if sel_project == "Select" else sel_project,
                "project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, 
                "site_status": None if status == "Select" else status, "project_amt": p_amt or 0, "po_no": po_n, 
                "team_name": None if t_name == "Select" else t_name, "team_billing": t_bill or 0, 
                "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0,
                "work_description": w_desc
            }
            if is_editing: supabase.table("site_data").update(data).eq('id', er['id']).execute()
            else: supabase.table("site_data").insert(data).execute()
            st.rerun()

    # ACTION BAR
    res = supabase.table("site_data").select("*").execute()
    df_raw = pd.DataFrame(res.data) if res.data else pd.DataFrame()
    
    if not df_raw.empty:
        cols_order = ['project_name'] + [c for c in df_raw.columns if c not in ['project_name', 'id']] + ['id']
        df_display = df_raw[cols_order]
    else:
        df_display = df_raw

    c_add, c_down, c_up, c_search = st.columns([1.2, 1.2, 2.3, 2.5])
    with c_add:
        if st.button("➕ Add New Site", key="add_new_btn"):
            open_popup_form()

    with c_down:
        if not df_display.empty: st.download_button("📥 Excel Download", data=to_excel(df_display.drop(columns=['id'], errors='ignore')), file_name="Site_Data.xlsx", use_container_width=True)

    with c_up:
        uploaded_file = st.file_uploader("Upload XLSX", type=['xlsx'], label_visibility="collapsed")
        if uploaded_file:
            if st.button("Confirm Bulk Upload", use_container_width=True):
                try:
                    df_up = pd.read_excel(uploaded_file)
                    for col in ['id', 'team_balance', 'balance_amt', 'created_at']:
                        if col in df_up.columns: df_up = df_up.drop(columns=[col])
                    records = [{k: (None if pd.isna(v) else v) for k, v in row.items()} for row in df_up.to_dict(orient="records")]
                    supabase.table("site_data").insert(records).execute()
                    st.success("Uploaded!")
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

    search = c_search.text_input("🔍 Search Database...", placeholder="Search Project, Site ID...")

    st.divider()
    if not df_display.empty:
        df_filtered = df_display.copy()
        if search: df_filtered = df_filtered[df_filtered.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        st.subheader("📋 Complete Site Database")
        edit_sel = st.selectbox("🎯 Select Project ID to EDIT", ["None"] + df_filtered['project_id'].tolist())
        if edit_sel != "None":
            edit_row = df_raw[df_raw['project_id'] == edit_sel].iloc[0].to_dict()
            if st.button("🛠️ Open Systematic Editor"):
                open_popup_form(edit_row)
        
        st.dataframe(df_filtered.drop(columns=['id'], errors='ignore'), use_container_width=True)

# --- 8. FINANCE LEDGER ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    pay_type = st.radio("Payment Type", ["Payment Received", "Payment Paid"], horizontal=True)
    s_res = supabase.table("site_data").select("project_id", "received_amt", "team_paid_amt", "team_billing").execute()
    projects = ["None"] + [s['project_id'] for s in s_res.data] if s_res.data else ["None"]

    if pay_type == "Payment Received":
        with st.form("recv_form"):
            f_client = st.text_input("From Client")
            f_amt = st.number_input("Amount", value=None, placeholder="Enter amount")
            f_project = st.selectbox("Project ID", projects)
            if st.form_submit_button("Submit"):
                if f_amt and f_amt > 0:
                    supabase.table("finance").insert({"received_from": f_client, "received_amt": f_amt}).execute()
                    st.success("Recorded")
                    st.rerun()
    else:
        with st.form("paid_form"):
            p_team = st.text_input("To Team")
            p_amt = st.number_input("Amount", value=None, placeholder="Enter amount")
            p_project = st.selectbox("Project ID", projects)
            if st.form_submit_button("Submit"):
                if p_amt:
                    supabase.table("finance").insert({"received_from": p_team, "paid_amount": p_amt}).execute()
                    st.success("Recorded")
                    st.rerun()

# --- 9. TEAM LEDGER ---
elif page == "👥 Team Ledger":
    st.markdown("<h1>👥 Team Ledger</h1>", unsafe_allow_html=True)
    s_res = supabase.table("site_data").select("team_name", "team_billing", "team_paid_amt").execute()
    if s_res.data:
        df = pd.DataFrame(s_res.data)
        team_df = df.groupby('team_name').sum().reset_index()
        team_df['Balance'] = team_df['team_paid_amt'] - team_df['team_billing']
        st.dataframe(team_df, use_container_width=True)
