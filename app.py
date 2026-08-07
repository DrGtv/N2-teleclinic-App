import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# Initialize SQLite Database
conn = sqlite3.connect('n2_teleclinic.db', check_same_thread=False)
c = conn.cursor()

# Create table for requested patient details
c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_date TEXT,
        patient_name TEXT,
        age INTEGER,
        address TEXT,
        complaints TEXT,
        investigation TEXT,
        treatment_history TEXT
    )
''')
conn.commit()

# Page Setup
st.set_page_config(page_title="N2 Care Teleclinic", layout="wide")
st.title("🏥 N2 Care Teleclinic - Patient Records System")

# Entry Form
with st.form("patient_form", clear_on_submit=True):
    st.subheader("📝 New Patient Entry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        patient_name = st.text_input("1. Patient Name *")
        age = st.number_input("2. Age", min_value=0, max_value=120, value=25)
        address = st.text_area("3. Address", height=120)
        
    with col2:
        complaints = st.text_area("4. Complaints", height=80)
        investigation = st.text_area("5. Investigation", height=80)
        treatment_history = st.text_area("6. Treatment History", height=80)

    submit_button = st.form_submit_button("Save Record")
    
    if submit_button:
        if not patient_name.strip():
            st.error("Patient Name is required.")
        else:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            c.execute('''
                INSERT INTO patients (entry_date, patient_name, age, address, complaints, investigation, treatment_history)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (current_time, patient_name, age, address, complaints, investigation, treatment_history))
            conn.commit()
            st.success(f"Record successfully saved for {patient_name}.")

# Database View
st.markdown("---")
st.subheader("📋 Registered Patient Records")

df = pd.read_sql_query("""
    SELECT 
        patient_id AS 'ID',
        entry_date AS 'Date & Time',
        patient_name AS 'Patient Name',
        age AS 'Age',
        address AS 'Address',
        complaints AS 'Complaints',
        investigation AS 'Investigation',
        treatment_history AS 'Treatment History'
    FROM patients 
    ORDER BY patient_id DESC
""", conn)

st.dataframe(df, use_container_width=True)

# Export Data Button
if not df.empty:
    csv_data = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Data (Excel / CSV)",
        data=csv_data,
        file_name=f"N2_Care_Patients_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )
