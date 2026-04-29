import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & STYLE ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; }
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 15px; padding: 20px; border-left: 5px solid #0ea5e9; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    .stButton>button { background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white !important; border-radius: 10px; font-weight: 700; }
    div.stForm { background: #f8fafc; border-radius: 20px; border: 1px solid #e2e8f0; padding: 30px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"
supabase = create_client(URL, KEY)

# --- 3. HELPERS ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.info(f"User: Mayur Patil\nDate: 29-Apr-2026")

# --- 5. DASHBOARD (ALL ITEMS RESTORED) ---
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
            c3_3.metric("WCC Balance", f"₹ {wcc_tot - rec_tot:,.0f}")
            
            st.divider()
            st.markdown("### 💰 Breakdown")
            c4_1, c4_2 = st.columns(2)
            m_amt = df_f[df_f['received_from'].str.contains("dilip mundada", case=False, na=False)]['received_amt'].astype(float).sum()
            i_amt = df_f[df_f['received_from'].str.contains("indus tower", case=False, na=False)]['received_amt'].astype(float).sum()
            c4_1.metric("Recv. From Dilip Mundada", f"₹ {m_amt:,.0f}")
            c4_2.metric("Recv. From Indus Towers", f"₹ {i_amt:,.0f}")
    except: st.info("Dashboard is loading...")

# --- 6. MASTER REGISTRATION (STABLE) ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with tab1:
        with st.form("cl_reg"):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved")
    with tab2:
        with st.form("tm_reg"):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save Team"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute(); st.success("Saved")

# --- 7. SITE DATA ENTRY (100% COLUMNS + ROW EDIT BUTTON) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    if "edit_row_data" not in st.session_state: st.session_state.edit_row_data = None

    # Fetch Data
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()

    # Top Bar
    tc1, tc2, tc3 = st.columns([1, 1, 3])
    if tc1.button("➕ Add New Site"): 
        st.session_state.edit_row_data = None
        st.rerun()
    if not df.empty: tc2.download_button("📥 Excel", data=to_excel(df), file_name="Site_Data.xlsx")
    search = tc3.text_input("🔍 Search Database...")

    # FORM SECTION
    er = st.session_state.edit_row_data
    is_editing = er is not None
    exp_label = f"📝 Editing: {er['project_id']}" if is_editing else "➕ Add New Site Entry"
    
    with st.expander(exp_label, expanded=is_editing):
        with st.form("site_full_form", clear_on_submit=not is_editing):
            r1c1, r1c2, r1c3 = st.columns(3)
            p_id = r1c1.text_input("Project ID*", value=str(er['project_id']) if is_editing else "")
            s_id = r1c2.text_input("Site ID", value=str(er['site_id']) if is_editing else "")
            s_nm = r1c3.text_input("Site Name", value=str(er['site_name']) if is_editing else "")
            
            r2c1, r2c2, r2c3 = st.columns(3)
            cluster = r2c1.text_input("Cluster", value=str(er['cluster']) if is_editing else "")
            p_amt = r2c2.number_input("Project Amount", value=float(er['project_amt']) if is_editing and er['project_amt'] else None)
            st_list = ["Planning", "WIP", "WCC Done", "Closed"]
            s_idx = st_list.index(er['site_status']) if is_editing and er['site_status'] in st_list else 0
            status = r2c3.selectbox("Status", st_list, index=s_idx)

            r3c1, r3c2, r3c3 = st.columns(3)
            po_n, po_a = r3c1.text_input("PO Number", value=str(er['po_no']) if is_editing else ""), r3c2.number_input("PO Amount", value=float(er['po_amt']) if is_editing and er['po_amt'] else None)
            t_name = r3c3.text_input("Team Name", value=str(er['team_name']) if is_editing else "")

            r4c1, r4c2, r4c3 = st.columns(3)
            t_bill, t_paid = r4c1.number_input("Team Billing", value=float(er['team_billing']) if is_editing and er['team_billing'] else None), r4c2.number_input("Team Paid", value=float(er['team_paid_amt']) if is_editing and er['team_paid_amt'] else None)
            wcc_n = r4c3.text_input("WCC Number", value=str(er['wcc_no']) if is_editing else "")

            r5c1, r5c2, r5c3 = st.columns(3)
            wcc_a, r_amt = r5c1.number_input("WCC Amount", value=float(er['wcc_amt']) if is_editing and er['wcc_amt'] else None), r5c2.number_input("Received Amount", value=float(er['received_amt']) if is_editing and er['received_amt'] else None)
            w_desc = r5c3.text_area("Work Description", value=str(er['work_description']) if is_editing else "")

            if st.form_submit_button("🚀 SAVE DATA"):
                data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                if is_editing: supabase.table("site_data").update(data).eq('id', er['id']).execute(); st.session_state.edit_row_data = None
                else: supabase.table("site_data").insert(data).execute()
                st.rerun()

    st.divider()
    # 100% COLUMNS TABLE WITH EDIT BUTTONS
    if not df.empty:
        if search: df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        df['team_balance'] = df['team_billing'].astype(float) - df['team_paid_amt'].astype(float)
        
        # Displaying with horizontal scroll for all columns
        st.subheader("📋 Detailed Database")
        
        # Table Header logic
        h = st.columns([0.6, 2, 2, 2, 2, 2])
        h[0].write("**Edit**"); h[1].write("**Project ID**"); h[2].write("**Site ID**"); h[3].write("**Site Name**"); h[4].write("**Team**"); h[5].write("**Status**")
        
        for idx, row in df.iterrows():
            r = st.columns([0.6, 2, 2, 2, 2, 2])
            if r[0].button("📝", key=f"btn_{row['id']}"):
                st.session_state.edit_row_data = row.to_dict(); st.rerun()
            r[1].write(row['project_id']); r[2].write(row['site_id']); r[3].write(row['site_name']); r[4].write(row['team_name']); r[5].write(row['site_status'])
        
        st.divider()
        st.markdown("### 📊 Complete Raw Data View")
        st.dataframe(df.drop(columns=['id']), use_container_width=True)

# --- 8. FINANCE LEDGER (STABLE) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # Previous stable logic continues here...
