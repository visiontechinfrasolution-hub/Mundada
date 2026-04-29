import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & LAVISH STYLE ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; }
    div[data-testid="stMetric"] { background: #ffffff; border-radius: 15px; padding: 20px; border-left: 5px solid #0ea5e9; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); }
    .stButton>button { background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white !important; border-radius: 10px; font-weight: 700; }
    div.stForm { background: #f8fafc; border-radius: 20px; border: 1px solid #e2e8f0; padding: 30px; }
    .edit-btn-style button { background-color: #ff9f43 !important; border: none !important; height: 30px !important; line-height: 1 !important; padding: 0 10px !important; }
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

# --- 5. DASHBOARD (ALL ITEMS STABLE) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        s_res = supabase.table("site_data").select("*").execute()
        f_res = supabase.table("finance").select("*").execute()
        if s_res.data:
            df_s, df_f = pd.DataFrame(s_res.data), (pd.DataFrame(f_res.data) if f_res.data else pd.DataFrame(columns=['received_from', 'received_amt']))
            st.markdown("### 📍 Summary")
            c1, c2 = st.columns(2)
            c1.metric("Total Site Count", len(df_s))
            c2.metric("Total PO Amt", f"₹ {df_s['po_amt'].sum():,.0f}")
            st.divider()
            c2_1, c2_2, c2_3 = st.columns(3)
            t_bill, t_paid = df_s['team_billing'].sum(), df_s['team_paid_amt'].sum()
            c2_1.metric("Total Team Billing", f"₹ {t_bill:,.0f}"); c2_2.metric("Total Team Paid", f"₹ {t_paid:,.0f}"); c2_3.metric("Total Team Balance", f"₹ {t_bill - t_paid:,.0f}")
            st.divider()
            st.markdown("### 💳 WCC & Breakdown")
            c3_1, c3_2 = st.columns(2)
            m_amt = df_f[df_f['received_from'].str.contains("dilip mundada", case=False, na=False)]['received_amt'].astype(float).sum()
            i_amt = df_f[df_f['received_from'].str.contains("indus tower", case=False, na=False)]['received_amt'].astype(float).sum()
            c3_1.metric("From Dilip Mundada", f"₹ {m_amt:,.0f}"); c3_2.metric("From Indus Towers", f"₹ {i_amt:,.0f}")
    except: pass

# --- 6. MASTER REGISTRATION (STABLE) ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with tab1:
        with st.form("cl_reg"):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved")

# --- 7. SITE DATA ENTRY (ROW-WISE EDIT BUTTON + POPUP) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    
    # State for Edit
    if "edit_row_data" not in st.session_state: st.session_state.edit_row_data = None

    # Fetch Data
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()

    # Top Bar
    tc1, tc2, tc3 = st.columns([1, 1, 3])
    if tc1.button("➕ New Site"): 
        st.session_state.edit_row_data = None
        st.rerun()
    if not df.empty: tc2.download_button("📥 Excel", data=to_excel(df), file_name="Site_Data.xlsx")
    search = tc3.text_input("🔍 Search Database...", placeholder="Project ID, Site, Team...")

    # POP-UP / FORM SECTION
    if st.session_state.get('edit_row_data') or st.session_state.edit_row_data is None:
        exp_label = "➕ Add New Site" if st.session_state.edit_row_data is None else f"📝 Edit: {st.session_state.edit_row_data['project_id']}"
        with st.expander(exp_label, expanded=(st.session_state.edit_row_data is not None)):
            er = st.session_state.edit_row_data
            with st.form("site_full_form", clear_on_submit=(er is None)):
                c1, c2, c3 = st.columns(3)
                p_id = c1.text_input("Project ID*", value=er['project_id'] if er else "")
                s_id = c2.text_input("Site ID", value=er['site_id'] if er else "")
                s_nm = c3.text_input("Site Name", value=er['site_name'] if er else "")
                
                c4, c5, c6 = st.columns(3)
                cluster = c4.text_input("Cluster", value=er['cluster'] if er else "")
                p_amt = c5.number_input("Project Amt", value=float(er['project_amt']) if er else None) # Blank logic
                status_list = ["Planning", "WIP", "WCC Done", "Closed"]
                status = c6.selectbox("Status", status_list, index=status_list.index(er['site_status']) if er and er['site_status'] in status_list else 0)

                c7, c8, c9 = st.columns(3)
                po_n, po_a = c7.text_input("PO No", value=er['po_no'] if er else ""), c8.number_input("PO Amt", value=float(er['po_amt']) if er else None)
                t_name = c9.text_input("Team Name", value=er['team_name'] if er else "")

                c10, c11, c12 = st.columns(3)
                t_bill, t_paid = c10.number_input("Team Billing", value=float(er['team_billing']) if er else None), c11.number_input("Team Paid", value=float(er['team_paid_amt']) if er else None)
                wcc_n = c12.text_input("WCC No", value=er['wcc_no'] if er else "")

                c13, c14, c15 = st.columns(3)
                wcc_a, r_amt = c13.number_input("WCC Amt", value=float(er['wcc_amt']) if er else None), c14.number_input("Recv Amt", value=float(er['received_amt']) if er else None)
                w_desc = c15.text_area("Work Description", value=er['work_description'] if er else "")

                if st.form_submit_button("🚀 SAVE DATA"):
                    data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                    if er: supabase.table("site_data").update(data).eq('id', er['id']).execute()
                    else: supabase.table("site_data").insert(data).execute()
                    st.session_state.edit_row_data = None
                    st.rerun()

    st.divider()
    
    # TABLE WITH REAL EDIT BUTTONS
    if not df.empty:
        if search: df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        # Header Row
        h = st.columns([0.6, 2, 2, 2, 2, 2])
        h[0].write("**Action**"); h[1].write("**Project ID**"); h[2].write("**Site ID**"); h[3].write("**Site Name**"); h[4].write("**Team**"); h[5].write("**Status**")
        
        # Data Rows
        for idx, row in df.iterrows():
            r = st.columns([0.6, 2, 2, 2, 2, 2])
            # YEH RAHA EDIT BUTTON HAR LINE KE AGE
            if r[0].button("📝", key=f"btn_{row['id']}"):
                st.session_state.edit_row_data = row
                st.rerun()
            r[1].write(row['project_id']); r[2].write(row['site_id']); r[3].write(row['site_name']); r[4].write(row['team_name']); r[5].write(row['site_status'])

# --- 8. FINANCE LEDGER ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # Stable logic...
