<div align="center">
  <h1>🚀 HackConnect-AI</h1>
  <p><em>An intelligent, AI-powered hackathon community platform to build, share, and collaborate.</em></p>

  ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
  ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
  ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
</div>

---

## 📖 Description
**HackConnect-AI** is a comprehensive, production-ready hackathon platform engineered to seamlessly connect developers. Built with Flask, vanilla JavaScript, and customized glassmorphic CSS, the platform intrinsically manages community messaging, team orchestration, and secure project submissions. Featuring a fully integrated **Generative AI Assistant** (powered by Google's Gemini LLM), users can dynamically brainstorm architectures, validate their development roadmaps, and instantly receive highly technical deployment advice directly inside the browser.

---

## ✨ Features

- **🔐 User Authentication:** Secure password hashing (Werkzeug) and active session management.
- **🤝 Team Creation & Joining:** Seamlessly orchestrate developer groups restricted natively by database integrity constraints to avoid duplicates.
- **📁 Project Submission:** Secure ZIP and PDF file routing natively linked to instantiated teams.
- **💬 Community Chat System:** A global chronological messaging interface bridging the entire platform.
- **📢 Administrator Announcements:** Verified admins can securely deploy synchronized platform news straight to user dashboards.
- **🤖 AI Assistant:** Embedded LLM generative chat for rapid hackathon brainstorming and agile sprint planning.

---

## 🛠️ Tech Stack

- **Frontend:** HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Backend:** Python (Flask)
- **Database:** SQLite3
- **AI Integrations:** `google-generativeai` (Gemini 1.5 Flash)

---

## 📸 Screenshots

> [!NOTE]
> *Placeholder for future platform screenshots.*
> ![Dashboard Image](#) | ![Chat Interface](#)

---

## ⚙️ Installation

To run **HackConnect-AI** down on your local machine locally, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/HackConnect-AI.git
   cd "HackConnect-AI"
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Configure the AI API Hook!**
   > [!IMPORTANT]
   > Ensure you explicitly export your Gemini keys to securely unlock the Hackathon AI Assistant interface.
   
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

4. **Launch the application:**
   ```bash
   python app.py
   ```
   > [!TIP]  
   > The local development SQLite database will safely auto-initialize if it is not found natively on your system! 

---

## 🚀 Deployment

This application has been meticulously structurally optimized to be deployed identically on **Railway** (or any other containerized PaaS):

1. Link your GitHub repository directly over to a new Railway project.
2. Add your `GEMINI_API_KEY` specifically into your Railway project's **Environment Variables** tabs.
3. Railway explicitly detects the `requirements.txt` build definitions and binds your internal Flask execution loop over `0.0.0.0:$PORT` avoiding all cloud port conflicts. No manual configuration necessary!

---

## 🔒 Security Architecture

> [!CAUTION]
> **Extremely Important:** Never ever hardcode keys into your git repository! The AI framework is designed to detect your `GEMINI_API_KEY` through your active environment variables uniquely. Create a hidden `.env` file parallel to `.env.example` to boot the application securely.

---

## 🔮 Future Improvements

> [!WARNING]
> While extremely capable, the backend architecture is mapped against an aggressive scaling trajectory!

- [ ] **Real-time chat (WebSockets):** Upgrade from API polling directly to `Flask-SocketIO` to minimize message latency.
- [ ] **Cloud file storage:** Hook the core `uploads/` directory directly into an AWS S3 Bucket or Firebase storage pipeline.
- [ ] **Advanced AI features:** Enable the Assistant to actively scan uploaded source code or PDF design drafts locally for structural reviews.

<div align="center">
  <p>Built with ❤️ by Hackathon Developers.</p>
</div>
