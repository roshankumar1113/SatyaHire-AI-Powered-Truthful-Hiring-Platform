-- Create interviews table with language support
CREATE TABLE IF NOT EXISTS interviews (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Interview configuration
    role VARCHAR(255) NOT NULL,
    experience_level VARCHAR(50) NOT NULL,
    language VARCHAR(50) NOT NULL DEFAULT 'english',
    max_questions INTEGER DEFAULT 5,
    
    -- Interview status
    status VARCHAR(50) DEFAULT 'IN_PROGRESS',
    current_question_number INTEGER DEFAULT 1,
    
    -- Timestamps
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    
    -- Duration in seconds
    total_duration INTEGER DEFAULT 0,
    
    -- Media URLs
    video_url TEXT,
    audio_url TEXT,
    
    -- Scores
    technical_score FLOAT,
    communication_score FLOAT,
    emotion_score FLOAT,
    overall_score FLOAT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create interview_questions table
CREATE TABLE IF NOT EXISTS interview_questions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interview_id UUID NOT NULL REFERENCES interviews(id) ON DELETE CASCADE,
    
    question_number INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    category VARCHAR(100),
    difficulty VARCHAR(50),
    expected_duration INTEGER DEFAULT 120,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create interview_answers table
CREATE TABLE IF NOT EXISTS interview_answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interview_id UUID NOT NULL REFERENCES interviews(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES interview_questions(id) ON DELETE CASCADE,
    
    -- Answer content
    transcript TEXT NOT NULL,
    audio_url TEXT,
    
    -- Timing
    duration FLOAT NOT NULL,
    
    -- Evaluation
    score FLOAT,
    confidence FLOAT DEFAULT 0.95,
    strengths TEXT,
    improvements TEXT,
    corrected_answer TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create emotion_analysis table
CREATE TABLE IF NOT EXISTS emotion_analysis (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    interview_id UUID NOT NULL REFERENCES interviews(id) ON DELETE CASCADE,
    
    timestamp TIMESTAMP NOT NULL,
    
    -- Emotion data
    emotion VARCHAR(50) NOT NULL,
    confidence FLOAT NOT NULL,
    
    -- Face detection
    face_detected BOOLEAN DEFAULT TRUE,
    blink_count INTEGER DEFAULT 0,
    
    -- Additional metadata (JSON)
    metadata TEXT,
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_interviews_user_id ON interviews(user_id);
CREATE INDEX IF NOT EXISTS idx_interviews_status ON interviews(status);
CREATE INDEX IF NOT EXISTS idx_interviews_language ON interviews(language);
CREATE INDEX IF NOT EXISTS idx_interviews_created_at ON interviews(created_at);

CREATE INDEX IF NOT EXISTS idx_interview_questions_interview_id ON interview_questions(interview_id);
CREATE INDEX IF NOT EXISTS idx_interview_questions_number ON interview_questions(question_number);

CREATE INDEX IF NOT EXISTS idx_interview_answers_interview_id ON interview_answers(interview_id);
CREATE INDEX IF NOT EXISTS idx_interview_answers_question_id ON interview_answers(question_id);

CREATE INDEX IF NOT EXISTS idx_emotion_analysis_interview_id ON emotion_analysis(interview_id);
CREATE INDEX IF NOT EXISTS idx_emotion_analysis_timestamp ON emotion_analysis(timestamp);

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger for interviews table
CREATE TRIGGER update_interviews_updated_at BEFORE UPDATE ON interviews
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add comments
COMMENT ON TABLE interviews IS 'Stores interview sessions with multilingual support';
COMMENT ON COLUMN interviews.language IS 'Interview language (english, hindi, tamil, etc.)';
COMMENT ON COLUMN interviews.experience_level IS 'Candidate experience level (junior, mid, senior)';
COMMENT ON COLUMN interviews.status IS 'Interview status (IN_PROGRESS, COMPLETED, PAUSED)';

COMMENT ON TABLE interview_questions IS 'Stores questions asked during interviews';
COMMENT ON TABLE interview_answers IS 'Stores candidate answers with evaluations';
COMMENT ON TABLE emotion_analysis IS 'Stores real-time emotion analysis data';
