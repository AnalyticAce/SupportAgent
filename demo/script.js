// SupportAgent Chatbot Demo JavaScript
class SupportAgentDemo {
    constructor() {
        this.apiBaseUrl = 'http://localhost:8080';
        this.messageCount = 0;
        this.isTyping = false;
        this.responses = this.loadMockResponses();
        this.init();
    }

    init() {
        this.updateStats();
        this.checkApiConnection();
        this.addEventListeners();
        
        // Show loading overlay briefly on initial load
        this.showLoading();
        setTimeout(() => this.hideLoading(), 1500);
    }

    addEventListeners() {
        // Auto-resize input
        const input = document.getElementById('messageInput');
        input.addEventListener('input', this.autoResizeInput.bind(this));
        
        // Focus input on page load
        setTimeout(() => input.focus(), 1000);
    }

    // Mock responses for demo purposes when API is not available
    loadMockResponses() {
        return {
            'password': [
                "I can help you reset your password! Here's how:\n\n1. Go to the login page\n2. Click 'Forgot Password?'\n3. Enter your email address\n4. Check your email for reset instructions\n5. Follow the link to create a new password\n\nIf you don't receive the email within 5 minutes, please check your spam folder. Would you like me to help with anything else?",
                "To reset your password securely:\n\n🔐 **Quick Reset Steps:**\n• Visit our password reset page\n• Enter your registered email\n• Click the verification link sent to your email\n• Create a strong new password\n\n**Security Tips:**\n• Use a mix of letters, numbers, and symbols\n• Make it at least 12 characters long\n• Don't reuse old passwords\n\nNeed help with anything else?"
            ],
            'subscription': [
                "Here are our current subscription plans:\n\n💎 **Premium Plan** - $29/month\n• Unlimited support requests\n• Priority response (< 1 hour)\n• Advanced AI features\n• Custom integrations\n\n⭐ **Standard Plan** - $15/month\n• Up to 100 support requests/month\n• Standard response time (< 24 hours)\n• Basic AI features\n\n🆓 **Free Plan** - $0/month\n• Up to 10 support requests/month\n• Community support\n\nWould you like to upgrade or learn more about any specific plan?",
                "Our subscription options are designed to fit your needs:\n\n**🚀 Enterprise** - Custom pricing\n• Unlimited everything\n• Dedicated account manager\n• Custom SLA agreements\n• White-label options\n\n**🏢 Business** - $99/month\n• Up to 10 team members\n• Advanced analytics\n• API access\n• Integration support\n\n**👤 Individual** - $19/month\n• Personal use\n• Standard features\n• Email support\n\nInterested in a specific plan? I can help you get started!"
            ],
            'account': [
                "I understand you're having trouble accessing your account. Let me help you troubleshoot:\n\n🔍 **Common Solutions:**\n\n1. **Password Issues:**\n   • Try the 'Forgot Password' option\n   • Check if Caps Lock is on\n   • Clear browser cache and cookies\n\n2. **Email Verification:**\n   • Check if your email is verified\n   • Look for verification emails in spam\n\n3. **Account Status:**\n   • Ensure your subscription is active\n   • Check for any security holds\n\n4. **Browser Issues:**\n   • Try a different browser\n   • Disable browser extensions\n   • Use incognito/private mode\n\nIf none of these work, I can escalate this to our technical team. What specific error are you seeing?",
                "Account access issues can be frustrating! Let's get this sorted:\n\n**🛠️ Diagnostic Steps:**\n\n**Step 1:** Verify your login credentials\n• Username/email correct?\n• Password entered correctly?\n\n**Step 2:** Check account status\n• Is your subscription active?\n• Any recent password changes?\n\n**Step 3:** Technical check\n• Clear browser data\n• Try different device/network\n• Disable VPN if using one\n\n**🚨 If urgent:** I can create a temporary access link for you while we resolve the main issue.\n\nWhat's the exact error message you're seeing when trying to log in?"
            ],
            'cancel': [
                "I'm sorry to hear you're considering canceling your subscription. Before we proceed, let me see if I can help address any concerns:\n\n**💭 Common reasons for cancellation:**\n• Not using all features → I can show you hidden gems!\n• Too expensive → Let's discuss our discount options\n• Technical issues → Our team can resolve these quickly\n• Changed needs → Maybe a different plan fits better?\n\n**📋 If you still want to cancel:**\n1. Go to Account Settings\n2. Click 'Subscription'\n3. Select 'Cancel Subscription'\n4. Follow the prompts\n\n**⏰ Important notes:**\n• You'll keep access until your billing cycle ends\n• We offer a 30-day grace period for reactivation\n• All your data will be preserved for 90 days\n\nWould you like to discuss what's not working for you, or shall I proceed with cancellation steps?",
                "I understand you want to cancel your subscription. Let me make this process smooth for you:\n\n**🎯 Quick Cancellation Process:**\n\n1. **Immediate cancellation:**\n   • Account → Billing → Cancel Subscription\n   • Confirm cancellation reason (helps us improve!)\n   • You'll receive a confirmation email\n\n2. **What happens next:**\n   • ✅ Service continues until billing cycle ends\n   • ✅ No future charges\n   • ✅ Data export available for 90 days\n   • ✅ Easy reactivation if you change your mind\n\n**🎁 Before you go:**\n• Would a 50% discount for 3 months help?\n• Or maybe switching to our free plan?\n• We also have a pause option (up to 6 months)\n\nShall I process the cancellation or explore alternatives?"
            ],
            'default': [
                "Thank you for reaching out! I'm here to help with any questions about your account, subscriptions, technical issues, or general support.\n\n**I can assist with:**\n• 🔐 Password resets and login issues\n• 💳 Billing and subscription management\n• 🛠️ Technical troubleshooting\n• 📞 Account settings and preferences\n• 🎯 Feature explanations and tutorials\n\nCould you please provide more details about what you need help with today?",
                "Hello! I'm your AI support assistant, powered by GPT-4 and ready to help!\n\n**✨ How I can help you today:**\n\n🔧 **Technical Support**\n• Troubleshoot issues\n• Configuration help\n• Performance optimization\n\n💼 **Account Management**\n• Subscription changes\n• Billing inquiries\n• Security settings\n\n📚 **Information & Guidance**\n• Feature tutorials\n• Best practices\n• FAQ answers\n\nWhat would you like assistance with? Feel free to be as specific as possible!",
                "Great question! I'm here to provide intelligent support using advanced AI capabilities.\n\n**🤖 My AI Features:**\n• **Contextual Understanding:** I remember our conversation\n• **Smart Search:** I can find relevant information quickly\n• **Risk Assessment:** I identify when issues need escalation\n• **Personalized Help:** Tailored to your account and needs\n\n**🎯 Popular topics I help with:**\n• Account access and security\n• Subscription and billing questions\n• Technical troubleshooting\n• Feature requests and feedback\n\nWhat specific topic can I help you explore today?"
            ]
        };
    }

