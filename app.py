import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse
import os

# 1. Page Configuration
st.set_page_config(
    page_title="N2 Care Teleclinic | Your Friendly Second Opinion",
    page_icon="🩺",
    layout="wide"
)

# Configuration Settings
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
def get_whatsapp_url(service_name, custom_notes=""):
    msg = f"Hello N2 Care Teleclinic, I would like to consult for '{service_name}' (Fee: {CONSULTATION_FEE})."
    if custom_notes:
        msg += f"\nDetails: {custom_notes}"
    msg += f"\nI am sending my reports/voice notes between {BOOKING_HOURS}."
    return f"https://wa.me/{CLINIC_PHONE}?text={urllib.parse.quote(msg)}"

def get_upi_qr_url():
    upi_payload = f"upi://pay?pa={UPI_ID}&pn=N2%20Care%20Teleclinic&am=100&cu=INR"
    return f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={urllib.parse.quote(upi_payload)}"

# 3. Clean CSS Styles
st.markdown("""
<style>
    .service-card {
        border: 1px solid #e2e8f0;
        padding: 20px;
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
    .inst-card {
        border-left: 4px solid #0284c7;
        background: #f8fafc;
        padding: 12px 16px;
        margin-bottom: 10px;
        border-radius: 6px;
    }
</style>
""", unsafe_allow_html=True)

# 4. Native Header UI with Direct logo.jpg Detection
col_l1, col_l2, col_l3 = st.columns([1, 2, 1])
with col_l2:
    logo_files = ["logo.jpg", "logo.png", "logo.jpeg", "Logo.png"]
    logo_found = False
    for f in logo_files:
        if os.path.exists(f):
            st.image(f, use_container_width=True)
            logo_found = True
            break
    if not logo_found:
        st.markdown("<h1 style='text-align: center; color: #0b3c5d;'>🏥 N2 CARE TELECLINIC</h1>", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align: center; margin-top: -10px; margin-bottom: 15px;">
        <h2 style="color: #0b3c5d; margin-bottom: 2px;">N2 CARE TELECLINIC</h2>
        <p style="font-size: 18px; font-style: italic; color: #0284c7; font-weight: 600; margin-top: 0;">"Your Friendly Second Opinion"</p>
        <p style="font-size: 14px; color: #475569; margin-top: -8px;">One Care. Many Specialties. One Purpose.</p>
    </div>
""", unsafe_allow_html=True)

# Doctor Verification Badges
d_col1, d_col2 = st.columns(2)
with d_col1:
    st.markdown("""
        <div style="background-color: #f0f9ff; border-left: 5px solid #0284c7; padding: 12px; border-radius: 8px;">
            👨‍⚕️ <b>Dr. Vigneshwar</b><br>
            <small style="color: #475569;">MBBS, MD General Medicine</small><br>
            <span style="background-color: #0284c7; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;">✓ TNMC Verified: Reg No 159693</span>
        </div>
    """, unsafe_allow_html=True)

with d_col2:
    st.markdown("""
        <div style="background-color: #f0f9ff; border-left: 5px solid #0284c7; padding: 12px; border-radius: 8px;">
            👩‍⚕️ <b>Dr. S. Malathi</b><br>
            <small style="color: #475569;">MBBS, MD General Medicine</small><br>
            <span style="background-color: #0284c7; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; font-weight: bold;">✓ TNMC Verified Practitioner</span>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Operational Status Banner
p_col1, p_col2, p_col3 = st.columns(3)
p_col1.error(f"Fee: {CONSULTATION_FEE} Only")
p_col2.info(f"📩 Report Submission: {BOOKING_HOURS}")
p_col3.success(f"🩺 Doctor Review: {REVIEW_HOURS}")

st.markdown("---")

# 5. Application Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🤝 Patient Portal & Booking",
    "🌐 National Directory & Referral Hub",
    "🔒 Doctor Dashboard",
    "🔒 Database & E-Prescription"
])

