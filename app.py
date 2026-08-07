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

# 3. Creative Option B Styling - Royal Gold Doctor Profiles
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
        padding: 12px 24px;
        font-weight: 700;
        text-decoration: none;
        border-radius: 10px;
        display: inline-block;
        margin-top: 12px;
        box-shadow: 0 6px 15px rgba(37, 211, 102, 0.35);
    }

    /* 🌟 OPTION B: Creative Royal Gold Doctor Card 🌟 */
    .option-b-card {
        background: linear-gradient(135deg, #ffffff 0%, #fefae0 100%) !important;
        border: 2px solid #dda15e !important;
        border-radius: 20px !important;
        padding: 20px !important;
        box-shadow: 0 10px 25px rgba(188, 108, 37, 0.12) !important;
        text-align: center;
        position: relative;
    }

    .option-b-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 6px;
        background: linear-gradient(90deg, #283618 0%, #dda15e 50%, #bc6c25 100%);
        border-radius: 20px 20px 0 0;
    }

    .photo-frame-gold {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 3px solid #dda15e;
        padding: 3px;
        background: #ffffff;
        box-shadow: 0 6px 15px rgba(188, 108, 37, 0.2);
        margin: 0 auto 10px auto;
        object-fit: cover;
    }

    .doc-name-b {
        color: #0b3c5d !important;
        font-size: 20px !important;
        font-weight: 800 !important;
        margin: 6px 0 2px 0 !important;
    }

    .doc-qual-b {
        color: #283618 !important;
        font-size: 13px !important;
        font-weight: 700 !important;
        margin: 0 0 10px 0 !important;
    }

    .doc-badge-gold {
        background: linear-gradient(135deg, #e0f2fe 0%, #bae6fd 100%);
        color: #0284c7 !important;
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 800;
        display: inline-block;
        border: 1px solid #0284c7;
    }

    .inst-card {
        border-left: 5px solid #283618;
        background: #ffffff !important;
        padding: 14px 18px;
        margin-bottom: 12px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }

    .testimonial-box {
        background: #ffffff;
        border-left: 4px solid #dda15e;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }

    h1, h2, h3, h4 {
        color: #0b3c5d !important;
        font-weight: 800 !important;
    }
    p, span, li {
        color: #1e293b !important;
    }
    label {
        color: #283618 !important;
        font-weight: 600 !important;
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

# 🌟 OPTION B: Creative Doctor Profiles 🌟
doc_col1, doc_col2 = st.columns(2)

with doc_col1:
    st.markdown('<div class="option-b-card">', unsafe_allow_html=True)
    if os.path.exists("doc_vigneshwar.png"):
        st.image("doc_vigneshwar.png", width=100)
    elif os.path.exists("doc_vigneshwar.jpg"):
        st.image("doc_vigneshwar.jpg", width=100)
    else:
        st.markdown('<div style="font-size: 54px; margin-bottom: 5px;">👨‍⚕️</div>', unsafe_allow_html=True)
        
    st.markdown("""
        <p class="doc-name-b">Dr. Vigneshwar</p>
        <p class="doc-qual-b">MBBS, MD General Medicine</p>
        <div class="doc-badge-gold">✓ TNMC Reg No: 159693</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with doc_col2:
    st.markdown('<div class="option-b-card">', unsafe_allow_html=True)
    if os.path.exists("doc_malathi.png"):
        st.image("doc_malathi.png", width=100)
    elif os.path.exists("doc_malathi.jpg"):
        st.image("doc_malathi.jpg", width=100)
    else:
        st.markdown('<div style="font-size: 54px; margin-bottom: 5px;">👩‍⚕️</div>', unsafe_allow_html=True)
        
    st.markdown("""
        <p class="doc-name-b">Dr. S. Malathi</p>
        <p class="doc-qual-b">MBBS, MD General Medicine</p>
        <div class="doc-badge-gold">✓ TNMC Verified Practitioner</div>
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
    "🌐 Regional & National Directory",
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
                    <b style="color: #0b3c5d !important; font-size: 16px;">Send Reports</b>
                    <p style="font-size: 13px; color: #1e293b !important; margin-top: 6px;">Share blood tests, CT/MRI links, or voice notes on WhatsApp between 9 AM - 3 PM.</p>
                </div>
                <div style="flex: 1; min-width: 220px; background: #fffbeb; padding: 18px; border-radius: 12px; border: 1px solid #dda15e;">
                    <div style="font-size: 32px;">2️⃣</div>
                    <b style="color: #0b3c5d !important; font-size: 16px;">Specialist Review</b>
                    <p style="font-size: 13px; color: #1e293b !important; margin-top: 6px;">MD General Medicine specialists analyze your clinical history daily from 4 PM - 6 PM.</p>
                </div>
                <div style="flex: 1; min-width: 220px; background: #fffbeb; padding: 18px; border-radius: 12px; border: 1px solid #dda15e;">
                    <div style="font-size: 32px;">3️⃣</div>
                    <b style="color: #0b3c5d !important; font-size: 16px;">Receive Guidance</b>
                    <p style="font-size: 13px; color: #1e293b !important; margin-top: 6px;">Get clear diagnosis validation, drug safety checks, or diet advice directly on WhatsApp.</p>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Interactive Direct Consultation Request Builder
    st.subheader("📋 Direct Consultation Request Builder")
    col_q1, col_q2 = st.columns(2)
    with col_q1:
        query_type = st.selectbox("Select Consultation Focus:", [
            "Lab & Blood Report Review",
            "CT / MRI Scan Second Opinion",
            "Drug Side-Effects & Dosage Check",
            "Diet & Nutrition Plan",
            "Chronic Disease Progression Tracking"
        ])
    with col_q2:
        report_link = st.text_input("Report Link / Drive URL (Optional):", placeholder="https://drive.google.com/...")

    notes_input = st.text_input("Describe your symptoms or clinical questions:", placeholder="e.g. Unsure about HbA1c results and current medication dosage...")
    
    combined_query = f"Focus: {query_type}"
    if report_link:
        combined_query += f" | Report Link: {report_link}"
    if notes_input:
        combined_query += f" | Notes: {notes_input}"

    st.markdown(f'''
        <a href="{get_whatsapp_url(query_type, combined_query)}" target="_blank" class="btn-wa" style="font-size: 16px;">
            💬 Launch WhatsApp Consultation Request (Fee: {CONSULTATION_FEE})
        </a>
    ''', unsafe_allow_html=True)

    st.markdown("---")

    # Service Modules
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top: 0; font-size: 18px;">🔬 Lab Report Review & Second Opinion</h4>
                <p style="color: #1e293b !important; font-size: 14px;">Unsure about blood tests or scans? Get an independent, expert MD review on diagnosis accuracy and safety.</p>
                <p><b>Consultation Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Lab Report Review & Second Opinion')}" target="_blank" class="btn-wa">
                    💬 Book Second Opinion on WhatsApp
                </a>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top: 0; font-size: 18px;">💊 Medication & Side-Effect Safety Check</h4>
                <p style="color: #1e293b !important; font-size: 14px;">Verify drug dosages, understand potential side effects, check long-term drug safety, or resolve medication doubts.</p>
                <p><b>Consultation Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Drug & Medication Review')}" target="_blank" class="btn-wa">
                    💬 Ask About Medicines
                </a>
            </div>
        """, unsafe_allow_html=True)

    with col_b:
        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top: 0; font-size: 18px;">🥗 Clinical Diet & Lifestyle Guidance</h4>
                <p style="color: #1e293b !important; font-size: 14px;">Evidence-based dietary advice for managing Diabetes, Hypertension, Fatty Liver, Cholesterol, and Metabolic conditions.</p>
                <p><b>Consultation Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Diet & Nutrition Guidance')}" target="_blank" class="btn-wa">
                    💬 Request Diet Guidance
                </a>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top: 0; font-size: 18px;">📈 Chronic Illness Tracker & Progression</h4>
                <p style="color: #1e293b !important; font-size: 14px;">Regular health check-ins to monitor disease trends over time and implement preventive steps for long-term health.</p>
                <p><b>Consultation Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Disease Progression Check')}" target="_blank" class="btn-wa">
                    💬 Book Health Tracker
                </a>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Patient Reviews Section
    st.subheader("💬 What Our Patients Say")
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown("""
            <div class="testimonial-box">
                <b>"Clear & Reassuring Guidance"</b><br>
                <small style="color: #1e293b !important;">"I was confused about my diabetes medication dosage changes. Dr. Vigneshwar explained everything clearly on WhatsApp!"</small><br>
                <span style="color: #0b3c5d !important; font-size: 12px; font-weight: bold;">— Arvind S., Trichy</span>
            </div>
        """, unsafe_allow_html=True)
    with r_col2:
        st.markdown("""
            <div class="testimonial-box">
                <b>"Saved Time & Unnecessary Anxiety"</b><br>
                <small style="color: #1e293b !important;">"Shared my MRI report scan link. Got an expert second opinion within the evening review window. Exceptional service!"</small><br>
                <span style="color: #0b3c5d !important; font-size: 12px; font-weight: bold;">— Divya R., Srirangam</span>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # FAQs
    st.subheader("❓ Frequently Asked Questions (FAQs)")
    with st.expander("1. How do I upload my blood or scan reports?"):
        st.write("You can attach report photos/PDFs directly in our WhatsApp chat, or paste your Google Drive / Cloud link in the consultation request builder above.")
    with st.expander("2. When will I receive the Doctor's second opinion?"):
        st.write("Reports received between 9:00 AM and 3:00 PM are analyzed during our daily MD Doctor Review Window from 4:00 PM to 6:00 PM.")
    with st.expander("3. How do I complete the ₹100 consultation payment?"):
        st.write("Scan our clinic UPI QR code below using GPay, PhonePe, or Paytm and send a screenshot of the payment in WhatsApp.")

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

# TAB 2: Specialty Second Opinion Bundles
with tab2:
    st.subheader("🩺 Specialty Second Opinion Packages")
    st.write("Structured report evaluation packages designed for specific health concerns:")

    b_col1, b_col2 = st.columns(2)

    with b_col1:
        if os.path.exists("card_diabetes.png"):
            st.image("card_diabetes.png", use_container_width=True)
        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top:0;">🩸 Diabetes & Metabolic Wellness Review</h4>
                <p style="font-size: 13px; color: #1e293b !important;">Ideal for Fasting Glucose, HbA1c, Lipid Profile & Kidney Function report validations.</p>
                <p><b>Package Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Diabetes & Metabolic Review')}" target="_blank" class="btn-wa">
                    💬 Book Diabetes Review
                </a>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if os.path.exists("card_cardiac.png"):
            st.image("card_cardiac.png", use_container_width=True)
        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top:0;">❤️ Cardiac & Vascular Safety Check</h4>
                <p style="font-size: 13px; color: #1e293b !important;">Validation of ECG, Echo, Lipid markers, & Hypertension medication safety.</p>
                <p><b>Package Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Cardiac Report Review')}" target="_blank" class="btn-wa">
                    💬 Book Cardiac Review
                </a>
            </div>
        """, unsafe_allow_html=True)

    with b_col2:
        if os.path.exists("card_womens.png"):
            st.image("card_womens.png", use_container_width=True)
        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top:0;">🌸 Women's Wellness & Hormonal Check</h4>
                <p style="font-size: 13px; color: #1e293b !important;">Thyroid profile, Vitamin D, Hb %, & PCOS metabolic evaluation.</p>
                <p><b>Package Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Womens Wellness Review')}" target="_blank" class="btn-wa">
                    💬 Book Women's Check
                </a>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        if os.path.exists("card_senior.png"):
            st.image("card_senior.png", use_container_width=True)
        st.markdown(f"""
            <div class="warm-card">
                <h4 style="color: #0b3c5d !important; margin-top:0;">👴 Senior Citizen Prescription & Safety Audit</h4>
                <p style="font-size: 13px; color: #1e293b !important;">Comprehensive drug safety audit, dosage check, & renal function safety review for elderly care.</p>
                <p><b>Package Fee:</b> <span style="color: #283618; font-weight: bold;">{CONSULTATION_FEE}</span></p>
                <a href="{get_whatsapp_url('Senior Citizen Prescription Audit')}" target="_blank" class="btn-wa">
                    💬 Book Elderly Prescription Audit
                </a>
            </div>
        """, unsafe_allow_html=True)

# TAB 3: Directory
with tab3:
    st.subheader("🌐 Regional & National Medical Referral Directory")
    st.write("Explore major healthcare institutions and specialized centers across Tamil Nadu & India alongside **N2 Care Teleclinic**:")

    dir_col1, dir_col2 = st.columns(2)

    with dir_col1:
        st.markdown("""
            <div class="inst-card">
                <b>🩺 N2 Care Teleclinic</b> — <a href="https://n2-teleclinic-app-7wvhshbbbpegzz7hne4gr3.streamlit.app/" target="_blank">Official Portal</a><br>
                <small style="color: #1e293b !important;">₹100 Friendly Second Opinions | MD General Medicine Review</small>
            </div>
            <div class="inst-card">
                <b>🏥 Apollo Speciality Hospitals, Trichy</b> — <a href="https://www.apollohospitals.com/hospitals/apollo-speciality-hospitals-trichy" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">Advanced Multi-Specialty Tertiary Healthcare in Trichy</small>
            </div>
            <div class="inst-card">
                <b>🏥 Sri Ramakrishna Hospital, Trichy</b> — <a href="https://www.sriramakrishnahospitaltrichy.com/" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">Comprehensive Healthcare Services & Tertiary Care</small>
            </div>
            <div class="inst-card">
                <b>🏥 Ganga Hospital, Coimbatore</b> — <a href="https://www.gangahospital.com/" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">Premier Center for Orthopaedics, Trauma & Plastic Surgery</small>
            </div>
            <div class="inst-card">
                <b>🏥 KMCH (Kovai Medical Center & Hospital)</b> — <a href="https://kmchihsr.edu.in/" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">Multi-Specialty Institute & Health Sciences Research</small>
            </div>
            <div class="inst-card">
                <b>🏥 MIOT International, Chennai</b> — <a href="https://www.miotinternational.com/" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">Multi-Specialty Care & Advanced Surgical Excellence</small>
            </div>
        """, unsafe_allow_html=True)

    with dir_col2:
        st.markdown("""
            <div class="inst-card">
                <b>🏥 Christian Medical College (CMC), Vellore</b> — <a href="https://admissions.cmcvellore.ac.in/" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">Premier Tertiary Medical Research Institution</small>
            </div>
            <div class="inst-card">
                <b>🏛️ AIIMS New Delhi</b> — <a href="https://www.aiims.edu/" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">Apex Autonomous Medical Institute of National Importance</small>
            </div>
            <div class="inst-card">
                <b>🔬 Tata Memorial Centre, Mumbai</b> — <a href="https://tmc.gov.in/" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">National Comprehensive Cancer Care & Research Center</small>
            </div>
            <div class="inst-card">
                <b>🏥 Medanta – The Medicity, Gurugram</b> — <a href="https://www.medanta.org/" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">Multi-Super Specialty Institute for Complex Care</small>
            </div>
            <div class="inst-card">
                <b>🏛️ PGIMER, Chandigarh</b> — <a href="https://pgimer.edu.in/" target="_blank">Official Website</a><br>
                <small style="color: #1e293b !important;">Postgraduate Institute of Medical Education & Research</small>
            </div>
        """, unsafe_allow_html=True)

# TAB 4: Doctor Entry
with tab4:
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

# TAB 5: Searchable Database & Rx Pad
with tab5:
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
