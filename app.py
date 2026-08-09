import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse
import os

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
    "1596": "Dr. Vigneshwar",
    "2026": "Dr. S. Malathi"
}

# Session State Initializations
if 'app_language' not in st.session_state:
    st.session_state.app_language = None

if 'selected_consultation_mode' not in st.session_state:
    st.session_state.selected_consultation_mode = "Fresh Teleconsultation"

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

# Helper Function: Structured WhatsApp Form Link
def get_detailed_whatsapp_url(mode, name, age, gender, city, service_name, notes, report_link, lang):
    if "Tamil" in lang:
        msg = f"🏥 *N2 CARE TELECLINIC - மருத்துவ ஆலோசனை விண்ணப்பம்*\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"📌 *ஆலோசனை வகை:* {mode}\n"
        msg += f"👤 *நோயாளி பெயர்:* {name if name else 'குறிப்பிடப்படவில்லை'}\n"
        msg += f"🎂 *வயது / பாலினம்:* {age} வயது | {gender}\n"
        msg += f"📍 *ஊர் / மாவட்டம்:* {city if city else 'குறிப்பிடப்படவில்லை'}\n"
        msg += f"🩺 *ஆலோசனைப் பிரிவு:* {service_name}\n"
        msg += f"🏷️ *கட்டணம்:* {CONSULTATION_FEE}\n"
        if report_link:
            msg += f"🔗 *ரிப்போர்ட் லிங்க்:* {report_link}\n"
        if notes:
            msg += f"📝 *அறிகுறிகள் / சந்தேகங்கள்:* {notes}\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"📩 *குறிப்பு:* எனது இரத்த பரிசோதனை / ஸ்கேன் அறிக்கை / கட்டண ஸ்கிரீன்ஷாட்டை இதில் இணைக்கிறேன். மாலை {REVIEW_HOURS} மணிக்குள் பரிசீலிக்கவும்."
    else:
        msg = f"🏥 *N2 CARE TELECLINIC - CONSULTATION REQUEST*\n"
        msg += f"━━━━━━━━━━━━━━━━━━━━━━\n"
        msg += f"📌 *Consultation Mode:* {mode}\n"
        msg += f"👤 *Patient Name:* {name if name else 'Not Provided'}\n"
        msg += f"🎂 *Age / Gender:* {age} yrs | {gender}\n"
        msg += f"📍 *Location/City:* {city if city else 'Not Provided'}\n"
        msg += f"🩺 *Focus Area:* {service_name}\n"
        msg += f"🏷️ *Fee:* {CONSULTATION_FEE}\n"
        if report_link:
            msg += f"🔗 *Report Link:* {report_link}\n"
        if notes:
            msg += f"📝 *Symptoms / Doubts:* {notes}\n"
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

    .doc-avatar-card {
        background: #ffffff !important;
        border: 2px solid #dda15e !important;
        border-radius: 18px !important;
        padding: 15px !important;
        text-align: center;
        box-shadow: 0 6px 18px rgba(188, 108, 37, 0.1) !important;
        height: 100%;
    }

    .doc-avatar-card-selected {
        background: #fefae0 !important;
        border: 3px solid #0b3c5d !important;
        border-radius: 18px !important;
        padding: 15px !important;
        text-align: center;
        box-shadow: 0 8px 22px rgba(11, 60, 93, 0.25) !important;
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

    .welcome-lang-box {
        background: #ffffff;
        border: 3px solid #dda15e;
        padding: 25px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 30px rgba(188, 108, 37, 0.15);
        margin-top: 15px;
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
                <small style="font-size: 14px;">Dr. Vigneshwar, MBBS, MD & Dr. S. Malathi, MBBS, MD</small>
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
            "🌐 மருத்துவமனை வழிகாட்டி",
            "🔒 மருத்துவர் உள்நுழைவு",
            "🔒 நோயாளி தரவுத்தளம் & மருந்துச் சீட்டு"
        ])
    else:
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🤝 Patient Portal & Booking",
            "🩺 Specialty Services & Packages",
            "🌐 Regional Directory",
            "🔒 Doctor Dashboard",
            "🔒 Database & E-Prescription"
        ])

    # TAB 1: Patient Consultation Portal
    with tab1:
        st.markdown("<br>", unsafe_allow_html=True)
        
        # 🌟 DOCTOR AVATAR TOGGLE SELECTOR 🌟
        if selected_lang == "தமிழ் (Tamil)":
            st.subheader("ஆலோசனை வகையைத் தேர்ந்தெடுக்கவும் (Choose Consultation Mode):")
        else:
            st.subheader("Select Consultation Mode:")

        doc_card1, doc_card2 = st.columns(2)

        # Avatar 1: Dr. Vigneshwar (Fresh Teleconsultation)
        with doc_card1:
            is_fresh = st.session_state.selected_consultation_mode == "Fresh Teleconsultation"
            card_class = "doc-avatar-card-selected" if is_fresh else "doc-avatar-card"
            
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            v_img_files = ["doc_vigneshwar.png", "116810.png", "doc_vigneshwar.jpg"]
            v_found = False
            for img in v_img_files:
                if os.path.exists(img):
                    st.image(img, width=120)
                    v_found = True
                    break
            if not v_found:
                st.markdown('<div style="font-size: 55px;">👨‍⚕️</div>', unsafe_allow_html=True)

            if selected_lang == "தமிழ் (Tamil)":
                st.markdown("""
                    <h4 style="color:#0b3c5d; margin:5px 0 2px 0;">Dr. Vigneshwar</h4>
                    <p style="font-size:12px; color:#475569; margin-bottom:8px;">MBBS, MD General Medicine (TNMC 159693)</p>
                    <b style="color:#059669; font-size:15px;">🟢 1. புதிய மருத்துவ ஆலோசனை</b>
                    <p style="font-size:12px; color:#57534e; margin-top:4px;">புதிய அறிகுறிகள், பொதுவான உடல்நலக் கேள்விகள் மற்றும் நேரடி வழிகாட்டுதலுக்கு.</p>
                """, unsafe_allow_html=True)
                if st.button("இது தேவை (Select Fresh Consult)", key="btn_fresh", type="primary" if is_fresh else "secondary"):
                    st.session_state.selected_consultation_mode = "Fresh Teleconsultation"
                    st.rerun()
            else:
                st.markdown("""
                    <h4 style="color:#0b3c5d; margin:5px 0 2px 0;">Dr. Vigneshwar</h4>
                    <p style="font-size:12px; color:#475569; margin-bottom:8px;">MBBS, MD General Medicine (TNMC 159693)</p>
                    <b style="color:#059669; font-size:15px;">🟢 1. Fresh Teleconsultation</b>
                    <p style="font-size:12px; color:#57534e; margin-top:4px;">For new symptoms, general health queries, and direct doctor guidance.</p>
                """, unsafe_allow_html=True)
                if st.button("Select Fresh Teleconsultation", key="btn_fresh", type="primary" if is_fresh else "secondary"):
                    st.session_state.selected_consultation_mode = "Fresh Teleconsultation"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        # Avatar 2: Dr. S. Malathi (Second Opinion)
        with doc_card2:
            is_second = st.session_state.selected_consultation_mode == "Second Opinion"
            card_class = "doc-avatar-card-selected" if is_second else "doc-avatar-card"
            
            st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
            m_img_files = ["doc_malathi.png", "116809.png", "doc_malathi.jpg"]
            m_found = False
            for img in m_img_files:
                if os.path.exists(img):
                    st.image(img, width=120)
                    m_found = True
                    break
            if not m_found:
                st.markdown('<div style="font-size: 55px;">👩‍⚕️</div>', unsafe_allow_html=True)

            if selected_lang == "தமிழ் (Tamil)":
                st.markdown("""
                    <h4 style="color:#0b3c5d; margin:5px 0 2px 0;">Dr. S. Malathi</h4>
                    <p style="font-size:12px; color:#475569; margin-bottom:8px;">MBBS, MD General Medicine</p>
                    <b style="color:#0284c7; font-size:15px;">🔵 2. இரண்டாம் கட்ட ஆலோசனை</b>
                    <p style="font-size:12px; color:#57534e; margin-top:4px;">இரத்தப் பரிசோதனை, ஸ்கேன் ரிப்போர்ட் மற்றும் மருந்துப் பாதுகாப்பு ஆய்வுக்கு.</p>
                """, unsafe_allow_html=True)
                if st.button("இது தேவை (Select Second Opinion)", key="btn_second", type="primary" if is_second else "secondary"):
                    st.session_state.selected_consultation_mode = "Second Opinion"
                    st.rerun()
            else:
                st.markdown("""
                    <h4 style="color:#0b3c5d; margin:5px 0 2px 0;">Dr. S. Malathi</h4>
                    <p style="font-size:12px; color:#475569; margin-bottom:8px;">MBBS, MD General Medicine</p>
                    <b style="color:#0284c7; font-size:15px;">🔵 2. Second Opinion</b>
                    <p style="font-size:12px; color:#57534e; margin-top:4px;">For blood test reviews, scan report evaluations, and drug safety checks.</p>
                """, unsafe_allow_html=True)
                if st.button("Select Second Opinion", key="btn_second", type="primary" if is_second else "secondary"):
                    st.session_state.selected_consultation_mode = "Second Opinion"
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Form Section
        consultation_mode = st.session_state.selected_consultation_mode

        if selected_lang == "தமிழ் (Tamil)":
            st.markdown(f"""
                <div style="background: #ffffff; border: 2px solid #0b3c5d; padding: 25px; border-radius: 16px;">
                    <h3 style="color: #0b3c5d !important; margin-top: 0;">📋 நோயாளி விவரங்கள் படிவம் ({consultation_mode})</h3>
                    <p style="font-size: 13px; color: #57534e;">உங்கள் விவரங்களை கீழே நிரப்பவும். இவை தானாகவே வாட்ஸ்அப் செய்தியாக மாறும்.</p>
            """, unsafe_allow_html=True)

            f_col1, f_col2, f_col3 = st.columns(3)
            with f_col1:
                p_name = st.text_input("1. முழு பெயர் *", placeholder="எ.கா. ரமேஷ் குமார்")
            with f_col2:
                p_age = st.number_input("2. வயது *", min_value=1, max_value=110, value=35)
            with f_col3:
                p_gender = st.selectbox("3. பாலினம் *", ["ஆண்", "பெண்", "மற்றவை"])

            f_col4, f_col5 = st.columns(2)
            with f_col4:
                p_city = st.text_input("4. ஊர் / மாவட்டம் *", placeholder="எ.கா. திருச்சி / சென்னை")
            with f_col5:
                p_service = st.selectbox("5. ஆலோசனை தேவைப்படும் பகுதி *", [
                    "உணவுப் பழக்க வழக்கம் (DASH Diet & Diabetic Diet)",
                    "சர்க்கரை & ரத்த அழுத்த மேலாண்மை (Diabetes & HTN)",
                    "இதயம் & சிறுநீரக பாதுகாப்பு (Drug Dosage Monitoring)",
                    "தடுப்பூசி வழிகாட்டுதல் (Vaccination Guidance)",
                    "பரிவுப் பராமரிப்பு (Palliative Care)",
                    "நாள்பட்ட வலி மேலாண்மை (Chronic Pain)",
                    "இரத்த பரிசோதனை அறிக்கை ஆய்வு (Lab Report Review)",
                    "ஸ்கேன் அறிக்கை ஆய்வு (CT / MRI Scan Opinion)"
                ])

            p_notes = st.text_area("6. அறிகுறிகள் அல்லது மருத்துவ கேள்விகள்:", placeholder="எ.கா. சர்க்கரை அளவு மற்றும் மாத்திரை அளவு பற்றி கேட்க வேண்டும்...")
            p_link = st.text_input("7. ஸ்கேன் / ரிப்போர்ட் லிங்க் (விருப்பமிருந்தால்):", placeholder="https://drive.google.com/...")

            wa_custom_url = get_detailed_whatsapp_url(consultation_mode, p_name, p_age, p_gender, p_city, p_service, p_notes, p_link, "தமிழ் (Tamil)")

            st.markdown(f'''
                <br>
                <a href="{wa_custom_url}" target="_blank" class="btn-wa" style="font-size: 17px;">
                    💬 படிவத்தை சமர்ப்பித்து வாட்ஸ்அப்பில் தொடங்கவும் (கட்டணம்: {CONSULTATION_FEE})
                </a>
                </div>
            ''', unsafe_allow_html=True)

        else:
            st.markdown(f"""
                <div style="background: #ffffff; border: 2px solid #0b3c5d; padding: 25px; border-radius: 16px;">
                    <h3 style="color: #0b3c5d !important; margin-top: 0; font-size: 22px;">📋 Patient Details & Consultation Form ({consultation_mode})</h3>
                    <p style="font-size: 13px; color: #57534e;">Please fill out your details below. These will be formatted and pre-filled into WhatsApp automatically.</p>
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
                p_service = st.selectbox("5. Focus Area *", [
                    "Diet Advice (DASH Diet & Diabetic Diet)",
                    "Diabetic & HTN Management",
                    "Heart & Kidney Care (Drug Dosage Monitoring)",
                    "Vaccination Doubts & Schedule Guidance",
                    "Palliative Care & Comfort Support",
                    "Chronic Pain Management",
                    "Lab & Blood Report Review",
                    "CT / MRI Scan Second Opinion"
                ])

            p_notes = st.text_area("6. Describe Your Symptoms or Clinical Questions:", placeholder="e.g. Want advice on diabetic diet plan and HbA1c report review. Currently taking Metformin 500mg...")
            p_link = st.text_input("7. Google Drive / Scan Report Link (Optional):", placeholder="https://drive.google.com/...")

            wa_custom_url = get_detailed_whatsapp_url(consultation_mode, p_name, p_age, p_gender, p_city, p_service, p_notes, p_link, "English")

            st.markdown(f'''
                <br>
                <a href="{wa_custom_url}" target="_blank" class="btn-wa" style="font-size: 17px;">
                    💬 Submit Form & Launch WhatsApp Consultation Request (Fee: {CONSULTATION_FEE})
                </a>
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
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🥗 1. உணவுப் பழக்க வழக்கம்</h4>
                        <p style="font-size:13px;">இரத்த அழுத்தத்தைக் கட்டுப்படுத்த <b>DASH Diet</b> திட்டம் மற்றும் சர்க்கரை அளவை நிர்வகிக்க <b>Diabetic Diet</b> வழிகாட்டுதல்.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🩸 2. சர்க்கரை & ரத்த அழுத்த மேலாண்மை</h4>
                        <p style="font-size:13px;">இரத்தச் சர்க்கரை இலக்கு மதிப்பீடு, இரத்த அழுத்தக் கண்காணிப்பு மற்றும் நீண்டகால உடல்நலப் பாதுகாப்பு.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🫀 3. இதயம் & சிறுநீரக பாதுகாப்பு</h4>
                        <p style="font-size:13px;">துல்லியமான <b>மருந்து அளவு கண்காணிப்பு (Drug Dosage Monitoring)</b> மற்றும் சிறுநீரகச் செயல்பாட்டுப் பாதுகாப்பு.</p>
                    </div>
                """, unsafe_allow_html=True)
            with s_col2:
                st.markdown("""
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">💉 4. தடுப்பூசி வழிகாட்டுதல்</h4>
                        <p style="font-size:13px;">பெரியவர்கள் மற்றும் குழந்தைகளுக்கான தடுப்பூசி அட்டவணை மற்றும் பாதுகாப்பு ஆலோசனைகள்.</p>
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
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🥗 1. Diet Advice</h4>
                        <p style="font-size:13px;">Tailored <b>DASH Diet</b> plans for Blood Pressure control and customized <b>Diabetic Diet</b> plans.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🩸 2. Diabetic & HTN Management</h4>
                        <p style="font-size:13px;">Blood glucose target evaluations, blood pressure trend reviews, and long-term metabolic risk prevention.</p>
                    </div>
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">🫀 3. Heart & Kidney Care</h4>
                        <p style="font-size:13px;">Precise <b>Drug Dosage Monitoring</b> and renal filtration safety checks.</p>
                    </div>
                """, unsafe_allow_html=True)
            with s_col2:
                st.markdown("""
                    <div class="service-box">
                        <h4 style="color: #0b3c5d !important; margin-top:0;">💉 4. Vaccination Guidance</h4>
                        <p style="font-size:13px;">Adult & pediatric immunization schedule guidance and vaccine safety evaluations.</p>
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

    # TAB 3: Directory
    with tab3:
        st.subheader("🌐 Regional & National Medical Directory")

    # TAB 4: Doctor Internal Portal
    with tab4:
        st.subheader("🔒 Doctor Internal Portal")
        pin_input_1 = st.text_input("Enter 4-Digit Doctor Passcode:", type="password", key="pin1")
        
        if pin_input_1 in DOCTOR_PINS:
            st.success(f"Welcome, {DOCTOR_PINS[pin_input_1]}! Authenticated Successfully.")
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
                        placeholder="1. Tab Paracetamol 650mg | 1-0-1 | 5 days | After Food",
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

    # TAB 5: Database & E-Prescription Pad
    with tab5:
        st.subheader("🔒 Doctor Internal Portal")
        pin_input_2 = st.text_input("Enter 4-Digit Doctor Passcode:", type="password", key="pin2")

        if pin_input_2 in DOCTOR_PINS:
            st.success(f"Welcome, {DOCTOR_PINS[pin_input_2]}! Authenticated Successfully.")
            df = pd.read_sql_query("SELECT * FROM patients ORDER BY patient_id DESC", conn)

            if not df.empty:
                search_query = st.text_input("🔍 Search Patients by Name or Phone Number:")
                df_filtered = df[df['patient_name'].str.contains(search_query, case=False, na=False)] if search_query else df
                st.dataframe(df_filtered, use_container_width=True)

                st.markdown("---")
                selected_id = st.selectbox("Select Patient ID to view Rx Pad:", df_filtered['patient_id'].tolist())
                patient_row = df_filtered[df_filtered['patient_id'] == selected_id].iloc[0]

                st.markdown(f"""
                    <div style="border: 2px solid #0b3c5d; padding: 30px; border-radius: 12px; background-color: #ffffff;">
                        <div style="text-align: center; border-bottom: 2px solid #0b3c5d; padding-bottom: 12px; margin-bottom: 20px;">
                            <h2 style="color: #0b3c5d !important; margin: 0;">N2 CARE TELECLINIC</h2>
                            <p style="margin: 3px 0; font-style: italic; font-weight: 700;">"Your Friendly Second Opinion"</p>
                            <small><b>Dr. Vigneshwar</b>, MBBS, MD (TNMC Reg No 159693) | <b>Dr. S. Malathi</b>, MBBS, MD</small><br>
                            <small>WhatsApp: +91 94868 72627 | UPI: 9486872627@upi</small>
                        </div>
                        <p><b>Patient Name:</b> {patient_row['patient_name']} &nbsp;|&nbsp; <b>Age/Gender:</b> {patient_row['age']} yrs / {patient_row['gender']}</p>
                        <p><b>Vitals:</b> BP: {patient_row['bp']} | Pulse: {patient_row['pulse']} | SpO2: {patient_row['spo2']} | Temp: {patient_row['temp']}</p>
                        <p><b>Chief Complaints:</b><br>{patient_row['complaints']}</p>
                        <p><b>Investigations Review:</b><br>{patient_row['investigation']}</p>
                        <p><b>Clinical Advice:</b><br>{patient_row['treatment_history']}</p>
                        <h4 style="color: #ef4444 !important;">💊 Rx (Prescription):</h4>
                        <p style="background-color: #fffbeb; padding: 15px; border-radius: 8px; font-family: monospace;">{patient_row['prescription_details']}</p>
                    </div>
                """, unsafe_allow_html=True)