    async checkApiConnection() {
        try {
            const response = await fetch(`${this.apiBaseUrl}/health`);
            if (response.ok) {
                const data = await response.json();
                this.showToast(`✅ Connected to ${data.service} v${data.version}`, 'success');
                console.log('API Connection successful:', data);
            } else {
                this.showToast('API connection issues - Using demo mode', 'error');
            }
        } catch (error) {
            console.log('API not available, using demo mode:', error.message);
            this.showToast('🎭 Demo Mode - Simulated AI responses', 'info');
        }
    }

    handleKeyPress(event) {
        if (event.key === 'Enter' && !event.shiftKey) {
            event.preventDefault();
            this.sendMessage();
        }
    }

    autoResizeInput() {
        const input = document.getElementById('messageInput');
        input.style.height = 'auto';
        input.style.height = Math.min(input.scrollHeight, 120) + 'px';
    }

    sendExample(message) {
        document.getElementById('messageInput').value = message;
        this.sendMessage();
    }

    async sendMessage() {
        const input = document.getElementById('messageInput');
        const message = input.value.trim();
        
        if (!message) return;

        // Clear input and reset height
        input.value = '';
        input.style.height = 'auto';

        // Add user message
        this.addMessage(message, 'user');
        this.messageCount++;
        this.updateStats();

        // Show typing indicator
        this.showTyping();

        try {
            // Try to call the real API first
            const response = await this.callSupportAPI(message);
            
            setTimeout(() => {
                this.hideTyping();
                this.addMessage(response, 'bot');
                this.showToast('✨ Response from AI agent', 'success');
            }, 1000 + Math.random() * 1000); // Simulate realistic response time
            
        } catch (error) {
            // Fall back to mock responses
            console.log('API call failed, using mock response:', error.message);
            const response = this.generateMockResponse(message);
            
            setTimeout(() => {
                this.hideTyping();
                this.addMessage(response, 'bot');
                this.showToast('🎭 Using demo response', 'warning');
            }, 1200 + Math.random() * 800);
        }
    }

