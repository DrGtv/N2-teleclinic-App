import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse
import os

# 1. Page Configuration
st.set_page_config(
    page_title="N2 Care Teleclinic | First Screen Blueprint Selector",
    page_icon="🩺",
    layout="wide"
)

# Configuration Variables
CLINIC_PHONE = "919486872627"
CONSULTATION_FEE = "₹100"

st.markdown("""
<style>
    .stApp { background: #fafaf9 !important; }
    .hero-btn-green {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white !important; padding: 20px; border-radius: 14px;
        text-align: center; font-weight: 800; font-size: 20px;
        box-shadow: 0 6px 16px rgba(16, 185, 129, 0.25);
    }
    .hero-btn-blue {
        background: linear-gradient(135deg, #0284c7 0%, #0369a1 100%);
        color: white !important; padding: 20px; border-radius: 14px;
        text-align: center; font-weight: 800; font-size: 20px;
        box-shadow: 0 6px 16px rgba(2, 132, 199, 0.25);
    }
    .service-card {
        background: #ffffff; border: 1.5px solid #dda15e;
        padding: 16px; border-radius: 12px; margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.04);
    }
</style>
""", unsafe_allow_html=True)

st.title("🩺 N2 Care Teleclinic - Blueprint Tester")
blueprint = st.radio("Select Blueprint Layout to Live Preview:", [
    "Blueprint 1: Modern Split Hero & Grid Cards",
    "Blueprint 2: Tabbed Action Bar & Clinical Badges",
    "Blueprint 3: Interactive Patient Portal Gateway",
    "Blueprint 4: Dual-Column Pathways",
    "Blueprint 5: Executive Service Matrix"
], horizontal=True)

st.markdown("---")

# 1. TOP GATEWAY OPTIONS (Common to all)
col_a, col_b = st.columns(2)
with col_a:
    st.markdown('<div class="hero-btn-green">🟢 Option 1: Fresh Teleconsultation<br><small style="font-size:13px; font-weight:normal;">For new symptoms, general checkups & quick guidance</small></div>', unsafe_allow_html=True)
with col_b:
    st.markdown('<div class="hero-btn-blue">🔵 Option 2: Second Opinion<br><small style="font-size:13px; font-weight:normal;">For blood report reviews, scan evaluations & drug safety</small></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 2. DOCTOR BRANDING
st.markdown("""
    <div style="text-align: center; background: #ffffff; border: 2px solid #dda15e; padding: 15px; border-radius: 16px;">
        <h3 style="color: #0b3c5d; margin:0;">N2 CARE TELECLINIC</h3>
        <p style="color: #bc6c25; margin:0; font-style: italic;">"Your Friendly Second Opinion"</p>
        <small><b>Dr. Vigneshwar</b>, MBBS, MD (TNMC Reg No: 159693) | <b>Dr. S. Malathi</b>, MBBS, MD</small>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 3. CLINICAL SERVICES SECTION (Rendered based on selected Blueprint)
st.subheader("📋 Our Clinical Focus & Specialty Services")

services = [
    ("🥗 1. Diet Advice", "Evidence-based DASH Diet plans for hypertension & customized Diabetic Diet regimens."),
    ("🩸 2. Diabetic & HTN Management", "Blood glucose monitoring, HbA1c target reviews, and Blood Pressure protocol management."),
    ("🫀 3. Heart & Kidney Disease", "Precise drug dosage monitoring, renal safety checks & cardiac risk factor evaluation."),
    ("💉 4. Vaccination Guidance", "Adult & pediatric vaccination schedule doubts, booster guidance & allergy safety."),
    ("🕊️ 5. Palliative Care", "Symptom relief, holistic comfort support, and chronic disease terminal care guidance."),
    ("⚡ 6. Chronic Pain Management", "Long-term pain protocol evaluation, arthritis management & lifestyle interventions.")
]

if "Blueprint 1" in blueprint or "Blueprint 4" in blueprint:
    c1, c2, c3 = st.columns(3)
    for i, (title, desc) in enumerate(services):
        target_col = [c1, c2, c3][i % 3]
        with target_col:
            st.markdown(f'<div class="service-card"><b>{title}</b><p style="font-size:13px; margin-top:5px;">{desc}</p></div>', unsafe_allow_html=True)

elif "Blueprint 2" in blueprint:
    st.info("<b>Group A: Metabolic Care</b>")
    st.write("• Diet Advice (DASH & Diabetic Diet)\n• Diabetes & HTN Management")
    st.info("<b>Group B: Organ Care & Pharmacovigilance</b>")
    st.write("• Heart & Kidney Disease (Drug Dosage Monitoring)\n• Vaccination Doubts")
    st.info("<b>Group C: Supportive & Pain Care</b>")
    st.write("• Palliative Care\n• Chronic Pain Management")

else:
    for title, desc in services:
        with st.expander(title):
            st.write(desc)
