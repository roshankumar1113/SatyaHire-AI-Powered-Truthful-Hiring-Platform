# AI Interview Platform - Production Architecture

## 1. System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         Load Balancer (Nginx)                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                      API Gateway (Go)                            │
│  - Rate Limiting                                                 │
│  - JWT Validation                                                │
│  - Request Routing                                               │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Interview  │    │   Emotion    │    │   Scoring    │
│   Service    │    │   Service    │    │   Service    │
│   (Go)       │    │   (Python)   │    │   (Go)       │
└──────────────┘    └──────────────┘    └──────────────┘
        │                     │                     │
        └─────────────────────┼─────────────────────┘
                              ▼
        ┌─────────────────────────────────────────┐
        │         Message Queue (RabbitMQ)        │
        │  - Emotion Analysis Queue               │
        │  - Scoring Queue                        │
        │  - Notification Queue                   │
        └─────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│  PostgreSQL  │    │    Redis     │    │   S3/Minio   │
│  (Primary)   │    │  (Cache)     │    │  (Storage)   │
└──────────────┘    └──────────────┘    └──────────────┘
        │
        ▼
┌──────────────┐
│  PostgreSQL  │
│  (Replica)   │
└──────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                    WebSocket Server (Go)                         │
│  - Real-time emotion updates                                     │
│  - Interview status updates                                      │
│  - Connection pooling                                            │
└─────────────────────────────────────────────────────────────────┘
```

## 2. Service Breakdown

### 2.1 Interview Service (Go)
**Responsibilities:**
- Interview session management
- Question delivery
- Answer recording
- Video frame capture
- Authentication & Authorization

**Tech Stack:**
- Go 1.21+
- Gin/Fiber framework
- GORM (ORM)
- JWT-Go
- WebSocket (gorilla/websocket)

### 2.2 Emotion Detection Service (Python)
**Responsibilities:**
- Face detection (HOG/MTCNN)
- Blink detection
- Emotion classification (XCeption)
- Feature extraction
- Model inference

**Tech Stack:**
- Python 3.11+
- FastAPI
- OpenCV
- TensorFlow/PyTorch
- dlib
- NumPy

### 2.3 Scoring Service (Go)
**Responsibilities:**
- Answer analysis
- Emotion scoring
- Behavioral scoring
- Final score calculation
- Report generation

**Tech Stack:**
- Go 1.21+
- OpenAI/Anthropic API
- Custom scoring algorithms

### 2.4 Background Workers (Go)
**Responsibilities:**
- Video processing
- Batch emotion analysis
- Report generation
- Email notifications
- Data cleanup

## 3. Data Flow

### Interview Flow
```
1. Client → API Gateway → Interview Service
   - Start interview session
   - Get JWT token
   - Establish WebSocket connection

2. Client → WebSocket → Interview Service
   - Stream video frames (every 500ms)
   - Send answers

3. Interview Service → Message Queue → Emotion Service
   - Queue video frames for analysis
   - Async processing

4. Emotion Service → Redis → WebSocket → Client
   - Cache emotion results
   - Push real-time updates

5. Interview Service → Scoring Service
   - Calculate final scores
   - Generate reports
```

## 4. Database Schema

### PostgreSQL Tables

```sql
-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Interview Sessions
CREATE TABLE interview_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP NOT NULL,
    completed_at TIMESTAMP,
    total_duration INTEGER,
    video_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Questions
CREATE TABLE questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    text TEXT NOT NULL,
    category VARCHAR(100),
    difficulty VARCHAR(50),
    expected_duration INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Answers
CREATE TABLE answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES interview_sessions(id),
    question_id UUID REFERENCES questions(id),
    transcript TEXT,
    audio_url TEXT,
    duration FLOAT,
    confidence FLOAT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Emotion Analysis
CREATE TABLE emotion_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES interview_sessions(id),
    timestamp TIMESTAMP NOT NULL,
    emotion VARCHAR(50),
    confidence FLOAT,
    blink_count INTEGER,
    face_detected BOOLEAN,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Scores
