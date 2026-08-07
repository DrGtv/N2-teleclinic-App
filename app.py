import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse

# 1. Page Configuration
st.set_page_config(
    page_title="N2 Care Teleclinic - Your Friendly Second Opinion",
    page_icon="🩺",
    layout="wide"
)

# Configuration Variables
CLINIC_PHONE = "919486872627"  # Official WhatsApp Number
UPI_ID = "9486872627@upi"
CONSULTATION_FEE = "₹100"
BOOKING_HOURS = "9:00 AM – 3:00 PM"
REVIEW_HOURS = "4:00 PM – 6:00 PM (Daily)"
DOCTOR_PIN = "1234"  # Default 4-digit Doctor Passcode (Change as needed)

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

# Helper function to generate pre-filled WhatsApp links
def get_whatsapp_url(service_name):
    msg = f"Hello N2 Care Teleclinic, I would like to book a '{service_name}' (Fee: {CONSULTATION_FEE}). I am sending my reports/voice notes between {BOOKING_HOURS}."
    return f"https://wa.me/{CLINIC_PHONE}?text={urllib.parse.quote(msg)}"

# Helper function to generate dynamic UPI Payment QR Code URL
def get_upi_qr_url():
    upi_payload = f"upi://pay?pa={UPI_ID}&pn=N2%20Care%20Teleclinic&am=100&cu=INR"
    return f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(upi_payload)}"

# 3. Header & Clinic Branding
st.markdown(f"""
    <div style="text-align: center; background-color: #0f4c81; padding: 25px; border-radius: 12px; margin-bottom: 25px; color: white;">
        <svg width="70" height="70" viewBox="0 0 100 100" style="margin-bottom: 10px;">
            <circle cx="50" cy="50" r="45" fill="#ffffff" />
            <rect x="43" y="25" width="14" height="50" fill="#e63946" />
            <rect x="25" y="43" width="50" height="14" fill="#e63946" />
        </svg>
        <h1 style="margin: 0; font-size: 38px; color: #ffffff; font-weight: 700;">N2 CARE TELECLINIC</h1>
        <p style="font-size: 20px; font-style: italic; margin-top: 5px; color: #a8dadc; font-weight: bold;">"Your Friendly Second Opinion"</p>
        <p style="font-size: 14px; margin-top: -5px; color: #f1faee;">Need for the needs</p>
        <hr style="border: 0.5px solid #457b9d; margin: 15px 0;">
        <div style="display: flex; justify-content: center; gap: 30px; flex-wrap: wrap; font-size: 16px;">
            <div>👨‍⚕️ <b>Dr. Vigneshwar</b> <br><small>MBBS, MD General Medicine</small></div>
            <div>👩‍⚕️ <b>Dr. S. Malathi</b> <br><small>MBBS, MD General Medicine</small></div>
        </div>
        <div style="margin-top: 15px; display: flex; justify-content: center; gap: 12px; flex-wrap: wrap;">
            <span style="background-color: #e63946; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 14px;">
                Affordable Fee: {CONSULTATION_FEE} Only
            </span>
            <span style="background-color: #1d3557; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 14px; color: #f1faee;">
                📩 Send Details: {BOOKING_HOURS}
            </span>
            <span style="background-color: #2a9d8f; padding: 6px 16px; border-radius: 20px; font-weight: bold; font-size: 14px; color: #ffffff;">
                🩺 Doctor Review Window: {REVIEW_HOURS}
            </span>
        </div>
        <p style="margin-top: 15px; font-size: 13px; color: #a8dadc;">
            ✨ Powered by Budding Young Doctors | WhatsApp: <b>+91 94868 72627</b>
        </p>
    </div>
""", unsafe_allow_html=True)

# 4. Navigation Tabs
tab1, tab2, tab3 = st.tabs([
    "🤝 Patient Services & Booking ({})".format(CONSULTATION_FEE),
    "🔒 Doctor Dashboard (PIN Protected)",
    "🔒 Patient Records & E-Prescription (PIN Protected)"
])