    async callSupportAPI(message) {
        const response = await fetch(`${this.apiBaseUrl}/agent/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: 3,
                query: message
            })
        });

        if (!response.ok) {
            throw new Error(`API call failed: ${response.status}`);
        }

        const data = await response.json();
        
        // Format the response to include escalation info if needed
        let formattedResponse = data.support_advice || 'I received your message but had trouble generating a response.';
        
        if (data.escalation_required) {
            formattedResponse += `\n\n⚠️ **Escalation Required** (Risk Level: ${data.risk_level}/10)\nThis issue has been flagged for human review.`;
        }
        
        return formattedResponse;
    }

    generateMockResponse(message) {
        const lowerMessage = message.toLowerCase();
        
        // Determine response category based on keywords
        let category = 'default';
        if (lowerMessage.includes('password') || lowerMessage.includes('reset') || lowerMessage.includes('login')) {
            category = 'password';
        } else if (lowerMessage.includes('subscription') || lowerMessage.includes('plan') || lowerMessage.includes('upgrade') || lowerMessage.includes('billing')) {
            category = 'subscription';
        } else if (lowerMessage.includes('account') || lowerMessage.includes('access') || lowerMessage.includes('cannot') || lowerMessage.includes("can't")) {
            category = 'account';
        } else if (lowerMessage.includes('cancel') || lowerMessage.includes('unsubscribe') || lowerMessage.includes('stop')) {
            category = 'cancel';
        }

        // Get random response from category
        const responses = this.responses[category];
        const randomIndex = Math.floor(Math.random() * responses.length);
        return responses[randomIndex];
    }

    addMessage(content, sender) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}-message`;

        const avatar = document.createElement('div');
        avatar.className = 'message-avatar';
        avatar.innerHTML = sender === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const header = document.createElement('div');
        header.className = 'message-header';
        
        const senderName = document.createElement('span');
        senderName.className = 'sender-name';
        senderName.textContent = sender === 'user' ? 'You' : 'SupportAgent AI';
        
        const timestamp = document.createElement('span');
        timestamp.className = 'message-time';
        timestamp.textContent = new Date().toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        header.appendChild(senderName);
        header.appendChild(timestamp);

        const textDiv = document.createElement('div');
        textDiv.className = 'message-text';
        
        // Format message content (support markdown-like formatting)
        const formattedContent = this.formatMessage(content);
        textDiv.innerHTML = formattedContent;

        contentDiv.appendChild(header);
        contentDiv.appendChild(textDiv);

        messageElement.appendChild(avatar);
        messageElement.appendChild(contentDiv);

        messagesContainer.appendChild(messageElement);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // Add read receipt animation for bot messages
        if (sender === 'bot') {
            setTimeout(() => {
                messageElement.style.opacity = '0.8';
                setTimeout(() => {
                    messageElement.style.opacity = '1';
                }, 100);
            }, 500);
        }
    }

    formatMessage(content) {
        // Convert simple markdown-like formatting to HTML
        let formatted = content
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/###\s*(.*?)$/gm, '<h4>$1</h4>')
            .replace(/##\s*(.*?)$/gm, '<h3>$1</h3>')
            .replace(/^•\s*(.*?)$/gm, '<li>$1</li>')
            .replace(/^(\d+\.)\s*(.*?)$/gm, '<li>$2</li>')
            .replace(/\n/g, '<br>');

        // Wrap consecutive <li> elements in <ul>
        formatted = formatted.replace(/(<li>.*?<\/li>(?:<br><li>.*?<\/li>)*)/g, '<ul>$1</ul>');
        formatted = formatted.replace(/<br><li>/g, '<li>');
        formatted = formatted.replace(/<\/li><br>/g, '</li>');

        return formatted;
    }

    showTyping() {
        const indicator = document.getElementById('typingIndicator');
        indicator.classList.add('show');
        this.isTyping = true;
    }

    hideTyping() {
        const indicator = document.getElementById('typingIndicator');
        indicator.classList.remove('show');
        this.isTyping = false;
    }

    showLoading() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.classList.add('show');
    }

    hideLoading() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.classList.remove('show');
    }

