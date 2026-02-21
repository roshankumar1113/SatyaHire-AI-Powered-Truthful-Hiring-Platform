# Microservice Communication Design

## 1. Communication Patterns

### Synchronous Communication (gRPC)
Used for: Real-time, low-latency operations

```
Interview Service ←→ Emotion Service (gRPC)
Interview Service ←→ Scoring Service (gRPC)
```

### Asynchronous Communication (RabbitMQ)
Used for: Background processing, decoupling

```
Interview Service → Queue → Worker Service
Worker Service → Queue → Emotion Service
Emotion Service → Queue → Scoring Service
```

### Real-time Communication (WebSocket)
Used for: Client updates

```
Client ←→ Interview Service (WebSocket)
```

## 2. gRPC Service Definitions

### emotion.proto
```protobuf
syntax = "proto3";

package emotion;

option go_package = "github.com/yourorg/ai-interview/shared/proto/emotion";

service EmotionService {
  rpc AnalyzeFrame(FrameRequest) returns (EmotionResponse);
  rpc AnalyzeBatch(BatchRequest) returns (stream EmotionResponse);
  rpc DetectFace(FrameRequest) returns (FaceResponse);
  rpc DetectBlink(FrameRequest) returns (BlinkResponse);
}

message FrameRequest {
  string session_id = 1;
  bytes image_data = 2;
  int64 timestamp = 3;
  string format = 4; // jpeg, png
}

message BatchRequest {
  string session_id = 1;
  repeated FrameRequest frames = 2;
}

message EmotionResponse {
  string session_id = 1;
  int64 timestamp = 2;
  string emotion = 3; // happy, sad, angry, neutral, etc.
  float confidence = 4;
  FaceMetrics face_metrics = 5;
  BlinkMetrics blink_metrics = 6;
}

message FaceResponse {
  bool detected = 1;
  BoundingBox box = 2;
  repeated Landmark landmarks = 3;
}

message BlinkResponse {
  int32 blink_count = 1;
  float blink_rate = 2;
  repeated int64 blink_timestamps = 3;
}

message FaceMetrics {
  bool detected = 1;
  float detection_confidence = 2;
  BoundingBox bounding_box = 3;
  repeated Landmark landmarks = 4;
}

message BlinkMetrics {
  int32 count = 1;
  float rate = 2;
  float avg_duration = 3;
}

message BoundingBox {
  int32 x = 1;
  int32 y = 2;
  int32 width = 3;
  int32 height = 4;
}

message Landmark {
  int32 x = 1;
  int32 y = 2;
  string type = 3; // eye, nose, mouth, etc.
}
```

### scoring.proto
```protobuf
syntax = "proto3";

package scoring;

option go_package = "github.com/yourorg/ai-interview/shared/proto/scoring";

service ScoringService {
  rpc CalculateScore(ScoreRequest) returns (ScoreResponse);
  rpc AnalyzeAnswer(AnswerRequest) returns (AnswerAnalysis);
  rpc GenerateReport(ReportRequest) returns (ReportResponse);
}

message ScoreRequest {
  string session_id = 1;
  repeated Answer answers = 2;
  repeated EmotionData emotions = 3;
  InterviewMetadata metadata = 4;
}

message Answer {
  string question_id = 1;
  string transcript = 2;
  float duration = 3;
  float confidence = 4;
}

message EmotionData {
  int64 timestamp = 1;
  string emotion = 2;
  float confidence = 3;
  int32 blink_count = 4;
}

message InterviewMetadata {
  string user_id = 1;
  int64 started_at = 2;
  int64 completed_at = 3;
  int32 total_questions = 4;
}

message ScoreResponse {
  string session_id = 1;
  float technical_score = 2;
  float communication_score = 3;
  float emotion_score = 4;
  float overall_score = 5;
  string feedback = 6;
  repeated Insight insights = 7;
}

message AnswerRequest {
  string question = 1;
  string answer = 2;
  string category = 3;
}

message AnswerAnalysis {
  float relevance_score = 1;
  float clarity_score = 2;
  float depth_score = 3;
  repeated string keywords = 4;
  string feedback = 5;
}

message ReportRequest {
  string session_id = 1;
  bool include_emotions = 2;
  bool include_video = 3;
}

message ReportResponse {
  string report_url = 1;
  bytes report_data = 2;
  string format = 3; // pdf, json
}

message Insight {
  string category = 1;
  string description = 2;
  float impact = 3;
}
```

## 3. Message Queue Events

### RabbitMQ Message Schemas

```go
// Frame Captured Event
type FrameCapturedEvent struct {
    SessionID   string    `json:"session_id"`
    Timestamp   time.Time `json:"timestamp"`
    ImageData   []byte    `json:"image_data"`
    Format      string    `json:"format"`
    FrameNumber int       `json:"frame_number"`
}

// Emotion Analyzed Event
type EmotionAnalyzedEvent struct {
    SessionID  string    `json:"session_id"`
    Timestamp  time.Time `json:"timestamp"`
    Emotion    string    `json:"emotion"`
    Confidence float64   `json:"confidence"`
    BlinkCount int       `json:"blink_count"`
    Metadata   map[string]interface{} `json:"metadata"`
}

// Interview Completed Event
type InterviewCompletedEvent struct {
    SessionID     string    `json:"session_id"`
    UserID        string    `json:"user_id"`
    CompletedAt   time.Time `json:"completed_at"`
    TotalDuration int       `json:"total_duration"`
    AnswerCount   int       `json:"answer_count"`
}

// Score Calculated Event
type ScoreCalculatedEvent struct {
    SessionID          string    `json:"session_id"`
    TechnicalScore     float64   `json:"technical_score"`
    CommunicationScore float64   `json:"communication_score"`
    EmotionScore       float64   `json:"emotion_score"`
    OverallScore       float64   `json:"overall_score"`
    CalculatedAt       time.Time `json:"calculated_at"`
}
```

