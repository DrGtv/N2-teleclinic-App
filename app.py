import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import urllib.parse
import os
import io

# ReportLab Libraries for PDF Generation
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable

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
