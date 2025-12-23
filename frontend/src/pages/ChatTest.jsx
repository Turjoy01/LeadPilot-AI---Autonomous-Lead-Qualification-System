import { useState } from 'react';
import Sidebar from '../components/Sidebar';
import api from '../utils/api';

function ChatTest() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [loading, setLoading] = useState(false);
    const [sessionId] = useState(() => `test-${Date.now()}`);

    const handleSend = async (e) => {
        e.preventDefault();
        if (!input.trim()) return;

        const userMessage = { role: 'user', content: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setLoading(true);

        try {
            const response = await api.post('/chat/message', {
                message: input,
                session_id: sessionId,
                tenant_key: 'demo-key-12345'
            });

            const aiMessage = { role: 'assistant', content: response.data.message };
            setMessages(prev => [...prev, aiMessage]);
        } catch (error) {
            console.error('Error sending message:', error);
            const errorMessage = { role: 'error', content: 'Failed to get response' };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setLoading(false);
        }
    };

    const handleClear = () => {
        setMessages([]);
    };

    return (
        <div style={{ display: 'flex' }}>
            <Sidebar />
            <div style={{ marginLeft: '260px', flex: 1, padding: '2rem', minHeight: '100vh' }}>
                <div className="animate-slide-in">
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
                        <div>
                            <h1 className="text-3xl font-bold mb-2">Chat Test</h1>
                            <p style={{ color: 'var(--gray-400)' }}>
                                Test your AI chatbot and knowledge base responses
                            </p>
                        </div>
                        <button
                            onClick={handleClear}
                            className="btn"
                            style={{
                                background: 'rgba(239, 68, 68, 0.1)',
                                border: '1px solid var(--error)',
                                color: 'var(--error)'
                            }}
                        >
                            🗑️ Clear Chat
                        </button>
                    </div>

                    {/* Chat Container */}
                    <div className="card" style={{ height: 'calc(100vh - 250px)', display: 'flex', flexDirection: 'column' }}>
                        {/* Messages Area */}
                        <div style={{
                            flex: 1,
                            overflowY: 'auto',
                            padding: '1.5rem',
                            display: 'flex',
                            flexDirection: 'column',
                            gap: '1rem'
                        }}>
                            {messages.length === 0 ? (
                                <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--gray-400)' }}>
                                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>💬</div>
                                    <p>Start a conversation to test your AI chatbot</p>
                                    <p style={{ fontSize: '0.875rem', marginTop: '0.5rem' }}>
                                        Try asking about your services, pricing, or any information in your knowledge base
                                    </p>
                                </div>
                            ) : (
                                messages.map((msg, idx) => (
                                    <div
                                        key={idx}
                                        style={{
                                            display: 'flex',
                                            justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start'
                                        }}
                                    >
                                        <div
                                            style={{
                                                maxWidth: '70%',
                                                padding: '1rem',
                                                borderRadius: 'var(--radius-md)',
                                                background: msg.role === 'user'
                                                    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                                                    : msg.role === 'error'
                                                        ? 'rgba(239, 68, 68, 0.1)'
                                                        : 'rgba(99, 102, 241, 0.1)',
                                                border: msg.role === 'error' ? '1px solid var(--error)' : 'none',
                                                color: msg.role === 'error' ? 'var(--error)' : 'inherit'
                                            }}
                                        >
                                            <div style={{ fontSize: '0.75rem', marginBottom: '0.5rem', opacity: 0.7 }}>
                                                {msg.role === 'user' ? '👤 You' : msg.role === 'error' ? '⚠️ Error' : '🤖 AI'}
                                            </div>
                                            <div style={{ whiteSpace: 'pre-wrap' }}>{msg.content}</div>
                                        </div>
                                    </div>
                                ))
                            )}
                            {loading && (
                                <div style={{ display: 'flex', justifyContent: 'flex-start' }}>
                                    <div style={{
                                        padding: '1rem',
                                        borderRadius: 'var(--radius-md)',
                                        background: 'rgba(99, 102, 241, 0.1)'
                                    }}>
                                        <div className="gradient-text">AI is typing...</div>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Input Area */}
                        <form
                            onSubmit={handleSend}
                            style={{
                                padding: '1.5rem',
                                borderTop: '1px solid rgba(255, 255, 255, 0.1)',
                                display: 'flex',
                                gap: '1rem'
                            }}
                        >
                            <input
                                type="text"
                                className="input"
                                placeholder="Type your message..."
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                disabled={loading}
                                style={{ flex: 1 }}
                            />
                            <button
                                type="submit"
                                className="btn btn-primary"
                                disabled={loading || !input.trim()}
                            >
                                {loading ? '⏳' : '📤'} Send
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ChatTest;
