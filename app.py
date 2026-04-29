import streamlit as st
from supabase import create_client, Client
import pandas as pd
from datetime import datetime
import io

# --- 1. PAGE CONFIG & CLEAN LOOK ---
st.set_page_config(page_title="Visiontech Site Data", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap');
    html, body, [class*="st-"] { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; }
    h1 { font-weight: 800; color: #0984e3; }
    div.stForm { background: #f8fafc; border-radius: 20px; border: 1px solid #e2e8f0; padding: 30px; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(135deg, #0f172a 0%, #334155 100%); color: white !important; border-radius: 10px; font-weight: 700; width: 100%; }
    .edit-btn>button { background: #ff9f43 !important; color: white !important; height: 35px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. SUPABASE ---
URL = "https://rdfntkqdpsotoerfrhiv.supabase.co"
KEY = "sb_publishable_nm3ciqWOzXwRj1pSj1NagA__WV9eVBc"
supabase = create_client(URL, KEY)

# --- 3. DATA FETCH ---
def get_data():
    res = supabase.table("site_data").select("*").execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

df = get_data()

# --- 4. EDIT LOGIC (STATE MANAGEMENT) ---
if "edit_row" not in st.session_state:
    st.session_state.edit_row = None

# --- 5. FORM SECTION ---
st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)

# Agar koi row edit ke liye select hui hai toh form upar dikhega
form_title = "📝 Edit Site Record" if st.session_state.edit_row else "➕ Add New Site Entry"
with st.form("site_form", clear_on_submit=True):
    st.subheader(form_title)
    row = st.session_state.edit_row
    
    c1, c2, c3 = st.columns(3)
    p_id = c1.text_input("Project ID*", value=row['project_id'] if row else "")
    s_id = c2.text_input("Site ID", value=row['site_id'] if row else "")
    s_nm = c3.text_input("Site Name", value=row['site_name'] if row else "")
    
    c4, c5, c6 = st.columns(3)
    cluster = c4.text_input("Cluster", value=row['cluster'] if row else "")
    p_amt = c5.number_input("Project Amt", value=float(row['project_amt']) if row else None)
    status_list = ["Planning", "WIP", "WCC Done", "Closed"]
    curr_status = row['site_status'] if row else "Planning"
    status = c6.selectbox("Status", status_list, index=status_list.index(curr_status) if curr_status in status_list else 0)

    c7, c8, c9 = st.columns(3)
    po_n = c7.text_input("PO No", value=row['po_no'] if row else "")
    po_a = c8.number_input("PO Amt", value=float(row['po_amt']) if row else None)
    t_name = c9.text_input("Team Name", value=row['team_name'] if row else "")

    c10, c11, c12 = st.columns(3)
    t_bill = c10.number_input("Team Billing", value=float(row['team_billing']) if row else None)
    t_paid = c11.number_input("Team Paid", value=float(row['team_paid_amt']) if row else None)
    wcc_n = c12.text_input("WCC No", value=row['wcc_no'] if row else "")

    c13, c14, c15 = st.columns(3)
    wcc_a = c13.number_input("WCC Amt", value=float(row['wcc_amt']) if row else None)
    r_amt = c14.number_input("Received Amt", value=float(row['received_amt']) if row else None)
    w_desc = c15.text_area("Work Description", value=row['work_description'] if row else "")

    sub_c1, sub_c2 = st.columns([1, 4])
    if sub_c1.form_submit_button("🚀 SAVE / UPDATE"):
        data = {
            "project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster,
            "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0,
            "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name,
            "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0,
            "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0
        }
        if row: # Update
            supabase.table("site_data").update(data).eq('id', row['id']).execute()
            st.session_state.edit_row = None
            st.success("Record Updated!")
        else: # Insert
            check = supabase.table("site_data").select("project_id").eq("project_id", p_id).execute()
            if check.data: st.error("Duplicate Project ID!")
            else:
                supabase.table("site_data").insert(data).execute()
                st.success("New Entry Saved!")
        st.rerun()
    
    if row:
        if sub_c2.form_submit_button("❌ CANCEL EDIT"):
            st.session_state.edit_row = None
            st.rerun()

st.divider()

# --- 6. DATA TABLE WITH ACTION BUTTONS ---
search = st.text_input("🔍 Search Site Database...")
if not df.empty:
    if search:
        df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
    
    # Header
    cols = st.columns([1, 2, 2, 2, 2, 2, 2])
    cols[0].write("**Action**")
    cols[1].write("**Project ID**")
    cols[2].write("**Site ID**")
    cols[3].write("**Site Name**")
    cols[4].write("**Team**")
    cols[5].write("**Status**")
    cols[6].write("**Balance**")
    st.divider()

    # Rows with Edit Button
    for i, r in df.iterrows():
        c = st.columns([1, 2, 2, 2, 2, 2, 2])
        # Har line ke aage Edit Button
        if c[0].button("📝 Edit", key=f"edit_{r['id']}"):
            st.session_state.edit_row = r
            st.rerun()
        
        c[1].write(r['project_id'])
        c[2].write(r['site_id'])
        c[3].write(r['site_name'])
        c[4].write(r['team_name'])
        c[5].write(r['site_status'])
        bal = float(r['team_billing'] or 0) - float(r['team_paid_amt'] or 0)
        c[6].write(f"₹ {bal:,.0f}")

st.markdown("<br><div style='text-align: center; color: #94a3b8;'>Visiontech Automation © 2026</div>", unsafe_allow_html=True)