## 4. REST API Endpoints

### Interview Service
```
POST   /api/v1/interviews/start
GET    /api/v1/interviews/:id
POST   /api/v1/interviews/:id/frames
POST   /api/v1/interviews/:id/answers
POST   /api/v1/interviews/:id/complete
GET    /api/v1/interviews/:id/status
WS     /ws/interviews/:id
```

### Emotion Service
```
POST   /api/v1/emotions/analyze
POST   /api/v1/emotions/batch
GET    /api/v1/emotions/session/:id
GET    /api/v1/emotions/health
```

### Scoring Service
```
POST   /api/v1/scores/calculate
GET    /api/v1/scores/session/:id
POST   /api/v1/scores/report
GET    /api/v1/scores/health
```

## 5. WebSocket Protocol

### Client → Server Messages
```json
{
  "type": "frame",
  "data": {
    "session_id": "uuid",
    "timestamp": 1234567890,
    "image": "base64_encoded_image"
  }
}

{
  "type": "answer",
  "data": {
    "question_id": "uuid",
    "transcript": "My answer...",
    "duration": 45.5
  }
}

{
  "type": "ping",
  "data": {}
}
```

### Server → Client Messages
```json
{
  "type": "emotion_update",
  "data": {
    "emotion": "confident",
    "confidence": 0.87,
    "timestamp": 1234567890
  }
}

{
  "type": "question",
  "data": {
    "id": "uuid",
    "text": "Tell me about yourself",
    "category": "introduction"
  }
}

{
  "type": "status",
  "data": {
    "progress": 60,
    "current_question": 3,
    "total_questions": 5
  }
}

{
  "type": "error",
  "data": {
    "code": "FACE_NOT_DETECTED",
    "message": "Please ensure your face is visible"
  }
}
```

## 6. Service Discovery

### Consul Configuration
```hcl
service {
  name = "interview-service"
  port = 8080
  tags = ["api", "v1"]
  
  check {
    http     = "http://localhost:8080/health"
    interval = "10s"
    timeout  = "2s"
  }
}

service {
  name = "emotion-service"
  port = 8081
  tags = ["ml", "grpc"]
  
  check {
    grpc     = "localhost:8081"
    interval = "10s"
    timeout  = "2s"
  }
}
```

## 7. Circuit Breaker Pattern

```go
// Example: Calling Emotion Service with Circuit Breaker
type EmotionClient struct {
    client  emotion.EmotionServiceClient
    breaker *gobreaker.CircuitBreaker
}

func (c *EmotionClient) AnalyzeFrame(ctx context.Context, req *emotion.FrameRequest) (*emotion.EmotionResponse, error) {
    result, err := c.breaker.Execute(func() (interface{}, error) {
        return c.client.AnalyzeFrame(ctx, req)
    })
    
    if err != nil {
        return nil, err
    }
    
    return result.(*emotion.EmotionResponse), nil
}
```

## 8. Retry Strategy

```go
// Exponential backoff with jitter
func retryWithBackoff(operation func() error, maxRetries int) error {
    backoff := time.Second
    
    for i := 0; i < maxRetries; i++ {
        err := operation()
        if err == nil {
            return nil
        }
        
        if i == maxRetries-1 {
            return err
        }
        
        // Add jitter
        jitter := time.Duration(rand.Int63n(int64(backoff)))
        time.Sleep(backoff + jitter)
        
        backoff *= 2
        if backoff > 30*time.Second {
            backoff = 30 * time.Second
        }
    }
    
    return fmt.Errorf("max retries exceeded")
}
```

## 9. Load Balancing

### gRPC Load Balancing
```go
// Client-side load balancing
conn, err := grpc.Dial(
    "consul://emotion-service",
    grpc.WithDefaultServiceConfig(`{"loadBalancingPolicy":"round_robin"}`),
    grpc.WithInsecure(),
)
```

### HTTP Load Balancing (Nginx)
```nginx
upstream interview_service {
    least_conn;
    server interview-1:8080 weight=1;
    server interview-2:8080 weight=1;
    server interview-3:8080 weight=1;
}

upstream emotion_service {
    least_conn;
    server emotion-1:8081 weight=2 max_fails=3 fail_timeout=30s;
    server emotion-2:8081 weight=2 max_fails=3 fail_timeout=30s;
}
```

## 10. API Gateway Pattern

```go
// API Gateway routes requests to appropriate services
type Gateway struct {
    interviewClient *InterviewClient
    emotionClient   *EmotionClient
    scoringClient   *ScoringClient
}

func (g *Gateway) HandleRequest(c *gin.Context) {
    path := c.Request.URL.Path
    
    switch {
    case strings.HasPrefix(path, "/api/v1/interviews"):
        g.proxyToInterview(c)
    case strings.HasPrefix(path, "/api/v1/emotions"):
        g.proxyToEmotion(c)
    case strings.HasPrefix(path, "/api/v1/scores"):
        g.proxyToScoring(c)
    default:
        c.JSON(404, gin.H{"error": "not found"})
    }
}
```
