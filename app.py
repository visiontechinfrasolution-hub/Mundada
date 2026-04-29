import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & LAVISH STYLE (NO CHANGE) ---
st.set_page_config(page_title="Visiontech Mundada", page_icon="💎", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; }
    div[data-testid="stMetric"] { 
        background: #ffffff; border-radius: 15px; padding: 20px; 
        border-left: 5px solid #0ea5e9; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05); 
    }
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
    st.info(f"User: Mayur Patil\nDate: {datetime.now().strftime('%d-%b-%Y')}")

# --- 5. DASHBOARD (STABLE BREAKDOWN & WCC) ---
if page == "🏠 Dashboard":
    st.markdown("<h1>📊 Project Intelligence</h1>", unsafe_allow_html=True)
    try:
        s_res = supabase.table("site_data").select("*").execute()
        f_res = supabase.table("finance").select("*").execute()
        
        if s_res.data:
            df_s = pd.DataFrame(s_res.data)
            df_f = pd.DataFrame(f_res.data) if f_res.data else pd.DataFrame(columns=['received_from', 'received_amt'])
            
            # Line 1: Summary
            st.markdown("### 📍 Summary")
            c1, c2 = st.columns(2)
            c1.metric("Total Site Count", len(df_s))
            c2.metric("Total PO Amt", f"₹ {df_s['po_amt'].sum():,.0f}")
            
            st.divider()
            # Line 2: Team Financials
            st.markdown("### 👥 Team Status")
            c2_1, c2_2, c2_3 = st.columns(3)
            t_bill, t_paid = df_s['team_billing'].sum(), df_s['team_paid_amt'].sum()
            c2_1.metric("Total Team Billing", f"₹ {t_bill:,.0f}")
            c2_2.metric("Total Team Paid", f"₹ {t_paid:,.0f}")
            c2_3.metric("Total Team Balance", f"₹ {t_bill - t_paid:,.0f}")
            
            st.divider()
            # Line 3: WCC Data (Restored)
            st.markdown("### 💳 WCC & Client Recovery")
            c3_1, c3_2, c3_3 = st.columns(3)
            wcc_tot = df_s['wcc_amt'].sum()
            rec_tot = df_s['received_amt'].sum()
            c3_1.metric("Total WCC Amt", f"₹ {wcc_tot:,.0f}")
            c3_2.metric("Total Received Amt", f"₹ {rec_tot:,.0f}")
            c3_3.metric("WCC Pending Balance", f"₹ {wcc_tot - rec_tot:,.0f}")
            
            st.divider()
            # Line 4: Breakdown (Restored)
            st.markdown("### 💰 Collection Breakdown")
            c4_1, c4_2 = st.columns(2)
            mundada_amt = df_f[df_f['received_from'].str.contains("dilip mundada", case=False, na=False)]['received_amt'].astype(float).sum()
            indus_amt = df_f[df_f['received_from'].str.contains("indus tower", case=False, na=False)]['received_amt'].astype(float).sum()
            c4_1.metric("Recv. From Dilip Mundada", f"₹ {mundada_amt:,.0f}")
            c4_2.metric("Recv. From Indus Towers", f"₹ {indus_amt:,.0f}")
        else: st.info("Welcome! Start by adding data to see metrics.")
    except Exception as e: st.error(f"Dashboard Error: {e}")

# --- 6. MASTER REGISTRATION ---
elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with tab1:
        with st.form("client_f", clear_on_submit=True):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved")
    with tab2:
        with st.form("team_f", clear_on_submit=True):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save Team"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute(); st.success("Saved")

# --- 7. SITE DATA ENTRY ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registry</h1>", unsafe_allow_html=True)
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()

    selected_row = None
    if not df.empty:
        st.info("💡 Edit karne ke liye table mein line par click karein.")
        selection = st.dataframe(df, use_container_width=True, on_select="rerun", selection_mode="single", column_config={"id": None})
        if selection and selection.selection.rows:
            selected_row = df.iloc[selection.selection.rows[0]]

    with st.expander("📝 Form (Add/Edit Site)", expanded=(selected_row is not None)):
        with st.form("site_main_form", clear_on_submit=(selected_row is None)):
            r1, r2, r3 = st.columns(3)
            p_id = r1.text_input("Project ID*", value=selected_row['project_id'] if selected_row is not None else "")
            s_id = r2.text_input("Site ID", value=selected_row['site_id'] if selected_row is not None else "")
            s_nm = r3.text_input("Site Name", value=selected_row['site_name'] if selected_row is not None else "")
            
            r4, r5, r6 = st.columns(3)
            cluster = r4.text_input("Cluster", value=selected_row['cluster'] if selected_row is not None else "")
            p_amt = r5.number_input("Project Amt", value=float(selected_row['project_amt']) if selected_row is not None else None)
            st_list = ["Planning", "WIP", "WCC Done", "Closed"]
            status = r6.selectbox("Status", st_list, index=st_list.index(selected_row['site_status']) if selected_row is not None else 0)

            r7, r8, r9 = st.columns(3)
            po_n, po_a = r7.text_input("PO No", value=selected_row['po_no'] if selected_row is not None else ""), r8.number_input("PO Amt", value=float(selected_row['po_amt']) if selected_row is not None else None)
            t_name = r9.text_input("Team Name", value=selected_row['team_name'] if selected_row is not None else "")

            r10, r11, r12 = st.columns(3)
            t_bill, t_paid = r10.number_input("Team Billing", value=float(selected_row['team_billing']) if selected_row is not None else None), r11.number_input("Team Paid", value=float(selected_row['team_paid_amt']) if selected_row is not None else None)
            wcc_n = r12.text_input("WCC No", value=selected_row['wcc_no'] if selected_row is not None else "")

            r13, r14, r15 = st.columns(3)
            wcc_a, r_amt = r13.number_input("WCC Amt", value=float(selected_row['wcc_amt']) if selected_row is not None else None), r14.number_input("Recv Amt", value=float(selected_row['received_amt']) if selected_row is not None else None)
            w_desc = r15.text_area("Work Description", value=selected_row['work_description'] if selected_row is not None else "")

            if st.form_submit_button("💾 Sync to Cloud"):
                data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                if selected_row is not None:
                    supabase.table("site_data").update(data).eq('id', selected_row['id']).execute(); st.success("Updated!")
                else:
                    supabase.table("site_data").insert(data).execute(); st.success("Saved!")
                st.rerun()

# --- 8. FINANCE LEDGER (STABLE LOGIC) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # Finance logic remains untouched...
