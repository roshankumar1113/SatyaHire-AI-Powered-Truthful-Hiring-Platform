# SatyaHire - AI-Powered Truthful Hiring Platform

🚀 Transform your hiring with AI-powered interviews, skill verification, and fraud detection.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-14-black)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.9+-blue)](https://www.python.org/)

---

## 🌟 Features

### ✅ Live Now
- **AI Voice Interview** - Real-time voice interview with Text-to-Speech and Speech-to-Text
- **AI API Key Management** - Multi-provider support (OpenAI, Gemini, Claude) with automatic rotation
- **Authentication System** - Secure JWT-based auth with role-based access (Company/Candidate)
- **AI Resume Parser** - Extract skills from PDF/DOCX with 85% accuracy (200+ skills taxonomy)
- **Beautiful UI** - Modern gradient design with Tailwind CSS

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 14+ (optional - can use simple backend without DB)

### 1. Clone Repository
```bash
git clone https://github.com/roshankumar1113/SatyaHire-AI-Powered-Truthful-Hiring-Platform.git
cd SatyaHire-AI-Powered-Truthful-Hiring-Platform
```

### 2. Backend Setup (Simple - No Database)
```bash
cd skillproof-backend

# Install dependencies
pip install -r requirements.txt

# Start simple backend (no database required)
python -m uvicorn simple_main:app --reload
```

Backend will run on http://localhost:8000

### 3. Frontend Setup
```bash
cd skillproof-frontend

# Install dependencies
npm install

# Start frontend
npm run dev
```

Frontend will run on http://localhost:3000

### 4. One-Click Start (Windows)
```bash
# Just double-click:
START.bat
```

---

## 🔑 AI API Keys Setup (Optional)

To enable AI features (interview questions, answer analysis):

### Step 1: Get API Keys
- **OpenAI:** https://platform.openai.com/api-keys
- **Gemini:** https://makersuite.google.com/app/apikey (optional)
- **Claude:** https://console.anthropic.com/ (optional)

### Step 2: Create .env File
Create `skillproof-backend/.env`:
```bash
# AI API Keys (comma-separated for rotation)
OPENAI_API_KEYS=sk-key1,sk-key2,sk-key3
GEMINI_API_KEYS=gemini-key1,gemini-key2
ANTHROPIC_API_KEYS=claude-key1,claude-key2

# AI Configuration
DEFAULT_AI_PROVIDER=openai
AI_MODEL=gpt-3.5-turbo
AI_TEMPERATURE=0.7
AI_MAX_TOKENS=1000

# Security
SECRET_KEY=your-super-secret-key-change-in-production-min-32-characters
DEBUG=True
```

### Step 3: Install AI Packages
```bash
cd skillproof-backend
pip install openai google-generativeai anthropic
```

### Step 4: Test AI
```bash
python test_ai_client.py
```

---

## 🎯 How It Works

### For Candidates
1. Sign up at http://localhost:3000/signup
2. Redirected to AI Interview
3. Enable camera & microphone
4. AI speaks questions (Text-to-Speech)
5. Answer with voice (Speech-to-Text)
6. Get instant feedback

### For Companies
1. Sign up as Company
2. Access dashboard
3. Post job descriptions
4. Review AI-analyzed candidates
5. Make data-driven hiring decisions

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/signup` | Create account |
| POST | `/api/v1/auth/login` | Login |
| GET | `/api/v1/auth/me` | Get user info |
| POST | `/api/v1/resume/parse` | Parse resume |
| POST | `/api/v1/ai/generate-question` | Generate interview question |
| POST | `/api/v1/ai/analyze-answer` | Analyze candidate answer |
| GET | `/api/v1/ai/health` | Check AI status |

Full API docs: http://localhost:8000/api/docs

---

## 🛠️ Tech Stack

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Icons:** Lucide React
- **Voice:** Web Speech API

### Backend
- **Framework:** FastAPI
- **Language:** Python 3.9+
- **Database:** PostgreSQL (optional)
- **Auth:** JWT (python-jose)
- **Security:** Bcrypt

### AI/ML
- **Providers:** OpenAI, Gemini, Anthropic
- **NLP:** spaCy
- **ML:** scikit-learn
- **Documents:** PyPDF2, python-docx

---

## 🎤 Voice Interview Features

### Text-to-Speech (AI Voice)
- AI speaks questions naturally
- Adjustable rate, pitch, volume
- Visual "AI Speaking" indicator

### Speech-to-Text (Your Voice)
- Real-time speech recognition
- Live transcript display
- Continuous listening
- Visual "Listening..." indicator

### Browser Support
- ✅ Chrome/Edge: Full support
- ✅ Safari: Good support
- ⚠️ Firefox: Limited support

---

## 🤖 AI Key Management Features

### Round-Robin Rotation
```
Request 1 → Key 1
Request 2 → Key 2
Request 3 → Key 3
Request 4 → Key 1 (cycles back)
```

### Automatic Fallback
```
Try Key 1 → Failed
Try Key 2 → Success ✓
```

### Provider Fallback
```
Try OpenAI → Failed
Try Gemini → Success ✓
```

### Features
✅ Multiple keys per provider
✅ Thread-safe operations
✅ Automatic retry
✅ Secure (keys never logged)

---

## 📁 Project Structure

```
SatyaHire/
├── skillproof-backend/     # FastAPI backend
│   ├── app/
│   │   ├── api/v1/         # API endpoints
│   │   ├── models/         # Database models
│   │   ├── ml/             # AI/ML modules
│   │   ├── utils/          # Utilities
│   │   └── main.py         # Main app
│   ├── simple_main.py      # Simple backend (no DB)
│   └── requirements.txt
│
├── skillproof-frontend/    # Next.js frontend
│   ├── app/
│   │   ├── (auth)/         # Auth pages
│   │   ├── interview/      # AI Interview
│   │   ├── dashboard/      # Dashboard
│   │   └── page.tsx        # Landing
│   └── package.json
│
├── START.bat               # One-click start
├── README.md               # This file
└── DOCS.md                 # Complete documentation
```

---

## 🧪 Testing

### Test Authentication
```bash
# Visit signup
http://localhost:3000/signup

# Create account
Email: test@example.com
Password: password123
Role: Candidate
```

### Test AI Interview
1. Create candidate account
2. Auto-redirected to interview
3. Enable camera/microphone
4. Click "Start Interview"
5. AI speaks question
6. Answer with voice
7. See transcript in real-time

### Test API
```bash
# Health check
curl http://localhost:8000/health

# AI health check
curl http://localhost:8000/api/v1/ai/health
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.9+

# Install dependencies
cd skillproof-backend
pip install -r requirements.txt
```

### Frontend won't start
```bash
# Install dependencies
cd skillproof-frontend
npm install

# Start
npm run dev
```

### Voice not working
- Use Chrome or Edge browser
- Allow microphone permissions
- Check speakers are unmuted

### AI not working
- Add API keys to `.env` file
- Install AI packages: `pip install openai`
- Test: `python test_ai_client.py`

---

## 📊 Current Progress

| Feature | Status | Progress |
|---------|--------|----------|
| Authentication | ✅ | 100% |
| AI Voice Interview | ✅ | 100% |
| AI Key Management | ✅ | 100% |
| Resume Parser | ✅ | 100% |
| Landing Page | ✅ | 100% |
| Dashboard | 🚧 | 50% |
| Company Portal | 📋 | 0% |

**Overall: 70% Complete**

---

## 🗺️ Roadmap

### Phase 1: Core Features ✅
- [x] Authentication system
- [x] AI Voice Interview
- [x] AI Key Management
- [x] Resume parser
- [x] Landing page

### Phase 2: Advanced Features 🚧
- [ ] Resume upload UI
- [ ] Dashboard features
- [ ] Company portal
- [ ] Interview history

### Phase 3: Production 📋
- [ ] Fraud detection
- [ ] AI test generation
- [ ] Analytics dashboard
- [ ] AWS deployment

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Roshan Kumar**
- GitHub: [@roshankumar1113](https://github.com/roshankumar1113)
- Repository: [SatyaHire](https://github.com/roshankumar1113/SatyaHire-AI-Powered-Truthful-Hiring-Platform)

---

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check [DOCS.md](DOCS.md) for detailed documentation
- Review API docs at http://localhost:8000/api/docs

---

## ⭐ Star This Repository

If you find this project useful, please give it a star! ⭐

---

**Built with ❤️ in India 🇮🇳**

**SatyaHire - Truth in Hiring, Powered by AI**
