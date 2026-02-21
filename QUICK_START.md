# 🚀 SatyaHire - Quick Start Guide

## ⚡ 5-Minute Setup

### Step 1: Start Everything
```bash
# Windows
START_PRODUCTION.bat

# Linux/Mac
docker-compose up -d
```

### Step 2: Access Services
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

### Step 3: Test Multilingual System
```bash
# Windows
TEST_MULTILINGUAL.bat

# Linux/Mac
curl http://localhost:8000/api/v1/multilingual/health
```

---

## 🌍 Multilingual Interview (NEW!)

### Supported Languages
✅ English | ✅ Hindi (हिंदी) | ✅ Tamil (தமிழ்) | ✅ Telugu (తెలుగు)  
✅ Kannada (ಕನ್ನಡ) | ✅ Malayalam (മലയാളം) | ✅ Marathi (मराठी)  
✅ Gujarati (ગુજરાતી) | ✅ Bengali (বাংলা) | ✅ Punjabi (ਪੰਜਾਬੀ) | ✅ Urdu (اردو)

### Start Interview in Hindi
```bash
curl -X POST http://localhost:8000/api/v1/multilingual/start \
  -H "Content-Type: application/json" \
  -d '{
    "role": "Python Developer",
    "experience_level": "mid",
    "language": "hindi",
    "max_questions": 5
  }'
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "question": "क्या आप अपना परिचय दे सकते हैं?",
    "difficulty": "easy",
    "interview_status": "IN_PROGRESS",
    "question_number": 1,
    "language": "hindi"
  }
}
```

---

## 📚 Complete Documentation

### Core Docs
- **[README.md](README.md)** - Project overview
- **[Architecture](docs/ARCHITECTURE.md)** - System design
- **[Multilingual Guide](docs/MULTILINGUAL_GUIDE.md)** - Language support
- **[Deployment](docs/DEPLOYMENT.md)** - Production deployment
- **[Implementation](docs/IMPLEMENTATION_GUIDE.md)** - Complete guide

### API Endpoints

#### Authentication
```bash
POST /api/v1/auth/signup
POST /api/v1/auth/login
GET  /api/v1/auth/me
```

#### Multilingual Interview
```bash
GET  /api/v1/multilingual/languages
POST /api/v1/multilingual/start
POST /api/v1/multilingual/submit-answer
GET  /api/v1/multilingual/experience-levels
GET  /api/v1/multilingual/health
```

#### Interview Management
```bash
POST /api/v1/interview/start
GET  /api/v1/interview/session/:id
POST /api/v1/interview/submit-answer
GET  /api/v1/interview/progress/:id
```

#### Voice & Audio
```bash
POST /api/v1/voice/text-to-speech
POST /api/v1/voice/speech-to-text
GET  /api/v1/voice/supported-voices
```

---

## 🎯 Key Features

### ✅ Production-Ready
- Docker containerization
- PostgreSQL database
- Redis caching
- RabbitMQ message queue
- Minio object storage

### ✅ AI-Powered
- Multi-provider support (OpenAI, Gemini, Claude)
- Automatic API key rotation
- Intelligent question generation
- Real-time answer evaluation

### ✅ Multilingual
- 11 Indian languages
- Native language interviews
- Culturally appropriate questions
- Accurate evaluation in any language

### ✅ Voice Integration
- Text-to-Speech (TTS)
- Speech-to-Text (STT)
- Real-time transcription
- Multi-language voice support

---

## 🛠️ Development Commands

### Using Makefile
```bash
make dev-up          # Start all services
make dev-down        # Stop all services
make test            # Run tests
make lint            # Run linters
make logs            # View logs
```

### Using Docker Compose
```bash
docker-compose up -d              # Start services
docker-compose down               # Stop services
docker-compose logs -f            # View logs
docker-compose ps                 # Check status
docker-compose restart backend    # Restart backend
```

---

