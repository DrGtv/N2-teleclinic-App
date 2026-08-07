import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse
import os
import base64

# 1. Page Configuration
st.set_page_config(
    page_title="N2 Care Teleclinic | Your Friendly Second Opinion",
    page_icon="🩺",
    layout="wide"
)

# Robust Logo Auto-Detection & Base64 Encoder
def get_logo_base64():
    possible_files = ["logo.png", "logo.jpg", "logo.jpeg", "Logo.png", "116741.jpg"]
    for file in possible_files:
        if os.path.exists(file):
            with open(file, "rb") as f:
                encoded = base64.b64encode(f.read()).decode()
                ext = file.split(".")[-1].lower()
                if ext == "jpg":
                    ext = "jpeg"
                return f"data:image/{ext};base64,{encoded}"
    return "https://raw.githubusercontent.com/DrGtv/N2-teleclinic-App/main/logo.png"

logo_src = get_logo_base64()

# Configuration & Clinic Settings
CLINIC_PHONE = "919486872627"
UPI_ID = "9486872627@upi"
CONSULTATION_FEE = "₹100"
BOOKING_HOURS = "9:00 AM – 3:00 PM"
REVIEW_HOURS = "4:00 PM – 6:00 PM (Daily)"
DOCTOR_PIN = "1234"

# 2. Database Initialization
conn = sqlite3.connect('n2_teleclinic.db', check_same_thread=False)
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS patients (
        patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
        entry_date TEXT,
        patient_name TEXT,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        address TEXT,
        bp TEXT,
        pulse TEXT,
        spo2 TEXT,
        temp TEXT,
        complaints TEXT,
        investigation TEXT,
        treatment_history TEXT,
        prescription_details TEXT,
        consultation_type TEXT,
        preferred_slot TEXT,
        followup_date TEXT
    )
