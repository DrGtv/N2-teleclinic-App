import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse
import os

# 1. Page Configuration
st.set_page_config(
    page_title="N2 Care Teleclinic | Official Second Opinion Portal",
    page_icon="🩺",
    layout="wide"
)

# Configuration Variables
CLINIC_PHONE = "919486872627"
UPI_ID = "9486872627@upi"
CONSULTATION_FEE = "₹100"
BOOKING_HOURS = "9:00 AM – 3:00 PM"
REVIEW_HOURS = "4:00 PM – 6:00 PM (Daily)"

# 🔑 Separate Doctor PINs
DOCTOR_PINS = {
    "1596": "Dr. Vigneshwar",
    "2026": "Dr. S. Malathi"
}

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
def get_detailed_whatsapp_url(name, age, gender, city, service_name, notes, report_link):
    msg = f"🏥 *N2 CARE TELECLINIC - CONSULTATION REQUEST*\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"👤 *Patient Name:* {name if name else 'Not Provided'}\n"
    msg += f"🎂 *Age / Gender:* {age} yrs | {gender}\n"
    msg += f"📍 *Location/City:* {city if city else 'Not Provided'}\n"
    msg += f"🩺 *Consultation Focus:* {service_name}\n"
    msg += f"🏷️ *Fee:* {CONSULTATION_FEE}\n"
    if report_link:
        msg += f"🔗 *Report Link:* {report_link}\n"
    if notes:
        msg += f"📝 *Clinical Symptoms / Questions:* {notes}\n"
    msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
    msg += f"📩 *Note:* I am attaching my blood reports / scan photos / payment screenshot here. Please review between {REVIEW_HOURS}."
    
    return f"https://wa.me/{CLINIC_PHONE}?text={urllib.parse.quote(msg)}"

def get_upi_qr_url():
    upi_payload = f"upi://pay?pa={UPI_ID}&pn=N2%20Care%20Teleclinic&am=100&cu=INR"
    return f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={urllib.parse.quote(upi_payload)}"

