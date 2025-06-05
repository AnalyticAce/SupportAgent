# SupportAgent AI Chatbot Demo 🤖

A modern, interactive demo showcasing the SupportAgent AI-powered customer support system.

## 🌟 Features

### Modern UI/UX
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Smooth Animations**: Typing indicators, message transitions, and hover effects
- **Dark/Light Theme**: Clean, professional appearance
- **Real-time Stats**: Message counter and response time tracking

### AI Simulation
- **Intelligent Responses**: Context-aware replies based on message content
- **Multiple Response Variants**: Different responses to keep conversations dynamic
- **Smart Categorization**: Automatically detects topics (password, billing, account, etc.)
- **Realistic Timing**: Simulated response delays for authentic feel

### Interactive Elements
- **Quick Examples**: Pre-built common questions
- **Voice Recording**: Simulated microphone functionality (visual demo)
- **File Attachment**: Placeholder for future file upload feature
- **Emoji Support**: Placeholder for emoji picker
- **Clear Chat**: Reset conversation history

### Technical Features
- **API Integration**: Attempts to connect to real SupportAgent API at `localhost:8080`
- **Fallback Mode**: Uses intelligent mock responses when API isn't available
- **Error Handling**: Graceful degradation with user notifications
- **Toast Notifications**: Status updates and feedback messages

## 🚀 Quick Start

### 1. Start Your SupportAgent API (Optional)
```bash
cd /home/dosseh/Github/Agent/SupportAgent
python -m uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
```

### 2. Open the Demo
Simply open `demo/index.html` in your browser:

```bash
# From the demo directory
cd demo
python -m http.server 8000
# Then visit: http://localhost:8000
```

Or double-click `index.html` to open directly in your browser.

## 📱 Demo Modes

### API Mode (Recommended)
When your SupportAgent API is running:
- Real AI responses from GPT-4
- Actual RAG search functionality
- True intelligent escalation
- Live API status indicators

### Demo Mode (Fallback)
When API is not available:
- Intelligent mock responses
- Simulated AI behavior
- Category-based response selection
- Full UI functionality demonstration

## 🎯 Interactive Examples

Try these sample questions to see the AI in action:

### Account & Security
- "How do I reset my password?"
- "I cannot access my account"
- "My login isn't working"

### Billing & Subscriptions
- "What are the available subscription plans?"
- "How do I cancel my subscription?"
- "I need to update my billing information"

### Technical Support
- "The app is running slowly"
- "I'm getting error messages"
- "How do I integrate the API?"

## Customization

### Colors & Theming
Edit `style.css` to customize:
```css
:root {
    --primary-color: #6366f1;    /* Main brand color */
    --secondary-color: #10b981;  /* Success/accent color */
    --accent-color: #f59e0b;     /* Warning/highlight color */
}
```

### Mock Responses
Edit `script.js` to add new response categories:
```javascript
loadMockResponses() {
    return {
        'your_category': [
            "Response option 1",
            "Response option 2"
        ]
    };
}
```

### API Configuration
Update the API endpoint in `script.js`:
```javascript
constructor() {
    this.apiBaseUrl = 'http://your-api-domain.com';
}
```

## 🎉 Easter Eggs

### Konami Code
Try entering the classic Konami code: ↑↑↓↓←→←→BA
- Triggers a fun rainbow animation
- Shows achievement notification
- Demonstrates advanced interaction capabilities

### Dynamic Features
- **Auto-resizing input**: Text area grows with content
- **Typing simulation**: Realistic bot response timing
- **Message formatting**: Supports markdown-like syntax
- **Responsive stats**: Real-time counter updates

## 🔧 Technical Details

### File Structure
```
demo/
├── index.html      # Main HTML structure
├── style.css       # Modern CSS styling with animations
├── script.js       # Interactive JavaScript functionality
└── README.md       # This documentation
```

### Dependencies
- **Font Awesome 6.4.0**: Icons and visual elements
- **Google Fonts (Inter)**: Modern typography
- **Pure Vanilla JS**: No frameworks, maximum compatibility

### Browser Support
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+
- ✅ Mobile browsers

## Deployment Options

### 1. Static Hosting
Upload the `demo/` folder to any static hosting service:
- Netlify
- Vercel
- GitHub Pages
- AWS S3 + CloudFront

### 2. Local Development
```bash
# Python 3
python -m http.server 8000

# Node.js
npx serve .

# PHP
php -S localhost:8000
```

### 3. Integration
Embed into existing applications:
- Copy HTML structure
- Include CSS and JS files
- Customize API endpoints
- Adapt styling to match your brand

## Use Cases

### Sales Demos
- Showcase AI capabilities to potential customers
- Demonstrate response quality and speed
- Highlight modern UI/UX design

### Testing & Development
- Test API responses without building a full frontend
- Prototype new features and interactions
- Debug conversation flows

### Documentation
- Interactive examples for API documentation
- User training and onboarding
- Feature demonstration videos

### Design Reference
- UI/UX inspiration for other projects
- Component library examples
- Animation and interaction patterns

## Future Enhancements

- **Real voice recording** with speech-to-text
- **File upload** capability with drag-and-drop
- **Emoji picker** with custom reactions
- **Chat history** persistence
- **User authentication** integration
- **Multi-language** support
- **Dark mode** toggle
- **Export conversation** feature

---

**Happy chatting! 🚀** If you have questions or suggestions, feel free to reach out!