''')
conn.commit()

# Helper Functions
def get_whatsapp_url(service_name):
    msg = f"Hello N2 Care Teleclinic, I would like to consult for '{service_name}' (Fee: {CONSULTATION_FEE}). I am sending my reports/voice notes between {BOOKING_HOURS}."
    return f"https://wa.me/{CLINIC_PHONE}?text={urllib.parse.quote(msg)}"

def get_upi_qr_url():
    upi_payload = f"upi://pay?pa={UPI_ID}&pn=N2%20Care%20Teleclinic&am=100&cu=INR"
    return f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={urllib.parse.quote(upi_payload)}"

# 3. CSS Stylesheet Injection
st.markdown("""
<style>
    .header-card {
        background: linear-gradient(135deg, #0b3c5d 0%, #1d5b84 100%);
        padding: 25px;
        border-radius: 16px;
        color: white;
        text-align: center;
        box-shadow: 0 10px 25px rgba(11, 60, 93, 0.15);
        margin-bottom: 25px;
    }
    .clinic-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: 1px;
        margin: 12px 0 2px 0;
        color: #ffffff;
    }
    .clinic-tagline {
        font-size: 18px;
        font-style: italic;
        color: #38bdf8;
        margin-bottom: 12px;
        font-weight: 600;
    }
    .doc-badge {
        background: rgba(255, 255, 255, 0.12);
        backdrop-filter: blur(6px);
        padding: 12px 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        display: inline-block;
        margin: 6px;
        text-align: left;
    }
    .tnmc-verified {
        background-color: #0284c7;
        color: white;
        padding: 3px 8px;
        border-radius: 10px;
        font-size: 11px;
        font-weight: bold;
        display: inline-block;
        margin-top: 4px;
    }
    .trust-pill {
        background-color: #059669;
        color: white;
        padding: 8px 20px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
        display: inline-block;
        margin-top: 15px;
    }
    .service-card {
        border: 1px solid #e2e8f0;
        padding: 22px;
        border-radius: 12px;
        background-color: #ffffff;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        height: 100%;
    }
    .btn-wa {
        background-color: #25D366;
        color: white !important;
        padding: 10px 20px;
        font-weight: 700;
        text-decoration: none;
        border-radius: 8px;
        display: inline-block;
        margin-top: 10px;
        box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Header HTML Injection
header_html = f"""
<div class="header-card">
    <div>
        <img src="{logo_src}" 
             onerror="this.onerror=null; this.src='https://cdn-icons-png.flaticon.com/512/3063/3063176.png';" 
             style="max-height: 120px; max-width: 90%; width: auto; background: #ffffff; padding: 10px 18px; border-radius: 14px; box-shadow: 0px 4px 15px rgba(0,0,0,0.25);">
    </div>
    <div class="clinic-title">N2 CARE TELECLINIC</div>
    <div class="clinic-tagline">"Your Friendly Second Opinion"</div>
    <p style="font-size: 14px; color: #e0f2fe; margin-top: -6px;">One Care. Many Specialties. One Purpose.</p>
    
    <div style="margin-top: 15px;">
        <div class="doc-badge">
            👨‍⚕️ <b>Dr. Vigneshwar</b> <br>
            <small style="color: #93c5fd;">MBBS, MD General Medicine</small><br>
            <span class="tnmc-verified">✓ TNMC Verified: Reg No 159693</span>
        </div>
        <div class="doc-badge">
            👩‍⚕️ <b>Dr. S. Malathi</b> <br>
            <small style="color: #93c5fd;">MBBS, MD General Medicine</small><br>
            <span class="tnmc-verified">✓ TNMC Verified Practitioner</span>
        </div>
    </div>

    <div style="margin-top: 15px; display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;">
        <span style="background-color: #ef4444; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 13px;">
            Fee: {CONSULTATION_FEE} Only
        </span>
        <span style="background-color: #0284c7; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 13px;">
            📩 Report Submission: {BOOKING_HOURS}
        </span>
        <span style="background-color: #10b981; color: white; padding: 6px 14px; border-radius: 20px; font-weight: bold; font-size: 13px;">
            🩺 Doctor Review Window: {REVIEW_HOURS}
        </span>
    </div>
    
    <div class="trust-pill">
        🛡️ Tamil Nadu Medical Council (TNMC) Registered Doctors | 100% Confidential
    </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# 4. Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "🤝 Patient Portal & Booking ({})".format(CONSULTATION_FEE),
    "🔒 Doctor Entry Dashboard",
    "🔒 Patient Database & E-Prescription"
])

# TAB 1: Public Patient Portal
with tab1:
    st.markdown("""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; margin-bottom: 25px;">
            <h4 style="color: #0f172a; margin-top: 0; text-align: center;">🏥 How Your Online Second Opinion Works</h4>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center; margin-top: 15px; gap: 15px;">
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 28px;">1️⃣</div>
                    <b>Send Reports</b>
                    <p style="font-size: 13px; color: #64748b;">Share lab results, prescriptions, or voice notes via WhatsApp between 9 AM - 3 PM.</p>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 28px;">2️⃣</div>
                    <b>Doctor Analysis</b>
                    <p style="font-size: 13px; color: #64748b;">MD General Medicine specialists review your medical history daily from 4 PM - 6 PM.</p>
                </div>
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 28px;">3️⃣</div>
                    <b>Receive Guidance</b>
                    <p style="font-size: 13px; color: #64748b;">Get clear treatment validation, drug safety checks, or diet advice directly on WhatsApp.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.info("🎙️ **Can't type long text?** You can record a short WhatsApp voice message explaining your symptoms alongside your report photos!")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"""
            <div class="service-card">
                <h4 style="color: #0b3c5d; margin-top: 0;">🔬 Lab Report Review & Second Opinion</h4>
                <p style="color: #475569; font-size: 14px;">Unsure about lab tests or scans? Get an independent, expert MD review on your diagnosis and treatment plan safety.</p>
                <p><b>Consultation Fee:</b> <span style="color: #ef4444; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Lab Report Review & Second Opinion')}" target="_blank" class="btn-wa">
                    💬 Book Second Opinion on WhatsApp
                </a>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
            <div class="service-card">
                <h4 style="color: #0b3c5d; margin-top: 0;">💊 Medication & Side-Effect Safety Check</h4>
                <p style="color: #475569; font-size: 14px;">Verify drug dosages, understand potential side effects, check long-term drug safety, or resolve medication doubts.</p>
                <p><b>Consultation Fee:</b> <span style="color: #ef4444; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Drug & Medication Review')}" target="_blank" class="btn-wa">
                    💬 Ask About Medicines
                </a>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
            <div class="service-card">
                <h4 style="color: #0b3c5d; margin-top: 0;">🥗 Clinical Diet & Lifestyle Guidance</h4>
                <p style="color: #475569; font-size: 14px;">Evidence-based dietary advice for managing Diabetes, Hypertension, Fatty Liver, Cholesterol, and Metabolic conditions.</p>
                <p><b>Consultation Fee:</b> <span style="color: #ef4444; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Diet & Nutrition Guidance')}" target="_blank" class="btn-wa">
                    💬 Request Diet Guidance
                </a>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
            <div class="service-card">
                <h4 style="color: #0b3c5d; margin-top: 0;">📈 Chronic Illness Tracker & Progression</h4>
                <p style="color: #475569; font-size: 14px;">Regular health check-ins to monitor disease trends over time and implement preventive steps for long-term health.</p>
                <p><b>Consultation Fee:</b> <span style="color: #ef4444; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Disease Progression Check')}" target="_blank" class="btn-wa">
                    💬 Book Health Tracker
                </a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Secure Payment Section
    st.subheader("💳 Instant ₹100 Payment Portal")
    pay_col1, pay_col2 = st.columns([1, 2])
    
    with pay_col1:
        st.image(get_upi_qr_url(), caption="Scan using GPay / PhonePe / Paytm", width=200)
        
    with pay_col2:
        st.markdown(f"""
            <div style="padding: 18px; background-color: #f8fafc; border-radius: 10px; border: 1px solid #e2e8f0;">
                <p style="margin-top: 0;"><b>Official Clinic UPI ID:</b> <code style="font-size: 16px; color: #0b3c5d; background: #e0f2fe; padding: 4px 8px; border-radius: 4px;">{UPI_ID}</code></p>
                <p><b>Fee:</b> ₹100 Only</p>
                <p><b>Official Contact / WhatsApp:</b> +91 94868 72627</p>
                <p style="font-size: 13px; color: #64748b; margin-bottom: 0;">
                    📌 <i>Once payment is completed, please share a screenshot of the confirmation in WhatsApp along with your health reports.</i>
                </p>
            </div>
        """, unsafe_allow_html=True)

# TAB 2: Internal Doctor Data Entry (PIN Protected)
with tab2:
    st.subheader("🔒 Doctor Internal Portal")
    pin_input_1 = st.text_input("Enter 4-Digit Doctor Passcode:", type="password", key="pin1")
    
    if pin_input_1 == DOCTOR_PIN:
        st.success("Authenticated Successfully.")
        st.subheader("📝 New Patient Registration & Clinical Notes")
        
        with st.form("clinical_entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                patient_name = st.text_input("1. Patient Name *")
                age = st.number_input("2. Age", min_value=0, max_value=120, value=25)
                gender = st.selectbox("3. Gender", ["Male", "Female", "Other"])
                phone = st.text_input("4. Contact Number")
                address = st.text_area("5. Address", height=80)

            with col2:
                consultation_type = st.selectbox("6. Consultation Focus", [
                    "Second Opinion (Report Review)",
                    "Drug / Medication Clarification",
                    "Diet & Nutrition Planning",
                    "Disease Progression Tracker",
                    "General Medical Consultation"
                ])
                preferred_slot = st.selectbox("7. Review Time Slot", [
                    "4:00 PM - 4:30 PM",
                    "4:30 PM - 5:00 PM",
                    "5:00 PM - 5:30 PM",
                    "5:30 PM - 6:00 PM"
                ])
                followup_date = st.date_input("8. Follow-Up Date")
                
                st.markdown("<b>9. Patient Vitals:</b>", unsafe_allow_html=True)
                v_col1, v_col2, v_col3, v_col4 = st.columns(4)
                bp = v_col1.text_input("BP", placeholder="120/80")
                pulse = v_col2.text_input("Pulse", placeholder="72")
                spo2 = v_col3.text_input("SpO2 %", placeholder="98%")
                temp = v_col4.text_input("Temp", placeholder="98.6 F")

            st.markdown("---")
            col_c1, col_c2 = st.columns(2)
            with col_c1:
                complaints = st.text_area("10. Chief Complaints / Symptoms", height=100)
                investigation = st.text_area("11. Lab Reports & Scans Review", height=100)
            with col_c2:
                treatment_history = st.text_area("12. Clinical Advice / Notes", height=100)
                prescription_details = st.text_area(
                    "13. Digital E-Prescription (Drug | Dosage | Duration | Instruction)", 
                    placeholder="1. Tab Paracetamol 650mg | 1-0-1 | 5 days | After Food\n2. Tab Pantoprazole 40mg | 1-0-0 | 7 days | Before Food",
                    height=100
                )

            submit_btn = st.form_submit_button("💾 Save Patient Clinical Record")

            if submit_btn:
                if not patient_name.strip():
                    st.error("Patient Name is required!")
                else:
                    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    c.execute('''
                        INSERT INTO patients (
                            entry_date, patient_name, age, gender, phone, address, 
                            bp, pulse, spo2, temp, complaints, investigation, 
                            treatment_history, prescription_details, consultation_type, 
                            preferred_slot, followup_date
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        entry_time, patient_name, age, gender, phone, address,
                        bp, pulse, spo2, temp, complaints, investigation,
                        treatment_history, prescription_details, consultation_type,
                        preferred_slot, str(followup_date)
                    ))
                    conn.commit()
                    st.success(f"Record successfully saved for {patient_name}!")
    elif pin_input_1:
        st.error("Incorrect Passcode.")

