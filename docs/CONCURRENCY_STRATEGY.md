# Concurrency Strategy & Performance Optimization

## 1. Go Concurrency Patterns

### Worker Pool Pattern
```go
// Frame processing worker pool
type FrameProcessor struct {
    workerCount int
    jobs        chan *FrameJob
    results     chan *FrameResult
    wg          sync.WaitGroup
}

type FrameJob struct {
    SessionID string
    Frame     []byte
    Timestamp time.Time
}

type FrameResult struct {
    SessionID string
    Emotion   string
    Error     error
}

func NewFrameProcessor(workerCount int) *FrameProcessor {
    return &FrameProcessor{
        workerCount: workerCount,
        jobs:        make(chan *FrameJob, 1000),
        results:     make(chan *FrameResult, 1000),
    }
}

func (fp *FrameProcessor) Start(ctx context.Context) {
    for i := 0; i < fp.workerCount; i++ {
        fp.wg.Add(1)
        go fp.worker(ctx, i)
    }
}

func (fp *FrameProcessor) worker(ctx context.Context, id int) {
    defer fp.wg.Done()
    
    for {
        select {
        case <-ctx.Done():
            return
        case job, ok := <-fp.jobs:
            if !ok {
                return
            }
            
            result := fp.processFrame(job)
            
            select {
            case fp.results <- result:
            case <-ctx.Done():
                return
            }
        }
    }
}

func (fp *FrameProcessor) processFrame(job *FrameJob) *FrameResult {
    // Call emotion service via gRPC
    emotion, err := fp.analyzeEmotion(job.Frame)
    
    return &FrameResult{
        SessionID: job.SessionID,
        Emotion:   emotion,
        Error:     err,
    }
}

func (fp *FrameProcessor) Stop() {
    close(fp.jobs)
    fp.wg.Wait()
    close(fp.results)
}
```

### Fan-Out/Fan-In Pattern
```go
// Process multiple frames concurrently and aggregate results
func ProcessBatchFrames(ctx context.Context, frames []*Frame) ([]*EmotionResult, error) {
    results := make(chan *EmotionResult, len(frames))
    errors := make(chan error, len(frames))
    
    var wg sync.WaitGroup
    
    // Fan-out: Process each frame concurrently
    for _, frame := range frames {
        wg.Add(1)
        go func(f *Frame) {
            defer wg.Done()
            
            result, err := analyzeFrame(ctx, f)
            if err != nil {
                errors <- err
                return
            }
            
            results <- result
        }(frame)
    }
    
    // Wait for all goroutines
    go func() {
        wg.Wait()
        close(results)
        close(errors)
    }()
    
    // Fan-in: Collect results
    var emotionResults []*EmotionResult
    var errs []error
    
    for {
        select {
        case result, ok := <-results:
            if !ok {
                results = nil
            } else {
                emotionResults = append(emotionResults, result)
            }
        case err, ok := <-errors:
            if !ok {
                errors = nil
            } else {
                errs = append(errs, err)
            }
        }
        
        if results == nil && errors == nil {
            break
        }
    }
    
    if len(errs) > 0 {
        return emotionResults, fmt.Errorf("errors occurred: %v", errs)
    }
    
    return emotionResults, nil
}
```

