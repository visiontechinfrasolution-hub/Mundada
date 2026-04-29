import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & LAVISH CLEAN STYLE ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; }
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 15px; padding: 20px; border-left: 5px solid #0ea5e9; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    .stButton>button { background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white !important; border-radius: 10px; font-weight: 700; }
    div.stForm { background: #f8fafc; border-radius: 20px; border: 1px solid #e2e8f0; padding: 30px; }
    .balance-box { padding: 10px; border-radius: 10px; background-color: #fef2f2; border: 1px solid #fee2e2; margin-bottom: 20px; }
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
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
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
            
            st.divider()
            st.markdown("### 💰 Recovery Breakdown")
            c4_1, c4_2 = st.columns(2)
            m_amt = df_f[df_f['received_from'].str.contains("dilip mundada", case=False, na=False)]['received_amt'].astype(float).sum()
            i_amt = df_f[df_f['received_from'].str.contains("indus tower", case=False, na=False)]['received_amt'].astype(float).sum()
            c4_1.metric("Total Recv. From Dilip Mundada", f"₹ {m_amt:,.0f}")
            c4_2.metric("Total Recv. From Indus Towers", f"₹ {i_amt:,.0f}")
    except: st.info("Dashboard loading...")

# --- 6. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with tab1:
        with st.form("cl_reg"):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved"); st.rerun()
        st.divider()
        st.subheader("👥 Registered Clients")
        c_res = supabase.table("client_master").select("*").execute()
        if c_res.data: st.dataframe(pd.DataFrame(c_res.data).drop(columns=['id'], errors='ignore'), use_container_width=True)
    with tab2:
        with st.form("tm_reg"):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save Team"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute(); st.success("Saved"); st.rerun()
        st.divider()
        st.subheader("🛠️ Registered Teams")
        t_res = supabase.table("team_master").select("*").execute()
        if t_res.data: st.dataframe(pd.DataFrame(t_res.data).drop(columns=['id'], errors='ignore'), use_container_width=True)

# --- 7. SITE DATA ENTRY ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    if "edit_row_data" not in st.session_state: st.session_state.edit_row_data = None
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()
    t_res = supabase.table("team_master").select("team_name").execute()
    teams_list = ["Select"] + [t['team_name'] for t in t_res.data] if t_res.data else ["Select"]
    tc1, tc2, tc3, tc4 = st.columns([1, 1, 1.5, 2.5])
    if tc1.button("➕ New Site"): 
        st.session_state.edit_row_data = None
        st.rerun()
    if not df.empty: tc2.download_button("📥 Download", data=to_excel(df), file_name="Site_Data.xlsx")
    uploaded_file = tc3.file_uploader("📤 Bulk Upload", type=['xlsx'], label_visibility="collapsed")
    search = tc4.text_input("🔍 Search Database...", placeholder="Search Site ID, Project ID...")
    er = st.session_state.edit_row_data
    is_editing = er is not None
    exp_label = f"📝 Editing Record: {er['project_id']}" if is_editing else "➕ Add New Site Entry"
    with st.expander(exp_label, expanded=is_editing):
        with st.form("site_full_form", clear_on_submit=not is_editing):
            c1, c2, c3 = st.columns(3)
            p_id, s_id, s_nm = c1.text_input("Project ID*", value=str(er['project_id']) if is_editing else ""), c2.text_input("Site ID", value=str(er['site_id']) if is_editing else ""), c3.text_input("Site Name", value=str(er['site_name']) if is_editing else "")
            c4, c5, c6 = st.columns(3)
            cluster, p_amt = c4.text_input("Cluster", value=str(er['cluster']) if is_editing else ""), c5.number_input("Project Amount", value=float(er['project_amt']) if is_editing and er['project_amt'] else None)
            st_list = ["Select", "Yet to Start", "WIP", "Completed"]
            s_idx = st_list.index(er['site_status']) if is_editing and er['site_status'] in st_list else 0
            status = c6.selectbox("Status", st_list, index=s_idx)
            c7, c8, c9 = st.columns(3)
            po_n, po_a = c7.text_input("PO Number", value=str(er['po_no']) if is_editing else ""), c8.number_input("PO Amount", value=float(er['po_amt']) if is_editing and er['po_amt'] else None)
            t_idx = 0
            if is_editing and er['team_name'] in teams_list: t_idx = teams_list.index(er['team_name'])
            t_name = c9.selectbox("Team Name", teams_list, index=t_idx)
            c10, c11, c12 = st.columns(3)
            t_bill, t_paid, wcc_n = c10.number_input("Team Billing", value=float(er['team_billing']) if is_editing and er['team_billing'] else None), c11.number_input("Team Paid", value=float(er['team_paid_amt']) if is_editing and er['team_paid_amt'] else None), c12.text_input("WCC Number", value=str(er['wcc_no']) if is_editing else "")
            c13, c14, c15 = st.columns(3)
            wcc_a = c13.number_input("WCC Amount", value=float(er['wcc_amt']) if is_editing and er['wcc_amt'] else None)
            r_amt = c14.number_input("Received Amount", value=float(er['received_amt']) if is_editing and er['received_amt'] else None)
            w_desc = c15.text_area("Work Description", value=str(er['work_description']) if is_editing else "")
            if st.form_submit_button("🚀 SAVE DATA"):
                save_status = None if status == "Select" else status
                save_team = None if t_name == "Select" else t_name
                data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "work_description": w_desc, "site_status": save_status, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "team_name": save_team, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                if is_editing: supabase.table("site_data").update(data).eq('id', er['id']).execute(); st.session_state.edit_row_data = None
                else: supabase.table("site_data").insert(data).execute()
                st.rerun()
    st.divider()
    if not df.empty:
        if search: df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        st.subheader("📋 Complete Site Database (Horizontal Scroll)")
        edit_sel = st.selectbox("🎯 Select Project ID to EDIT", ["None"] + df['project_id'].tolist())
        if edit_sel != "None":
            st.session_state.edit_row_data = df[df['project_id'] == edit_sel].iloc[0].to_dict()
            st.rerun()
        st.dataframe(df.drop(columns=['id']), use_container_width=True)

# --- 8. FINANCE LEDGER (FIXED TABLE LOGIC) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    pay_type = st.radio("Select Payment Type", ["Payment Received", "Payment Paid"], horizontal=True)
    
    s_res = supabase.table("site_data").select("project_id", "received_amt", "team_paid_amt", "team_billing").execute()
    projects = ["None"] + [s['project_id'] for s in s_res.data] if s_res.data else ["None"]
    
    # Common Data Fetch for Transactions Table
    f_all_res = supabase.table("finance").select("*").order("transaction_date", desc=True).execute()
    df_finance = pd.DataFrame(f_all_res.data) if f_all_res.data else pd.DataFrame()

    if pay_type == "Payment Received":
        c_res = supabase.table("client_master").select("client_name").execute()
        master_clients = [c['client_name'] for c in c_res.data] if c_res.data else []
        combined = set(master_clients + ["Dilip Mundada", "Indus Towers Ltd."])
        clients = ["Select"] + sorted(list(combined))

        f_client = st.selectbox("Received From (Client)", clients)
        f_date = st.date_input("Date", datetime.now(), key="recv_date")
        f_amt = st.number_input("Received Amt", value=None, key="recv_amt")
        f_project = "None"
        if f_client == "Indus Towers Ltd.": f_project = st.selectbox("Project ID", projects, key="recv_proj")
        
        if st.button("🚀 Submit Received Payment"):
            if f_client != "Select" and f_amt is not None:
                try:
                    # 'received_amt' is the column name in DB
                    supabase.table("finance").insert({"received_from": f_client, "transaction_date": str(f_date), "received_amt": float(f_amt), "project_id": f_project if f_project != "None" else None}).execute()
                    if f_client == "Indus Towers Ltd." and f_project != "None":
                        current_row = next((item for item in s_res.data if item["project_id"] == f_project), None)
                        old_amt = float(current_row['received_amt']) if current_row and current_row['received_amt'] else 0.0
                        supabase.table("site_data").update({"received_amt": old_amt + float(f_amt)}).eq("project_id", f_project).execute()
                    st.success("Finance Ledger Updated!"); st.rerun()
                except Exception as e: st.error(f"Error: {e}")
            else: st.error("Please fill all required fields.")

        # SHOW ONLY RECEIVED TRANSACTIONS
        st.divider()
        st.subheader("📜 Received Payments Table")
        if not df_finance.empty:
            # Filtering entries where received_amt is > 0 and column paid_to is None or empty
            # Adjusting columns to only show what is relevant
            df_recv = df_finance[df_finance['received_amt'] > 0].copy()
            if not df_recv.empty:
                cols_to_show = ['received_from', 'transaction_date', 'received_amt', 'project_id', 'created_at']
                st.dataframe(df_recv[[c for c in cols_to_show if c in df_recv.columns]], use_container_width=True)
            else: st.info("No received payments found.")

    else:
        # --- PAYMENT PAID LOGIC ---
        t_master_res = supabase.table("team_master").select("team_name").execute()
        teams_list = ["Select"] + [t['team_name'] for t in t_master_res.data] if t_master_res.data else ["Select"]
        p_team = st.selectbox("Paid To (Team Name)", teams_list)
        p_project = st.selectbox("Project ID", projects, key="paid_proj")
        
        if p_project != "None":
            site_info = next((item for item in s_res.data if item["project_id"] == p_project), None)
            if site_info:
                billing = float(site_info['team_billing']) if site_info['team_billing'] else 0.0
                paid = float(site_info['team_paid_amt']) if site_info['team_paid_amt'] else 0.0
                st.markdown(f"<div class='balance-box'><h3 style='color: #dc2626; margin:0;'>Current Team Balance: ₹ {billing - paid:,.0f}</h3></div>", unsafe_allow_html=True)

        p_date = st.date_input("Date", datetime.now(), key="paid_date")
        # In your DB image, paid entries seem to be using 'paid_amount' column or 'received_amt' with 0. 
        # We will use 'paid_amount' if it exists.
        p_amt = st.number_input("Paid Amt", value=None, key="paid_amt")
        
        if st.button("🚀 Submit Paid Payment"):
            if p_team != "Select" and p_amt is not None and p_project != "None":
                try:
                    # In DB image 'received_from' is used for team name in paid entries too. 
                    # Column 'paid_amount' is used for the value.
                    supabase.table("finance").insert({"received_from": p_team, "transaction_date": str(p_date), "paid_amount": float(p_amt), "project_id": p_project}).execute()
                    current_row = next((item for item in s_res.data if item["project_id"] == p_project), None)
                    old_paid = float(current_row['team_paid_amt']) if current_row and current_row['team_paid_amt'] else 0.0
                    supabase.table("site_data").update({"team_paid_amt": old_paid + float(p_amt)}).eq("project_id", p_project).execute()
                    st.success(f"Payment recorded and Site Data Updated!"); st.rerun()
                except Exception as e: st.error(f"Error: {e}")
            else: st.error("Team Name, Amount, and Project ID are mandatory.")

        # SHOW ONLY PAID TRANSACTIONS
        st.divider()
        st.subheader("📜 Paid Payments Table")
        if not df_finance.empty:
            # Filtering entries where paid_amount is > 0
            if 'paid_amount' in df_finance.columns:
                df_paid = df_finance[df_finance['paid_amount'] > 0].copy()
                if not df_paid.empty:
                    cols_to_show = ['received_from', 'transaction_date', 'paid_amount', 'project_id', 'created_at']
                    st.dataframe(df_paid[[c for c in cols_to_show if c in df_paid.columns]], use_container_width=True)
                else: st.info("No paid payments found.")
            else: st.warning("Database column 'paid_amount' not detected.")
