# LeadPilot AI — Autonomous Lead Qualification System

![LeadPilot AI](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green)
![React](https://img.shields.io/badge/React-18.2-blue)

**Turn anonymous website visitors into qualified leads automatically** using AI-powered chat, intelligent lead scoring, and instant sales notifications.

## 🚀 Features

### Core Capabilities
- ✅ **AI-Powered Chat Widget** - Embeddable on any website
- ✅ **Intelligent Lead Extraction** - Automatically captures name, email, phone, budget, timeline
- ✅ **Smart Lead Scoring** - Grades leads as HOT/WARM/COLD (0-100 score)
- ✅ **RAG-Based Answers** - Grounded responses from your knowledge base
- ✅ **Instant Email Alerts** - Notify sales team when hot leads arrive
- ✅ **Premium Admin Dashboard** - Manage leads, KB, and settings
- ✅ **Multi-Tenant Ready** - SaaS architecture from day one

### Success Metrics
- 📈 Lead capture rate ↑
- ⚡ Sales response time ↓
- 📉 Missed leads ↓
- 💰 Cost per lead ↓
- ✨ Answer quality ↑

## 🏗️ Architecture

```
┌─────────────────┐
│  Chat Widget    │ (Vanilla JS - Embeddable)
│  (Frontend)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   FastAPI       │ (Python - Async)
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┬──────────┬──────────┐
    ▼         ▼          ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│MongoDB │ │OpenAI│ │ Gmail  │ │ React  │
│ Atlas  │ │ API  │ │ SMTP   │ │ Admin  │
└────────┘ └──────┘ └────────┘ └────────┘
```

## 📦 Tech Stack

**Backend:**
- FastAPI (Python) - High-performance async API
- Motor - Async MongoDB driver
- OpenAI GPT-4 - AI agent & embeddings
- Pydantic - Data validation

**Frontend:**
- React 18 - Admin dashboard
- Vite - Fast build tool
- Vanilla JS - Embeddable widget

**Database:**
- MongoDB Atlas - Document store + Vector search

**Services:**
- Gmail SMTP - Email notifications
- OpenAI API - Chat & embeddings

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- MongoDB Atlas account
- OpenAI API key
- Gmail account with app password

### 1. Clone & Setup

```bash
cd "LeadPilot AI"
```

### 2. Backend Setup

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run backend (from project root)
uvicorn backend.main:app --reload
```

Backend will start at `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

```

## 📖 User Guide

### Getting Started

#### Step 1: Login to Admin Dashboard

1. Navigate to `http://localhost:5173/login`
2. Enter credentials:
   - **Email:** `admin@demo.com`
   - **Password:** `demo123`
3. Click "Login"

You'll be redirected to the dashboard showing lead statistics.

#### Step 2: Upload Knowledge Base Documents

The knowledge base powers AI responses. Upload your business information, FAQs, and product details.

1. Go to **Knowledge Base** section from sidebar
2. Fill in the form:
   - **Document Name:** `Product Information` (or any descriptive name)
   - **Content:** Paste your document content

**Example Content:**
```
Our company offers premium web development services. 

Services:
- Custom Website Development: Starting at $5,000
- E-commerce Solutions: Starting at $8,000
- Mobile App Development: Starting at $10,000

Timeline: Most projects are completed within 4-8 weeks.

Contact: We offer free consultations. Email us at sales@company.com or call +1-555-0123.
```

3. Click **Upload Document**
4. Document will be chunked and embedded for RAG retrieval

#### Step 3: Test the Chat Widget

1. Open `frontend/public/widget/demo.html` in your browser
2. Click the chat bubble in bottom-right corner
3. Start a conversation

**Example Conversation:**
```
User: Hi, what services do you offer?
AI: We offer premium web development services including:
- Custom Website Development (starting at $5,000)
- E-commerce Solutions (starting at $8,000)
- Mobile App Development (starting at $10,000)

User: I'm interested in a custom website. My name is John Doe.
AI: Great to meet you, John! I'd be happy to help with your custom website project.

User: My email is john@example.com and phone is +1-555-9999
AI: Thank you for providing your contact information.

User: I have a budget of around $6,000 and need it done in 6 weeks.
AI: Perfect! Your budget aligns well with our custom website development service...
```

4. Check the **Leads** section in admin dashboard
5. You should see the new lead with extracted information

#### Step 4: Embed Widget on Your Website

Copy this code and paste it before the `</body>` tag on your website:

```html
<!-- LeadPilot AI Chat Widget -->
<script>
  window.leadpilotConfig = {
    tenantKey: 'demo-key-12345',
    apiUrl: 'http://localhost:8000'
  };
</script>
<script src="http://localhost:5173/widget/leadpilot-widget.js"></script>
<link rel="stylesheet" href="http://localhost:5173/widget/widget.css">
```

### API Usage Examples

#### 1. Login and Get JWT Token

```bash
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@demo.com",
    "password": "demo123"
  }'
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### 2. Upload Knowledge Base Document

```bash
curl -X POST http://localhost:8000/v1/knowledge-base/upload \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "name": "Pricing Information",
    "content": "Our basic package starts at $1,000/month. Premium package is $5,000/month with dedicated support."
  }'