### Pipeline Pattern
```go
// Frame processing pipeline
type Pipeline struct {
    stages []Stage
}

type Stage func(context.Context, <-chan interface{}) <-chan interface{}

func NewPipeline(stages ...Stage) *Pipeline {
    return &Pipeline{stages: stages}
}

func (p *Pipeline) Execute(ctx context.Context, input <-chan interface{}) <-chan interface{} {
    out := input
    for _, stage := range p.stages {
        out = stage(ctx, out)
    }
    return out
}

// Stage 1: Decode frames
func decodeStage(ctx context.Context, input <-chan interface{}) <-chan interface{} {
    out := make(chan interface{})
    
    go func() {
        defer close(out)
        for {
            select {
            case <-ctx.Done():
                return
            case data, ok := <-input:
                if !ok {
                    return
                }
                
                frame := decodeFrame(data.([]byte))
                
                select {
                case out <- frame:
                case <-ctx.Done():
                    return
                }
            }
        }
    }()
    
    return out
}

// Stage 2: Preprocess frames
func preprocessStage(ctx context.Context, input <-chan interface{}) <-chan interface{} {
    out := make(chan interface{})
    
    go func() {
        defer close(out)
        for {
            select {
            case <-ctx.Done():
                return
            case data, ok := <-input:
                if !ok {
                    return
                }
                
                processed := preprocessFrame(data.(*Frame))
                
                select {
                case out <- processed:
                case <-ctx.Done():
                    return
                }
            }
        }
    }()
    
    return out
}

// Stage 3: Analyze emotions
func analyzeStage(ctx context.Context, input <-chan interface{}) <-chan interface{} {
    out := make(chan interface{})
    
    go func() {
        defer close(out)
        for {
            select {
            case <-ctx.Done():
                return
            case data, ok := <-input:
                if !ok {
                    return
                }
                
                emotion := analyzeEmotion(data.(*Frame))
                
                select {
                case out <- emotion:
                case <-ctx.Done():
                    return
                }
            }
        }
    }()
    
    return out
}

// Usage
func ProcessFrames(ctx context.Context, frames <-chan []byte) <-chan interface{} {
    pipeline := NewPipeline(
        decodeStage,
        preprocessStage,
        analyzeStage,
    )
    
    input := make(chan interface{})
    go func() {
        defer close(input)
        for frame := range frames {
            input <- frame
        }
    }()
    
    return pipeline.Execute(ctx, input)
}
```

## 2. WebSocket Connection Management

### Connection Pool
```go
type Hub struct {
    clients    map[string]*Client
    broadcast  chan *Message
    register   chan *Client
    unregister chan *Client
    mu         sync.RWMutex
}

type Client struct {
    hub       *Hub
    conn      *websocket.Conn
    send      chan []byte
    sessionID string
    userID    string
}

func NewHub() *Hub {
    return &Hub{
        clients:    make(map[string]*Client),
        broadcast:  make(chan *Message, 256),
        register:   make(chan *Client),
        unregister: make(chan *Client),
    }
}

func (h *Hub) Run(ctx context.Context) {
    for {
        select {
        case <-ctx.Done():
            return
        case client := <-h.register:
            h.mu.Lock()
            h.clients[client.sessionID] = client
            h.mu.Unlock()
            
        case client := <-h.unregister:
            h.mu.Lock()
            if _, ok := h.clients[client.sessionID]; ok {
                delete(h.clients, client.sessionID)
                close(client.send)
            }
            h.mu.Unlock()
            
        case message := <-h.broadcast:
            h.mu.RLock()
            for _, client := range h.clients {
                if client.sessionID == message.SessionID {
                    select {
                    case client.send <- message.Data:
                    default:
                        close(client.send)
                        delete(h.clients, client.sessionID)
                    }
                }
            }
            h.mu.RUnlock()
        }
    }
}

func (c *Client) ReadPump() {
    defer func() {
        c.hub.unregister <- c
        c.conn.Close()
    }()
    
    c.conn.SetReadDeadline(time.Now().Add(pongWait))
    c.conn.SetPongHandler(func(string) error {
        c.conn.SetReadDeadline(time.Now().Add(pongWait))
        return nil
    })
    
    for {
        _, message, err := c.conn.ReadMessage()
        if err != nil {
            break
        }
        
        // Process message in goroutine
        go c.handleMessage(message)
    }
}

func (c *Client) WritePump() {
    ticker := time.NewTicker(pingPeriod)
    defer func() {
        ticker.Stop()
        c.conn.Close()
    }()
    
    for {
        select {
        case message, ok := <-c.send:
            c.conn.SetWriteDeadline(time.Now().Add(writeWait))
            if !ok {
                c.conn.WriteMessage(websocket.CloseMessage, []byte{})
                return
            }
            
            w, err := c.conn.NextWriter(websocket.TextMessage)
            if err != nil {
                return
            }
            w.Write(message)
            
            // Add queued messages
            n := len(c.send)
            for i := 0; i < n; i++ {
                w.Write(newline)
                w.Write(<-c.send)
            }
            
            if err := w.Close(); err != nil {
                return
            }
            
        case <-ticker.C:
            c.conn.SetWriteDeadline(time.Now().Add(writeWait))
            if err := c.conn.WriteMessage(websocket.PingMessage, nil); err != nil {
                return
            }
        }
    }
}
```

## 3. Database Connection Pooling

