# 🏥 Smart Healthcare Data Management Using Cloud Computing

🌐 **Live Deployed Application:** [https://streamlit.app](https://streamlit.app)

## 📌 Project Overview
**Smart Healthcare Data Management Using Cloud Computing** is a cloud-enabled web application designed to digitize, store, analyze, and manage patient medical records securely in real time. By leveraging cloud database and object storage services, healthcare providers can eliminate paper-based record loss, access patient histories anytime, visualize disease trends, and generate official medical summary reports instantly.

---

## 🧩 Key Modules

### 1. Patient Data Management and Cloud Storage
* **Patient Registration:** Captures essential patient details (Patient ID, Name, Age, Gender, Blood Group, Contact, Diagnosis, and Assigned Doctor).
* **Cloud Database Sync:** Stores structured patient records in a cloud-hosted **PostgreSQL database** via REST API.
* **Cloud Medical File Storage:** Uploads lab reports, X-rays, and prescriptions (PDF, PNG, JPG) directly to a **Cloud Storage Bucket** and links public retrieval URLs to the patient record.

### 2. Cloud Patient Records & Retrieval
* **Real-Time Search & Filter:** Instantly searches cloud records by Patient Name, Patient ID, or Diagnosis.
* **Direct Cloud File Access:** Provides one-click view/download access for attached medical scans and documents stored in the cloud.

### 3. Healthcare Data Analytics and Report Generation
* **Live KPI Metrics:** Displays total cloud patients, average patient age, unique medical conditions tracked, and total uploaded cloud reports.
* **Interactive Visualizations:** Generates dynamic bar charts (Cases by Diagnosis) and donut charts (Gender Distribution) using Plotly.
* **Automated PDF Report Generation:** Creates and downloads a formatted, official **Patient Medical Summary PDF Report** in one click.

---

## 🛠️ Complete Software & Technology Stack

| Category | Software / Tool | Purpose in Project |
| :--- | :--- | :--- |
| **Programming Language** | Python 3 | Core application logic, API requests, and data processing |
| **Web Framework & UI** | Streamlit + Custom HTML/CSS | Responsive frontend dashboard, forms, and interactive UI |
| **Cloud Database (DBaaS)** | Supabase (PostgreSQL) | Cloud-hosted relational database for patient records |
| **Cloud Object Storage** | Supabase Storage Bucket | Secure cloud storage for medical scans and PDF reports |
| **Cloud Hosting Platform** | Streamlit Community Cloud | Continuous deployment and public web hosting |
| **API Communication** | REST API (`requests`) | Secure HTTP communication between app and cloud backend |
| **Data Analytics & Charts** | Pandas & Plotly Express | Data aggregation and interactive visual analytics |
| **PDF Generation** | FPDF | Automated generation of downloadable medical summary PDFs |
| **IDE / Code Editor** | Visual Studio Code (VS Code) | Development, testing, and debugging environment |
| **Version Control** | Git & GitHub | Source code management, version control, and repository hosting |

---

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nayabrasool369/Smart-Healthcare-Cloud.git
   cd Smart-Healthcare-Cloud
   ```

2. **Install required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python -m streamlit run app.py
   ```
