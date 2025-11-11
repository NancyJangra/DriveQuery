import { useState, useRef, useEffect } from 'react';
import './App.css';

// Add Message interface
interface Message {
  type: 'user' | 'assistant' | 'error' | 'system';
  content: string;
  sources?: string[];
}

// Icon components
const UploadIcon = () => (
  <svg className="icon" viewBox="0 0 32 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path d="M 12 30 L 12 20 L 8 20 L 16 12 L 24 20 L 20 20 L 20 30 Z" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
    <path d="M 6 30 C 6 30 4 30 4 32 C 4 34 6 34 6 34 L 26 34 C 26 34 28 34 28 32 C 28 30 26 30 26 30" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round"/>
    <path d="M 22 36 L 26 40 L 30 36" stroke="currentColor" strokeWidth="1.5" fill="none" strokeLinecap="round" strokeLinejoin="round"/>
    <line x1="26" y1="40" x2="26" y2="34" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
  </svg>
);

const ManualIcon = () => (
  <svg className="icon" viewBox="0 0 32 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="8" y="6" width="16" height="24" rx="2" stroke="currentColor" strokeWidth="2" fill="none"/>
    <line x1="11" y1="11" x2="21" y2="11" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <line x1="11" y1="15" x2="19" y2="15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <line x1="11" y1="19" x2="21" y2="19" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
    <circle cx="20" cy="26" r="5" stroke="currentColor" strokeWidth="1.5" fill="none"/>
    <circle cx="20" cy="26" r="2" stroke="currentColor" strokeWidth="1.5" fill="currentColor"/>
  </svg>
);

const SearchIcon = () => (
  <svg className="icon" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="16" cy="16" r="8" stroke="currentColor" strokeWidth="2" fill="none"/>
    <line x1="22" y1="22" x2="28" y2="28" stroke="currentColor" strokeWidth="2" strokeLinecap="round"/>
    <path d="M 12 15 L 13 13 L 17 13 L 18 15 L 20 15 L 20 17 L 12 17 Z" stroke="currentColor" strokeWidth="1" fill="none"/>
    <circle cx="14" cy="17" r="1" fill="currentColor"/>
    <circle cx="18" cy="17" r="1" fill="currentColor"/>
  </svg>
);