```

**Response:**
```json
{
  "document_id": "507f1f77bcf86cd799439011",
  "name": "Pricing Information",
  "chunks_count": 3,
  "created_at": "2024-12-14T10:30:00"
}
```

#### 3. Send Chat Message (Public Endpoint)

```bash
curl -X POST http://localhost:8000/v1/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What are your pricing plans?",
    "session_id": "test-session-123",
    "tenant_key": "demo-key-12345"
  }'
```

**Response:**
```json
{
  "response": "Our pricing plans include:\n- Basic Package: $1,000/month\n- Premium Package: $5,000/month with dedicated support",
  "lead_extracted": false
}
```

#### 4. Get All Leads

```bash
curl -X GET "http://localhost:8000/v1/leads?status=new&grade=HOT&limit=50" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
[
  {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-9999",
    "grade": "HOT",
    "score": 85,
    "status": "new",
    "service_interest": "Custom Website Development",
    "budget": "$6,000",
    "timeline": "6 weeks",
    "created_at": "2024-12-14T10:30:00"
  }
]
```

#### 5. Get Lead Details with Conversation

```bash
curl -X GET http://localhost:8000/v1/leads/507f1f77bcf86cd799439011 \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Response:**
```json
{
  "lead": {
    "id": "507f1f77bcf86cd799439011",
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1-555-9999",
    "grade": "HOT",
    "score": 85
  },
  "conversation": {
    "messages": [
      {
        "role": "user",
        "content": "Hi, what services do you offer?",
        "timestamp": "2024-12-14T10:25:00"
      },
      {
        "role": "assistant",
        "content": "We offer premium web development services...",
        "timestamp": "2024-12-14T10:25:02"
      }
    ]
  }
}
```

### Embed Widget on Your Website

Add this code before `</body>`:

```html
<!-- LeadPilot AI Chat Widget -->
<script>
  window.leadpilotConfig = {
    tenantKey: 'demo-key-12345',
    apiUrl: 'http://localhost:8000'
  };
</script>
<script src="http://localhost:5173/widget/leadpilot-widget.js"></script>
<link rel="stylesheet" href="http://localhost:5173/widget/widget.css">
```

## 🎯 How It Works

### Lead Capture Flow

1. **Visitor Opens Widget** → Loads tenant config & greeting
2. **Conversation Starts** → AI answers using RAG (knowledge base)
3. **Lead Extraction** → OpenAI function calling extracts fields
4. **Lead Scoring** → Multi-factor scoring (contact, budget, timeline, engagement)
5. **Hot Lead Alert** → If score ≥ 70, email sent to sales team
6. **CRM Storage** → All data saved in MongoDB

### Lead Scoring Algorithm

```
Score = Contact Info (30) + Budget (25) + Timeline (25) + Service (10) + Engagement (10)

Grades:
- HOT: Score ≥ 70
- WARM: Score ≥ 40
- COLD: Score < 40
```

## 📁 Project Structure

