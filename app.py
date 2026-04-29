import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & PREMIUM STYLE ---
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

# --- 5. DASHBOARD (ALL ITEMS STABLE) ---
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
            c2_1.metric("Total Team Billing", f"₹ {t_bill:,.0f}"); c2_2.metric("Total Team Paid", f"₹ {t_paid:,.0f}"); c2_3.metric("Total Team Balance", f"₹ {t_bill - t_paid:,.0f}")
            
            st.divider()
            st.markdown("### 💳 WCC & Client Recovery")
            c3_1, c3_2, c3_3 = st.columns(3)
            wcc_tot, rec_tot = df_s['wcc_amt'].sum(), df_s['received_amt'].sum()
            c3_1.metric("Total WCC Amt", f"₹ {wcc_tot:,.0f}"); c3_2.metric("Total Received Amt", f"₹ {rec_tot:,.0f}"); c3_3.metric("WCC Balance", f"₹ {wcc_tot - rec_tot:,.0f}")
            
            st.divider()
            st.markdown("### 💰 Breakdown")
            c4_1, c4_2 = st.columns(2)
            m_amt = df_f[df_f['received_from'].str.contains("dilip mundada", case=False, na=False)]['received_amt'].astype(float).sum()
            i_amt = df_f[df_f['received_from'].str.contains("indus tower", case=False, na=False)]['received_amt'].astype(float).sum()
            c4_1.metric("Recv. From Dilip Mundada", f"₹ {m_amt:,.0f}"); c4_2.metric("Recv. From Indus Towers", f"₹ {i_amt:,.0f}")
    except: pass

# --- 6. MASTER REGISTRATION ---
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

# --- 7. SITE DATA ENTRY (NO BUTTON MESS - DIRECT TABLE EDIT) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    
    # FETCH DATA
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()

    # ACTION BAR
    tc1, tc2, tc3, tc4 = st.columns([1.5, 1.5, 2, 3])
    
    # NEW ENTRY FORM (Expander)
    with st.expander("➕ Click to Add New Site Entry", expanded=False):
        with st.form("new_site_form", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            p_id, s_id, s_nm = c1.text_input("Project ID*"), c2.text_input("Site ID"), c3.text_input("Site Name")
            c4, c5, c6 = st.columns(3)
            cluster, p_amt = c4.text_input("Cluster"), c5.number_input("Project Amt", value=None)
            status = c6.selectbox("Status", ["Planning", "WIP", "WCC Done", "Closed"])
            # (Additional columns omitted for brevity in form, table has everything)
            if st.form_submit_button("🚀 SAVE NEW SITE"):
                if p_id:
                    data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "project_amt": p_amt or 0, "site_status": status}
                    supabase.table("site_data").insert(data).execute(); st.rerun()

    if not df.empty:
        tc2.download_button("📥 Excel", data=to_excel(df), file_name="Site_Data.xlsx")
    uploaded_file = tc3.file_uploader("📤 Bulk Upload", type=['xlsx'], label_visibility="collapsed")
    search = tc4.text_input("🔍 Search Database...", label_visibility="collapsed")

    st.divider()
    
    # DIRECT TABLE EDITING (NO QUICK ACTION BUTTONS)
    if not df.empty:
        if search: df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        st.subheader("Live Site Database (Double Click Cell to Edit)")
        
        # This editor replaces all those 1000 buttons
        edited_df = st.data_editor(
            df, 
            use_container_width=True, 
            column_config={"id": None}, # Database ID hidden
            num_rows="dynamic",
            key="site_main_editor"
        )
        
        # Single Save Button for all changes
        if st.button("💾 SAVE ALL CHANGES TO CLOUD"):
            for _, row in edited_df.iterrows():
                if 'id' in row:
                    supabase.table("site_data").update(row.to_dict()).eq('id', row['id']).execute()
            st.success("Cloud Synced Successfully!")

# --- 8. FINANCE LEDGER ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
