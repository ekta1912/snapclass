# 📸 SnapClass — AI-Powered Face & Voice Recognition Attendance System 🎙️✨

> ⚡ **Automating large-scale classroom attendance through multi-photo face embeddings, SVC classification, and speaker verification.**

---

## 🎯 The Core Problem & Solution 💡

* ⏳ **The Pain Point:** Calling roll manually for classrooms of 60–70+ students drains valuable lecture time and introduces human error.
* 🧠 **The SnapClass Solution:** Teachers simply snap a few classroom group photos 📷 or activate voice recognition 🗣️. The system extracts biometric embeddings, resolves duplicates across frames, and generates instant attendance records in Supabase.

---

## 🔥 Key Features at a Glance 🌟

* 🔐 **Role-Based Authentication:** Secure signup/login with dedicated Teacher & Student dashboards.
* 📸 **Multi-Photo Face Recognition:** Upload multiple row-wise classroom pictures without duplicate marking.
* 🎙️ **Voice Biometric Verification:** Backup attendance identification using voice embedding similarity matching.
* 📲 **Instant QR Enrollment:** Frictionless subject joining via dynamically generated QR codes and invite links.
* 🤖 **Smart Embeddings & SVC Engine:** Deep learning face representations classified using a Support Vector Classifier.
* 📊 **Automated Present/Absent Logs:** Real-time generation of full attendance logs saved directly to Supabase SQL.

---

## 🛠️ Technology Stack 💻

* 🐍 **Backend & Core ML:** Python 3.10+, Scikit-Learn (Support Vector Classifier / SVC)
* 👁️ **Computer Vision:** `dlib`, `face_recognition_models`, Deep Metric Face Embedding Pipeline
* 🎧 **Audio Processing:** `resemblyzer`, `librosa`, Speaker Embedding & Voice Similarity Matching
* 🗄️ **Database:** Supabase (PostgreSQL)
* 🎨 **Application Frontend:** Streamlit

---

## 🚀 Getting Started Locally

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/snapclass.git
cd snapclass
```

### 2. Set Up Virtual Environment (`venv`)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Supabase Database
1. Create a project at [supabase.com](https://supabase.com).
2. Go to **SQL Editor** in your Supabase dashboard.
3. Open [`supabase_schema.sql`](supabase_schema.sql), paste the SQL commands, and click **Run**.

### 5. Configure `.streamlit/secrets.toml`
Create or edit `.streamlit/secrets.toml` in the project root:
```toml
SUPABASE_URL = "https://your-project-id.supabase.co"
SUPABASE_KEY = "your-supabase-anon-or-service-role-key"

# Optional: URL of your deployed app for QR code invite links
APP_URL = "https://your-app.streamlit.app"
```
*(You can find your API URL and keys in Supabase under **Project Settings ➡️ API**)*

### 6. Run the Application
```bash
streamlit run app.py
```

---

## ☁️ Deploying to Streamlit Community Cloud

1. **Push to GitHub**:
   ```bash
   git add .
   git commit -m "Configure SnapClass for Streamlit Cloud deployment"
   git push origin main
   ```
   *(Note: `.streamlit/secrets.toml` and `venv/` are safely ignored by `.gitignore`)*

2. **Deploy on Streamlit Community Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io/) and log in with GitHub.
   - Click **New app**.
   - Select your repository: `snapclass` and branch: `main`.
   - Set **Main file path**: `app.py`.
   - Click **Advanced Settings** -> choose **Python 3.11** or **Python 3.12**.

3. **Configure Secrets on Streamlit Cloud**:
   - In the **Secrets** section (or via **App Settings ➡️ Secrets**), paste:
     ```toml
     SUPABASE_URL = "https://your-project-id.supabase.co"
     SUPABASE_KEY = "your-supabase-anon-or-service-role-key"
     APP_URL = "https://your-app-name.streamlit.app"
     ```
   - Click **Deploy**!

---

## 📁 Project Structure

```
snapclass/
│
├── app.py                         # Streamlit application entrypoint
├── packages.txt                   # Linux system packages for Streamlit Cloud
├── requirements.txt               # Python package dependencies
├── supabase_schema.sql            # Supabase database schema & indexes
├── .gitignore                     # Git ignore rules (secrets & venv protected)
│
├── .streamlit/
│   ├── config.toml                # Streamlit server & theme configuration
│   ├── secrets.toml               # Local secrets (ignored by git)
│   └── secrets.toml.example       # Template secrets for contributors
│
└── src/
    ├── components/                # UI modal dialogs & cards
    │   ├── dialog_add_photo.py
    │   ├── dialog_attendance_results.py
    │   ├── dialog_auto_enroll.py
    │   ├── dialog_create_subject.py
    │   ├── dialog_enroll.py
    │   ├── dialog_share_subject.py
    │   ├── dialog_voice_attendance.py
    │   ├── footer.py
    │   ├── header.py
    │   └── subject_card.py
    │
    ├── database/                  # Supabase connection & DB operations
    │   ├── config.py
    │   └── db.py
    │
    ├── pipelines/                 # AI / ML recognition engines
    │   ├── face_pipeline.py       # Face detection & SVC classification
    │   └── voice_pipeline.py      # Resemblyzer voice embedding extraction
    │
    ├── screens/                   # Page layouts & user flows
    │   ├── home_screen.py
    │   ├── student_screen.py
    │   └── teacher_screen.py
    │
    └── ui/
        └── base_layout.py         # Global CSS styles & typography
```

---

## 👩‍💻 Author

Created with ❤️ by **Ekta Singh - IET Lucknow**