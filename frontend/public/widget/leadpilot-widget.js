(function () {
    'use strict';

    // Configuration
    const config = window.leadpilotConfig || {
        tenantKey: 'demo-key-12345',
        apiUrl: 'http://localhost:8000'
    };

    // Session management
    let sessionId = localStorage.getItem('leadpilot_session_id');
    if (!sessionId) {
        sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        localStorage.setItem('leadpilot_session_id', sessionId);
    }

    // State
    let isOpen = false;
    let isTyping = false;
    let widgetConfig = null;

    // Create widget HTML
    function createWidget() {
        const container = document.createElement('div');
        container.id = 'leadpilot-widget-container';
        container.innerHTML = `
      <button id="leadpilot-chat-button" aria-label="Open chat">
        💬
      </button>
      <div id="leadpilot-chat-window">
        <div class="leadpilot-chat-header">
          <div>
            <h3 id="leadpilot-business-name">LeadPilot AI</h3>
            <p>We're here to help!</p>
          </div>
          <button class="leadpilot-close-button" aria-label="Close chat">×</button>
        </div>
        <div class="leadpilot-chat-messages" id="leadpilot-messages"></div>
        <div class="leadpilot-chat-input-container">
          <div class="leadpilot-chat-input-wrapper">
            <input 
              type="text" 
              class="leadpilot-chat-input" 
              id="leadpilot-input"
              placeholder="Type your message..."
              autocomplete="off"
            />
            <button class="leadpilot-send-button" id="leadpilot-send-btn" aria-label="Send message">
              ➤
            </button>
          </div>
        </div>
      </div>
    `;
        document.body.appendChild(container);
    }

    // Fetch widget configuration
    async function fetchConfig() {
        try {
            const response = await fetch(`${config.apiUrl}/v1/widget/config?tenant_key=${config.tenantKey}`);
            if (response.ok) {
                widgetConfig = await response.json();
                document.getElementById('leadpilot-business-name').textContent = widgetConfig.tenant_name;

                // Add greeting message
                if (widgetConfig.greeting) {
                    addMessage('assistant', widgetConfig.greeting);
                }
            }
        } catch (error) {
            console.error('LeadPilot: Failed to fetch config', error);
        }
    }

    // Add message to chat
    function addMessage(role, content) {
        const messagesContainer = document.getElementById('leadpilot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `leadpilot-message ${role}`;

        const contentDiv = document.createElement('div');
        contentDiv.className = 'leadpilot-message-content';
        contentDiv.textContent = content;

        messageDiv.appendChild(contentDiv);
        messagesContainer.appendChild(messageDiv);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Show typing indicator
    function showTyping() {
        if (isTyping) return;
        isTyping = true;

        const messagesContainer = document.getElementById('leadpilot-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'leadpilot-message assistant';
        typingDiv.id = 'leadpilot-typing';
        typingDiv.innerHTML = `
      <div class="leadpilot-typing-indicator">
        <span></span>
        <span></span>
        <span></span>
      </div>
    `;
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Hide typing indicator
    function hideTyping() {
        isTyping = false;
        const typingDiv = document.getElementById('leadpilot-typing');
        if (typingDiv) {
            typingDiv.remove();
        }
    }

    // Send message
    async function sendMessage(message) {
        if (!message.trim()) return;

        // Add user message
        addMessage('user', message);

        // Clear input
        document.getElementById('leadpilot-input').value = '';

        // Show typing
        showTyping();

        try {
            const response = await fetch(`${config.apiUrl}/v1/chat/message`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    session_id: sessionId,
                    tenant_key: config.tenantKey,
                    language: widgetConfig?.language || 'en'
                })
            });

            hideTyping();

            if (response.ok) {
                const data = await response.json();
                addMessage('assistant', data.message);

                // Update session ID if new
                if (data.session_id && data.session_id !== sessionId) {
                    sessionId = data.session_id;
                    localStorage.setItem('leadpilot_session_id', sessionId);
                }
            } else {
                addMessage('assistant', 'Sorry, I encountered an error. Please try again.');
            }
        } catch (error) {
            hideTyping();
            console.error('LeadPilot: Failed to send message', error);
            addMessage('assistant', 'Sorry, I\'m having trouble connecting. Please try again later.');
        }
    }

    // Toggle chat window
    function toggleChat() {
        isOpen = !isOpen;
        const chatWindow = document.getElementById('leadpilot-chat-window');
        const chatButton = document.getElementById('leadpilot-chat-button');

        if (isOpen) {
            chatWindow.classList.add('open');
            chatButton.textContent = '💬';
            document.getElementById('leadpilot-input').focus();
        } else {
            chatWindow.classList.remove('open');
            chatButton.textContent = '💬';
        }
    }

    // Initialize widget
    function init() {
        createWidget();
        fetchConfig();

        // Event listeners
        document.getElementById('leadpilot-chat-button').addEventListener('click', toggleChat);
        document.querySelector('.leadpilot-close-button').addEventListener('click', toggleChat);

        document.getElementById('leadpilot-send-btn').addEventListener('click', () => {
            const input = document.getElementById('leadpilot-input');
            sendMessage(input.value);
        });

        document.getElementById('leadpilot-input').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage(e.target.value);
            }
        });
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
