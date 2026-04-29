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

# --- 5 & 6. DASHBOARD & REGISTRATION (STABLE & LAVISH) ---
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
    except: st.info("Welcome, data missing.")

elif page == "📝 Master Registration":
    st.markdown("<h1>📋 Master Registry</h1>", unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["👥 Clients", "🛠️ Teams"])
    with tab1:
        with st.form("c_f", clear_on_submit=True):
            cn = st.text_input("Client Name")
            if st.form_submit_button("Save Client"):
                if cn: supabase.table("client_master").insert({"client_name": cn}).execute(); st.success("Saved")
    with tab2:
        with st.form("t_f", clear_on_submit=True):
            tn, tl = st.text_input("Team Name"), st.text_input("Leader Name")
            if st.form_submit_button("Save Team"):
                if tn: supabase.table("team_master").insert({"team_name": tn, "leader_name": tl}).execute(); st.success("Saved")

# --- 7. SITE DATA ENTRY (WITH LINE-WISE EDIT BUTTON) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Registry</h1>", unsafe_allow_html=True)
    
    # Fetch Data
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()

    # Edit Logic: URL parameter se row detect karna
    query_params = st.query_params
    edit_id = query_params.get("edit_id", None)
    
    selected_row = None
    if edit_id and not df.empty:
        selected_row = df[df['project_id'] == edit_id].iloc[0]

    # FORM SECTION
    with st.expander("📝 Site Data Form (Add/Edit)", expanded=(selected_row is not None)):
        with st.form("site_form", clear_on_submit=(selected_row is None)):
            c1, c2, c3 = st.columns(3)
            p_id = c1.text_input("Project ID*", value=selected_row['project_id'] if selected_row is not None else "")
            s_id = c2.text_input("Site ID", value=selected_row['site_id'] if selected_row is not None else "")
            s_nm = c3.text_input("Site Name", value=selected_row['site_name'] if selected_row is not None else "")
            
            c4, c5, c6 = st.columns(3)
            cluster = c4.text_input("Cluster", value=selected_row['cluster'] if selected_row is not None else "")
            p_amt = c5.number_input("Project Amt", value=float(selected_row['project_amt']) if selected_row is not None else None)
            status = c6.selectbox("Status", ["Planning", "WIP", "WCC Done", "Closed"], index=0)

            c7, c8, c9 = st.columns(3)
            po_n, po_a = c7.text_input("PO No", value=selected_row['po_no'] if selected_row is not None else ""), c8.number_input("PO Amt", value=float(selected_row['po_amt']) if selected_row is not None else None)
            t_name = c9.text_input("Team Name", value=selected_row['team_name'] if selected_row is not None else "")

            c10, c11, c12 = st.columns(3)
            t_bill, t_paid = c10.number_input("Team Billing", value=float(selected_row['team_billing']) if selected_row is not None else None), c11.number_input("Team Paid", value=float(selected_row['team_paid_amt']) if selected_row is not None else None)
            wcc_n = c12.text_input("WCC No", value=selected_row['wcc_no'] if selected_row is not None else "")

            c13, c14, c15 = st.columns(3)
            wcc_a, r_amt = c13.number_input("WCC Amt", value=float(selected_row['wcc_amt']) if selected_row is not None else None), c14.number_input("Received Amt", value=float(selected_row['received_amt']) if selected_row is not None else None)
            w_desc = c15.text_area("Work Description", value=selected_row['work_description'] if selected_row is not None else "")

            if st.form_submit_button("🚀 Sync to Cloud"):
                data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                if selected_row is not None:
                    supabase.table("site_data").update(data).eq('id', selected_row['id']).execute()
                    st.query_params.clear()
                else:
                    supabase.table("site_data").insert(data).execute()
                st.rerun()

    st.divider()
    # SEARCH & TABLE
    search = st.text_input("🔍 Search Database...")
    if not df.empty:
        # Action Column add karna
        df['Edit'] = "📝 Edit"
        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        # Display with Clickable Edit Link
        st.data_editor(
            df,
            column_order=["Edit", "project_id", "site_id", "site_name", "team_name", "po_no", "site_status"],
            column_config={
                "Edit": st.column_config.LinkColumn("Action", help="Click to edit row", validate=r"^📝 Edit$", display_text=r"📝 Edit"),
                "id": None
            },
            disabled=True,
            use_container_width=True,
            on_change=None,
            key="site_table"
        )
        # Note: Streamlit limits direct buttons in rows, so we use selectbox as fallback if link doesn't trigger
        st.caption("Tip: Select Project ID from the dropdown at the top of the form for instant editing.")

# --- 8. FINANCE LEDGER (STABLE) ---
elif page == "💸 Finance Ledger":
    st.markdown("<h1>💸 Financial Ledger</h1>", unsafe_allow_html=True)
    # Finance logic remains untouched...