# TAB 1: Public Patient Portal & Friendly Branding
with tab1:
    st.markdown(f"""
        <div style="background-color: #f0f7f7; border-left: 6px solid #2a9d8f; padding: 20px; border-radius: 8px; margin-bottom: 25px;">
            <h3 style="color: #0f4c81; margin-top: 0;">🤝 Got Medical Doubts? Don't Guess. Ask Us!</h3>
            <p style="font-size: 15px; color: #333333; line-height: 1.6; margin-bottom: 5px;">
                Medical decisions can feel overwhelming. Whether you want to double-check a treatment plan, 
                understand complex lab reports, ask about drug side effects, or plan your diet for chronic illnesses, 
                <b>N2 Care Teleclinic</b> provides caring, expert doctor reviews for <b>{CONSULTATION_FEE}</b>.
            </p>
            <p style="margin-bottom: 0; font-weight: bold; color: #2a9d8f; font-size: 14px;">
                📩 Send details: {BOOKING_HOURS} | 🩺 Doctor Consultations: {REVIEW_HOURS}
            </p>
        </div>
    """, unsafe_allow_html=True)

    # Voice Note & Report Reminder Banner
    st.info("🎙️ **Can't type a long message?** Simply send us a WhatsApp Voice Note explaining your problem along with photos of your medical reports!")

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4>🔬 Lab Report Review & Second Opinion</h4>
                <p style="color: #555555; font-size: 14px;">Upload your blood reports, scans, or prescriptions for a comprehensive second opinion on your diagnosis and treatment safety.</p>
                <b>Fee: {CONSULTATION_FEE}</b><br><br>
                <a href="{get_whatsapp_url('Lab Report Review & Second Opinion')}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 18px; font-weight: bold; text-decoration: none; border-radius: 6px; display: inline-block;">
                    💬 Book Second Opinion via WhatsApp
                </a>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4>💊 Drug, Dosage & Side-Effect Doubts</h4>
                <p style="color: #555555; font-size: 14px;">Clear your queries regarding long-term medications, drug interactions, proper timing, or potential side effects.</p>
                <b>Fee: {CONSULTATION_FEE}</b><br><br>
                <a href="{get_whatsapp_url('Drug & Medication Review')}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 18px; font-weight: bold; text-decoration: none; border-radius: 6px; display: inline-block;">
                    💬 Ask About Medicines
                </a>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4>🥗 Diet & Medical Nutrition Guidance</h4>
                <p style="color: #555555; font-size: 14px;">Tailored dietary advice for Diabetes, Hypertension, Fatty Liver, Kidney health, and lifestyle disease management.</p>
                <b>Fee: {CONSULTATION_FEE}</b><br><br>
                <a href="{get_whatsapp_url('Diet & Nutrition Guidance')}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 18px; font-weight: bold; text-decoration: none; border-radius: 6px; display: inline-block;">
                    💬 Get Diet Plan
                </a>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
            <div style="border: 1px solid #e0e0e0; padding: 20px; border-radius: 10px; background-color: #ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                <h4>📈 Chronic Illness Progression Check</h4>
                <p style="color: #555555; font-size: 14px;">Track disease progression trends over time and plan preventive steps for long-term wellness.</p>
                <b>Fee: {CONSULTATION_FEE}</b><br><br>
                <a href="{get_whatsapp_url('Disease Progression Check')}" target="_blank" style="background-color: #25D366; color: white; padding: 10px 18px; font-weight: bold; text-decoration: none; border-radius: 6px; display: inline-block;">
                    💬 Book Health Tracker
                </a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Instant UPI Payment Section
    st.subheader("💳 Instant ₹100 Payment via UPI")
    pay_col1, pay_col2 = st.columns([1, 2])
    
    with pay_col1:
        st.image(get_upi_qr_url(), caption="Scan with GPay / PhonePe / Paytm to Pay ₹100", width=200)
        
    with pay_col2:
        st.markdown(f"""
            <div style="padding: 15px; background-color: #f8f9fa; border-radius: 8px; border: 1px solid #e0e0e0;">
                <p><b>GPay / PhonePe / Paytm UPI ID:</b> <code style="font-size: 16px; color: #0f4c81;">{UPI_ID}</code></p>
                <p><b>Consultation Fee:</b> ₹100 Only</p>
                <p style="font-size: 13px; color: #666666;">
                    📌 <i>After completing payment, please attach a screenshot of the payment receipt along with your health details or reports in WhatsApp.</i>
                </p>
            </div>
        """, unsafe_allow_html=True)