```go
type DBPool struct {
    db *sql.DB
}

func NewDBPool(dsn string) (*DBPool, error) {
    db, err := sql.Open("postgres", dsn)
    if err != nil {
        return nil, err
    }
    
    // Connection pool settings
    db.SetMaxOpenConns(25)                 // Maximum open connections
    db.SetMaxIdleConns(5)                  // Maximum idle connections
    db.SetConnMaxLifetime(5 * time.Minute) // Connection lifetime
    db.SetConnMaxIdleTime(10 * time.Minute)// Idle connection timeout
    
    // Verify connection
    if err := db.Ping(); err != nil {
        return nil, err
    }
    
    return &DBPool{db: db}, nil
}

// Use prepared statements for better performance
type InterviewRepo struct {
    db              *sql.DB
    insertStmt      *sql.Stmt
    selectStmt      *sql.Stmt
    updateStmt      *sql.Stmt
    stmtMu          sync.RWMutex
}

func NewInterviewRepo(db *sql.DB) (*InterviewRepo, error) {
    repo := &InterviewRepo{db: db}
    
    // Prepare statements
    var err error
    repo.insertStmt, err = db.Prepare(`
        INSERT INTO interviews (id, user_id, status, started_at)
        VALUES ($1, $2, $3, $4)
    `)
    if err != nil {
        return nil, err
    }
    
    repo.selectStmt, err = db.Prepare(`
        SELECT id, user_id, status, started_at, completed_at
        FROM interviews WHERE id = $1
    `)
    if err != nil {
        return nil, err
    }
    
    return repo, nil
}
```

## 4. Redis Connection Pooling

```go
type RedisPool struct {
    client *redis.Client
}

func NewRedisPool(addr string) *RedisPool {
    client := redis.NewClient(&redis.Options{
        Addr:         addr,
        PoolSize:     10,              // Connection pool size
        MinIdleConns: 5,               // Minimum idle connections
        MaxRetries:   3,               // Retry attempts
        DialTimeout:  5 * time.Second,
        ReadTimeout:  3 * time.Second,
        WriteTimeout: 3 * time.Second,
        PoolTimeout:  4 * time.Second,
    })
    
    return &RedisPool{client: client}
}

// Use pipelining for batch operations
func (r *RedisPool) SaveEmotionsBatch(emotions []*Emotion) error {
    pipe := r.client.Pipeline()
    
    for _, emotion := range emotions {
        key := fmt.Sprintf("emotion:%s:%d", emotion.SessionID, emotion.Timestamp)
        pipe.Set(context.Background(), key, emotion.ToJSON(), time.Hour)
    }
    
    _, err := pipe.Exec(context.Background())
    return err
}
```

## 5. Rate Limiting

### Token Bucket Algorithm
```go
type RateLimiter struct {
    limiters sync.Map // map[string]*rate.Limiter
    rate     rate.Limit
    burst    int
}

func NewRateLimiter(r rate.Limit, b int) *RateLimiter {
    return &RateLimiter{
        rate:  r,
        burst: b,
    }
}

func (rl *RateLimiter) GetLimiter(key string) *rate.Limiter {
    limiter, exists := rl.limiters.Load(key)
    if !exists {
        limiter = rate.NewLimiter(rl.rate, rl.burst)
        rl.limiters.Store(key, limiter)
    }
    return limiter.(*rate.Limiter)
}

func (rl *RateLimiter) Allow(key string) bool {
    limiter := rl.GetLimiter(key)
    return limiter.Allow()
}

// Middleware
func RateLimitMiddleware(limiter *RateLimiter) gin.HandlerFunc {
    return func(c *gin.Context) {
        userID := c.GetString("user_id")
        
        if !limiter.Allow(userID) {
            c.JSON(429, gin.H{"error": "rate limit exceeded"})
            c.Abort()
            return
        }
        
        c.Next()
    }
}
```

## 6. Caching Strategy

### Multi-Level Cache
```go
type CacheManager struct {
    local  *ristretto.Cache  // In-memory cache
    redis  *redis.Client     // Distributed cache
}

func (cm *CacheManager) Get(ctx context.Context, key string) (interface{}, error) {
    // Level 1: Check local cache
    if value, found := cm.local.Get(key); found {
        return value, nil
    }
    
    // Level 2: Check Redis
    value, err := cm.redis.Get(ctx, key).Result()
    if err == nil {
        // Store in local cache
        cm.local.Set(key, value, 1)
        return value, nil
    }
    
    return nil, errors.New("cache miss")
}

func (cm *CacheManager) Set(ctx context.Context, key string, value interface{}, ttl time.Duration) error {
    // Set in both caches
    cm.local.SetWithTTL(key, value, 1, ttl)
    return cm.redis.Set(ctx, key, value, ttl).Err()
}
```

