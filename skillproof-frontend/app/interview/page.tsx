'use client';

import { useState, useRef, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Camera, Mic, MicOff, Video, VideoOff, MessageSquare, CheckCircle, AlertCircle, Loader2, ArrowRight } from 'lucide-react';

export default function AIInterviewPage() {
  const router = useRouter();
  const videoRef = useRef<HTMLVideoElement>(null);
  const [stream, setStream] = useState<MediaStream | null>(null);
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [isMicOn, setIsMicOn] = useState(false);
  const [interviewStarted, setInterviewStarted] = useState(false);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [isRecording, setIsRecording] = useState(false);
  const [aiResponse, setAiResponse] = useState('');
  const [isAiSpeaking, setIsAiSpeaking] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const recognitionRef = useRef<any>(null);

  const questions = [
    "Hello! I'm your AI interviewer. Can you please introduce yourself and tell me about your background?",
    "What motivated you to apply for this position?",
    "Can you describe a challenging project you've worked on and how you overcame obstacles?",
    "What are your key technical skills and how have you applied them in real-world scenarios?",
    "Where do you see yourself in the next 3-5 years?",
  ];

  useEffect(() => {
    // Initialize speech recognition
    if (typeof window !== 'undefined' && ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      const SpeechRecognition = (window as any).webkitSpeechRecognition || (window as any).SpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      
      recognitionRef.current.onresult = (event: any) => {
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            finalTranscript += event.results[i][0].transcript;
          }
        }
        if (finalTranscript) {
          setTranscript(prev => prev + ' ' + finalTranscript);
        }
      };
      
      recognitionRef.current.onerror = (event: any) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
      };
    }
    
    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, [stream]);

  const startCamera = async () => {
    try {
      const mediaStream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });
      setStream(mediaStream);
      if (videoRef.current) {
        videoRef.current.srcObject = mediaStream;
      }
      setIsCameraOn(true);
      setIsMicOn(true);
    } catch (error) {
      console.error('Error accessing camera:', error);
      alert('Please allow camera and microphone access to continue with the interview.');
    }
  };

  const stopCamera = () => {
    if (stream) {
      stream.getTracks().forEach(track => track.stop());
      setStream(null);
      setIsCameraOn(false);
      setIsMicOn(false);
    }
  };

  const toggleMic = () => {
    if (stream) {
      const audioTrack = stream.getAudioTracks()[0];
      if (audioTrack) {
        audioTrack.enabled = !audioTrack.enabled;
        setIsMicOn(audioTrack.enabled);
      }
    }
  };

  const startInterview = () => {
    if (!isCameraOn) {
      alert('Please enable your camera to start the interview.');
      return;
    }
    setInterviewStarted(true);
    const firstQuestion = questions[0];
    if (firstQuestion) {
      speakQuestion(firstQuestion);
    }
  };

  const speakQuestion = (question: string) => {
    setAiResponse(question);
    setIsAiSpeaking(true);
    
    // Use Web Speech API for text-to-speech
    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(question);
      utterance.rate = 0.9;
      utterance.pitch = 1;
      utterance.volume = 1;
      
      utterance.onend = () => {
        setIsAiSpeaking(false);
      };
      
      window.speechSynthesis.speak(utterance);
    } else {
      // Fallback: just show text
      setTimeout(() => {
        setIsAiSpeaking(false);
      }, 3000);
    }
  };

  const startRecording = () => {
    setIsRecording(true);
    setTranscript('');
    
    // Start speech recognition
    if (recognitionRef.current) {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch (error) {
        console.error('Error starting recognition:', error);
      }
    }
  };

  const stopRecording = () => {
    setIsRecording(false);
    setIsListening(false);
    
    // Stop speech recognition
    if (recognitionRef.current) {
      recognitionRef.current.stop();
    }
    
    // Process the transcript
    console.log('Answer transcript:', transcript);
    
    // Simulate processing answer
    setTimeout(() => {
      if (currentQuestion < questions.length - 1) {
        const nextQuestion = currentQuestion + 1;
        setCurrentQuestion(nextQuestion);
        const nextQ = questions[nextQuestion];
        if (nextQ) {
          speakQuestion(nextQ);
        }
      } else {
        completeInterview();
      }
    }, 1000);
  };

  const completeInterview = () => {
    setAiResponse("Thank you for completing the interview! Your responses have been recorded and will be analyzed. You'll receive feedback within 24 hours.");
    setIsAiSpeaking(true);
    
    setTimeout(() => {
      router.push('/dashboard?interview=completed');
    }, 5000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="container mx-auto px-6 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Camera className="h-8 w-8 text-purple-400" />
            <span className="text-2xl font-bold text-white">AI Interview</span>
          </div>
          <button
            onClick={() => router.push('/dashboard')}
            className="px-4 py-2 bg-white/10 text-white rounded-lg hover:bg-white/20 transition"
          >
            Exit Interview
          </button>
        </div>
      </div>

      <div className="container mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-8">
          {/* Video Section */}
          <div className="lg:col-span-2">
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
              {/* Video Feed */}
              <div className="relative bg-black rounded-xl overflow-hidden mb-6" style={{ aspectRatio: '16/9' }}>
                {isCameraOn ? (
                  <video
                    ref={videoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <div className="text-center">
                      <VideoOff className="h-16 w-16 text-gray-500 mx-auto mb-4" />
                      <p className="text-gray-400">Camera is off</p>
                    </div>
                  </div>
                )}

                {/* Recording Indicator */}
                {isRecording && (
                  <div className="absolute top-4 left-4 flex items-center gap-2 bg-red-500 px-3 py-1 rounded-full">
                    <div className="w-2 h-2 bg-white rounded-full animate-pulse" />
                    <span className="text-white text-sm font-semibold">Recording</span>
                  </div>
                )}

                {/* AI Speaking Indicator */}
                {isAiSpeaking && (
                  <div className="absolute top-4 right-4 flex items-center gap-2 bg-purple-500 px-3 py-1 rounded-full animate-pulse">
                    <MessageSquare className="w-4 h-4 text-white" />
                    <span className="text-white text-sm font-semibold">AI Speaking</span>
                  </div>
                )}

                {/* Listening Indicator */}
                {isListening && (
                  <div className="absolute top-16 right-4 flex items-center gap-2 bg-green-500 px-3 py-1 rounded-full">
                    <div className="flex gap-1">
                      <div className="w-1 h-4 bg-white rounded-full animate-pulse" style={{ animationDelay: '0ms' }} />
                      <div className="w-1 h-4 bg-white rounded-full animate-pulse" style={{ animationDelay: '150ms' }} />
                      <div className="w-1 h-4 bg-white rounded-full animate-pulse" style={{ animationDelay: '300ms' }} />
                    </div>
                    <span className="text-white text-sm font-semibold">Listening...</span>
                  </div>
                )}

                {/* Question Progress */}
                {interviewStarted && (
                  <div className="absolute bottom-4 left-4 right-4">
                    <div className="bg-black/50 backdrop-blur-sm rounded-lg p-3">
                      <div className="flex justify-between text-white text-sm mb-2">
                        <span>Question {currentQuestion + 1} of {questions.length}</span>
                        <span>{Math.round(((currentQuestion + 1) / questions.length) * 100)}%</span>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <div
                          className="bg-gradient-to-r from-purple-600 to-pink-600 h-2 rounded-full transition-all duration-500"
                          style={{ width: `${((currentQuestion + 1) / questions.length) * 100}%` }}
                        />
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Controls */}
              <div className="flex items-center justify-center gap-4">
                {!interviewStarted ? (
                  <>
                    <button
                      onClick={isCameraOn ? stopCamera : startCamera}
                      className={`p-4 rounded-full transition ${
                        isCameraOn
                          ? 'bg-green-500 hover:bg-green-600'
                          : 'bg-red-500 hover:bg-red-600'
                      }`}
                    >
                      {isCameraOn ? (
                        <Video className="h-6 w-6 text-white" />
                      ) : (
                        <VideoOff className="h-6 w-6 text-white" />
                      )}
                    </button>

                    <button
                      onClick={toggleMic}
                      disabled={!isCameraOn}
                      className={`p-4 rounded-full transition ${
                        isMicOn
                          ? 'bg-green-500 hover:bg-green-600'
                          : 'bg-red-500 hover:bg-red-600'
                      } disabled:opacity-50 disabled:cursor-not-allowed`}
                    >
                      {isMicOn ? (
                        <Mic className="h-6 w-6 text-white" />
                      ) : (
                        <MicOff className="h-6 w-6 text-white" />
                      )}
                    </button>

                    <button
                      onClick={startInterview}
                      disabled={!isCameraOn}
                      className="px-8 py-4 bg-gradient-to-r from-purple-600 to-pink-600 text-white rounded-full font-semibold hover:shadow-lg hover:shadow-purple-500/50 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
                    >
                      Start Interview
                      <ArrowRight className="h-5 w-5" />
                    </button>
                  </>
                ) : (
                  <button
                    onClick={isRecording ? stopRecording : startRecording}
                    disabled={isAiSpeaking}
                    className={`px-8 py-4 rounded-full font-semibold transition flex items-center gap-2 ${
                      isRecording
                        ? 'bg-red-500 hover:bg-red-600'
                        : 'bg-gradient-to-r from-purple-600 to-pink-600 hover:shadow-lg hover:shadow-purple-500/50'
                    } text-white disabled:opacity-50 disabled:cursor-not-allowed`}
                  >
                    {isRecording ? (
                      <>
                        <div className="w-3 h-3 bg-white rounded-sm" />
                        Stop Recording
                      </>
                    ) : (
                      <>
                        <div className="w-3 h-3 bg-white rounded-full" />
                        Start Recording Answer
                      </>
                    )}
                  </button>
                )}
              </div>
            </div>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* AI Response */}
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
              <div className="flex items-center gap-2 mb-4">
                <MessageSquare className="h-5 w-5 text-purple-400" />
                <h3 className="text-lg font-semibold text-white">AI Interviewer</h3>
              </div>
              
              {aiResponse ? (
                <div className="bg-purple-500/10 border border-purple-500/20 rounded-lg p-4">
                  <p className="text-white leading-relaxed">{aiResponse}</p>
                  {isAiSpeaking && (
                    <div className="flex items-center gap-2 mt-3 text-purple-300 text-sm">
                      <Loader2 className="h-4 w-4 animate-spin" />
                      <span>Speaking...</span>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-400">
                  Enable your camera and click "Start Interview" to begin.
                </p>
              )}
            </div>

            {/* Your Answer Transcript */}
            {(isRecording || transcript) && (
              <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
                <div className="flex items-center gap-2 mb-4">
                  <Mic className="h-5 w-5 text-green-400" />
                  <h3 className="text-lg font-semibold text-white">Your Answer</h3>
                </div>
                
                <div className="bg-green-500/10 border border-green-500/20 rounded-lg p-4 min-h-[100px]">
                  {transcript ? (
                    <p className="text-white leading-relaxed">{transcript}</p>
                  ) : (
                    <p className="text-gray-400 italic">Start speaking...</p>
                  )}
                  {isListening && (
                    <div className="flex items-center gap-2 mt-3 text-green-300 text-sm">
                      <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse" />
                      <span>Listening to your answer...</span>
                    </div>
                  )}
                </div>
              </div>
            )}

            {/* Instructions */}
            <div className="bg-white/5 backdrop-blur-sm border border-white/10 rounded-2xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4">Instructions</h3>
              <ul className="space-y-3">
                <li className="flex items-start gap-2 text-gray-300 text-sm">
                  <CheckCircle className="h-5 w-5 text-green-400 flex-shrink-0 mt-0.5" />
                  <span>Enable camera and microphone</span>
                </li>
                <li className="flex items-start gap-2 text-gray-300 text-sm">
                  <CheckCircle className="h-5 w-5 text-green-400 flex-shrink-0 mt-0.5" />
                  <span>Listen to each question carefully</span>
                </li>
                <li className="flex items-start gap-2 text-gray-300 text-sm">
                  <CheckCircle className="h-5 w-5 text-green-400 flex-shrink-0 mt-0.5" />
                  <span>Click "Start Recording" to answer</span>
                </li>
                <li className="flex items-start gap-2 text-gray-300 text-sm">
                  <CheckCircle className="h-5 w-5 text-green-400 flex-shrink-0 mt-0.5" />
                  <span>Click "Stop Recording" when done</span>
                </li>
                <li className="flex items-start gap-2 text-gray-300 text-sm">
                  <AlertCircle className="h-5 w-5 text-yellow-400 flex-shrink-0 mt-0.5" />
                  <span>Don't switch tabs during interview</span>
                </li>
              </ul>
            </div>

            {/* Tips */}
            <div className="bg-gradient-to-br from-purple-500/10 to-pink-500/10 backdrop-blur-sm border border-purple-500/20 rounded-2xl p-6">
              <h3 className="text-lg font-semibold text-white mb-3">💡 Tips</h3>
              <ul className="space-y-2 text-gray-300 text-sm">
                <li>• Speak clearly and confidently</li>
                <li>• Look at the camera</li>
                <li>• Take your time to think</li>
                <li>• Be honest and authentic</li>
                <li>• Provide specific examples</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