const EmptyStateIcon = () => (
  <svg className="icon-large" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="6" y="10" width="10" height="14" rx="1" stroke="currentColor" strokeWidth="2" fill="none"/>
    <line x1="8" y1="14" x2="14" y2="14" stroke="currentColor" strokeWidth="1" strokeLinecap="round"/>
    <line x1="8" y1="17" x2="14" y2="17" stroke="currentColor" strokeWidth="1" strokeLinecap="round"/>
    <line x1="8" y1="20" x2="12" y2="20" stroke="currentColor" strokeWidth="1" strokeLinecap="round"/>
    <path d="M 18 16 L 20 14 L 26 14 L 28 16 L 30 16 L 30 20 L 18 20 Z" stroke="currentColor" strokeWidth="1.5" fill="none"/>
    <circle cx="21" cy="20" r="2" stroke="currentColor" strokeWidth="1.5" fill="none"/>
    <circle cx="27" cy="20" r="2" stroke="currentColor" strokeWidth="1.5" fill="none"/>
  </svg>
);

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState('');
  const [documents, setDocuments] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Fetch documents on mount
  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const response = await fetch('https://drivequery-backend.onrender.com/api/documents/list');
      const data = await response.json();
      setDocuments(data.documents || []);
    } catch (error) {
      console.error('Error fetching documents:', error);
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    console.log('📁 File selected:', file.name, file.type, file.size);

    const formData = new FormData();
    formData.append('file', file);

    setIsLoading(true);
    try {
      console.log('📤 Sending to backend...');
      const response = await fetch('https://drivequery-backend.onrender.com/api/documents/upload', {
        method: 'POST',
        body: formData,
      });
      
      console.log('📥 Response status:', response.status);
      console.log('📥 Response ok?:', response.ok);
      
      const responseText = await response.text();
      console.log('📥 Raw response:', responseText);
      
      let data;
      try {
        data = JSON.parse(responseText);
        console.log('📥 Parsed data:', data);
      } catch (e) {
        console.error('❌ Failed to parse JSON:', e);
      }
      
      if (response.ok && data) {
        setMessages([...messages, {
          type: 'system',
          content: `✓ Upload successful — ${data.filename} added (${data.total_chars} characters, ${data.chunks || 0} chunks)`
        }]);
        fetchDocuments();
      } else {
        setMessages([...messages, {
          type: 'error',
          content: data?.detail || 'Unable to parse this file. Try uploading a PDF or DOCX of the manual.'
        }]);
      }
    } catch (error) {
      console.error('❌ Upload error:', error);
      setMessages([...messages, {
        type: 'error',
        content: 'Upload failed. Please try again.'
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isLoading) return;

    const userMessage = inputValue;
    setInputValue('');
    setMessages([...messages, { type: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch('https://drivequery-backend.onrender.com/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      });

      const data = await response.json();
      setMessages(prev => [...prev, { 
        type: 'assistant', 
        content: data.response,
        sources: data.sources 
      }]);
    } catch (error) {
      setMessages(prev => [...prev, { 
        type: 'error', 
        content: 'Failed to get response. Please try again.' 
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const clearChat = () => {
    setMessages([]);
  };

  return (
    <div className="app">
      {/* Decorative background accents */}
      <div className="bg-accent wheel-accent"></div>
      <div className="bg-accent road-accent"></div>
      <div className="bg-accent bolt-accent"></div>

      {/* Left sidebar - Documents */}
      <div className="sidebar">
        <div className="sidebar-header">
          <ManualIcon />
          <h2>Manuals</h2>
        </div>
        
        <div className="documents-list">
          {documents.length === 0 ? (
            <div className="empty-state">
              <EmptyStateIcon />
              <p className="empty-heading">No manuals uploaded</p>
              <p className="empty-subtext">Upload owner's manuals, workshop guides, or parts lists</p>
            </div>
          ) : (
            documents.map((doc, index) => (
              <div key={index} className="document-item">
                <ManualIcon />
                <div className="document-info">
                  <span className="document-name">{doc}</span>
                  <span className="document-type">PDF</span>
                </div>
              </div>
            ))
          )}
        </div>

        <button className="upload-button" onClick={() => fileInputRef.current?.click()}>
          <UploadIcon />
          <span>Upload Manual</span>
        </button>
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileUpload}
          style={{ display: 'none' }}
        />

        <button className="clear-button" onClick={clearChat}>
          Clear Chat
        </button>
      </div>

      {/* Main content area */}
      <div className="main-content">
        <header className="app-header">
          <h1>DriveQuery</h1>
          <p className="subtitle">Your vehicle manual assistant</p>
        </header>

        <div className="chat-container">
          {messages.length === 0 ? (
            <div className="welcome-card">
              <div className="hero-illustration">
                {/* Inline simplified hero */}
                <svg viewBox="0 0 800 300" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <defs>
                    <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                      <stop offset="0%" style={{stopColor:'#0E3B61'}} />
                      <stop offset="100%" style={{stopColor:'#071833'}} />
                    </linearGradient>
                  </defs>
                  <rect width="800" height="300" fill="url(#heroGrad)" rx="12"/>
                  
                  {/* Manual book */}
                  <g transform="translate(100, 80)">
                    <rect x="0" y="0" width="150" height="140" rx="6" fill="#0B2A4A" stroke="#1E90FF" strokeWidth="2"/>
                    <line x1="20" y1="30" x2="130" y2="30" stroke="#B9CBDD" strokeWidth="2"/>
                    <line x1="20" y1="50" x2="110" y2="50" stroke="#B9CBDD" strokeWidth="1.5"/>
                    <line x1="20" y1="65" x2="120" y2="65" stroke="#B9CBDD" strokeWidth="1.5"/>
                    <rect x="50" y="85" width="50" height="40" stroke="#1E90FF" strokeWidth="2" fill="none"/>
                    <text x="75" y="135" fontSize="10" fill="#B9CBDD" textAnchor="middle">DIAGRAM</text>
                  </g>
                  
                  {/* Car silhouette */}
                  <g transform="translate(450, 120)">
                    <path d="M 20 50 L 50 50 L 70 30 L 140 30 L 160 45 L 200 45 L 200 65 L 20 65 Z" 
                          fill="#0E3B61" stroke="#1E90FF" strokeWidth="2"/>
                    <path d="M 75 35 L 85 45 L 130 45 L 135 35 Z" fill="#071833"/>
                    <circle cx="70" cy="65" r="15" fill="#0B2A4A" stroke="#1E90FF" strokeWidth="2"/>
                    <circle cx="170" cy="65" r="15" fill="#0B2A4A" stroke="#1E90FF" strokeWidth="2"/>
                  </g>
                  
                  {/* Connecting line */}
                  <path d="M 270 150 Q 400 120, 470 150" stroke="#1E90FF" strokeWidth="1.5" fill="none" opacity="0.4" strokeDasharray="5,5"/>
                </svg>
              </div>

              <h2 className="welcome-title">Welcome to AutoQuery</h2>
              <p className="welcome-subtitle">Your vehicle manual assistant</p>
              
              <div className="welcome-body">
                <p>Upload service manuals, owner's manuals, and repair guides for quick, accurate answers about your vehicle.</p>
                
                <div className="steps">
                  <div className="step">
                    <div className="step-number">1</div>
                    <div className="step-content">
                      <h4>Upload manuals</h4>
                      <p>PDF, DOCX, or TXT formats supported</p>
                    </div>
                  </div>
                  <div className="step">
                    <div className="step-number">2</div>
                    <div className="step-content">
                      <h4>Ask questions</h4>
                      <p>Parts, torque specs, maintenance steps</p>
                    </div>
                  </div>
                  <div className="step">
                    <div className="step-number">3</div>
                    <div className="step-content">
                      <h4>Get fast answers</h4>
                      <p>With reference pages from your manuals</p>
                    </div>
                  </div>
                </div>

                <div className="tip">
                  <span className="tip-icon">💡</span>
                  <span>Tip: Upload multiple manuals (owner's, workshop, parts) to improve answer accuracy.</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((msg, index) => (
                <div key={index} className={`message ${msg.type}`}>
                  {msg.type === 'user' && <div className="message-label">You</div>}
                  {msg.type === 'assistant' && <div className="message-label">AutoQuery</div>}
                  <div className="message-content">
                    {msg.content}
                    {msg.sources && msg.sources.length > 0 && (
                      <div className="sources">
                        <small>Sources: {msg.sources.join(', ')}</small>
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="message assistant">
                  <div className="message-label">AutoQuery</div>
                  <div className="message-content loading">
                    <span className="dot">.</span>
                    <span className="dot">.</span>
                    <span className="dot">.</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input area */}
        <div className="input-container">
          <div className="example-queries">
            <span className="example-label">Try asking:</span>
            <button className="example-query" onClick={() => setInputValue("How often to change spark plugs?")}>
              How often to change spark plugs?
            </button>
            <button className="example-query" onClick={() => setInputValue("Torque spec for front axle nut")}>
              Torque spec for front axle nut
            </button>
            <button className="example-query" onClick={() => setInputValue("Fuse box diagram location")}>
              Fuse box diagram location
            </button>
          </div>
          
          <div className="input-wrapper">
            <SearchIcon />
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder='Ask about a manual: "How to change timing belt on 2014 Accord?"'
              disabled={isLoading}
              rows={1}
            />
            <button 
              className="send-button" 
              onClick={handleSendMessage}
              disabled={isLoading || !inputValue.trim()}
            >
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </button>
          </div>
          
          <div className="input-hint">
            Press <kbd>Enter</kbd> to send, <kbd>Shift + Enter</kbd> for new line
          </div>
        </div>
        
        <footer className="app-footer">
          Built by Nancy | Internship Project
        </footer>
      </div>
    </div>
  );
}

export default App;