# TAB 2: Clinical Data Entry (Doctor Authenticated)
with tab2:
    st.subheader("🔒 Doctor Access Portal")
    pin_input_1 = st.text_input("Enter 4-Digit Doctor Passcode to unlock:", type="password", key="pin1")
    
    if pin_input_1 == DOCTOR_PIN:
        st.success("Access Granted! Welcome Doctor.")
        st.subheader("📝 Clinical Record Entry & Patient Documentation")
        
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
                preferred_slot = st.selectbox("7. Consultation Review Slot", [
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
                complaints = st.text_area("10. Chief Complaints / Presenting Symptoms", height=100)
                investigation = st.text_area("11. Investigation / Report Review", height=100)
            with col_c2:
                treatment_history = st.text_area("12. Medical Notes / Advice", height=100)
                prescription_details = st.text_area(
                    "13. Digital E-Prescription (Medicine | Dosage | Duration | Timing)", 
                    placeholder="Example:\n1. Tab Paracetamol 650mg | 1-0-1 | 5 days | After Food\n2. Tab Pantoprazole 40mg | 1-0-0 | 7 days | Before Food",
                    height=100
                )

            submit_btn = st.form_submit_button("💾 Save Clinical & Prescription Record")

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
        st.error("Incorrect Passcode. Access Denied.")


# TAB 3: Searchable Database & E-Prescription Summary (Doctor Authenticated)
with tab3:
    st.subheader("🔒 Doctor Access Portal")
    pin_input_2 = st.text_input("Enter 4-Digit Doctor Passcode to view database:", type="password", key="pin2")

    if pin_input_2 == DOCTOR_PIN:
        st.success("Access Granted!")
        st.subheader("📋 Patient Database & E-Prescription Generator")

        df = pd.read_sql_query("SELECT * FROM patients ORDER BY patient_id DESC", conn)

        if not df.empty:
            search_query = st.text_input("🔍 Search Patient Records by Name or Phone Number:")
            
            if search_query:
                df_filtered = df[
                    df['patient_name'].str.contains(search_query, case=False, na=False) |
                    df['phone'].str.contains(search_query, case=False, na=False)
                ]
            else:
                df_filtered = df

            st.dataframe(df_filtered, use_container_width=True)

            st.markdown("---")
            st.subheader("📄 Formal E-Prescription & Summary Pad")
            selected_id = st.selectbox("Select Patient ID to generate formal Rx Pad:", df_filtered['patient_id'].tolist())
            
            patient_row = df_filtered[df_filtered['patient_id'] == selected_id].iloc[0]

            st.markdown(f"""
                <div style="border: 2px solid #0f4c81; padding: 25px; border-radius: 10px; background-color: #ffffff;">
                    <div style="text-align: center; border-bottom: 2px solid #0f4c81; padding-bottom: 10px; margin-bottom: 15px;">
                        <h2 style="color: #0f4c81; margin: 0;">N2 CARE TELECLINIC</h2>
                        <p style="margin: 0; font-style: italic; font-weight: bold; color: #2a9d8f;">"Your Friendly Second Opinion"</p>
                        <small>Dr. Vigneshwar, MBBS, MD | Dr. S. Malathi, MBBS, MD</small><br>
                        <small>WhatsApp: +91 94868 72627 | UPI: 9486872627@upi</small>
                    </div>
                    <div style="display: flex; justify-content: space-between;">
                        <div><b>Patient ID:</b> N2-{patient_row['patient_id']}</div>
                        <div><b>Date:</b> {patient_row['entry_date']}</div>
                    </div>
                    <hr>
                    <p><b>Name:</b> {patient_row['patient_name']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Age/Gender:</b> {patient_row['age']} yrs / {patient_row['gender']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Phone:</b> {patient_row['phone']}</p>
                    <p><b>Focus:</b> {patient_row['consultation_type']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Review Slot:</b> {patient_row['preferred_slot']}</p>
                    <p><b>Vitals:</b> BP: {patient_row['bp']} | Pulse: {patient_row['pulse']} | SpO2: {patient_row['spo2']} | Temp: {patient_row['temp']}</p>
                    <hr>
                    <p><b>Chief Complaints:</b><br>{patient_row['complaints']}</p>
                    <p><b>Investigations / Report Review:</b><br>{patient_row['investigation']}</p>
                    <p><b>Medical Advice & Clinical Notes:</b><br>{patient_row['treatment_history']}</p>
                    <hr>
                    <h4 style="color: #e63946; margin-bottom: 5px;">💊 Rx (Prescription):</h4>
                    <p style="background-color: #f8f9fa; padding: 12px; border-radius: 6px; font-family: monospace; white-space: pre-wrap;">{patient_row['prescription_details']}</p>
                    <hr>
                    <p style="text-align: right;"><b>Next Follow-Up Date:</b> {patient_row['followup_date']}</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Export Complete Database (Excel / CSV)",
                data=csv_data,
                file_name=f"N2_Care_Patients_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("No patient records found yet. Use Tab 2 to enter clinical records.")
    elif pin_input_2:
        st.error("Incorrect Passcode. Access Denied.")
