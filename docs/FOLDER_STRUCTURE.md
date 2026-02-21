# Production Folder Structure

```
ai-interview-platform/
│
├── services/
│   │
│   ├── interview-service/              # Go - Main Interview Service
│   │   ├── cmd/
│   │   │   └── server/
│   │   │       └── main.go
│   │   ├── internal/
│   │   │   ├── domain/                 # Business entities
│   │   │   │   ├── interview.go
│   │   │   │   ├── question.go
│   │   │   │   ├── answer.go
│   │   │   │   └── user.go
│   │   │   ├── repository/             # Data access layer
│   │   │   │   ├── postgres/
│   │   │   │   │   ├── interview_repo.go
│   │   │   │   │   ├── question_repo.go
│   │   │   │   │   └── user_repo.go
│   │   │   │   └── redis/
│   │   │   │       ├── cache.go
│   │   │   │       └── session_cache.go
│   │   │   ├── usecase/                # Business logic
│   │   │   │   ├── interview_usecase.go
│   │   │   │   ├── question_usecase.go
│   │   │   │   └── auth_usecase.go
│   │   │   ├── delivery/               # API handlers
│   │   │   │   ├── http/
│   │   │   │   │   ├── handler.go
│   │   │   │   │   ├── interview_handler.go
│   │   │   │   │   ├── auth_handler.go
│   │   │   │   │   └── middleware.go
│   │   │   │   └── websocket/
│   │   │   │       ├── hub.go
│   │   │   │       ├── client.go
│   │   │   │       └── handler.go
│   │   │   ├── infrastructure/         # External services
│   │   │   │   ├── queue/
│   │   │   │   │   └── rabbitmq.go
│   │   │   │   ├── storage/
│   │   │   │   │   └── s3.go
│   │   │   │   └── grpc/
│   │   │   │       └── emotion_client.go
│   │   │   └── config/
│   │   │       └── config.go
│   │   ├── pkg/                        # Shared packages
│   │   │   ├── jwt/
│   │   │   │   └── jwt.go
│   │   │   ├── logger/
│   │   │   │   └── logger.go
│   │   │   ├── validator/
│   │   │   │   └── validator.go
│   │   │   └── errors/
│   │   │       └── errors.go
│   │   ├── migrations/
│   │   │   ├── 001_create_users.up.sql
│   │   │   ├── 001_create_users.down.sql
│   │   │   ├── 002_create_interviews.up.sql
│   │   │   └── 002_create_interviews.down.sql
│   │   ├── Dockerfile
│   │   ├── go.mod
│   │   ├── go.sum
│   │   └── Makefile
│   │
│   ├── emotion-service/                # Python - Emotion Detection
│   │   ├── app/
│   │   │   ├── api/
│   │   │   │   ├── v1/
│   │   │   │   │   ├── endpoints/
│   │   │   │   │   │   ├── emotion.py
│   │   │   │   │   │   ├── face.py
│   │   │   │   │   │   └── health.py
│   │   │   │   │   └── router.py
│   │   │   │   └── deps.py
│   │   │   ├── core/
│   │   │   │   ├── config.py
│   │   │   │   ├── logging.py
│   │   │   │   └── security.py
│   │   │   ├── models/
│   │   │   │   ├── emotion_model.py
│   │   │   │   ├── face_detector.py
│   │   │   │   └── blink_detector.py
│   │   │   ├── services/
│   │   │   │   ├── emotion_service.py
│   │   │   │   ├── preprocessing.py
│   │   │   │   └── cam_service.py
│   │   │   ├── schemas/
│   │   │   │   ├── emotion.py
│   │   │   │   └── response.py
│   │   │   ├── utils/
│   │   │   │   ├── image_utils.py
│   │   │   │   └── model_loader.py
│   │   │   └── main.py
│   │   ├── models/                     # ML model files
│   │   │   ├── xception_emotion.h5
│   │   │   ├── haarcascade_frontalface.xml
│   │   │   └── shape_predictor_68.dat
│   │   ├── tests/
│   │   │   ├── test_emotion.py
│   │   │   └── test_face_detection.py
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   └── pyproject.toml
│   │
│   ├── scoring-service/                # Go - Scoring Logic
│   │   ├── cmd/
│   │   │   └── server/
│   │   │       └── main.go
│   │   ├── internal/
│   │   │   ├── domain/
│   │   │   │   ├── score.go
│   │   │   │   └── report.go
│   │   │   ├── repository/
│   │   │   │   └── score_repo.go
│   │   │   ├── usecase/
│   │   │   │   ├── scoring_usecase.go
│   │   │   │   └── ai_analyzer.go
│   │   │   ├── delivery/
│   │   │   │   └── http/
│   │   │   │       └── handler.go
│   │   │   └── infrastructure/
│   │   │       ├── openai/
│   │   │       │   └── client.go
│   │   │       └── apikey/
│   │   │           └── rotator.go
│   │   ├── pkg/
│   │   │   └── algorithms/
│   │   │       ├── emotion_scorer.go
│   │   │       ├── answer_scorer.go
│   │   │       └── aggregator.go
│   │   ├── Dockerfile
│   │   ├── go.mod
│   │   └── go.sum
│   │
│   └── worker-service/                 # Go - Background Workers
│       ├── cmd/
│       │   └── worker/
│       │       └── main.go
│       ├── internal/
│       │   ├── workers/
│       │   │   ├── emotion_worker.go
│       │   │   ├── scoring_worker.go
│       │   │   ├── video_worker.go
│       │   │   └── notification_worker.go
│       │   ├── jobs/
│       │   │   ├── job.go
│       │   │   └── scheduler.go
│       │   └── queue/
│       │       └── consumer.go
│       ├── Dockerfile
│       ├── go.mod
│       └── go.sum
│
├── infrastructure/
│   ├── docker/
│   │   ├── docker-compose.yml
│   │   ├── docker-compose.prod.yml
│   │   └── nginx/
│   │       ├── nginx.conf
│   │       └── Dockerfile
│   ├── kubernetes/
│   │   ├── deployments/
│   │   │   ├── interview-service.yaml
│   │   │   ├── emotion-service.yaml
│   │   │   ├── scoring-service.yaml
│   │   │   └── worker-service.yaml
│   │   ├── services/
│   │   │   ├── interview-service.yaml
│   │   │   └── emotion-service.yaml
│   │   ├── configmaps/
│   │   │   └── app-config.yaml
│   │   ├── secrets/
│   │   │   └── app-secrets.yaml
│   │   ├── ingress/
│   │   │   └── ingress.yaml
│   │   └── hpa/
│   │       ├── interview-hpa.yaml
│   │       └── emotion-hpa.yaml
│   ├── terraform/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   ├── outputs.tf
│   │   ├── modules/
│   │   │   ├── vpc/
│   │   │   ├── eks/
│   │   │   ├── rds/
│   │   │   └── elasticache/
│   │   └── environments/
│   │       ├── dev/
│   │       ├── staging/
│   │       └── prod/
│   └── monitoring/
│       ├── prometheus/
│       │   └── prometheus.yml
│       ├── grafana/
│       │   └── dashboards/
│       └── alertmanager/
│           └── config.yml
│
├── shared/
│   ├── proto/                          # gRPC definitions
│   │   ├── emotion.proto
│   │   ├── interview.proto
│   │   └── scoring.proto
│   └── events/                         # Event schemas
│       ├── interview_events.go
│       └── emotion_events.go
│
├── scripts/
│   ├── deploy.sh
│   ├── migrate.sh
│   ├── seed.sh
│   └── backup.sh
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── DEPLOYMENT.md
│   └── DEVELOPMENT.md
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── security-scan.yml
│
├── Makefile
├── README.md
└── .gitignore
```

## Key Design Principles

### 1. Clean Architecture (Go Services)
```
Delivery Layer (HTTP/WebSocket)
    ↓
Use Case Layer (Business Logic)
    ↓
Domain Layer (Entities)
    ↓
Repository Layer (Data Access)
```

### 2. Separation of Concerns
- Each service has a single responsibility
- Clear boundaries between layers
- Dependency injection for testability

### 3. Scalability
- Stateless services
- Horizontal scaling ready
- Queue-based async processing

### 4. Maintainability
- Consistent structure across services
- Shared packages for common functionality
- Comprehensive documentation