## 🧪 Testing

### Test All Services
```bash
# Backend health
curl http://localhost:8000/health

# Interview service
curl http://localhost:8000/api/v1/interview/health

# Multilingual service
curl http://localhost:8000/api/v1/multilingual/health

# Voice service
curl http://localhost:8000/api/v1/voice/voice-test
```

### Test Multilingual Interview
```bash
# Get supported languages
curl http://localhost:8000/api/v1/multilingual/languages

# Start English interview
curl -X POST http://localhost:8000/api/v1/multilingual/start \
  -d '{"role":"Developer","experience_level":"mid","language":"english","max_questions":5}'

# Start Hindi interview
curl -X POST http://localhost:8000/api/v1/multilingual/start \
  -d '{"role":"Developer","experience_level":"mid","language":"hindi","max_questions":5}'
```

---

## 🔧 Configuration

### Environment Variables (.env)
```env
# Database
DB_PASSWORD=your_secure_password

# JWT
JWT_SECRET=your-secret-key-min-32-chars

# AI API Keys (comma-separated for rotation)
OPENAI_API_KEYS=sk-key1,sk-key2
GEMINI_API_KEYS=gemini-key1
ANTHROPIC_API_KEYS=claude-key1

# Default AI Provider
DEFAULT_AI_PROVIDER=openai
```

---

## 📊 Architecture

```
┌─────────────┐
│   Client    │
│  (Browser)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Nginx     │
│Load Balancer│
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│       Backend (FastAPI)         │
│  - Authentication               │
│  - Multilingual Interview       │
│  - Voice Processing             │
│  - AI Integration               │
└────────┬────────────────────────┘
         │
    ┌────┴────┬────────┬──────────┐
    ▼         ▼        ▼          ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│Postgres│ │ Redis  │ │RabbitMQ│ │ Minio  │
└────────┘ └────────┘ └────────┘ └────────┘
```

---

## 🚀 Production Deployment

### Docker Compose (Recommended)
```bash
# Start production stack
docker-compose up -d

# Scale services
docker-compose up -d --scale backend=3

# View logs
docker-compose logs -f backend
```

### Kubernetes
```bash
# Apply manifests
kubectl apply -f infrastructure/kubernetes/

# Check status
kubectl get pods -n ai-interview

# Scale deployment
kubectl scale deployment backend --replicas=5 -n ai-interview
```

---

## 💡 Pro Tips

### 1. Use AI API Keys
Add your OpenAI/Gemini/Claude API keys to `.env` for real AI-powered interviews.

### 2. Enable Voice Features
The system supports browser-based voice recognition and synthesis in all 11 languages.

### 3. Monitor Performance
Access Prometheus metrics at http://localhost:9090 (if enabled).

### 4. Scale Horizontally
Add more backend containers: `docker-compose up -d --scale backend=3`

### 5. Use Redis Caching
Redis is pre-configured for session management and caching.

---

## 🐛 Troubleshooting

### Services Won't Start
```bash
# Check Docker
docker ps

# View logs
docker-compose logs

# Restart
docker-compose restart
```

### Port Already in Use
```bash
# Windows - Kill process
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Database Issues
```bash
# Reset database
docker-compose down -v
docker-compose up -d
```

---

## 📞 Support

### Documentation
- Full docs in `/docs` folder
- API docs: http://localhost:8000/api/docs
- GitHub: https://github.com/roshankumar1113/SatyaHire

### Contact
- Issues: GitHub Issues
- Email: support@satyahire.com

---

## ⭐ What's New

### v2.0.0 - Multilingual Support
- ✅ 11 Indian languages supported
- ✅ AI-powered multilingual interviews
- ✅ Native language evaluation
- ✅ Voice integration for all languages
- ✅ Production-ready architecture
- ✅ Complete documentation

---

**🇮🇳 Built with ❤️ for India**

**Making AI Interviews Accessible in Every Indian Language**