# TAB 3: Searchable Records & Printable Rx Sheet (PIN Protected)
with tab3:
    st.subheader("🔒 Doctor Internal Portal")
    pin_input_2 = st.text_input("Enter 4-Digit Doctor Passcode:", type="password", key="pin2")

    if pin_input_2 == DOCTOR_PIN:
        st.success("Authenticated Successfully.")
        st.subheader("📋 Registered Patient Records & Printable E-Prescription")

        df = pd.read_sql_query("SELECT * FROM patients ORDER BY patient_id DESC", conn)

        if not df.empty:
            search_query = st.text_input("🔍 Search Patients by Name or Phone Number:")
            
            if search_query:
                df_filtered = df[
                    df['patient_name'].str.contains(search_query, case=False, na=False) |
                    df['phone'].str.contains(search_query, case=False, na=False)
                ]
            else:
                df_filtered = df

            st.dataframe(df_filtered, use_container_width=True)

            st.markdown("---")
            st.subheader("📄 Formal Clinical Summary & E-Prescription Pad")
            selected_id = st.selectbox("Select Patient ID to view Rx Pad:", df_filtered['patient_id'].tolist())
            
            patient_row = df_filtered[df_filtered['patient_id'] == selected_id].iloc[0]

            st.markdown(f"""
                <div style="border: 2px solid #0b3c5d; padding: 30px; border-radius: 12px; background-color: #ffffff; box-shadow: 0 4px 15px rgba(0,0,0,0.05);">
                    <div style="text-align: center; border-bottom: 2px solid #0b3c5d; padding-bottom: 12px; margin-bottom: 20px;">
                        <h2 style="color: #0b3c5d; margin: 0; letter-spacing: 1px;">N2 CARE TELECLINIC</h2>
                        <p style="margin: 3px 0; font-style: italic; font-weight: 700; color: #38bdf8;">"Your Friendly Second Opinion"</p>
                        <small style="color: #475569;"><b>Dr. Vigneshwar</b>, MBBS, MD (TNMC Reg No 159693) | <b>Dr. S. Malathi</b>, MBBS, MD</small><br>
                        <small style="color: #64748b;">WhatsApp: +91 94868 72627 | UPI: 9486872627@upi</small>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px;">
                        <div><b>Patient ID:</b> N2-{patient_row['patient_id']}</div>
                        <div><b>Date:</b> {patient_row['entry_date']}</div>
                    </div>
                    <hr style="border: 0.5px solid #cbd5e1;">
                    <p style="font-size: 14px;"><b>Patient Name:</b> {patient_row['patient_name']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Age/Gender:</b> {patient_row['age']} yrs / {patient_row['gender']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Phone:</b> {patient_row['phone']}</p>
                    <p style="font-size: 14px;"><b>Consultation Focus:</b> {patient_row['consultation_type']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Review Slot:</b> {patient_row['preferred_slot']}</p>
                    <p style="font-size: 14px;"><b>Vitals:</b> BP: {patient_row['bp']} | Pulse: {patient_row['pulse']} | SpO2: {patient_row['spo2']} | Temp: {patient_row['temp']}</p>
                    <hr style="border: 0.5px solid #cbd5e1;">
                    <p><b>Chief Complaints:</b><br>{patient_row['complaints']}</p>
                    <p><b>Investigations / Scans Review:</b><br>{patient_row['investigation']}</p>
                    <p><b>Clinical Advice & Notes:</b><br>{patient_row['treatment_history']}</p>
                    <hr style="border: 0.5px solid #cbd5e1;">
                    <h4 style="color: #ef4444; margin-bottom: 5px;">💊 Rx (Prescription):</h4>
                    <p style="background-color: #f8fafc; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; border: 1px solid #e2e8f0;">{patient_row['prescription_details']}</p>
                    <hr style="border: 0.5px solid #cbd5e1;">
                    <p style="text-align: right; font-size: 14px;"><b>Next Recommended Follow-Up Date:</b> {patient_row['followup_date']}</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Full Database (CSV)",
                data=csv_data,
                file_name=f"N2_Care_Patients_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No patient records registered yet.")
    elif pin_input_2:
        st.error("Incorrect Passcode.")        
                        
        
