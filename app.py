# --- 7. SITE DATA ENTRY (ONLY NEW/FIXED LINES) ---
elif page == "🏗️ Site Data Entry":
    st.markdown("<h1>🏗️ Site Data Registry</h1>", unsafe_allow_html=True)
    if "edit_row_data" not in st.session_state: st.session_state.edit_row_data = None

    # Fetch Data
    res = supabase.table("site_data").select("*").execute()
    df = pd.DataFrame(res.data) if res.data else pd.DataFrame()

    # ACTION BAR (UPLOAD WAPAS LAYA GAYA HAI)
    tc1, tc2, tc3, tc4 = st.columns([1, 1, 1.5, 2.5])
    if tc1.button("➕ New Site"): 
        st.session_state.edit_row_data = None
        st.rerun()
    if not df.empty: tc2.download_button("📥 Download", data=to_excel(df), file_name="Site_Data.xlsx")
    
    # Bulk Upload Section - Fixed Position
    uploaded_file = tc3.file_uploader("📤 Bulk Upload", type=['xlsx'], label_visibility="collapsed")
    search = tc4.text_input("🔍 Search Database...", placeholder="Search Site ID, Project ID...")

    # FORM SECTION (SAME LOGIC - NO CHANGE)
    er = st.session_state.edit_row_data
    is_editing = er is not None
    exp_label = f"📝 Editing: {er['project_id']}" if is_editing else "➕ Add New Site Entry"
    
    with st.expander(exp_label, expanded=is_editing):
        with st.form("site_full_form", clear_on_submit=not is_editing):
            c1, c2, c3 = st.columns(3)
            p_id, s_id, s_nm = c1.text_input("Project ID*", value=str(er['project_id']) if is_editing else ""), c2.text_input("Site ID", value=str(er['site_id']) if is_editing else ""), c3.text_input("Site Name", value=str(er['site_name']) if is_editing else "")
            c4, c5, c6 = st.columns(3)
            cluster, p_amt = c4.text_input("Cluster", value=str(er['cluster']) if is_editing else ""), c5.number_input("Project Amount", value=float(er['project_amt']) if is_editing and er['project_amt'] else None)
            st_list = ["Planning", "WIP", "WCC Done", "Closed"]
            s_idx = st_list.index(er['site_status']) if is_editing and er['site_status'] in st_list else 0
            status = c6.selectbox("Status", st_list, index=s_idx)
            c7, c8, c9 = st.columns(3)
            po_n, po_a, t_name = c7.text_input("PO Number", value=str(er['po_no']) if is_editing else ""), c8.number_input("PO Amount", value=float(er['po_amt']) if is_editing and er['po_amt'] else None), c9.text_input("Team Name", value=str(er['team_name']) if is_editing else "")
            c10, c11, c12 = st.columns(3)
            t_bill, t_paid, wcc_n = c10.number_input("Team Billing", value=float(er['team_billing']) if is_editing and er['team_billing'] else None), c11.number_input("Team Paid", value=float(er['team_paid_amt']) if is_editing and er['team_paid_amt'] else None), c12.text_input("WCC Number", value=str(er['wcc_no']) if is_editing else "")
            c13, c14, c15 = st.columns(3)
            wcc_a, r_amt, w_desc = c13.number_input("WCC Amount", value=float(er['wcc_amt']) if is_editing and er['wcc_amt'] else None), c14.number_input("Received Amount", value=float(er['received_amt']) if is_editing and er['received_amt'] else None), c15.text_area("Work Description", value=str(er['work_description']) if is_editing else "")

            if st.form_submit_button("🚀 SAVE DATA"):
                data = {"project_id": p_id, "site_id": s_id, "site_name": s_nm, "cluster": cluster, "work_description": w_desc, "site_status": status, "project_amt": p_amt or 0, "po_no": po_n, "po_amt": po_a or 0, "team_name": t_name, "team_billing": t_bill or 0, "team_paid_amt": t_paid or 0, "wcc_no": wcc_n, "wcc_amt": wcc_a or 0, "received_amt": r_amt or 0}
                if is_editing: supabase.table("site_data").update(data).eq('id', er['id']).execute(); st.session_state.edit_row_data = None
                else: supabase.table("site_data").insert(data).execute()
                st.rerun()

    st.divider()
    
    # SINGLE CLEAN TABLE VIEW (DO TABLE WALA KAAM KHATAM)
    if not df.empty:
        if search: df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        
        st.subheader("📋 Detailed Database")
        
        # Display Logic: Action Button and Horizontal Data in one Row
        for idx, row in df.iterrows():
            # Column configuration to match your 'Lavish' look
            r = st.columns([0.6, 1.5, 1.5, 2, 2, 1.5, 2])
            if r[0].button("📝", key=f"btn_{row['id']}"):
                st.session_state.edit_row_data = row.to_dict()
                st.rerun()
            
            # Show all key columns in one row
            r[1].write(f"**ID:** {row['project_id']}")
            r[2].write(f"**Site:** {row['site_id']}")
            r[3].write(row['site_name'])
            r[4].write(row['team_name'])
            r[5].write(f"Status: {row['site_status']}")
            
            # Calculate Balance for display
            bal = float(row['team_billing'] or 0) - float(row['team_paid_amt'] or 0)
            r[6].write(f"Bal: ₹{bal:,.0f}")
            st.divider()

        # Download raw data hidden at bottom if needed
        with st.expander("📊 View Complete Raw Data Grid"):
            st.dataframe(df.drop(columns=['id']), use_container_width=True)
