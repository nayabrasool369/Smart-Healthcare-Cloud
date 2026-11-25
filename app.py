import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from fpdf import FPDF
import datetime

SUPABASE_URL = "https://rocrquouidbtkrnfzjsp.supabase.co"
SUPABASE_KEY = "sb_publishable_IiYOEU8ScJOXnF_HuGgYew_E5WbhaP7"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

st.set_page_config(page_title="Smart Healthcare Cloud", page_icon="🏥", layout="wide")

st.markdown("""
<style>
    .hero-banner {
        background: linear-gradient(135deg, #008080 0%, #0066CC 50%, #4A00E0 100%);
        padding: 25px 30px;
        border-radius: 15px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 8px 20px rgba(0, 102, 204, 0.25);
    }
    .hero-banner h1 { margin: 0; font-size: 2.1rem; font-weight: 700; color: #FFFFFF; }
    .hero-banner p { margin: 8px 0 0 0; font-size: 1.05rem; color: #E0F7FA; }
    .kpi-card {
        padding: 20px;
        border-radius: 14px;
        color: white;
        text-align: center;
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
        margin-bottom: 10px;
    }
    .kpi-blue { background: linear-gradient(135deg, #2193b0, #6dd5ed); }
    .kpi-purple { background: linear-gradient(135deg, #8E2DE2, #4A00E0); }
    .kpi-green { background: linear-gradient(135deg, #11998e, #38ef7d); }
    .kpi-orange { background: linear-gradient(135deg, #FF512F, #F09819); }
    .kpi-card h3 { margin: 0; font-size: 1rem; font-weight: 500; opacity: 0.95; }
    .kpi-card h2 { margin: 8px 0 0 0; font-size: 2rem; font-weight: 700; }
    .stButton>button {
        background: linear-gradient(90deg, #008080, #0066CC);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.2rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-banner">
    <h1>🏥 Smart Healthcare Data Management Using Cloud Computing</h1>
    <p>☁️ Real-Time Cloud Storage • 📊 Intelligent Medical Analytics • 📄 Automated PDF Reporting</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🩺 Navigation Panel")
st.sidebar.success("🟢 Cloud Status: Connected")
menu = st.sidebar.radio(
    "Choose Module:",
    (
        "📋 Patient Registration & Upload",
        "☁️ Cloud Patient Database",
        "📊 Analytics & PDF Reports"
    )
)
st.sidebar.divider()
st.sidebar.info("💡 **Capstone Project**\nPowered by Python, Streamlit & Supabase Cloud.")

if menu == "📋 Patient Registration & Upload":
    st.subheader("➕ Register New Patient & Upload Medical Scan to Cloud")

    with st.form("patient_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            patient_id = st.text_input("🆔 Patient ID (e.g., PID-104)*")
            full_name = st.text_input("👤 Full Name*")
            age = st.number_input("🎂 Age*", min_value=0, max_value=120, step=1)
            gender = st.selectbox("⚧ Gender*", ("Male", "Female", "Other"))
        with col2:
            blood_group = st.selectbox("🩸 Blood Group", ("A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"))
            contact = st.text_input("📞 Contact Number")
            diagnosis = st.text_input("🩺 Diagnosis / Condition (e.g., Fever, Diabetes)*")
            doctor_name = st.text_input("👨‍⚕️ Assigned Doctor")

        uploaded_file = st.file_uploader("📎 Upload Lab Report / X-Ray / Prescription (PDF, PNG, JPG)", type=("pdf", "png", "jpg", "jpeg"))
        submitted = st.form_submit_button("🚀 Save Patient & Upload to Cloud")

        if submitted:
            if not patient_id or not full_name or not diagnosis:
                st.error("⚠️ Please fill all mandatory fields marked with *")
            else:
                report_url = None
                try:
                    if uploaded_file is not None:
                        file_bytes = uploaded_file.read()
                        clean_name = uploaded_file.name.replace(" ", "_")
                        file_path = f"{patient_id}_{clean_name}"
                        upload_endpoint = f"{SUPABASE_URL}/storage/v1/object/medical-reports/{file_path}"
                        file_headers = {
                            "apikey": SUPABASE_KEY,
                            "Authorization": f"Bearer {SUPABASE_KEY}",
                            "Content-Type": uploaded_file.type,
                            "x-upsert": "true"
                        }
                        up_res = requests.post(upload_endpoint, headers=file_headers, data=file_bytes)
                        if up_res.status_code in (200, 201):
                            report_url = f"{SUPABASE_URL}/storage/v1/object/public/medical-reports/{file_path}"

                    data = {
                        "patient_id": patient_id,
                        "full_name": full_name,
                        "age": age,
                        "gender": gender,
                        "blood_group": blood_group,
                        "contact": contact,
                        "diagnosis": diagnosis.strip().title(),
                        "doctor_name": doctor_name,
                        "report_url": report_url
                    }
                    db_res = requests.post(f"{SUPABASE_URL}/rest/v1/patients", headers=HEADERS, json=data)
                    if db_res.status_code in (200, 201):
                        st.balloons()
                        st.success(f"🎉 Patient **{full_name}** registered & synced to Cloud successfully!")
                    else:
                        st.error(f"Database Error: {db_res.text}")
                except Exception as e:
                    st.error(f"Error saving data: {e}")

elif menu == "☁️ Cloud Patient Database":
    st.subheader("🗂️ Live Cloud Patient Records")
    try:
        res = requests.get(f"{SUPABASE_URL}/rest/v1/patients?select=*&order=created_at.desc", headers=HEADERS)
        records = res.json() if res.status_code == 200 else []
        if records:
            df = pd.DataFrame(records)
            search = st.text_input("🔍 Search Patient by Name, ID, or Diagnosis:")
            if search:
                df = df[df["full_name"].str.contains(search, case=False, na=False) |
                        df["patient_id"].str.contains(search, case=False, na=False) |
                        df["diagnosis"].str.contains(search, case=False, na=False)]
            
            cols = ["patient_id", "full_name", "age", "gender", "blood_group", "diagnosis", "doctor_name"]
            st.dataframe(df[cols], use_container_width=True)

            st.markdown("### 📂 Attached Cloud Medical Reports")
            found_files = False
            for row in records:
                if row.get("report_url"):
                    found_files = True
                    clean_url = row["report_url"].replace(" ", "%20")
                    col_a, col_b = st.columns((3, 1))
                    with col_a:
                        st.info(f"📄 **{row['patient_id']} — {row['full_name']}** ({row['diagnosis']})")
                    with col_b:
                        st.link_button("⬇️ Open / Download Report", clean_url)
            if not found_files:
                st.caption("No scanned files attached yet.")
        else:
            st.info("No patient records found in the cloud yet.")
    except Exception as e:
        st.error(f"Error fetching records: {e}")

elif menu == "📊 Analytics & PDF Reports":
    st.subheader("📈 Real-Time Healthcare Analytics Dashboard")
    try:
        res = requests.get(f"{SUPABASE_URL}/rest/v1/patients?select=*", headers=HEADERS)
        records = res.json() if res.status_code == 200 else []

        if not records:
            st.warning("Add at least 1-2 patients first to view analytics.")
        else:
            df = pd.DataFrame(records)
            df["diagnosis"] = df["diagnosis"].str.strip().str.title()
            files_count = df["report_url"].notna().sum()

            k1, k2, k3, k4 = st.columns(4)
            with k1:
                st.markdown(f'<div class="kpi-card kpi-blue"><h3>Total Patients</h3><h2>{len(df)}</h2></div>', unsafe_allow_html=True)
            with k2:
                st.markdown(f'<div class="kpi-card kpi-purple"><h3>Average Age</h3><h2>{df["age"].mean():.1f} yrs</h2></div>', unsafe_allow_html=True)
            with k3:
                st.markdown(f'<div class="kpi-card kpi-green"><h3>Conditions Tracked</h3><h2>{df["diagnosis"].nunique()}</h2></div>', unsafe_allow_html=True)
            with k4:
                st.markdown(f'<div class="kpi-card kpi-orange"><h3>Cloud Reports</h3><h2>{files_count}</h2></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### 🩺 Cases by Diagnosis")
                diag_df = df["diagnosis"].value_counts().reset_index()
                fig_diag = px.bar(diag_df, x="diagnosis", y="count", color="diagnosis", color_discrete_sequence=px.colors.qualitative.Bold)
                fig_diag.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_diag, use_container_width=True)

            with c2:
                st.markdown("#### ⚧ Gender Distribution")
                fig_gen = px.pie(df, names="gender", hole=0.45, color_discrete_sequence=px.colors.qualitative.Vivid)
                fig_gen.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig_gen, use_container_width=True)

            st.divider()

            st.subheader("🖨️ Official Patient Medical Summary PDF Generator")
            selected_pid = st.selectbox("Select Patient ID:", df["patient_id"].tolist())
            patient_row = next(iter(df[df["patient_id"] == selected_pid].to_dict(orient="records")))
            if st.button("✨ Generate Official PDF Report"):
                pdf = FPDF()
                pdf.add_page()
                pdf.set_fill_color(0, 128, 128)
                pdf.set_text_color(255, 255, 255)
                pdf.set_font("Arial", "B", 15)
                pdf.cell(0, 14, "SMART HEALTHCARE CLOUD - MEDICAL SUMMARY REPORT", ln=True, align="C", fill=True)
                pdf.ln(8)

                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Arial", "", 12)
                fields = (
                    ("Report Date", str(datetime.date.today())),
                    ("Patient ID", str(patient_row["patient_id"])),
                    ("Full Name", str(patient_row["full_name"])),
                    ("Age / Gender", f"{patient_row['age']} / {patient_row['gender']}"),
                    ("Blood Group", str(patient_row["blood_group"])),
                    ("Contact", str(patient_row["contact"])),
                    ("Diagnosis", str(patient_row["diagnosis"])),
                    ("Consulting Doctor", str(patient_row["doctor_name"])),
                    ("Cloud Report URL", str(patient_row["report_url"] or "No file attached"))
                )
                for label, val in fields:
                    pdf.set_font("Arial", "B", 11)
                    pdf.cell(55, 10, f"{label}:", border=1)
                    pdf.set_font("Arial", "", 11)
                    pdf.cell(0, 10, f" {val}", border=1, ln=True)

                pdf_bytes = pdf.output(dest="S").encode("latin-1")
                st.download_button(
                    label="⬇️ Download Colorful Medical PDF",
                    data=pdf_bytes,
                    file_name=f"{selected_pid}_Medical_Report.pdf",
                    mime="application/pdf"
                )
    except Exception as e:
        st.error(f"Error loading analytics: {e}")
