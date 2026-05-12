/**
 * Chat interface for LLM with PDF document context
 * Connects to existing backend that handles PDF extraction and LLM responses
 */

const messagesContainer = document.getElementById('chatMessagesContainer');
const promptTextarea = document.getElementById('promptInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const errorContainer = document.getElementById('errorContainer');

let conversationHistory = []; 



function showError(message, isTemporary = true) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.innerText = message;
    errorContainer.innerHTML = '';
    errorContainer.appendChild(errorDiv);
    
    if (isTemporary) {
        setTimeout(() => {
            if (errorContainer.firstChild === errorDiv) {
                errorContainer.innerHTML = '';
            }
        }, 4500);
    }
}


function clearErrors() {
    errorContainer.innerHTML = '';
}


function escapeHtml(str) {
    if (!str) return '';
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}


function formatMessageContent(text) {
    if (!text) return '';
    let safe = escapeHtml(text);
    safe = safe.replace(/\n/g, '<br>');
    safe = safe.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    safe = safe.replace(/`(.*?)`/g, '<code style="background:#eef2f5;padding:2px 6px;border-radius:8px;">$1</code>');
    return safe;
}


function renderMessages() {
    if (!messagesContainer) return;
    messagesContainer.innerHTML = '';
    
    if (conversationHistory.length === 0) {
        const emptyDiv = document.createElement('div');
        emptyDiv.className = 'empty-chat';
        emptyDiv.id = 'emptyChatMsg';
        emptyDiv.innerHTML = '💬 Ask about your PDF documents — I\'ll answer based on the extracted content.<br><br>✨ Example: "What are the key findings?" or "Summarize the methodology."';
        messagesContainer.appendChild(emptyDiv);
        return;
    }
    
    for (let i = 0; i < conversationHistory.length; i++) {
        const msg = conversationHistory[i];
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${msg.role}`;
        
        const roleSpan = document.createElement('div');
        roleSpan.className = 'role-badge';
        roleSpan.innerText = msg.role === 'user' ? '👤 You' : '🤖 Assistant';
        
        const bubble = document.createElement('div');
        bubble.className = 'message-bubble';
        bubble.innerHTML = formatMessageContent(msg.content);
        
        msgDiv.appendChild(roleSpan);
        msgDiv.appendChild(bubble);
        messagesContainer.appendChild(msgDiv);
    }
    
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}


function addLoadingMessage() {
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'message assistant';
    loadingDiv.id = 'tempLoaderMsg';
    
    const badge = document.createElement('div');
    badge.className = 'role-badge';
    badge.innerText = '🤖 Assistant';
    
    const bubble = document.createElement('div');
    bubble.className = 'message-bubble';
    bubble.innerHTML = '<span class="thinking-indicator">✨ Thinking <span class="loader"></span></span>';
    
    loadingDiv.appendChild(badge);
    loadingDiv.appendChild(bubble);
    messagesContainer.appendChild(loadingDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    
    return 'tempLoaderMsg';
}


function removeLoadingMessage(loaderId) {
    const loader = document.getElementById(loaderId);
    if (loader) loader.remove();
}


async function sendToLLM(userMessage, previousMessages) {
    const API_URL = '/chat'; 
    
    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                message: userMessage,
                history: previousMessages,  
            })
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Server error (${response.status}): ${errorText}`);
        }
        
        const data = await response.json();
        
        if (data.response) return data.response;
        if (data.reply) return data.reply;
        if (data.message) return data.message;
        if (data.content) return data.content;
        
        console.warn('Unexpected response format:', data);
        return data.answer || "I received your message but couldn't parse the response format.";
        
    } catch (error) {
        console.error('LLM API Error:', error);
        
        if (error.message.includes('Failed to fetch')) {
            throw new Error(`Cannot connect to backend at ${API_URL}. Please ensure your LLM server is running and the endpoint is correct.`);
        }
        throw new Error(`LLM request failed: ${error.message}`);
    }
}


async function sendMessage() {
    const userMessage = promptTextarea.value.trim();
    
    if (!userMessage) {
        showError('Please enter a question before sending.', true);
        return;
    }
    
    clearErrors();
    
    conversationHistory.push({ role: 'user', content: userMessage });
    renderMessages();
    
    promptTextarea.value = '';
    promptTextarea.style.height = 'auto';
    
    const loaderId = addLoadingMessage();
    
    try {
        const assistantReply = await sendToLLM(userMessage, conversationHistory.slice(0, -1));
        
        removeLoadingMessage(loaderId);
        
        conversationHistory.push({ role: 'assistant', content: assistantReply });
        renderMessages();
        
    } catch (error) {
        removeLoadingMessage(loaderId);
        
        showError(error.message, true);
        
        conversationHistory.push({ 
            role: 'assistant', 
            content: `⚠️ Sorry, I encountered an error: ${error.message}. Please check your backend connection or try again.` 
        });
        renderMessages();
    }
}


async function clearChat() {
    conversationHistory = [];
    renderMessages();
    showError('Chat history cleared. Start a new conversation!', true);
    setTimeout(() => clearErrors(), 2000);
    
    try {
        const RESET_URL = '/clear';
        await fetch(RESET_URL, { method: 'POST', headers: { 'Content-Type': 'application/json' } });
    } catch (e) {
        console.debug('Backend clear endpoint not configured:', e);
    }
}

function handleKeyPress(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
}

function autoResizeTextarea() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 150) + 'px';
}

sendBtn.addEventListener('click', sendMessage);
clearBtn.addEventListener('click', clearChat);
promptTextarea.addEventListener('keydown', handleKeyPress);
promptTextarea.addEventListener('input', autoResizeTextarea);


renderMessages();

promptTextarea.focus();