    updateStats() {
        document.getElementById('messageCount').textContent = this.messageCount;
        
        // Simulate dynamic response time
        const responseTime = (1.0 + Math.random() * 0.8).toFixed(1);
        document.getElementById('responseTime').textContent = `~${responseTime}s`;
    }

    showToast(message, type = 'info') {
        const container = document.getElementById('toastContainer');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <div style="display: flex; align-items: center; gap: 8px;">
                <i class="fas fa-${this.getToastIcon(type)}"></i>
                <span>${message}</span>
            </div>
        `;

        container.appendChild(toast);

        // Auto-remove after 4 seconds
        setTimeout(() => {
            toast.style.animation = 'toastSlide 0.3s ease-out reverse';
            setTimeout(() => {
                container.removeChild(toast);
            }, 300);
        }, 4000);
    }

    getToastIcon(type) {
        switch (type) {
            case 'success': return 'check-circle';
            case 'error': return 'exclamation-circle';
            case 'warning': return 'exclamation-triangle';
            default: return 'info-circle';
        }
    }

    clearChat() {
        const messagesContainer = document.getElementById('chatMessages');
        const welcomeMessage = messagesContainer.querySelector('.welcome-message');
        
        // Remove all messages except welcome message
        messagesContainer.innerHTML = '';
        messagesContainer.appendChild(welcomeMessage);
        
        this.messageCount = 0;
        this.updateStats();
        this.showToast('Chat cleared successfully', 'success');
    }

    showApiDocs() {
        window.open(`${this.apiBaseUrl}/docs`, '_blank');
    }

    toggleMicrophone() {
        const micButton = document.getElementById('micButton');
        const isActive = micButton.classList.contains('active');
        
        if (isActive) {
            micButton.classList.remove('active');
            micButton.innerHTML = '<i class="fas fa-microphone"></i>';
            this.showToast('Voice recording stopped', 'info');
        } else {
            micButton.classList.add('active');
            micButton.innerHTML = '<i class="fas fa-microphone-slash"></i>';
            this.showToast('Voice recording started (demo)', 'info');
            
            // Auto-disable after 5 seconds in demo
            setTimeout(() => {
                if (micButton.classList.contains('active')) {
                    this.toggleMicrophone();
                }
            }, 5000);
        }
    }

    attachFile() {
        this.showToast('File attachment feature coming soon!', 'info');
    }

    toggleEmoji() {
        this.showToast('😊 Emoji picker coming soon! 🚀', 'info');
    }
}

// Global functions (called by HTML elements)
function sendMessage() {
    demo.sendMessage();
}

function sendExample(message) {
    demo.sendExample(message);
}

function handleKeyPress(event) {
    demo.handleKeyPress(event);
}

function clearChat() {
    demo.clearChat();
}

function showApiDocs() {
    demo.showApiDocs();
}

function toggleMicrophone() {
    demo.toggleMicrophone();
}

function attachFile() {
    demo.attachFile();
}

function toggleEmoji() {
    demo.toggleEmoji();
}

// Initialize the demo when the page loads
let demo;
document.addEventListener('DOMContentLoaded', () => {
    demo = new SupportAgentDemo();
});

// Add some fun easter eggs
document.addEventListener('keydown', (event) => {
    // Konami code: ↑↑↓↓←→←→BA
    const konamiCode = [38, 38, 40, 40, 37, 39, 37, 39, 66, 65];
    window.konamiProgress = window.konamiProgress || 0;
    
    if (event.keyCode === konamiCode[window.konamiProgress]) {
        window.konamiProgress++;
        if (window.konamiProgress === konamiCode.length) {
            demo.showToast('🎉 Konami Code activated! You found the easter egg!', 'success');
            window.konamiProgress = 0;
            
            // Add some fun visual effects
            document.body.style.animation = 'rainbow 2s ease-in-out';
            setTimeout(() => {
                document.body.style.animation = '';
            }, 2000);
        }
    } else {
        window.konamiProgress = 0;
    }
});

// Add rainbow animation for easter egg
const style = document.createElement('style');
style.textContent = `
    @keyframes rainbow {
        0% { filter: hue-rotate(0deg); }
        25% { filter: hue-rotate(90deg); }
        50% { filter: hue-rotate(180deg); }
        75% { filter: hue-rotate(270deg); }
        100% { filter: hue-rotate(360deg); }
    }
`;
document.head.appendChild(style);