```
LeadPilot AI/
├── backend/
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Settings
│   ├── database.py             # MongoDB connection
│   ├── models/                 # Pydantic models
│   │   ├── tenant.py
│   │   ├── user.py
│   │   ├── lead.py
│   │   ├── conversation.py
│   │   └── kb_chunk.py
│   ├── routes/                 # API endpoints
│   │   ├── chat.py
│   │   ├── widget.py
│   │   ├── auth.py
│   │   ├── leads.py
│   │   └── knowledge_base.py
│   ├── services/               # Business logic
│   │   ├── ai_agent.py         # Core AI orchestration
│   │   ├── lead_extraction.py  # OpenAI function calling
│   │   ├── lead_scoring.py     # Scoring engine
│   │   ├── rag_service.py      # RAG retrieval
│   │   ├── kb_processor.py     # Document chunking
│   │   └── email_service.py    # SMTP notifications
│   └── utils/
│       ├── auth.py             # JWT authentication
│       ├── rate_limiter.py     # Rate limiting
│       └── logger.py           # Structured logging
├── frontend/
│   ├── src/
│   │   ├── pages/              # React pages
│   │   │   ├── Login.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Leads.jsx
│   │   │   ├── LeadDetail.jsx
│   │   │   ├── KnowledgeBase.jsx
│   │   │   └── Settings.jsx
│   │   ├── components/
│   │   │   └── Sidebar.jsx
│   │   ├── utils/
│   │   │   └── api.js          # Axios client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css           # Premium design system
│   └── public/
│       └── widget/             # Embeddable widget
│           ├── leadpilot-widget.js
│           ├── widget.css
│           └── demo.html
├── .env                        # Environment variables
├── .env.example                # Template
├── requirements.txt            # Python dependencies
└── README.md
```

## 🔐 Security

- ✅ JWT authentication for admin dashboard
- ✅ Rate limiting on public endpoints
- ✅ Environment variables for secrets
- ✅ CORS configuration
- ✅ Input validation with Pydantic
- ✅ MongoDB tenant isolation

## 🎨 Premium UI Features

- Glassmorphism effects
- Gradient backgrounds
- Smooth animations
- Responsive design
- Dark mode optimized
- Micro-interactions
- Premium typography (Inter font)

## 📧 Email Notifications

Hot leads (score ≥ 70) trigger instant email alerts with:
- Lead contact information
- Score and grade
- Service interest, budget, timeline
- Conversation transcript
- Beautiful HTML template

## 🧪 Testing

### Manual Testing Checklist

1. **Widget Test:**
   - Open `frontend/public/widget/demo.html`
   - Start conversation
   - Provide name, email, phone
   - Mention budget and timeline
   - Check lead appears in dashboard

2. **Email Test:**
   - Create high-value lead (budget: "high", timeline: "ASAP")
   - Check email received at configured address

3. **Knowledge Base Test:**
   - Upload sample document
   - Ask questions related to content
   - Verify grounded answers

## 🚀 Deployment

### Backend (Render/Railway)

```bash
# Build command
pip install -r requirements.txt

# Start command
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

### Frontend (Vercel/Netlify)

```bash
# Build command
cd frontend && npm install && npm run build

# Output directory
frontend/dist
```

## 🔧 Configuration

Edit `.env` file:

```env
# MongoDB
MONGODB_URI=your_mongodb_uri

# OpenAI
OPENAI_API_KEY=your_openai_key

# Email
GMAIL_ADDRESS=your_email
APP_PASSWORD=your_app_password

# JWT
JWT_SECRET=your_secret_key

# Thresholds
HOT_LEAD_THRESHOLD=70
WARM_LEAD_THRESHOLD=40
```

## 📊 API Endpoints

### Public Endpoints
- `POST /v1/chat/message` - Send chat message
- `GET /v1/widget/config` - Get widget configuration

### Protected Endpoints (Require JWT)
- `POST /v1/auth/login` - Login
- `GET /v1/leads` - List leads
- `GET /v1/leads/{id}` - Get lead details
- `PATCH /v1/leads/{id}` - Update lead
- `POST /v1/knowledge-base/upload` - Upload document
- `GET /v1/knowledge-base/documents` - List documents

## 🎯 Roadmap

- [ ] PDF upload support for knowledge base
- [ ] WhatsApp integration
- [ ] Advanced analytics dashboard
- [ ] A/B testing for greetings
- [ ] Multi-language support (Bangla)
- [ ] Slack notifications
- [ ] CRM integrations (HubSpot, Salesforce)

## 📝 License

MIT License - feel free to use for commercial projects!

## 🙏 Credits

Built with ❤️ using:
- FastAPI
- React
- OpenAI
- MongoDB

---

**LeadPilot AI** - Never miss a lead again! 🚀
<img width="1901" height="934" alt="image" src="https://github.com/user-attachments/assets/60b5d4d2-7c4f-4116-a3fe-9cf1c6e4e1ec" />

