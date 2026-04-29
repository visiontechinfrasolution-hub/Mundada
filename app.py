import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & CLEAN WHITE STYLE ---
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

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #0f172a;'>MUNDADA</h1>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN NAVIGATION", ["🏠 Dashboard", "📝 Master Registration", "🏗️ Site Data Entry", "💸 Finance Ledger"])
    st.info(f"User: Mayur Patil\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5. DASHBOARD (RECOVERY ITEMS RESTORED) ---
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
            # RESTORED: Specific Collection Breakdown
            st.markdown("### 💰 Recovery Breakdown")
            c4_1, c4_2 = st.columns(2)
            mundada_amt = df_f[df_f['received_from'].str.contains("dilip mundada", case=False, na=False)]['received_amt'].astype(float).sum()
            indus_amt = df_f[df_f['received_from'].str.contains("indus tower", case=False, na=False)]['received_amt'].astype(float).sum()
            c4_1.metric("Total Recv. From Dilip Mundada", f"₹ {mundada_amt:,.0f}")
            c4_2.metric("Total Recv. From Indus Towers", f"₹ {indus_amt:,.0f}")
    except: st.info("Welcome! Start adding data.")

# --- 6. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with tab1:
        with st.form("client_reg"):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved")
    with tab2:
        with st.form("team_reg"):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save Team"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute(); st.success("Saved")

# --- 7. SITE DATA ENTRY (BLANK FIELDS & FULL TABLE) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    if "edit_row" not in st.session_state: st.session_state.edit_row = None
    if "show_modal" not in st.session_state: st.session_state.show_modal = False

    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()

    tc1, tc2, tc3, tc4 = st.columns([1.5, 1.5, 1.5, 3])
    if tc1.button("➕ New Site"):
        st.session_state.edit_row = None
        st.session_state.show_modal = True
        st.rerun()
    if not df.empty:
        tc2.download_button("📥 Download Excel", data=to_excel(df), file_name="Site_Data.xlsx")
    uploaded_file = tc3.file_uploader("📤 Bulk Upload", type=['xlsx'], label_visibility="collapsed")
    search = tc4.text_input("🔍 Search Database...", label_visibility="collapsed")

    # POP-UP MODAL (BLANK NUMERIC FIELDS)
    if st.session_state.show_modal:
        with st.expander("📝 SITE ENTRY FORM", expanded=True):
            er = st.session_state.edit_row
            with st.form("modal_form"):
                c1, c2, c3 = st.columns(3)
                p_id = c1.text_input("Project ID*", value=er['project_id'] if er else "")
                s_id = c2.text_input("Site ID", value=er['site_id'] if er else "")
                s_nm = c3.text_input("Site Name", value=er['site_name'] if er else "")
                
                c4, c5, c6 = st.columns(3)
                cluster = c4.text_input("Cluster", value=er['cluster'] if er else "")
                p_amt = c5.number_input("Project Amt", value=float(er['project_amt']) if er else None)
                status = c6.selectbox("Status", ["Planning", "WIP", "WCC Done", "Closed"])

                c7, c8, c9 = st.columns(3)
                po_n = c7.text_input("PO No", value=er['po_no'] if er else "")
                po_a = c8.number_input("PO Amt", value=float(er['po_amt']) if er else None)
                t_name = c9.text_input("Team Name", value=er['team_name'] if er else "")

                c10, c11, c12 = st.columns(3)
                t_bill = c10.number_input("Team Billing", value=float(er['team_billing']) if er else None)
                t_paid = c11.number_input("Team Paid", value=float(er['team_paid_amt']) if er else None)
                wcc_n = c12.text_input("WCC No", value=er['wcc_no'] if er else "")

                c13, c14, c15 = st.columns(3)
                wcc_a = c13.number_input("WCC Amt", value=float(er['wcc_amt']) if er else None)
                r_amt = c14.number_input("Recv Amt", value=float(er['received_amt']) if er else None)
                w_desc = c15.text_area("Work Description", value=er['work_description'] if er else "")

                sc1, sc2 = st.columns(2)
                if sc1.form_submit_button("💾 Save & Sync"):
                    data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                    if er: supabase.table("site_data").update(data).eq('id', er['id']).execute()
                    else: supabase.table("site_data").insert(data).execute()
                    st.session_state.show_modal = False
                    st.rerun()
                if sc2.form_submit_button("❌ Cancel"):
                    st.session_state.show_modal = False
                    st.rerun()

    st.divider()
    # FULL TABLE DISPLAY
    if not df.empty:
        if search: df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        st.subheader("⚡ Quick Actions")
        for idx, row in df.head(15).iterrows():
            ec1, ec2, ec3, ec4 = st.columns([1, 2, 2, 5])
            if ec1.button("📝 Edit", key=f"ed_{row['id']}"):
                st.session_state.edit_row = row
                st.session_state.show_modal = True
                st.rerun()
            ec2.write(f"**ID:** {row['project_id']}")
            ec3.write(f"**Site:** {row['site_id']}")
            ec4.write(f"**Status:** {row['site_status']}")

# --- 8. FINANCE LEDGER ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # Stable finance logic remains same...
