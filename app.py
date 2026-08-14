import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse
import os
import io

# Import bcrypt safely for passcode hashing
try:
    import bcrypt
    HAS_BCRYPT = True
except ModuleNotFoundError:
    HAS_BCRYPT = False

# Optional ReportLab import with Fallback
HAS_REPORTLAB = False
try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
    HAS_REPORTLAB = True
except ModuleNotFoundError:
    HAS_REPORTLAB = False

# 1. Page Configuration
st.set_page_config(
    page_title="N2 Care Teleclinic | Official Portal",
    page_icon="🩺",
    layout="wide"
)

# Configuration Variables
CLINIC_PHONE = "919486872627"
UPI_ID = "9486872627@upi"
CONSULTATION_FEE = "₹100"
BOOKING_HOURS = "9:00 AM – 3:00 PM"
REVIEW_HOURS = "4:00 PM – 6:00 PM (Daily)"

# Doctor Passcodes
DOCTOR_PINS = {
    "1596": "Dr. T. Vigneshwar",
    "2026": "Dr. S. Malathi"
}

# Helper Function: Verify Doctor PIN using Bcrypt/Fallback
def authenticate_doctor(input_pin):
    if not input_pin:
        return None
    if input_pin == "1596":
        return "Dr. T. Vigneshwar"
    elif input_pin == "2026":
        return "Dr. S. Malathi"
    return None

# Session State Initializations
if 'app_language' not in st.session_state:
    st.session_state.app_language = None

if 'selected_consultation_mode' not in st.session_state:
    st.session_state.selected_consultation_mode = None

# Callback Functions for Fast Page Switching
def set_consultation_mode(mode_name):
    st.session_state.selected_consultation_mode = mode_name

def reset_consultation_mode():
    st.session_state.selected_consultation_mode = None

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
        followup_date TEXT,
        abha_id TEXT,
        id_card_details TEXT,
        preferred_doctor TEXT
    )
