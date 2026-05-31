import streamlit as st
import google.generativeai as genai
import os

from dotenv import load_dotenv
from PIL import Image

from risk_engine import calculate_risk
from prompts import build_prompt
from pdf_reader import extract_pdf_text
from report_generator import create_report

from database import (
    init_db,
    save_result,
    get_history,
    get_total_analyses,
    get_high_risk_count,
    get_average_risk
)

from scam_matcher import (
    find_similar_scam
)

# ---------------------------------
# INITIALIZATION
# ---------------------------------

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

init_db()

# ---------------------------------
# PAGE CONFIG
# ---------------------------------

st.set_page_config(
    page_title="ScamShield India AI",
    page_icon="🛡️",
    layout="wide"
)

# ---------------------------------
# SIDEBAR
# ---------------------------------

with st.sidebar:

    st.header("📜 Analysis History")

    history = get_history()

    if history:

        for item in history[:10]:

            st.write(
                f"ID {item[0]}"
            )

            st.write(
                f"Score: {item[1]}/100"
            )

            st.write(
                f"Level: {item[2]}"
            )

            st.divider()

    else:

        st.write(
            "No analysis history yet."
        )

# ---------------------------------
# HEADER
# ---------------------------------

st.title(
    "🛡️ ScamShield India AI"
)

st.markdown(
    """
Detect and analyze:

- Job Scams
- Internship Scams
- Scholarship Scams
- UPI Frauds
- KYC Frauds
- Lottery Scams
- Phishing Attempts

Powered by Gemini AI
"""
)

st.divider()

# ---------------------------------
# LANGUAGE SELECTION
# ---------------------------------

language = st.selectbox(
    "Select Response Language",
    [
        "English",
        "Hindi",
        "Punjabi"
    ]
)

# ---------------------------------
# INPUTS
# ---------------------------------

user_text = st.text_area(
    "Paste suspicious text",
    height=200
)

uploaded_image = st.file_uploader(
    "Upload Screenshot",
    type=[
        "png",
        "jpg",
        "jpeg"
    ]
)

uploaded_pdf = st.file_uploader(
    "Upload PDF Document",
    type=["pdf"]
)

# ---------------------------------
# ANALYZE BUTTON
# ---------------------------------

if st.button(
    "🔍 Analyze Content"
):

    if (
        not user_text
        and uploaded_image is None
        and uploaded_pdf is None
    ):

        st.warning(
            "Please provide text, image or PDF."
        )

        st.stop()

    with st.spinner(
        "Analyzing..."
    ):

        image_analysis = ""

        pdf_text = ""

        # -----------------------------
        # IMAGE ANALYSIS
        # -----------------------------

        if uploaded_image:

            image = Image.open(
                uploaded_image
            )

            image_response = (
                model.generate_content(
                    [
                        image,
                        """
Analyze this screenshot.

Extract:

1. Visible text

2. Whether it appears to be:

- Job Offer
- Internship Offer
- Scholarship Notice
- UPI Request
- Banking Message
- Lottery Message
- Other

3. Any suspicious indicators
"""
                    ]
                )
            )

            image_analysis = (
                image_response.text
            )

        # -----------------------------
        # PDF ANALYSIS
        # -----------------------------

        if uploaded_pdf:

            pdf_text = (
                extract_pdf_text(
                    uploaded_pdf
                )
            )

        # -----------------------------
        # COMBINE CONTENT
        # -----------------------------

        combined_text = f"""

USER TEXT:
{user_text}

IMAGE CONTENT:
{image_analysis}

PDF CONTENT:
{pdf_text}

"""

        # -----------------------------
        # RISK ENGINE
        # -----------------------------

        score, level, matches = (
            calculate_risk(
                combined_text
            )
        )

        # -----------------------------
        # DATABASE MATCH
        # -----------------------------

        similar_type, similarity = (
            find_similar_scam(
                combined_text
            )
        )

        # -----------------------------
        # GEMINI ANALYSIS
        # -----------------------------

        prompt = build_prompt(
            combined_text,
            score,
            level,
            matches,
            language
        )

        response = (
            model.generate_content(
                prompt
            )
        )

        analysis_result = (
            response.text
        )

        # -----------------------------
        # SAVE HISTORY
        # -----------------------------

        save_result(
            combined_text,
            score,
            level
        )

        # -----------------------------
        # GENERATE REPORT
        # -----------------------------

        report_path = (
            "reports/latest_report.pdf"
        )

        create_report(
            report_path,
            score,
            level,
            analysis_result
        )

        # -----------------------------
        # DISPLAY RESULTS
        # -----------------------------

        st.success(
            "Analysis Complete!"
        )

        st.divider()

        # -----------------------------
        # SCORE
        # -----------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.subheader(
                "📊 Risk Score"
            )

            st.progress(
                score / 100
            )

            st.metric(
                "Score",
                f"{score}/100"
            )

        with col2:

            st.subheader(
                "🚨 Risk Level"
            )

            if level == "LOW":

                st.success(level)

            elif level == "MEDIUM":

                st.warning(level)

            elif level == "HIGH":

                st.error(level)

            else:

                st.error(level)

        st.divider()

        # -----------------------------
        # RED FLAGS
        # -----------------------------

        st.subheader(
            "🚩 Detected Red Flags"
        )

        if matches:

            for flag in matches:

                st.write(
                    f"• {flag}"
                )

        else:

            st.write(
                "No obvious scam indicators found."
            )

        st.divider()

        # -----------------------------
        # DATABASE MATCH
        # -----------------------------

        st.subheader(
            "📚 Scam Knowledge Base Match"
        )

        st.write(
            f"Closest Scam Type: {similar_type}"
        )

        st.write(
            f"Similarity Score: {similarity}%"
        )

        st.divider()

        # -----------------------------
        # AI ANALYSIS
        # -----------------------------

        st.subheader(
            "🤖 AI Fraud Analysis"
        )

        st.markdown(
            analysis_result
        )

        st.divider()

        # -----------------------------
        # REPORT DOWNLOAD
        # -----------------------------

        st.subheader(
            "📄 Download Report"
        )

        with open(
            report_path,
            "rb"
        ) as report_file:

            st.download_button(
                label="Download PDF Report",
                data=report_file,
                file_name="ScamShield_Report.pdf",
                mime="application/pdf"
            )

st.metric(
    "Average Risk Score",
    get_average_risk()
)

st.divider()

st.caption(
    """
ScamShield India AI

Built using:
• Gemini AI
• Streamlit
• Fraud Knowledge Base
• Risk Scoring Engine
"""
)