## 7. Batch Processing

```go
type BatchProcessor struct {
    batchSize int
    interval  time.Duration
    buffer    []interface{}
    mu        sync.Mutex
    ticker    *time.Ticker
    done      chan struct{}
}

func NewBatchProcessor(size int, interval time.Duration) *BatchProcessor {
    bp := &BatchProcessor{
        batchSize: size,
        interval:  interval,
        buffer:    make([]interface{}, 0, size),
        ticker:    time.NewTicker(interval),
        done:      make(chan struct{}),
    }
    
    go bp.run()
    return bp
}

func (bp *BatchProcessor) Add(item interface{}) {
    bp.mu.Lock()
    defer bp.mu.Unlock()
    
    bp.buffer = append(bp.buffer, item)
    
    if len(bp.buffer) >= bp.batchSize {
        bp.flush()
    }
}

func (bp *BatchProcessor) run() {
    for {
        select {
        case <-bp.ticker.C:
            bp.mu.Lock()
            bp.flush()
            bp.mu.Unlock()
        case <-bp.done:
            return
        }
    }
}

func (bp *BatchProcessor) flush() {
    if len(bp.buffer) == 0 {
        return
    }
    
    // Process batch
    go bp.processBatch(bp.buffer)
    
    // Reset buffer
    bp.buffer = make([]interface{}, 0, bp.batchSize)
}

func (bp *BatchProcessor) processBatch(items []interface{}) {
    // Batch insert to database
    // Or batch send to message queue
}
```

## 8. Context Propagation

```go
// Propagate context through service calls
func (s *InterviewService) StartInterview(ctx context.Context, req *StartRequest) (*Interview, error) {
    // Add tracing
    ctx, span := trace.StartSpan(ctx, "StartInterview")
    defer span.End()
    
    // Add timeout
    ctx, cancel := context.WithTimeout(ctx, 30*time.Second)
    defer cancel()
    
    // Create interview
    interview, err := s.repo.Create(ctx, req)
    if err != nil {
        return nil, err
    }
    
    // Call emotion service with context
    err = s.emotionClient.Initialize(ctx, interview.ID)
    if err != nil {
        return nil, err
    }
    
    return interview, nil
}
```

## 9. Graceful Shutdown

```go
func main() {
    server := &http.Server{Addr: ":8080"}
    
    // Start server
    go func() {
        if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
            log.Fatal(err)
        }
    }()
    
    // Wait for interrupt signal
    quit := make(chan os.Signal, 1)
    signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
    <-quit
    
    log.Println("Shutting down server...")
    
    // Graceful shutdown with timeout
    ctx, cancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer cancel()
    
    if err := server.Shutdown(ctx); err != nil {
        log.Fatal("Server forced to shutdown:", err)
    }
    
    log.Println("Server exited")
}
```

## 10. Performance Metrics

```go
// Prometheus metrics
var (
    requestDuration = promauto.NewHistogramVec(
        prometheus.HistogramOpts{
            Name:    "http_request_duration_seconds",
            Help:    "HTTP request duration",
            Buckets: prometheus.DefBuckets,
        },
        []string{"method", "endpoint", "status"},
    )
    
    activeConnections = promauto.NewGauge(
        prometheus.GaugeOpts{
            Name: "websocket_active_connections",
            Help: "Number of active WebSocket connections",
        },
    )
    
    queueDepth = promauto.NewGauge(
        prometheus.GaugeOpts{
            Name: "queue_depth",
            Help: "Current queue depth",
        },
    )
)

// Middleware to track metrics
func MetricsMiddleware() gin.HandlerFunc {
    return func(c *gin.Context) {
        start := time.Now()
        
        c.Next()
        
        duration := time.Since(start).Seconds()
        requestDuration.WithLabelValues(
            c.Request.Method,
            c.FullPath(),
            strconv.Itoa(c.Writer.Status()),
        ).Observe(duration)
    }
}
```