# 3. Clean CSS Styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(180deg, #fffbeb 0%, #ffffff 350px, #fafaf9 100%) !important;
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }
    
    .emergency-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: #0b3c5d;
        padding: 10px 18px;
        border-radius: 12px;
        margin-bottom: 20px;
        color: white;
    }
    
    .emergency-text {
        color: white !important;
        font-weight: 700 !important;
        font-size: 15px;
    }
    
    .btn-emergency {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white !important;
        padding: 8px 16px;
        font-weight: 700;
        text-decoration: none;
        border-radius: 8px;
        box-shadow: 0 4px 10px rgba(239, 68, 68, 0.3);
    }

    .warm-card {
        background: #ffffff !important;
        border: 1px solid #dda15e;
        padding: 22px;
        border-radius: 16px;
        box-shadow: 0 8px 24px rgba(188, 108, 37, 0.08);
        height: 100%;
    }
    
    .btn-wa {
        background: linear-gradient(135deg, #25D366 0%, #128C7E 100%);
        color: white !important;
        padding: 14px 28px;
        font-weight: 700;
        text-decoration: none;
        border-radius: 10px;
        display: inline-block;
        margin-top: 12px;
        box-shadow: 0 6px 15px rgba(37, 211, 102, 0.35);
        width: 100%;
        text-align: center;
    }

    .doc-card-border {
        background: linear-gradient(145deg, #ffffff 0%, #fffbeb 100%) !important;
        border: 2px solid #dda15e !important;
        border-radius: 18px !important;
        padding: 16px !important;
        box-shadow: 0 8px 20px rgba(188, 108, 37, 0.1) !important;
        height: 100%;
    }

    .doc-name {
        color: #0b3c5d !important;
        font-size: 18px !important;
        font-weight: 800 !important;
        margin: 4px 0 2px 0 !important;
    }

    .doc-qual {
        color: #475569 !important;
        font-size: 13px !important;
        font-weight: 600 !important;
        margin: 0 0 8px 0 !important;
    }

    .doc-badge-pill {
        background: #e0f2fe;
        color: #0284c7 !important;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 800;
        display: inline-block;
        border: 1px solid #bae6fd;
    }

    .inst-card {
        border-left: 5px solid #283618;
        background: #ffffff !important;
        padding: 14px 18px;
        margin-bottom: 12px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }

    label {
        color: #0b3c5d !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# Top Urgent Helpline Bar
st.markdown("""
    <div class="emergency-bar">
        <span class="emergency-text">🚨 Urgent Clinical Helpline: +91 94868 72627</span>
        <a href="tel:919486872627" class="btn-emergency">📞 Call Clinic Now</a>
    </div>
""", unsafe_allow_html=True)

# Main Hero Banner Logo
hero_banner_files = ["hero_banner.png", "hero_banner.jpg", "116795.png"]
for b in hero_banner_files:
    if os.path.exists(b):
        st.image(b, use_container_width=True)
        break

st.markdown("<br>", unsafe_allow_html=True)

# Doctor Avatars Section
doc_col1, doc_col2 = st.columns(2)

with doc_col1:
    st.markdown('<div class="doc-card-border">', unsafe_allow_html=True)
    a_col1, a_col2 = st.columns([1, 2.2])
    with a_col1:
        v_img_files = ["doc_vigneshwar.png", "116810.png", "doc_vigneshwar.jpg"]
        v_found = False
        for img in v_img_files:
            if os.path.exists(img):
                st.image(img, use_container_width=True)
                v_found = True
                break
        if not v_found:
            st.markdown('<div style="font-size: 50px; text-align: center;">👨‍⚕️</div>', unsafe_allow_html=True)
    with a_col2:
        st.markdown("""
            <div>
                <p class="doc-name">Dr. Vigneshwar</p>
                <p class="doc-qual">MBBS, MD General Medicine</p>
                <div class="doc-badge-pill">✓ TNMC Reg No: 159693</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with doc_col2:
    st.markdown('<div class="doc-card-border">', unsafe_allow_html=True)
    m_col1, m_col2 = st.columns([1, 2.2])
    with m_col1:
        m_img_files = ["doc_malathi.png", "116809.png", "doc_malathi.jpg"]
        m_found = False
        for img in m_img_files:
            if os.path.exists(img):
                st.image(img, use_container_width=True)
                m_found = True
                break
        if not m_found:
            st.markdown('<div style="font-size: 50px; text-align: center;">👩‍⚕️</div>', unsafe_allow_html=True)
    with m_col2:
        st.markdown("""
            <div>
                <p class="doc-name">Dr. S. Malathi</p>
                <p class="doc-qual">MBBS, MD General Medicine</p>
                <div class="doc-badge-pill">✓ TNMC Verified Practitioner</div>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Operational Status Banners
p_col1, p_col2, p_col3 = st.columns(3)
p_col1.error(f"🏷️ Consultation Fee: {CONSULTATION_FEE} Only")
p_col2.info(f"📩 Report Submission: {BOOKING_HOURS}")
p_col3.success(f"🩺 MD Doctor Review: {REVIEW_HOURS}")

st.markdown("<br>", unsafe_allow_html=True)

# Navigation Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🤝 Patient Portal & Booking",
    "🩺 Specialty Second Opinion Packages",
    "🌐 Regional Directory",
    "🔒 Doctor Dashboard",
    "🔒 Database & E-Prescription"
])

# TAB 1: Patient Consultation Portal
with tab1:
    st.markdown("""
        <div class="warm-card" style="margin-bottom: 25px; text-align: center;">
            <h3 style="color: #0b3c5d !important; margin-top: 0; font-weight: 800;">✨ How Your Online Second Opinion Works</h3>
            <div style="display: flex; justify-content: space-around; flex-wrap: wrap; text-align: center; margin-top: 20px; gap: 15px;">
                <div style="flex: 1; min-width: 220px; background: #fffbeb; padding: 18px; border-radius: 12px; border: 1px solid #dda15e;">
                    <div style="font-size: 32px;">1️⃣</div>
                    <b style="color: #0b3c5d !important; font-size: 16px;">Fill Patient Form</b>
                    <p style="font-size: 13px; color: #1e293b !important; margin-top: 6px;">Enter name, age, city, and symptoms in the builder below.</p>
                </div>
                <div style="flex: 1; min-width: 220px; background: #fffbeb; padding: 18px; border-radius: 12px; border: 1px solid #dda15e;">
                    <div style="font-size: 32px;">2️⃣</div>
                    <b style="color: #0b3c5d !important; font-size: 16px;">Send via WhatsApp</b>
                    <p style="font-size: 13px; color: #1e293b !important; margin-top: 6px;">Click the WhatsApp button & attach blood reports or payment screenshot.</p>
                </div>
                <div style="flex: 1; min-width: 220px; background: #fffbeb; padding: 18px; border-radius: 12px; border: 1px solid #dda15e;">
                    <div style="font-size: 32px;">3️⃣</div>
                    <b style="color: #0b3c5d !important; font-size: 16px;">Specialist Guidance</b>
                    <p style="font-size: 13px; color: #1e293b !important; margin-top: 6px;">Receive MD Doctor validation & advice daily from 4 PM - 6 PM.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Patient Registration Form
    st.markdown("""
        <div style="background: #ffffff; border: 2px solid #0b3c5d; padding: 25px; border-radius: 16px; box-shadow: 0 8px 24px rgba(11, 60, 93, 0.08);">
            <h3 style="color: #0b3c5d !important; margin-top: 0; font-size: 22px;">📋 Patient Details & Consultation Form</h3>
            <p style="font-size: 13px; color: #57534e !important; margin-bottom: 20px;">Please fill out your details below. These will be formatted and pre-filled into WhatsApp automatically.</p>
    """, unsafe_allow_html=True)

    f_col1, f_col2, f_col3 = st.columns(3)
    with f_col1:
        p_name = st.text_input("1. Full Name *", placeholder="e.g. Ramesh Kumar")
    with f_col2:
        p_age = st.number_input("2. Age *", min_value=1, max_value=110, value=35)
    with f_col3:
        p_gender = st.selectbox("3. Gender *", ["Male", "Female", "Other"])

    f_col4, f_col5 = st.columns(2)
    with f_col4:
        p_city = st.text_input("4. City / Location *", placeholder="e.g. Trichy / Chennai")
    with f_col5:
        p_service = st.selectbox("5. Consultation Focus *", [
            "Lab & Blood Report Review",
            "CT / MRI Scan Second Opinion",
            "Drug Side-Effects & Dosage Check",
            "Diet & Nutrition Plan",
            "Chronic Disease Progression Tracking"
        ])

    p_notes = st.text_area("6. Symptoms or Specific Clinical Questions:", placeholder="e.g. Want to check FBS, PPBS, and HbA1c values. Currently taking Metformin 500mg...")
    p_link = st.text_input("7. Google Drive / Scan Report Link (Optional):", placeholder="https://drive.google.com/...")

    wa_custom_url = get_detailed_whatsapp_url(p_name, p_age, p_gender, p_city, p_service, p_notes, p_link)

    st.markdown(f'''
        <br>
        <a href="{wa_custom_url}" target="_blank" class="btn-wa" style="font-size: 17px;">
            💬 Submit Form & Launch WhatsApp Consultation Request (Fee: {CONSULTATION_FEE})
        </a>
        </div>
    ''', unsafe_allow_html=True)

    st.markdown("---")

    # FAQs
    st.subheader("❓ Frequently Asked Questions (FAQs)")
    with st.expander("1. How do I upload my blood or scan reports?"):
        st.write("After clicking the WhatsApp button above, attach report photos/PDFs directly in our WhatsApp chat.")
    with st.expander("2. When will I receive the Doctor's second opinion?"):
        st.write("Reports received between 9:00 AM and 3:00 PM are analyzed during our daily MD Doctor Review Window from 4:00 PM to 6:00 PM.")

    st.markdown("---")
    
    # UPI Payment
    st.subheader("💳 Instant ₹100 Payment Portal")
    pay_col1, pay_col2 = st.columns([1, 2])
    
    with pay_col1:
        st.image(get_upi_qr_url(), caption="Scan using GPay / PhonePe / Paytm", width=200)
        
    with pay_col2:
        st.markdown(f"""
            <div class="warm-card">
                <p style="margin-top: 0;"><b>Official Clinic UPI ID:</b> <code style="font-size: 16px; color: #0b3c5d; background: #fffbeb; padding: 4px 8px; border-radius: 6px;">{UPI_ID}</code></p>
                <p><b>Fee:</b> ₹100 Only</p>
                <p><b>Official Contact / WhatsApp:</b> +91 94868 72627</p>
                <p style="font-size: 13px; color: #57534e !important; margin-bottom: 0;">
                    📌 <i>Once payment is completed, please share a screenshot of the confirmation in WhatsApp along with your health reports.</i>
                </p>
            </div>
        """, unsafe_allow_html=True)

# TAB 2: Packages
with tab2:
    st.subheader("🩺 Specialty Second Opinion Packages")
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top:0;">🩸 Diabetes & Metabolic Wellness Review</h4>
                <p style="font-size: 13px; color: #1e293b !important;">Ideal for Fasting Glucose, HbA1c, Lipid Profile & Kidney Function report validations.</p>
                <p><b>Package Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
            </div>
        """, unsafe_allow_html=True)
    with b_col2:
        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top:0;">🌸 Women's Wellness & Hormonal Check</h4>
                <p style="font-size: 13px; color: #1e293b !important;">Thyroid profile, Vitamin D, Hb %, & PCOS metabolic evaluation.</p>
                <p><b>Package Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
            </div>
        """, unsafe_allow_html=True)

# TAB 3: Directory
with tab3:
    st.subheader("🌐 Regional Directory")

# TAB 4: Doctor Internal Portal
with tab4:
    st.subheader("🔒 Doctor Internal Portal")
    pin_input_1 = st.text_input("Enter 4-Digit Doctor Passcode:", type="password", key="pin1")
    
    if pin_input_1 in DOCTOR_PINS:
        st.success(f"Welcome, {DOCTOR_PINS[pin_input_1]}! Authenticated Successfully.")
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

# TAB 5: Searchable Database & Rx Pad
with tab5:
    st.subheader("🔒 Doctor Internal Portal")
    pin_input_2 = st.text_input("Enter 4-Digit Doctor Passcode:", type="password", key="pin2")

    if pin_input_2 in DOCTOR_PINS:
        st.success(f"Welcome, {DOCTOR_PINS[pin_input_2]}! Authenticated Successfully.")
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
                        <h2 style="color: #0b3c5d !important; margin: 0; letter-spacing: 1px;">N2 CARE TELECLINIC</h2>
                        <p style="margin: 3px 0; font-style: italic; font-weight: 700; color: #283618 !important;">"Your Friendly Second Opinion"</p>
                        <small style="color: #1e293b !important;"><b>Dr. Vigneshwar</b>, MBBS, MD (TNMC Reg No 159693) | <b>Dr. S. Malathi</b>, MBBS, MD</small><br>
                        <small style="color: #57534e !important;">WhatsApp: +91 94868 72627 | UPI: 9486872627@upi</small>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 14px;">
                        <div><b>Patient ID:</b> N2-{patient_row['patient_id']}</div>
                        <div><b>Date:</b> {patient_row['entry_date']}</div>
                    </div>
                    <hr style="border: 0.5px solid #dda15e;">
                    <p style="font-size: 14px;"><b>Patient Name:</b> {patient_row['patient_name']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Age/Gender:</b> {patient_row['age']} yrs / {patient_row['gender']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Phone:</b> {patient_row['phone']}</p>
                    <p style="font-size: 14px;"><b>Consultation Focus:</b> {patient_row['consultation_type']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Review Slot:</b> {patient_row['preferred_slot']}</p>
                    <p style="font-size: 14px;"><b>Vitals:</b> BP: {patient_row['bp']} | Pulse: {patient_row['pulse']} | SpO2: {patient_row['spo2']} | Temp: {patient_row['temp']}</p>
                    <hr style="border: 0.5px solid #dda15e;">
                    <p><b>Chief Complaints:</b><br>{patient_row['complaints']}</p>
                    <p><b>Investigations / Scans Review:</b><br>{patient_row['investigation']}</p>
                    <p><b>Clinical Advice & Notes:</b><br>{patient_row['treatment_history']}</p>
                    <hr style="border: 0.5px solid #dda15e;">
                    <h4 style="color: #ef4444 !important; margin-bottom: 5px;">💊 Rx (Prescription):</h4>
                    <p style="background-color: #fffbeb; padding: 15px; border-radius: 8px; font-family: monospace; white-space: pre-wrap; border: 1px solid #dda15e;">{patient_row['prescription_details']}</p>
                    <hr style="border: 0.5px solid #dda15e;">
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