# TAB 1: Patient Consultation Portal
with tab1:
    st.markdown("""
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; padding: 20px; border-radius: 12px; margin-bottom: 25px;">
            <h4 style="color: #0f172a; margin-top: 0; text-align: center;">🏥 How Your Online Second Opinion Works</h4>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center; margin-top: 15px; gap: 15px;">
                <div style="flex: 1; min-width: 200px;">
                    <div style="font-size: 28px;">1️⃣</div>
                    <b>Send Reports</b>
                    <p style="font-size: 13px; color: #64748b;">Share lab results, scan links, or voice notes via WhatsApp between 9 AM - 3 PM.</p>
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

    # Interactive Consultation Form
    st.subheader("📋 Quick Consultation Request Builder")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        query_type = st.selectbox("I need help with:", [
            "Lab & Blood Report Review",
            "CT / MRI Scan Second Opinion",
            "Drug Side-Effects & Dosage Check",
            "Diet & Nutrition Plan",
            "Chronic Disease Progression Tracking"
        ])
    with col_q2:
        report_link = st.text_input("Report / Google Drive Link (Optional):", placeholder="https://drive.google.com/...")

    notes_input = st.text_input("Briefly describe your question/concern:", placeholder="e.g. Need second opinion on lab reports or current medication...")
    
    combined_query = f"Focus: {query_type}"
    if report_link:
        combined_query += f" | Report Link: {report_link}"
    if notes_input:
        combined_query += f" | Notes: {notes_input}"

    st.markdown(f'''
        <a href="{get_whatsapp_url(query_type, combined_query)}" target="_blank" class="btn-wa" style="font-size: 16px;">
            💬 Send Consultation Request via WhatsApp (Fee: {CONSULTATION_FEE})
        </a>
    ''', unsafe_allow_html=True)

    st.markdown("---")

    # Service Modules
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
    
    # UPI Payment Gateway
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

# TAB 2: National Directory & Tertiary Care Hub
with tab2:
    st.subheader("🌐 Premier National Institutes & Medical Referral Directory")
    st.write("Explore premier healthcare institutions across India alongside **N2 Care Teleclinic** for tele-consultations, report validations, and tertiary care referrals:")

    dir_col1, dir_col2 = st.columns(2)

    with dir_col1:
        st.markdown("""
            <div class="inst-card">
                <b>🩺 N2 Care Teleclinic</b> — <a href="https://n2-teleclinic-app-7wvhshbbbpegzz7hne4gr3.streamlit.app/" target="_blank">Official Teleconsultation Portal</a><br>
                <small style="color: #475569;">₹100 Friendly Second Opinions | MD General Medicine Review</small>
            </div>
            <div class="inst-card">
                <b>🏛️ AIIMS New Delhi</b> — <a href="https://www.aiims.edu/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">Apex Autonomous Medical Institute of National Importance</small>
            </div>
            <div class="inst-card">
                <b>🏥 Apollo Hospitals</b> — <a href="https://www.apollohospitals.com/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">Multi-Specialty Super-Specialty Healthcare Network</small>
            </div>
            <div class="inst-card">
                <b>🏥 Christian Medical College (CMC), Vellore</b> — <a href="https://admissions.cmcvellore.ac.in/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">Premier Tertiary Research & Medical Institution</small>
            </div>
            <div class="inst-card">
                <b>🏥 Medanta – The Medicity, Gurugram</b> — <a href="https://www.medanta.org/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">Multi-Super Specialty Institute for Complex Care</small>
            </div>
            <div class="inst-card">
                <b>🏛️ PGIMER, Chandigarh</b> — <a href="https://pgimer.edu.in/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">Postgraduate Institute of Medical Education & Research</small>
            </div>
        """, unsafe_allow_html=True)

    with dir_col2:
        st.markdown("""
            <div class="inst-card">
                <b>🔬 Tata Memorial Centre, Mumbai</b> — <a href="https://tmc.gov.in/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">National Comprehensive Cancer Care & Research Center</small>
            </div>
            <div class="inst-card">
                <b>🏥 Kokilaben Dhirubhai Ambani Hospital</b> — <a href="https://www.kokilabenhospital.com/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">Advanced Multi-Specialty Tertiary Care Center, Mumbai</small>
            </div>
            <div class="inst-card">
                <b>🏥 Fortis Healthcare</b> — <a href="https://www.fortishealthcare.com/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">Leading Integrated Healthcare Delivery Service Provider</small>
            </div>
            <div class="inst-card">
                <b>🏥 Manipal Hospitals</b> — <a href="https://www.manipalhospitals.com/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">Pioneer Multi-Specialty Healthcare Network</small>
            </div>
            <div class="inst-card">
                <b>🏥 Narayana Health</b> — <a href="https://www.narayanahealth.org/" target="_blank">Official Website</a><br>
                <small style="color: #475569;">Affordable Cardiac & Multi-Specialty Care Network</small>
            </div>
        """, unsafe_allow_html=True)

# TAB 3: Doctor Internal Clinical Entry (PIN Protected)
with tab3:
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

# TAB 4: Searchable Patient Database & Printable Rx Pad (PIN Protected)
with tab4:
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
                        <p style="margin: 3px 0; font-style: italic; font-weight: 700; color: #0284c7;">"Your Friendly Second Opinion"</p>
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