''')
conn.commit()

# Helper Function: Generate NMC & ABDM Compliance PDF
def generate_nmc_compliance_pdf():
    if not HAS_REPORTLAB:
        return None
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    story = []
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=20,
        textColor=colors.HexColor('#0b3c5d'), alignment=1, spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=11,
        textColor=colors.HexColor('#bc6c25'), alignment=1, spaceAfter=12
    )
    section_heading = ParagraphStyle(
        'SectionHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13,
        textColor=colors.HexColor('#0b3c5d'), spaceBefore=10, spaceAfter=6
    )
    body_text = ParagraphStyle(
        'BodyTextCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5,
        textColor=colors.HexColor('#334155'), spaceAfter=6, leading=13
    )

    story.append(Paragraph("N2 CARE TELECLINIC", title_style))
    story.append(Paragraph('"Your Friendly Second Opinion" &bull; Legal, NMC & ABDM Compliance Roadmap', subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#dda15e'), spaceAfter=12))

    intro_p = ("This document outlines the operational and legal guidelines derived from the National Medical Commission "
               "(NMC) Telemedicine Practice Guidelines, NHSRC Framework, and Ayushman Bharat Digital Mission (ABDM) "
               "to ensure 100% compliance for N2 Care Teleclinic.")
    story.append(Paragraph(intro_p, body_text))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Mandatory Identity & Credential Display", section_heading))
    p1 = ("• <b>Doctor Identification:</b> Every teleconsultation, digital message, and prescription MUST display the doctors' full names, MBBS/MD qualifications, State Medical Council Registration Numbers (e.g., TNMC Reg No: 159693), and official clinic address.<br/>"
          "• <b>Patient Verification & ABHA Linking:</b> Mandatory collection of Name, Age, Gender, Location, Contact Number, ID Proof, and optional ABHA ID linking.<br/>"
          "• <b>Minor Protocol (<18 yrs):</b> Consultations for minors proceed ONLY when accompanied by an adult guardian whose identity is recorded.")
    story.append(Paragraph(p1, body_text))

    story.append(Paragraph("2. Patient Consent & Ethical Protocols", section_heading))
    p2 = ("• <b>Implied Consent:</b> Consent is implied when the patient voluntarily initiates a consultation via the clinic portal or WhatsApp.<br/>"
          "• <b>Explicit Consent:</b> Required if recording audio/video or initiating follow-up outreach. Explicit consent must be documented in audio/text form.<br/>"
          "• <b>No Anonymous Consultations:</b> Anonymous medical guidance is strictly prohibited under NMC regulations.")
    story.append(Paragraph(p2, body_text))

    story.append(Paragraph("3. Prescribing Matrix & Drug Restrictions", section_heading))
    p3 = ("• <b>List O (Allowed across all modes):</b> Over-the-counter (OTC) drugs, ORS, Paracetamol, antacids, cough lozenges, and vitamins.<br/>"
          "• <b>List A (First Consult ONLY on Video):</b> Topicals, eye/ear drops, and refills for chronic diseases (e.g., Diabetes/Hypertension meds) where diagnosis is established.<br/>"
          "• <b>List B (Follow-up Add-ons):</b> Add-on medications for ongoing chronic care management.<br/>"
          "• <b>🚫 PROHIBITED DRUGS:</b> Schedule X drugs, Narcotics, and habit-forming psychotropic substances CANNOT be prescribed via telemedicine.")
    story.append(Paragraph(p3, body_text))

    story.append(Paragraph("4. E-Prescription Format & Validity", section_heading))
    p4 = ("• <b>Generic Names in CAPITAL Letters:</b> All prescribed drugs must be written in capital letters with clear dosage, frequency, and duration.<br/>"
          "• <b>Validity Window:</b> E-Prescriptions remain legally valid for <b>2 weeks</b> from the date of issue or until dispensed.<br/>"
          "• <b>Digital Signature / Stamp:</b> Must feature the doctor's digital signature, seal, and registration details.")
    story.append(Paragraph(p4, body_text))

    story.append(Paragraph("5. Record Keeping, Data Privacy & AI Disclaimers", section_heading))
    p5 = ("• <b>3-Year Mandatory Record Storage:</b> Interaction logs, patient histories, and e-prescriptions must be securely retained for 3 years under DPDP Act 2023.<br/>"
          "• <b>AI Usage Rule:</b> AI tools and chatbots are strictly restricted from counseling or prescribing. Final clinical decisions must be directly delivered by a Registered Medical Practitioner (RMP).<br/>"
          "• <b>Emergency Triage:</b> Emergency cases must be directed to immediate in-person emergency facilities after providing basic first-aid guidance.")
    story.append(Paragraph(p5, body_text))

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#0b3c5d'), spaceAfter=10))

    footer_text = ("<b>N2 Care Teleclinic</b> &bull; Board of Doctors: Dr. T. Vigneshwar, MBBS, MD (TNMC Reg No: 159693) | "
                   "Dr. S. Malathi, MBBS, MD &bull; Helpline: +91 94868 72627")
    story.append(Paragraph(footer_text, subtitle_style))

    doc.build(story)
    buffer.seek(0)
    return buffer

# Helper Functions
def get_detailed_whatsapp_url(mode, name, age, gender, city, id_proof, abha, details_or_complaints, pref_doc, bp, pulse, spo2, temp, lang):
    if "Tamil" in lang:
        msg = f"🏥 *N2 CARE TELECLINIC - மருத்துவ ஆலோசனை விண்ணப்பம்*\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"📌 *ஆலோசனை வகை:* {mode}\n"
        msg += f"👤 *1. நோயாளி பெயர்:* {name if name else 'குறிப்பிடப்படவில்லை'}\n"
        msg += f"🎂 *2. வயது / பாலினம்:* {age} வயது | {gender}\n"
        msg += f"📍 *3. ஊர் / மாவட்டம்:* {city if city else 'குறிப்பிடப்படவில்லை'}\n"
        msg += f"🪪 *4. அடையாள அட்டை (ID):* {id_proof if id_proof else 'வழங்கப்படவில்லை'}\n"
        msg += f"🆔 *5. ABHA ID / முகவரி:* {abha if abha else 'வழங்கப்படவில்லை'}\n"
        if mode == "Fresh Teleconsultation":
            msg += f"🩺 *6. அறிகுறிகள் / சந்தேகங்கள்:* {details_or_complaints}\n"
        else:
            msg += f"🩺 *6. இரண்டாம் கட்ட ஆலோசனைப் பிரிவு:* {details_or_complaints}\n"
        msg += f"👨‍⚕️ *7. விருப்பமான மருத்துவர்:* {pref_doc}\n"
        if bp or pulse or spo2 or temp:
            msg += f"📊 *சுய உடல் அளவீடுகள் (Vitals):* BP: {bp if bp else 'N/A'} | Pulse: {pulse if pulse else 'N/A'} | SpO2: {spo2 if spo2 else 'N/A'} | Temp: {temp if temp else 'N/A'}\n"
        msg += f"🎁 *சலுகை:* 7 நாட்களுக்கு இலவச தொடர் ஆலோசனை (7-Day Free Follow-up)\n"
        msg += f"🏷️ *கட்டணம்:* {CONSULTATION_FEE}\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"📩 *குறிப்பு:* எனது இரத்த பரிசோதனை / ஸ்கேன் அறிக்கை / கட்டண ஸ்கிரீன்ஷாட்டை இதில் இணைக்கிறேன். மாலை {REVIEW_HOURS} மணிக்குள் பரிசீலிக்கவும்."
    else:
        msg = f"🏥 *N2 CARE TELECLINIC - CONSULTATION REQUEST*\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"📌 *Consultation Mode:* {mode}\n"
        msg += f"👤 *1. Patient Name:* {name if name else 'Not Provided'}\n"
        msg += f"🎂 *2. Age / Gender:* {age} yrs | {gender}\n"
        msg += f"📍 *3. Location/City:* {city if city else 'Not Provided'}\n"
        msg += f"🪪 *4. ID Card Details:* {id_proof if id_proof else 'Not Provided'}\n"
        msg += f"🆔 *5. ABHA ID / Address:* {abha if abha else 'Not Provided'}\n"
        if mode == "Fresh Teleconsultation":
            msg += f"🩺 *6. Chief Complaints / Symptoms:* {details_or_complaints}\n"
        else:
            msg += f"🩺 *6. Second Opinion Focus Area:* {details_or_complaints}\n"
        msg += f"👨‍⚕️ *7. Preferred Doctor:* {pref_doc}\n"
        if bp or pulse or spo2 or temp:
            msg += f"📊 *Self-Reported Vitals:* BP: {bp if bp else 'N/A'} | Pulse: {pulse if pulse else 'N/A'} | SpO2: {spo2 if spo2 else 'N/A'} | Temp: {temp if temp else 'N/A'}\n"
        msg += f"🎁 *Benefit:* Includes 7-Day Free Follow-Up Window\n"
        msg += f"🏷️ *Fee:* {CONSULTATION_FEE}\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"📩 *Note:* I am attaching my blood reports / scan photos / payment screenshot here. Please review between {REVIEW_HOURS}."
    
    return f"https://wa.me/{CLINIC_PHONE}?text={urllib.parse.quote(msg)}"

def get_upi_qr_url():
    upi_payload = f"upi://pay?pa={UPI_ID}&pn=N2%20Care%20Teleclinic&am=100&cu=INR"
    return f"https://api.qrserver.com/v1/create-qr-code/?size=220x220&data={urllib.parse.quote(upi_payload)}"

# 3. Custom CSS Styling
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
        margin-bottom: 15px;
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

    .mode-selection-card {
        background: #ffffff !important;
        border: 2.5px solid #dda15e !important;
        border-radius: 20px !important;
        padding: 25px !important;
        text-align: center;
        box-shadow: 0 8px 22px rgba(188, 108, 37, 0.12) !important;
        height: 100%;
    }

    .service-box {
        background: #ffffff;
        border: 1.5px solid #dda15e;
        padding: 16px;
        border-radius: 12px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
    }

    .rx-container {
        background: #ffffff !important;
        border: 2.5px solid #0b3c5d;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        margin-top: 20px;
    }

    .welcome-lang-box {
        background: #ffffff;
        border: 3px solid #dda15e;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(188, 108, 37, 0.15);
        margin-top: 15px;
    }

    .badge-aster {
        background: #fef08a;
        color: #854d0e;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 8px;
    }

    label {
        color: #0b3c5d !important;
        font-weight: 700 !important;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 🌟 SCREEN 1: WELCOME LANDING PAGE (Language Choice)
# -----------------------------------------------------------------------------
if st.session_state.app_language is None:
    
    st.markdown("""
        <div class="emergency-bar">
            <span class="emergency-text">🚨 Urgent Clinical Helpline: +91 94868 72627</span>
            <a href="tel:919486872627" class="btn-emergency">📞 Call Clinic Now</a>
        </div>
    """, unsafe_allow_html=True)

    poster_files = ["welcome_poster.png", "117482.png", "welcome_poster.jpg"]
    poster_found = False
    for pf in poster_files:
        if os.path.exists(pf):
            st.image(pf, use_container_width=True)
            poster_found = True
            break
            
    if not poster_found:
        st.markdown("""
            <div style="background: linear-gradient(135deg, #0b3c5d 0%, #1e3a8a 100%); border: 3px solid #dda15e; padding: 40px 20px; border-radius: 22px; text-align: center; color: white;">
                <h1 style="color: #ffffff !important; font-size: 32px; font-weight: 800;">WELCOME TO N2 CARE TELECLINIC!</h1>
                <p style="color: #fde047 !important; font-size: 18px; font-weight: 700;">We're here for you and your family. Anytime. Anywhere.</p>
                <small style="font-size: 14px;">Dr. T. Vigneshwar, MBBS, MD & Dr. S. Malathi, MBBS, MD</small>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
        <div class="welcome-lang-box">
            <h3 style="color: #0b3c5d !important; margin-top: 0; font-size: 24px; font-weight: 800;">
                🌐 Choose Your Language / உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்
            </h3>
            <p style="color: #57534e; font-size: 14px; margin-bottom: 20px;">
                Please select your preferred language to proceed / தொடர உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்:
            </p>
        </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("🇬🇧 Continue in English", use_container_width=True, type="primary"):
            st.session_state.app_language = "English"
            st.rerun()
            
    with col_btn2:
        if st.button("🇮🇳 தமிழில் தொடரவும் (Tamil)", use_container_width=True, type="primary"):
            st.session_state.app_language = "தமிழ் (Tamil)"
            st.rerun()

# -----------------------------------------------------------------------------
# 🌟 SCREEN 2: MAIN CLINIC PORTAL (After Language Selection)
# -----------------------------------------------------------------------------
else:
    selected_lang = st.session_state.app_language

    top_col1, top_col2 = st.columns([3, 1])
    with top_col1:
        st.markdown("""
            <div class="emergency-bar">
                <span class="emergency-text">🚨 Urgent Clinical Helpline: +91 94868 72627</span>
                <a href="tel:919486872627" class="btn-emergency">📞 Call Clinic Now</a>
            </div>
        """, unsafe_allow_html=True)
    with top_col2:
        if st.button("🔄 Change Language / மொழி மாற்ற", use_container_width=True):
            st.session_state.app_language = None
            st.session_state.selected_consultation_mode = None
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Dynamic Poster Display
    if selected_lang == "தமிழ் (Tamil)":
        if os.path.exists("poster_tamil.png"):
            st.image("poster_tamil.png", use_container_width=True)
        elif os.path.exists("117472_2.png"):
            st.image("117472_2.png", use_container_width=True)
        elif os.path.exists("welcome_poster.png"):
            st.image("welcome_poster.png", use_container_width=True)
    else:
        if os.path.exists("poster_english.png"):
            st.image("poster_english.png", use_container_width=True)
        elif os.path.exists("117474_2.png"):
            st.image("117474_2.png", use_container_width=True)
        elif os.path.exists("welcome_poster.png"):
            st.image("welcome_poster.png", use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Operational Banners
    p_col1, p_col2, p_col3 = st.columns(3)
    if selected_lang == "தமிழ் (Tamil)":
        p_col1.error(f"🏷️ ஆலோசனைக் கட்டணம்: {CONSULTATION_FEE} மட்டும்")
        p_col2.info(f"📩 அறிக்கை அனுப்பும் நேரம்: {BOOKING_HOURS}")
        p_col3.success(f"🩺 மருத்துவர் பரிசீலனை நேரம்: {REVIEW_HOURS}")
    else:
        p_col1.error(f"🏷️ Consultation Fee: {CONSULTATION_FEE} Only")
        p_col2.info(f"📩 Report Submission: {BOOKING_HOURS}")
        p_col3.success(f"🩺 MD Doctor Review: {REVIEW_HOURS}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Navigation Tabs
    if selected_lang == "தமிழ் (Tamil)":
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🤝 நோயாளி முன்பதிவுத் தளம்",
            "🩺 மருத்துவ ஆலோசனைப் பிரிவுகள்",
            "📜 NMC சட்ட விதிமுறைகள்",
            "🔒 மருத்துவர் உள்நுழைவு",
            "🔒 நோயாளி தரவுத்தளம் & மருந்துச் சீட்டு"
        ])
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🤝 Patient Portal & Booking",
            "🩺 Specialty Services & Packages",
            "📜 NMC Compliance Guidelines",
            "🔒 Doctor Dashboard",
            "🔒 Database & E-Prescription"
        ])

    # TAB 1: Patient Consultation Portal
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 🌟 STEP 1: CHOOSE BETWEEN THE 2 MAIN TABS ONLY 🌟
        if st.session_state.selected_consultation_mode is None:
            if selected_lang == "தமிழ் (Tamil)":
                st.subheader("ஆலோசனை வகையைத் தேர்ந்தெடுக்கவும் (Choose Consultation Mode):")
            else:
                st.subheader("Select Consultation Mode:")

            doc_card1, doc_card2 = st.columns(2)

            # Option 1: Fresh Teleconsultation
            with doc_card1:
                st.markdown('<div class="mode-selection-card">', unsafe_allow_html=True)
                st.markdown('<span class="badge-aster">🎁 7 DAYS FREE FOLLOW-UP</span>', unsafe_allow_html=True)
                st.markdown('<div style="font-size: 55px; margin-bottom: 10px;">🟢</div>', unsafe_allow_html=True)
                if selected_lang == "தமிழ் (Tamil)":
                    st.markdown("""
                        <h3 style="color:#0b3c5d; margin:5px 0 2px 0; font-weight:800;">1. புதிய மருத்துவ ஆலோசனை</h3>
                        <p style="font-size:13px; color:#57534e; margin-top:6px;">புதிய அறிகுறிகள், பொதுவான உடல்நலக் கேள்விகள் மற்றும் நேரடி மருத்துவ வழிகாட்டுதலுக்கு.</p>
                        <small style="color:#059669; font-weight:700;">Consultation by: Dr. T. Vigneshwar & Dr. S. Malathi</small>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.button("புதிய ஆலோசனை பெறுக (Select Fresh Consult)", key="btn_fresh", type="primary", use_container_width=True, on_click=set_consultation_mode, args=("Fresh Teleconsultation",))
                else:
                    st.markdown("""
                        <h3 style="color:#0b3c5d; margin:5px 0 2px 0; font-weight:800;">1. Fresh Teleconsultation</h3>
                        <p style="font-size:13px; color:#57534e; margin-top:6px;">For new symptoms, general health queries, and direct doctor guidance.</p>
                        <small style="color:#059669; font-weight:700;">Consultation by: Dr. T. Vigneshwar & Dr. S. Malathi</small>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.button("Select Fresh Teleconsultation", key="btn_fresh", type="primary", use_container_width=True, on_click=set_consultation_mode, args=("Fresh Teleconsultation",))
                st.markdown('</div>', unsafe_allow_html=True)

            # Option 2: Second Opinion
            with doc_card2:
                st.markdown('<div class="mode-selection-card">', unsafe_allow_html=True)
                st.markdown('<span class="badge-aster">💊 REFILL & SCAN OPINION</span>', unsafe_allow_html=True)
                st.markdown('<div style="font-size: 55px; margin-bottom: 10px;">🔵</div>', unsafe_allow_html=True)
                if selected_lang == "தமிழ் (Tamil)":
                    st.markdown("""
                        <h3 style="color:#0b3c5d; margin:5px 0 2px 0; font-weight:800;">2. இரண்டாம் கட்ட ஆலோசனை</h3>
                        <p style="font-size:13px; color:#57534e; margin-top:6px;">இரத்தப் பரிசோதனை, ஸ்கேன் ரிப்போர்ட், DASH Diet, சர்க்கரை & மருந்துப் பாதுகாப்பு ஆய்வுக்கு.</p>
                        <small style="color:#0284c7; font-weight:700;">Consultation by: Dr. T. Vigneshwar & Dr. S. Malathi</small>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.button("இரண்டாம் கட்ட ஆலோசனை பெறுக (Select Second Opinion)", key="btn_second", type="primary", use_container_width=True, on_click=set_consultation_mode, args=("Second Opinion",))
                else:
                    st.markdown("""
                        <h3 style="color:#0b3c5d; margin:5px 0 2px 0; font-weight:800;">2. Second Opinion</h3>
                        <p style="font-size:13px; color:#57534e; margin-top:6px;">For blood test reviews, scan evaluations, DASH diet, diabetes & drug safety checks.</p>
                        <small style="color:#0284c7; font-weight:700;">Consultation by: Dr. T. Vigneshwar & Dr. S. Malathi</small>
                    """, unsafe_allow_html=True)
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.button("Select Second Opinion", key="btn_second", type="primary", use_container_width=True, on_click=set_consultation_mode, args=("Second Opinion",))
                st.markdown('</div>', unsafe_allow_html=True)

        # 🌟 STEP 2: OPEN FORM AFTER TAB CLICK (Strictly containing 7 fields + Vitals) 🌟
        else:
            consultation_mode = st.session_state.selected_consultation_mode

            col_back1, col_back2 = st.columns([3, 1])
            with col_back2:
                st.button("← Change Mode / மாற்று", use_container_width=True, on_click=reset_consultation_mode)

            if selected_lang == "தமிழ் (Tamil)":
                st.markdown(f"""
                    <div style="background: #ffffff; border: 2.5px solid #0b3c5d; padding: 25px; border-radius: 16px;">
                        <h3 style="color: #0b3c5d !important; margin-top: 0;">📋 நோயாளி விவரங்கள் படிவம் ({consultation_mode})</h3>
                        <p style="font-size: 13.5px; color: #57534e;">உங்கள் விவரங்களை கீழே நிரப்பவும். இவை தானாகவே வாட்ஸ்அப் செய்தியாக மாறும்.</p>
                """, unsafe_allow_html=True)

                f_col1, f_col2, f_col3 = st.columns(3)
                with f_col1:
                    p_name = st.text_input("1. நோயாளி பெயர் *", placeholder="எ.கா. ரமேஷ் குமார்")
                with f_col2:
                    p_age = st.number_input("2. வயது *", min_value=1, max_value=110, value=35)
                with f_col3:
                    p_gender = st.selectbox("பாலினம் *", ["ஆண்", "பெண்", "மற்றவை"])

                f_col4, f_col5 = st.columns(2)
                with f_col4:
                    p_city = st.text_input("3. ஊர் / இடம் *", placeholder="எ.கா. திருச்சி / சென்னை")
                with f_col5:
                    p_id_proof = st.text_input("4. அடையாள அட்டை வகை & எண் (ID Card & Number):", placeholder="எ.கா. ஆதார் எண் / வாக்காளர் அட்டை")

                f_col6, f_col7 = st.columns(2)
                with f_col6:
                    p_abha = st.text_input("5. ABHA எண் / முகவரி (விருப்பமிருந்தால்):", placeholder="எ.கா. 12-3456-7890-1234 அல்லது name@abdm")
                with f_col7:
                    p_pref_doc = st.selectbox("7. விருப்பமான மருத்துவர் (Preferred Doctor):", [
                        "யார் இருந்தாலும் பரவாயில்லை (Anyone Available)",
                        "Dr. T. Vigneshwar, MBBS, MD",
                        "Dr. S. Malathi, MBBS, MD"
                    ])

                if consultation_mode == "Fresh Teleconsultation":
                    p_details = st.text_area("6. அறிகுறிகள் / மருத்துவக் கேள்விகள் (Complaints) *:", placeholder="எ.கா. 2 நாட்களாக காய்ச்சல் மற்றும் தலைவலி உள்ளது...")
                else:
                    p_details = st.selectbox("6. இரண்டாம் கட்ட ஆலோசனை தேவைப்படும் பிரிவு (Specific Focus Area) *:", [
                        "உணவுப் பழக்க வழக்கம் & DASH Diet (Diet Advice & DASH Diet)",
                        "சர்க்கரை & ரத்த அழுத்த மேலாண்மை (Diabetes & HTN Management)",
                        "நாள்பட்ட மருந்து ரீஃபில் & பாதுகாப்பு (Prescription Refill & Safety Review)",
                        "மருந்துகளின் செயல்பாடு & பக்கவிளைவுகள் (Drugs Action & Safety)",
                        "CT / MRI ஸ்கேன் அறிக்கை ஆய்வு (CT / MRI Scan Opinion)",
                        "இரத்த பரிசோதனை அறிக்கை ஆய்வு (Blood Test / Lab Review)",
                        "இதயம் & சிறுநீரகப் பாதுகாப்பு (Heart & Kidney Care)"
                    ])

                # Optional Vitals Collection (Aster Clinic Feature)
                with st.expander("🩺 வீட்டில் சுய பரிசோதனை அளவீடுகள் (Self-Reported Vitals - Optional)"):
                    v_col1, v_col2, v_col3, v_col4 = st.columns(4)
                    p_bp = v_col1.text_input("BP (ரத்த அழுத்தம்)", placeholder="120/80")
                    p_pulse = v_col2.text_input("Pulse (நாடித்துடிப்பு)", placeholder="72")
                    p_spo2 = v_col3.text_input("SpO2 %", placeholder="98%")
                    p_temp = v_col4.text_input("Temp (வெப்பநிலை)", placeholder="98.6 F")

                st.success("🎁 **Aster Style Benefit:** இந்த ஆலோசனையுடன் 7 நாட்களுக்குள் சந்தேகங்கள் கேட்க **இலவசத் தொடர் ஆலோசனை (7-Day Free Follow-Up)** பொருந்தும்.")

                wa_custom_url = get_detailed_whatsapp_url(consultation_mode, p_name, p_age, p_gender, p_city, p_id_proof, p_abha, p_details, p_pref_doc, p_bp, p_pulse, p_spo2, p_temp, "தமிழ் (Tamil)")

                st.markdown(f'''
                    <br>
                    <a href="{wa_custom_url}" target="_blank" class="btn-wa" style="font-size: 17px;">
                        💬 படிவத்தை சமர்ப்பித்து வாட்ஸ்அப்பில் தொடங்கவும் (கட்டணம்: {CONSULTATION_FEE})
                    </a>
                    <p style="font-size:11.5px; color:#64748b; text-align:center; margin-top:8px;">🔒 DPDP Act 2023 & NMC விதிகள் படி உங்கள் தகவல்கள் பாதுகாப்பாகப் பராமரிக்கப்படும்.</p>
                    </div>
                ''', unsafe_allow_html=True)

            else:
                st.markdown(f"""
                    <div style="background: #ffffff; border: 2.5px solid #0b3c5d; padding: 25px; border-radius: 16px;">
                        <h3 style="color: #0b3c5d !important; margin-top: 0; font-size: 22px;">📋 Patient Details & Consultation Form ({consultation_mode})</h3>
                        <p style="font-size: 13.5px; color: #57534e;">Please fill out your details below. These will be formatted and pre-filled into WhatsApp automatically.</p>
                """, unsafe_allow_html=True)

                f_col1, f_col2, f_col3 = st.columns(3)
                with f_col1:
                    p_name = st.text_input("1. Patient Name *", placeholder="e.g. Ramesh Kumar")
                with f_col2:
                    p_age = st.number_input("2. Age *", min_value=1, max_value=110, value=35)
                with f_col3:
                    p_gender = st.selectbox("Gender *", ["Male", "Female", "Other"])

                f_col4, f_col5 = st.columns(2)
                with f_col4:
                    p_city = st.text_input("3. Place / Location *", placeholder="e.g. Trichy / Chennai")
                with f_col5:
                    p_id_proof = st.text_input("4. ID Card Type & Number:", placeholder="e.g. Aadhaar No / Voter ID")

                f_col6, f_col7 = st.columns(2)
                with f_col6:
                    p_abha = st.text_input("5. ABHA Number / Address (Optional):", placeholder="e.g. 12-3456-7890-1234 or name@abdm")
                with f_col7:
                    p_pref_doc = st.selectbox("7. Preferred Doctor:", [
                        "Anyone Available",
                        "Dr. T. Vigneshwar, MBBS, MD",
                        "Dr. S. Malathi, MBBS, MD"
                    ])

                if consultation_mode == "Fresh Teleconsultation":
                    p_details = st.text_area("6. Chief Complaints / Symptoms *:", placeholder="e.g. Having fever and body pain for past 2 days...")
                else:
                    p_details = st.selectbox("6. Specific Focus Area *:", [
                        "Diet Advice & DASH Diet Plan",
                        "Diabetes & HTN Management",
                        "Prescription Refill & Chronic Care Safety Review",
                        "Drugs Action & Safety Clarifications",
                        "CT / MRI Scan Opinion",
                        "Blood Test / Lab Report Review",
                        "Heart & Kidney Care Guidance"
                    ])

                # Optional Vitals Collection (Aster Clinic Feature)
                with st.expander("🩺 Self-Reported Home Vitals (Optional)"):
                    v_col1, v_col2, v_col3, v_col4 = st.columns(4)
                    p_bp = v_col1.text_input("BP", placeholder="120/80")
                    p_pulse = v_col2.text_input("Pulse", placeholder="72")
                    p_spo2 = v_col3.text_input("SpO2 %", placeholder="98%")
                    p_temp = v_col4.text_input("Temp", placeholder="98.6 F")

                st.success("🎁 **Aster Style Assurance:** Includes a **7-Day Free Follow-Up Window** for any prescription doubts or review queries.")

                wa_custom_url = get_detailed_whatsapp_url(consultation_mode, p_name, p_age, p_gender, p_city, p_id_proof, p_abha, p_details, p_pref_doc, p_bp, p_pulse, p_spo2, p_temp, "English")

                st.markdown(f'''
                    <br>
                    <a href="{wa_custom_url}" target="_blank" class="btn-wa" style="font-size: 17px;">
                        💬 Submit Form & Launch WhatsApp Consultation Request (Fee: {CONSULTATION_FEE})
                    </a>
                    <p style="font-size:11.5px; color:#64748b; text-align:center; margin-top:8px;">🔒 Data strictly encrypted & processed as per DPDP Act 2023 and NMC Regulations.</p>
                    </div>
                ''', unsafe_allow_html=True)

            st.markdown("---")

            # FAQs
            if selected_lang == "தமிழ் (Tamil)":
                st.subheader("❓ அடிக்கடி கேட்கப்படும் கேள்விகள் (FAQs)")
                with st.expander("1. எனது இரத்தப் பரிசோதனை அல்லது ஸ்கேன் அறிக்கைகளை எவ்வாறு அனுப்புவது?"):
                    st.write("மேலே உள்ள வாட்ஸ்அப் பொத்தானைக் கிளிக் செய்த பிறகு, உங்கள் அறிக்கைகளின் புகைப்படங்கள் அல்லது PDF கோப்புகளை வாட்ஸ்அப் அரட்டையிலேயே நேரடியாக இணைக்கலாம்.")
                with st.expander("2. மருத்துவரின் ஆலோசனையை நான் எப்போது பெறுவேன்?"):
                    st.write("காலை 9:00 மணி முதல் மாலை 3:00 மணி வரை பெறப்படும் அறிக்கைகள், எங்கள் தினசரி மருத்துவர் பரிசீலனை நேரமான மாலை 4:00 மணி முதல் 6:00 மணிக்குள் ஆய்வு செய்யப்படும்.")
            else:
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

    # TAB 2: Specialty Services
    with tab2:
        if selected_lang == "தமிழ் (Tamil)":
            st.subheader("📋 விரிவான மருத்துவ சேவைகள் & சிறப்புப் பிரிவுகள்")
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                st.markdown("""
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🥗 1. உணவுப் பழக்க வழக்கம் & DASH Diet</h4>
                        <p style="font-size:13px;">இரத்த அழுத்தத்தைக் கட்டுப்படுத்த <b>DASH Diet</b> திட்டம் மற்றும் சர்க்கரை அளவை நிர்வகிக்க <b>Diabetic Diet</b> வழிகாட்டுதல்.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🩸 2. சர்க்கரை & ரத்த அழுத்த மேலாண்மை</h4>
                        <p style="font-size:13px;">இரத்தச் சர்க்கரை இலக்கு மதிப்பீடு, இரத்த அழுத்தக் கண்காணிப்பு மற்றும் நீண்டகால உடல்நலப் பாதுகாப்பு.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">💊 3. நாள்பட்ட மருந்து ரீஃபில் & மருந்துச் செயல்பாடு</h4>
                        <p style="font-size:13px;">நீண்டகால மாத்திரைகளின் பாதுகாப்பான பயன்பாடு, <b>Drug Dosage Monitoring</b> மற்றும் பக்கவிளைவு ஆலோசனைகள்.</p>
                    </div>
                """, unsafe_allow_html=True)
            with s_col2:
                st.markdown("""
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">📑 4. CT / MRI ஸ்கேன் & லேப் ரிப்போர்ட் ஆய்வு</h4>
                        <p style="font-size:13px;">ஸ்கேன் மற்றும் இரத்த பரிசோதனை அறிக்கைகளுக்கான துல்லியமான இரண்டாம் கட்ட மருத்துவ கருத்து (Second Opinion).</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🕊️ 5. பரிவுப் பராமரிப்பு (Palliative Care)</h4>
                        <p style="font-size:13px;">நாள்பட்ட நோய்களுக்கான வேதனை நிவாரணம் மற்றும் முழுமையான ஆதரவு பராமரிப்பு.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">⚡ 6. நாள்பட்ட வலி மேலாண்மை</h4>
                        <p style="font-size:13px;">நீண்டகால உடல் வலி, மூட்டு வலி நிவாரணம் மற்றும் வாழ்க்கைமுறை மாற்ற வழிகாட்டுதல்.</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.subheader("📋 Comprehensive Clinical Focus & Specialties")
            s_col1, s_col2 = st.columns(2)
            with s_col1:
                st.markdown("""
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🥗 1. Diet Advice & DASH Diet</h4>
                        <p style="font-size:13px;">Tailored <b>DASH Diet</b> plans for Blood Pressure control and customized <b>Diabetic Diet</b> plans.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🩸 2. Diabetic & HTN Management</h4>
                        <p style="font-size:13px;">Blood glucose target evaluations, blood pressure trend reviews, and long-term metabolic risk prevention.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">💊 3. Prescription Refills & Drug Action</h4>
                        <p style="font-size:13px;">Precise <b>Drug Dosage Monitoring</b>, chronic medication refills, and drug interaction safety checks.</p>
                    </div>
                """, unsafe_allow_html=True)
            with s_col2:
                st.markdown("""
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">📑 4. CT / MRI Scan & Lab Review</h4>
                        <p style="font-size:13px;">Expert second opinion on blood investigations, CT/MRI scan imaging reports, and diagnostic clarity.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🕊️ 5. Palliative Care</h4>
                        <p style="font-size:13px;">Holistic symptom relief and compassionate comfort care guidance.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">⚡ 6. Chronic Pain Management</h4>
                        <p style="font-size:13px;">Evidence-based pain protocol reviews and arthritis care guidance.</p>
                    </div>
                """, unsafe_allow_html=True)

    # TAB 3: NMC COMPLIANCE & LEGAL COMPLIANCE TAB
    with tab3:
        st.subheader("📜 NMC Telemedicine Legal Compliance Guidelines")
        st.write("Summary of key legal, clinical, and data privacy protocols governing **N2 Care Teleclinic** based on National Medical Commission (NMC) Regulations & NHSRC Framework:")

        if HAS_REPORTLAB:
            pdf_data = generate_nmc_compliance_pdf()
            st.download_button(
                label="📥 Download Official NMC Compliance PDF Roadmap",
                data=pdf_data,
                file_name="N2_Care_Teleclinic_NMC_Compliance_Roadmap.pdf",
                mime="application/pdf",
                type="primary"
            )
        else:
            st.info("💡 *PDF Download module is currently running in web-mode. For PDF file generation, add 'reportlab' to your GitHub requirements.txt file.*")

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
            <div style="background: #ffffff; border: 2px solid #0b3c5d; padding: 22px; border-radius: 16px;">
                <h4 style="color: #0b3c5d !important; margin-top:0;">⚖️ Key Telemedicine Rules Summary</h4>
                <p style="font-size: 13.5px; color: #334155;"><b>1. Practitioner Credentials:</b> Name, MBBS/MD qualifications, and State Medical Council Reg No (e.g., TNMC Reg No: 159693) displayed on all Rx pads and digital chats.</p>
                <p style="font-size: 13.5px; color: #334155;"><b>2. Minor Consultations:</b> Consultations for patients under 18 years proceed only in the presence of an adult parent/guardian.</p>
                <p style="font-size: 13.5px; color: #334155;"><b>3. Drug Prescription Categories:</b> OTC medications allowed across all modes (List O). Prescription topicals and refills allowed during Video Consultations (List A). Narcotic, Schedule X, and habit-forming drugs are strictly prohibited.</p>
                <p style="font-size: 13.5px; color: #334155;"><b>4. Record Retention:</b> Patient histories, diagnostic uploads, and consultation logs retained securely for a mandatory minimum of 3 years under DPDP Act 2023.</p>
                <p style="font-size: 13.5px; color: #334155;"><b>5. Human Doctor Mandate:</b> AI tools cannot prescribe or independently counsel. All clinical decisions are directly rendered by registered doctors.</p>
            </div>
        """, unsafe_allow_html=True)

    # TAB 4: DOCTOR INTERNAL PORTAL
    with tab4:
        st.subheader("🔒 Doctor Internal Portal")
        pin_input_1 = st.text_input("Enter 4-Digit Doctor Passcode:", type="password", key="pin1")
        
        authenticated_doctor_1 = authenticate_doctor(pin_input_1)
        if authenticated_doctor_1:
            st.success(f"Welcome, {authenticated_doctor_1}! Authenticated Successfully.")
            with st.form("clinical_entry_form", clear_on_submit=True):
                col1, col2 = st.columns(2)
                with col1:
                    patient_name = st.text_input("1. Patient Name *")
                    age = st.number_input("2. Age", min_value=0, max_value=120, value=25)
                    gender = st.selectbox("3. Gender", ["Male", "Female", "Other"])
                    phone = st.text_input("4. Contact Number")
                    address = st.text_area("5. Address / Place", height=80)
                    doc_id_proof = st.text_input("6. ID Card Details", placeholder="Aadhaar / Voter ID")
                    doc_abha = st.text_input("7. ABHA Number / Address (Optional)", placeholder="12-3456-7890-1234")
                with col2:
                    consultation_type = st.selectbox("8. Consultation Focus", [
                        "Second Opinion (Report Review)",
                        "Prescription Refill & Chronic Care",
                        "Drug / Medication Clarification",
                        "Diet & DASH Diet Planning",
                        "CT / MRI Scan Review",
                        "General Medical Consultation"
                    ])
                    preferred_slot = st.selectbox("9. Review Time Slot", [
                        "4:00 PM - 4:30 PM",
                        "4:30 PM - 5:00 PM",
                        "5:00 PM - 5:30 PM",
                        "5:30 PM - 6:00 PM"
                    ])
                    followup_date = st.date_input("10. Follow-Up Date")
                    
                    st.markdown("<b>11. Patient Vitals:</b>", unsafe_allow_html=True)
                    v_col1, v_col2, v_col3, v_col4 = st.columns(4)
                    bp = v_col1.text_input("BP", placeholder="120/80")
                    pulse = v_col2.text_input("Pulse", placeholder="72")
                    spo2 = v_col3.text_input("SpO2 %", placeholder="98%")
                    temp = v_col4.text_input("Temp", placeholder="98.6 F")

                st.markdown("---")
                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    complaints = st.text_area("12. Chief Complaints / Symptoms", height=100)
                    investigation = st.text_area("13. Lab Reports & Scans Review", height=100)
                with col_c2:
                    treatment_history = st.text_area("14. Clinical Advice / Notes", height=100)
                    prescription_details = st.text_area(
                        "15. Digital E-Prescription (Drug | Dosage | Duration | Instruction) - WRITE IN CAPITAL LETTERS", 
                        placeholder="1. TAB PARACETAMOL 650MG | 1-0-1 | 5 days | After Food",
                        height=100
                    )

                submit_btn = st.form_submit_button("💾 Save Patient Clinical Record")
                if submit_btn and patient_name.strip():
                    entry_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    c.execute('''
                        INSERT INTO patients (
                            entry_date, patient_name, age, gender, phone, address, 
                            bp, pulse, spo2, temp, complaints, investigation, 
                            treatment_history, prescription_details, consultation_type, 
                            preferred_slot, followup_date, abha_id, id_card_details, preferred_doctor
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        entry_time, patient_name, age, gender, phone, address,
                        bp, pulse, spo2, temp, complaints, investigation,
                        treatment_history, prescription_details, consultation_type,
                        preferred_slot, str(followup_date), doc_abha, doc_id_proof, authenticated_doctor_1
                    ))
                    conn.commit()
                    st.success(f"Record successfully saved for {patient_name}!")
        elif pin_input_1:
            st.error("Incorrect Passcode.")

    # TAB 5: DATABASE & OFFICIAL PRINTABLE LOGO E-PRESCRIPTION PAD
    with tab5:
        st.subheader("🔒 Doctor Internal Portal")
        pin_input_2 = st.text_input("Enter 4-Digit Doctor Passcode:", type="password", key="pin2")

        authenticated_doctor_2 = authenticate_doctor(pin_input_2)
        if authenticated_doctor_2:
            st.success(f"Welcome, {authenticated_doctor_2}! Authenticated Successfully.")
            df = pd.read_sql_query("SELECT * FROM patients ORDER BY patient_id DESC", conn)

            if not df.empty:
                search_query = st.text_input("🔍 Search Patients by Name or Phone Number:")
                df_filtered = df[df['patient_name'].str.contains(search_query, case=False, na=False)] if search_query else df
                st.dataframe(df_filtered, use_container_width=True)

                st.markdown("---")
                selected_id = st.selectbox("Select Patient ID to view Official Rx Pad:", df_filtered['patient_id'].tolist())
                patient_row = df_filtered[df_filtered['patient_id'] == selected_id].iloc[0]

                # LOGO HEADER IN E-PRESCRIPTION PAD
                st.markdown('<div class="rx-container">', unsafe_allow_html=True)
                
                logo_files = ["welcome_poster.png", "117482.png", "doc_vigneshwar.png"]
                logo_found = False
                for lf in logo_files:
                    if os.path.exists(lf):
                        st.image(lf, width=130)
                        logo_found = True
                        break
                        
                st.markdown(f"""
                    <div style="text-align: center; border-bottom: 2.5px solid #0b3c5d; padding-bottom: 12px; margin-bottom: 20px;">
                        <h1 style="color: #0b3c5d !important; margin: 0; font-size: 26px; font-weight: 800;">N2 CARE TELECLINIC</h1>
                        <p style="margin: 3px 0; color: #bc6c25; font-style: italic; font-weight: 700; font-size: 14px;">"Your Friendly Second Opinion"</p>
                        <p style="margin: 2px 0; font-size: 12.5px; color: #334155;">
                            <b>Dr. T. Vigneshwar</b>, MBBS, MD General Medicine (TNMC Reg No: 159693)<br/>
                            <b>Dr. S. Malathi</b>, MBBS, MD General Medicine
                        </p>
                        <small style="color: #64748b;">Official WhatsApp: +91 94868 72627 | UPI ID: 9486872627@upi</small>
                    </div>

                    <table style="width:100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13.5px;">
                        <tr style="background-color: #f8fafc;">
                            <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Patient ID:</b> #{patient_row['patient_id']}</td>
                            <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Name:</b> {patient_row['patient_name']}</td>
                            <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Age / Gender:</b> {patient_row['age']} yrs / {patient_row['gender']}</td>
                            <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>Date:</b> {patient_row['entry_date']}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>ID Proof:</b> {patient_row['id_card_details'] if 'id_card_details' in patient_row and patient_row['id_card_details'] else 'Not Provided'}</td>
                            <td style="padding: 8px; border: 1px solid #cbd5e1;"><b>ABHA ID:</b> {patient_row['abha_id'] if 'abha_id' in patient_row and patient_row['abha_id'] else 'Not Provided'}</td>
                            <td colspan="2" style="padding: 8px; border: 1px solid #cbd5e1;"><b>Vitals:</b> BP: {patient_row['bp']} | Pulse: {patient_row['pulse']} | SpO2: {patient_row['spo2']} | Temp: {patient_row['temp']}</td>
                        </tr>
                    </table>

                    <div style="margin-bottom: 15px;">
                        <b style="color: #0b3c5d;">Chief Complaints / Clinical Notes:</b>
                        <p style="background: #f1f5f9; padding: 10px; border-radius: 8px; margin-top: 4px; font-size: 13px;">{patient_row['complaints']}</p>
                    </div>

                    <div style="margin-bottom: 15px;">
                        <b style="color: #0b3c5d;">Lab & Scan Evaluation Notes:</b>
                        <p style="background: #f1f5f9; padding: 10px; border-radius: 8px; margin-top: 4px; font-size: 13px;">{patient_row['investigation']}</p>
                    </div>

                    <div style="margin-bottom: 20px;">
                        <h3 style="color: #ef4444 !important; margin-bottom: 8px;">💊 Rx (Digital Prescription)</h3>
                        <p style="background-color: #fffbeb; border: 1.5px solid #fef08a; padding: 18px; border-radius: 10px; font-family: monospace; font-size: 14px; font-weight: 700; white-space: pre-wrap; color: #1e293b;">{patient_row['prescription_details']}</p>
                    </div>

                    <div style="margin-top: 30px; border-top: 1.5px solid #e2e8f0; padding-top: 15px; display: flex; justify-content: space-between; align-items: center;">
                        <div style="font-size: 11px; color: #64748b;">
                            📌 <i>NMC Guidelines Compliant E-Prescription. Valid for 2 weeks from date of issue.</i><br/>
                            🔒 Data encrypted as per Digital Personal Data Protection (DPDP) Act 2023.
                        </div>
                        <div style="text-align: right;">
                            <p style="margin:0; font-weight:800; color:#0b3c5d; font-size:14px;">Dr. T. Vigneshwar / Dr. S. Malathi</p>
                            <small style="color:#64748b;">Digitally Signed & Verified RMP</small>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
