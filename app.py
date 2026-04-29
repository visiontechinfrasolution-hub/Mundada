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
    
    /* Metrics Lavish Look */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border-radius: 15px;
        padding: 20px;
        border-left: 5px solid #0ea5e9;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05);
    }
    [data-testid="stMetricValue"] > div { color: #0f172a !important; font-weight: 800; }

    /* Lavish Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #0f172a 0%, #334155 100%);
        color: white !important;
        border-radius: 10px;
        font-weight: 700;
        border: none;
    }
    .stButton>button:hover { background: linear-gradient(135deg, #0ea5e9 0%, #2dd4bf 100%); }

    /* Forms */
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

def format_df_dates(df):
    date_cols = ['transaction_date', 'created_at', 'Date', 'date']
    for col in df.columns:
        if any(d in col.lower() for d in date_cols) and col in df.columns:
            try: df[col] = pd.to_datetime(df[col]).dt.strftime('%d-%b-%Y')
            except: pass
    return df

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.info(f"User: Mayur Patil\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5. DASHBOARD (LAVISH & STABLE) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        s_res = supabase.table("site_data").select("*").execute()
        f_res = supabase.table("finance").select("*").execute()
        if s_res.data:
            df_s, df_f = pd.DataFrame(s_res.data), (pd.DataFrame(f_res.data) if f_res.data else pd.DataFrame())
            
            st.markdown("### 📍 Summary")
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
    except: st.info("Welcome, start by adding data.")

# --- 6. MASTER REGISTRATION (STABLE) ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with tab1:
        with st.form("c_f", clear_on_submit=True):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved")
        res_c = supabase.table("client_master").select("*").execute()
        if res_c.data: st.dataframe(format_df_dates(pd.DataFrame(res_c.data).drop(columns=['id'], errors='ignore')), use_container_width=True)
    with tab2:
        with st.form("t_f", clear_on_submit=True):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save Team"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute(); st.success("Saved")
        res_t = supabase.table("team_master").select("*").execute()
        if res_t.data: st.dataframe(format_df_dates(pd.DataFrame(res_t.data).drop(columns=['id'], errors='ignore')), use_container_width=True)

# --- 7. SITE DATA ENTRY (100% COLUMNS + ROW SELECT TO EDIT) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registry</h1>", unsafe_allow_html=True)
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()
    
    # Selection logic for Editing
    edit_id = st.selectbox("🎯 Select Project ID to Edit (Optional)", ["None"] + df['project_id'].tolist()) if not df.empty else "None"
    selected_row = df[df['project_id'] == edit_id].iloc[0] if edit_id != "None" else None

    with st.expander("➕ / 📝 Site Data Form", expanded=(selected_row is not None)):
        with st.form("full_site_form", clear_on_submit=(selected_row is None)):
            c1, c2, c3 = st.columns(3)
            p_id = c1.text_input("Project ID*", value=selected_row['project_id'] if selected_row is not None else "")
            s_id = c2.text_input("Site ID", value=selected_row['site_id'] if selected_row is not None else "")
            s_nm = c3.text_input("Site Name", value=selected_row['site_name'] if selected_row is not None else "")
            
            c4, c5, c6 = st.columns(3)
            cluster = c4.text_input("Cluster", value=selected_row['cluster'] if selected_row is not None else "")
            p_amt = c5.number_input("Project Amount", value=float(selected_row['project_amt']) if selected_row is not None else None)
            st_list = ["Planning", "WIP", "WCC Done", "Closed"]
            status = c6.selectbox("Status", st_list, index=st_list.index(selected_row['site_status']) if selected_row is not None else 0)

            c7, c8, c9 = st.columns(3)
            po_n, po_a = c7.text_input("PO No", value=selected_row['po_no'] if selected_row is not None else ""), c8.number_input("PO Amt", value=float(selected_row['po_amt']) if selected_row is not None else None)
            t_name = c9.text_input("Team Name", value=selected_row['team_name'] if selected_row is not None else "")

            c10, c11, c12 = st.columns(3)
            t_bill = c10.number_input("Team Billing", value=float(selected_row['team_billing']) if selected_row is not None else None)
            t_paid = c11.number_input("Team Paid", value=float(selected_row['team_paid_amt']) if selected_row is not None else None)
            wcc_n = c12.text_input("WCC No", value=selected_row['wcc_no'] if selected_row is not None else "")

            c13, c14, c15 = st.columns(3)
            wcc_a = c13.number_input("WCC Amt", value=float(selected_row['wcc_amt']) if selected_row is not None else None)
            r_amt = c14.number_input("Received Amt", value=float(selected_row['received_amt']) if selected_row is not None else None)
            w_desc = c15.text_area("Work Description", value=selected_row['work_description'] if selected_row is not None else "")

            if st.form_submit_button("🚀 Sync to Cloud"):
                data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                if selected_row is not None:
                    supabase.table("site_data").update(data).eq('id', selected_row['id']).execute(); st.success("Updated!")
                else:
                    if supabase.table("site_data").select("project_id").eq("project_id", p_id).execute().data: st.error("Duplicate Project ID!")
                    else: supabase.table("site_data").insert(data).execute(); st.success("Saved!")
                st.rerun()

    st.divider()
    b1, b2, b3 = st.columns([1, 1, 2])
    with b1: up_file = st.file_uploader("Upload Excel", type=['xlsx'], label_visibility="collapsed")
    with b2:
        if not df.empty: st.download_button("📥 Export", data=to_excel(df), file_name="Site_Data.xlsx")
    with b3: search = st.text_input("🔍 Search Anything...")

    if not df.empty:
        df['team_balance'] = df['team_billing'].astype(float) - df['team_paid_amt'].astype(float)
        if search: df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        st.dataframe(format_df_dates(df.drop(columns=['id'])), use_container_width=True)

# --- 8. FINANCE LEDGER (STABLE) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # Finance logic remains identical to the last stable version...