CREATE TABLE scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID REFERENCES interview_sessions(id),
    technical_score FLOAT,
    communication_score FLOAT,
    emotion_score FLOAT,
    overall_score FLOAT,
    feedback TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- API Keys (for rotation)
CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    provider VARCHAR(50) NOT NULL,
    key_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    usage_count INTEGER DEFAULT 0,
    last_used_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_sessions_user ON interview_sessions(user_id);
CREATE INDEX idx_sessions_status ON interview_sessions(status);
CREATE INDEX idx_answers_session ON answers(session_id);
CREATE INDEX idx_emotion_session ON emotion_analysis(session_id);
CREATE INDEX idx_emotion_timestamp ON emotion_analysis(timestamp);
```

## 5. Redis Cache Strategy

```
# Session Cache (TTL: 2 hours)
session:{session_id} → {session_data}

# Emotion Cache (TTL: 1 hour)
emotion:{session_id}:{timestamp} → {emotion_data}

# User Cache (TTL: 30 minutes)
user:{user_id} → {user_data}

# Rate Limiting (TTL: 1 minute)
ratelimit:{user_id}:{endpoint} → {count}

# WebSocket Connections
ws:connections → Set of active connection IDs

# API Key Rotation (TTL: 5 minutes)
apikey:{provider}:current → {key_id}
```

## 6. Message Queue Design

### RabbitMQ Exchanges & Queues

```
Exchange: interview.events (topic)
├── Queue: emotion.analysis
│   └── Routing Key: interview.frame.captured
├── Queue: scoring.process
│   └── Routing Key: interview.completed
├── Queue: notification.email
│   └── Routing Key: interview.scored
└── Queue: video.processing
    └── Routing Key: interview.video.uploaded
```

## 7. Security Measures

1. **JWT Authentication**
   - Access token: 15 min expiry
   - Refresh token: 7 days expiry
   - Token rotation on refresh

2. **API Key Rotation**
   - Round-robin selection
   - Automatic failover
   - Usage tracking
   - Rate limiting per key

3. **Data Encryption**
   - TLS 1.3 for all communications
   - AES-256 for data at rest
   - Encrypted video storage

4. **Rate Limiting**
   - Per user: 100 req/min
   - Per IP: 1000 req/min
   - WebSocket: 10 frames/sec

## 8. Scalability Strategy

### Horizontal Scaling
- Interview Service: 3-10 instances
- Emotion Service: 2-5 instances (GPU)
- Scoring Service: 2-5 instances
- Workers: 5-20 instances

### Vertical Scaling
- Emotion Service: GPU instances (NVIDIA T4/V100)
- Database: 16-32 GB RAM
- Redis: 8-16 GB RAM

### Auto-scaling Rules
```yaml
Interview Service:
  min: 3
  max: 10
  cpu_threshold: 70%
  
Emotion Service:
  min: 2
  max: 5
  queue_depth: 100
  
Workers:
  min: 5
  max: 20
  queue_depth: 500
```

## 9. Monitoring & Observability

### Metrics (Prometheus)
- Request latency (p50, p95, p99)
- Error rates
- Queue depth
- WebSocket connections
- GPU utilization
- Database connections

### Logging (ELK Stack)
- Structured JSON logs
- Request tracing
- Error tracking
- Audit logs

### Tracing (Jaeger)
- Distributed tracing
- Service dependencies
- Performance bottlenecks

## 10. Disaster Recovery

### Backup Strategy
- PostgreSQL: Daily full + hourly incremental
- Redis: RDB snapshots every 5 minutes
- S3: Cross-region replication

### Recovery Time Objectives
- RTO: 15 minutes
- RPO: 5 minutes

### High Availability
- Multi-AZ deployment
- Database replication (master-slave)
- Redis Sentinel for failover
- Load balancer health checks
