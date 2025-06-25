import React, { useState } from 'react';
import { Message } from './types';
import { ApiService } from './services/api';
import { Person } from '@mui/icons-material';
import './App.css';

const AgentIcon = () => (
  <div className="agent-icon">
    <img src="/logo.jpg" alt="Agent" />
  </div>
);

function App() {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [model, setModel] = useState<'gemini' | 'openai'>('gemini');

  const getCurrentTime = () => {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  const addMessage = (text: string, sender: Message['sender']) => {
    const message: Message = {
      sender,
      text,
      timestamp: getCurrentTime(),
    };
    setMessages((msgs) => [...msgs, message]);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedInput = input.trim();
    if (!trimmedInput || isLoading) return;

    // Add user message
    addMessage(trimmedInput, 'user');
    setInput('');
    setIsLoading(true);

    try {
      const response = await ApiService.classifyText(trimmedInput, model);
      if (response.result) {
        addMessage(response.result, 'agent');
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      const errorMessage = error instanceof Error 
        ? `Error: ${error.message}`
        : 'An unexpected error occurred';
      addMessage(errorMessage, 'agent');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="AppWideLayout">
      <aside className="sidebar">
        <div className="sidebar-content">
          <img src="/logo.jpg" alt="Sortz logo" className="brand" />
          <p className="sidebar-desc">AI Text Categorizer<br/>Type a message and let the agent sort it for you.</p>
        </div>
      </aside>
      <main className="main-chat-area">
        <header className="app-header">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', gap: 24 }}>
            <h2 style={{ margin: 0 }}>Chat with Sortz</h2>
            <div className="model-select-wrapper">
              <label htmlFor="model-select" className="model-select-label">Model:</label>
              <select
                id="model-select"
                value={model}
                onChange={e => setModel(e.target.value as 'gemini' | 'openai')}
                className="model-select"
                aria-label="Select AI model"
              >
                <option value="gemini">Gemini</option>
                <option value="openai">OpenAI</option>
              </select>
            </div>
          </div>
        </header>
        <section className="chat-area" aria-live="polite">
          {messages.length === 0 && (
            <div className="empty-chat">No messages yet. Start the conversation!</div>
          )}
          {messages.map((msg, idx) => (
            <div key={idx} className={`msg msg-${msg.sender}`}>  
              <div className="msg-meta">
                {msg.sender === 'user' ? (
                  <Person className="avatar user-avatar" />
                ) : (
                  <AgentIcon />
                )}
                <span className="sender">{msg.sender === 'user' ? 'You' : 'Agent'}</span>
                <span className="timestamp">{msg.timestamp}</span>
              </div>
              <div className="msg-text-wrapper" style={{ position: 'relative' }}>
                <div className="msg-text">{msg.text}</div>
                {msg.sender === 'agent' && (
                  <button
                    className="copy-btn"
                    style={{
                      position: 'absolute',
                      top: 6,
                      right: 6,
                      background: 'none',
                      border: 'none',
                      padding: 0,
                      cursor: 'pointer',
                      zIndex: 2
                    }}
                    title="Copy to clipboard"
                    onClick={() => navigator.clipboard.writeText(msg.text)}
                    aria-label="Copy agent message"
                  >
                    <svg width="18" height="18" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <rect x="6" y="6" width="9" height="9" rx="2" stroke="#3a8fff" strokeWidth="1.5" fill="#fff"/>
                      <rect x="3" y="3" width="9" height="9" rx="2" stroke="#3a8fff" strokeWidth="1.5" fill="#fff"/>
                    </svg>
                  </button>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="msg msg-agent">
              <div className="msg-meta">
                {isLoading && (
                  <>
                    <AgentIcon />
                    <span className="sender">Agent</span>
                    <span className="timestamp">{getCurrentTime()}</span>
                  </>
                )}
              </div>
              <div className="msg-text typing">Thinking...</div>
            </div>
          )}
        </section>
        <form className="input-area" onSubmit={handleSubmit} autoComplete="off">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message..."
            disabled={isLoading}
            autoFocus
            aria-label="Type your message"
          />
          <button 
            type="submit" 
            disabled={isLoading || !input.trim()}
            aria-label="Send message"
          >
            {isLoading ? 'Sending...' : 'Send'}
          </button>
        </form>
      </main>
    </div>
  );
}

export default App;
