import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; }
    .stApp { background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); }
    h1 { font-weight: 800; color: #0984e3; }
    div.stForm { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .stButton>button { border-radius: 8px; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"
supabase = create_client(URL, KEY)

# --- 3. HELPER ---
def to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
    return output.getvalue()

def format_df_dates(df):
    date_cols = ['transaction_date', 'created_at', 'Date', 'date']
    for col in df.columns:
        if any(d in col.lower() for d in date_cols) and col in df.columns:
            try: df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%b-%Y')
            except: pass
    return df

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0984e3;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.info(f"User: Mayur Patil\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5. DASHBOARD (UNTOUCHED LOGIC) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        s_res = supabase.table("site_data").select("*").execute()
        f_res = supabase.table("finance").select("*").execute()
        if s_res.data:
            df_s, df_f = pd.DataFrame(s_res.data), (pd.DataFrame(f_res.data) if f_res.data else pd.DataFrame())
            st.markdown("### 📍 Project Summary")
            c1, c2 = st.columns(2)
            c1.metric("Total Site Count", len(df_s))
            c2.metric("Total PO Amt", f"₹ {df_s['po_amt'].sum():,.0f}")
            st.divider()
            st.markdown("### 👥 Team Status")
            c2_1, c2_2, c2_3 = st.columns(3)
            t_bill, t_paid = df_s['team_billing'].sum(), df_s['team_paid_amt'].sum()
            c2_1.metric("Total Team Billing", f"₹ {t_bill:,.0f}"); c2_2.metric("Total Team Paid", f"₹ {t_paid:,.0f}"); c2_3.metric("Total Team Balance", f"₹ {t_bill - t_paid:,.0f}")
            st.divider()
            st.markdown("### 💳 Client Recovery")
            c3_1, c3_2, c3_3 = st.columns(3)
            wcc_tot, rec_tot = df_s['wcc_amt'].sum(), df_s['received_amt'].sum()
            c3_1.metric("Total WCC Amt", f"₹ {wcc_tot:,.0f}"); c3_2.metric("Total Received Amt", f"₹ {rec_tot:,.0f}"); c3_3.metric("Total Balance", f"₹ {wcc_tot - rec_tot:,.0f}")
            st.divider()
            st.markdown("### 💰 Breakdown")
            c4_1, c4_2 = st.columns(2)
            mundada_total = df_f[df_f['received_from'].str.contains("dilip mundada", case=False, na=False)]['received_amt'].sum() if not df_f.empty else 0
            indus_total = df_f[df_f['received_from'].str.contains("indus tower", case=False, na=False)]['received_amt'].sum() if not df_f.empty else 0
            c4_1.metric("Recv. From Dilip Mundada", f"₹ {mundada_total:,.0f}"); c4_2.metric("Recv. From Indus Towers", f"₹ {indus_total:,.0f}")
    except Exception as e: st.error(f"Error: {e}")

# --- 6. MASTER REGISTRATION (UNTOUCHED LOGIC - FIXED NAMEERROR) ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with tab1:
        with st.form("client_master_form", clear_on_submit=True):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved")
        res_c = supabase.table("client_master").select("*").execute()
        if res_c.data: st.dataframe(format_df_dates(pd.DataFrame(res_c.data).drop(columns=['id'], errors='ignore')), use_container_width=True)
    with tab2:
        with st.form("team_master_form", clear_on_submit=True):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save Team"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute(); st.success("Saved")
        res_t = supabase.table("team_master").select("*").execute()
        if res_t.data: st.dataframe(format_df_dates(pd.DataFrame(res_t.data).drop(columns=['id'], errors='ignore')), use_container_width=True)

# --- 7. SITE DATA ENTRY (100% COLUMNS & DIRECT EDIT) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registry & Operations</h1>", unsafe_allow_html=True)
    
    if st.button("➕ Add New Site Entry (Full Form)"):
        st.session_state.show_form = not st.session_state.get('show_form', False)

    if st.session_state.get('show_form', False):
        with st.form("site_full_form", clear_on_submit=True):
            st.subheader("Enter All 100% Site Data Columns")
            c1, c2, c3 = st.columns(3)
            p_id, s_id, s_nm = c1.text_input("Project ID (Unique)*"), c2.text_input("Site ID"), c3.text_input("Site Name")
            c4, c5, c6 = st.columns(3)
            cluster, p_amt, status = c4.text_input("Cluster"), c5.number_input("Project Amount", value=None), c6.selectbox("Status", ["Planning", "WIP", "WCC Done", "Closed"])
            c7, c8, c9 = st.columns(3)
            po_n, po_a, w_desc = c7.text_input("PO Number"), c8.number_input("PO Amount", value=None), c9.text_area("Work Description", height=65)
            c10, c11, c12 = st.columns(3)
            t_name, t_bill, t_paid = c10.text_input("Team Name"), c11.number_input("Team Billing", value=None), c12.number_input("Team Paid Amount", value=None)
            c13, c14, c15 = st.columns(3)
            wcc_n, wcc_a, r_amt = c13.text_input("WCC Number"), c14.number_input("WCC Amount", value=None), c15.number_input("Received Amount", value=None)

            if st.form_submit_button("🚀 Save Site"):
                check = supabase.table("site_data").select("project_id").eq("project_id", p_id).execute()
                if check.data: st.error(f"Remark: Project ID '{p_id}' already available!"); 
                elif p_id:
                    data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                    supabase.table("site_data").insert(data).execute(); st.success("Added!"); st.rerun()

    st.divider()
    b1, b2, b3, b4 = st.columns([1, 0.5, 0.5, 2])
    with b1: up_file = st.file_uploader("Upload", type=['xlsx'], label_visibility="collapsed")
    with b2:
        if up_file and st.button("Sync"):
            up_df = pd.read_excel(up_file).fillna(0)
            existing = [x['project_id'] for x in supabase.table("site_data").select("project_id").execute().data]
            to_add, dups = [], []
            for _, r in up_df.iterrows():
                if str(r['project_id']) in existing: dups.append(str(r['project_id']))
                else: to_add.append(r.to_dict())
            if to_add: supabase.table("site_data").insert(to_add).execute()
            if dups: st.warning(f"Duplicates: {', '.join(dups)}")
            st.success(f"Added {len(to_add)} records."); st.rerun()

    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()
    if not df.empty: df['team_balance'] = df['team_billing'].astype(float) - df['team_paid_amt'].astype(float)

    with b3:
        if not df.empty: st.download_button("Excel", data=to_excel(df), file_name="Site_Data.xlsx")
    with b4: search = st.text_input("🔍 Search Database...")

    if not df.empty:
        if search: df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        st.subheader("Live Database (Double-click to Edit)")
        edited_df = st.data_editor(df, column_order=["project_id", "site_id", "site_name", "cluster", "project_amt", "po_no", "po_amt", "site_status", "team_name", "team_billing", "team_paid_amt", "team_balance", "wcc_no", "wcc_amt", "received_amt", "work_description"], column_config={"id": None, "team_balance": st.column_config.NumberColumn("Team Balance", disabled=True)}, use_container_width=True, num_rows="dynamic", key="site_editor")
        if st.button("💾 Save All Changes"):
            for _, row in edited_df.iterrows():
                if 'id' in row:
                    d = row.to_dict(); d.pop('team_balance', None); supabase.table("site_data").update(d).eq('id', row['id']).execute()
            st.success("Cloud Synced!")

# --- 8. FINANCE LEDGER (UNTOUCHED LOGIC) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    trans_type = st.radio("Type", ["Payment Received", "Payment Paid"], horizontal=True)
    c_res = supabase.table("client_master").select("client_name").execute()
    s_res = supabase.table("site_data").select("project_id").execute()
    clients, projects = [c['client_name'] for c in c_res.data] if c_res.data else [], [s['project_id'] for s in s_res.data] if s_res.data else []

    if trans_type == "Payment Received":
        c_sel = st.selectbox("Received From", ["Select"] + clients + ["dilip mundada"])
        with st.form("rec_f", clear_on_submit=True):
            r_dt, r_at = st.date_input("Date", datetime.now()), st.number_input("Received Amt", value=None)
            p_sel = st.selectbox("Project ID", ["Select ID"] + projects) if "indus tower" in c_sel.lower() else None
            if st.form_submit_button("Submit"):
                if c_sel != "Select":
                    amt = r_at or 0
                    supabase.table("finance").insert({"received_from": c_sel, "transaction_date": str(r_dt), "received_amt": amt, "paid_amount": 0}).execute()
                    if p_sel and p_sel != "Select ID":
                        curr = supabase.table("site_data").select("received_amt").eq("project_id", p_sel).execute()
                        if curr.data:
                            new_v = float(curr.data[0]['received_amt'] or 0) + amt
                            supabase.table("site_data").update({"received_amt": new_v}).eq("project_id", p_sel).execute()
                    st.success("Payment logged.")
    st.divider()
    f_res = supabase.table("finance").select("*").order('transaction_date', desc=True).execute()
    if f_res.data:
        df_f = format_df_dates(pd.DataFrame(f_res.data).drop(columns=['id'], errors='ignore'))
        st.dataframe(df_f, use_container_width=True)

st.markdown("<div class='elegant-footer'>Visiontech Automation © 2026</div>", unsafe_allow_html=True)
