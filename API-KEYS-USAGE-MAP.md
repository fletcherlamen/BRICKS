# API Keys Usage Map - Where Each Key is Used

## 📍 Overview

This document shows **exactly where** each API key is used in the I PROACTIVE BRICK Orchestration Intelligence project.

---

## 🔑 1. OPENAI_API_KEY (⭐ CRITICAL)

### Where It's Used:

#### A. **RealOrchestrator** (`backend/app/services/real_orchestrator.py`)
```python
Lines 34-40:
self.openai_api_key = os.getenv("OPENAI_API_KEY")
if self.openai_api_key:
    self.available_ai_services.append("openai")

Lines 137-168: _call_openai() method
- Direct API calls to OpenAI GPT-4 and GPT-3.5
- Used for strategic analysis
- Endpoint: https://api.openai.com/v1/chat/completions
```

#### B. **MultiModelRouter** (`backend/app/services/multi_model_router.py`)
```python
Lines 44-60:
if settings.OPENAI_API_KEY:
    import openai
    self.models["gpt-4"] = {
        "client": openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY),
        "model": "gpt-4"
    }
    self.models["gpt-3.5-turbo"] = {
        "client": openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY),
        "model": "gpt-3.5-turbo"
    }
```

### What It Powers:
- ✅ **Real AI Strategic Analysis** via Orchestration page
- ✅ **GPT-4** for complex reasoning and strategic planning
- ✅ **GPT-3.5 Turbo** for quick general tasks
- ✅ **Multi-Model Router** intelligent task routing
- ✅ **Chat functionality** with real AI responses
- ✅ **BRICK development proposals** generation
- ✅ **Revenue optimization analysis**
- ✅ **Strategic gap detection**

### API Calls:
```
POST https://api.openai.com/v1/chat/completions
Headers:
  Authorization: Bearer {OPENAI_API_KEY}
  Content-Type: application/json
Body:
  {
    "model": "gpt-4" or "gpt-3.5-turbo",
    "messages": [...],
    "max_tokens": 1000,
    "temperature": 0.7
  }
```

---

## 🔑 2. ANTHROPIC_API_KEY (⭐ HIGHLY RECOMMENDED)

### Where It's Used:

#### A. **RealOrchestrator** (`backend/app/services/real_orchestrator.py`)
```python
Lines 35-42:
self.anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
if self.anthropic_api_key:
    self.available_ai_services.append("anthropic")

Lines 170-201: _call_anthropic() method
- Direct API calls to Claude 3 models
- Used for high-quality reasoning
- Endpoint: https://api.anthropic.com/v1/messages
```

#### B. **MultiModelRouter** (`backend/app/services/multi_model_router.py`)
```python
Lines 66-85:
if settings.ANTHROPIC_API_KEY:
    import anthropic
    self.models["claude-3-opus"] = {
        "client": anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY),
        "model": "claude-3-opus-20240229"
    }
    self.models["claude-3-sonnet"] = {
        "client": anthropic.AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY),
        "model": "claude-3-sonnet-20240229"
    }
```

### What It Powers:
- ✅ **Claude 3 Opus** for highest quality strategic analysis
- ✅ **Claude 3 Sonnet** for balanced performance
- ✅ **Claude 3 Haiku** (future) for fast cost-effective tasks
- ✅ **Multi-Model Router** quality-optimized routing
- ✅ **Complex reasoning tasks**
- ✅ **Code generation and analysis**
- ✅ **Long-context understanding**

### API Calls:
```
POST https://api.anthropic.com/v1/messages
Headers:
  x-api-key: {ANTHROPIC_API_KEY}
  Content-Type: application/json
  anthropic-version: 2023-06-01
Body:
  {
    "model": "claude-3-opus-20240229" or "claude-3-sonnet-20240229",
    "max_tokens": 1000,
    "messages": [...]
  }
```

---

## 🔑 3. GOOGLE_GEMINI_API_KEY (⭐ RECOMMENDED)

### Where It's Used:

#### A. **RealOrchestrator** (`backend/app/services/real_orchestrator.py`)
```python
Lines 36-45:
self.google_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
if self.google_api_key:
    self.available_ai_services.append("google")

Lines 203-230: _call_google() method
- Direct API calls to Google Gemini
- Used for cost-effective tasks
```

#### B. **MultiModelRouter** (`backend/app/services/multi_model_router.py`)
```python
Lines 88-101:
if settings.GOOGLE_GEMINI_API_KEY:
    import google.generativeai as genai
    genai.configure(api_key=settings.GOOGLE_GEMINI_API_KEY)
    self.models["gemini-pro"] = {
        "client": genai.GenerativeModel('gemini-pro'),
        "model": "gemini-pro"
    }
```

### What It Powers:
- ✅ **Gemini Pro** for cost-effective general tasks
- ✅ **Gemini Ultra** (future) for high-quality reasoning
- ✅ **Multi-Model Router** cost-optimized routing
- ✅ **Multimodal capabilities** (text + images)
- ✅ **Fast creative tasks**
- ✅ **Budget-conscious operations**

### API Usage:
```python
import google.generativeai as genai
genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(prompt)
```

---

## 🔑 4. MEM0_API_KEY (✅ CONFIGURED)

### Where It's Used:

#### A. **Mem0Service** (`backend/app/services/mem0_service.py`)
```python
Lines 35-47:
if not settings.MEM0_API_KEY:
    logger.warning("Mem0 API key not configured, running in mock mode")
    return

self.client = mem0.Mem0(
    api_key=settings.MEM0_API_KEY,
    base_url=settings.MEM0_BASE_URL
)
```

#### B. **AIOrchestrator** (`backend/app/services/ai_orchestrator.py`)
```python
Lines 75-76:
if settings.MEM0_API_KEY:
    tasks.append(self._init_mem0())
```

### What It Powers:
- ✅ **Enhanced AI Memory** - better context retention
- ✅ **Cross-session memory** - remembers past conversations
- ✅ **Intelligent context storage** - stores relevant information
- ✅ **Memory retrieval** - retrieves context for AI responses
- ✅ **User-specific memory** - personalized AI responses
- ✅ **Long-term learning** - AI learns from interactions

### Key Methods Using This:
```python
Lines 53-102: store_context()
  - Stores orchestration context in Mem0
  
Lines 104-155: store_result()
  - Stores orchestration results with metadata
  
Lines 157-219: retrieve_relevant_memories()
  - Retrieves relevant memories for AI context
  
Lines 221-272: search_memories()
  - Searches stored memories by query
```

### What Happens WITHOUT Mem0 Key:
- ⚠️ Falls back to VPS database-only memory
- ⚠️ Less sophisticated context understanding
- ⚠️ No cross-AI-service memory sharing
- ✅ Basic memory still works via PostgreSQL

---

## 🔑 5. CREWAI_API_KEY (⚠️ OPTIONAL)

### Where It's Used:

#### A. **CrewAIService** (`backend/app/services/crewai_service.py`)
```python
Lines 37-40:
if not settings.CREWAI_API_KEY:
    logger.warning("CrewAI API key not configured, running in mock mode")
    return
```

#### B. **AIOrchestrator** (`backend/app/services/ai_orchestrator.py`)
```python
Lines 73-74:
if settings.CREWAI_API_KEY:
    tasks.append(self._init_crewai())
```

### What It Powers (When Configured):
- 🔷 **Multi-agent orchestration** - specialized AI agents working together
- 🔷 **Strategic analysis crew** - multiple AI agents for strategy
- 🔷 **BRICK development planning** - coordinated development tasks
- 🔷 **Complex task decomposition** - breaking down big tasks

### Mock Mode (Without Key):
- ✅ Enhanced mock implementation provides intelligent responses
- ✅ System works perfectly without this key
- ✅ All features remain functional

---

## 🔑 6. DEVIN_API_KEY (⚠️ OPTIONAL)

### Where It's Used:

#### A. **DevinService** (`backend/app/services/devin_service.py`)
```python
Checks for DEVIN_API_KEY on initialization
If not present: Uses EnhancedMockDevinClient
If present: Uses RealDevinClient
```

#### B. **AIOrchestrator** (`backend/app/services/ai_orchestrator.py`)
```python
Lines 77-78:
if settings.DEVIN_API_KEY:
    tasks.append(self._init_devin())
```

### What It Powers (When Configured):
- 🔷 **Autonomous code development** - AI writes code automatically
- 🔷 **Code optimization** - improves existing code
- 🔷 **Test generation** - creates automated tests
- 🔷 **Bug fixing** - identifies and fixes issues

### Mock Mode (Without Key):
- ✅ EnhancedMockDevinClient provides realistic mock responses
- ✅ Code generation templates
- ✅ Optimization suggestions
- ✅ Test generation patterns

---

## 🔑 7. COPILOT_STUDIO_API_KEY (⚠️ OPTIONAL)

### Where It's Used:

#### A. **CopilotService** (`backend/app/services/copilot_service.py`)
```python
Checks for COPILOT_STUDIO_API_KEY on initialization
If not present: Uses EnhancedMockCopilotClient
If present: Uses RealCopilotClient
```

#### B. **AIOrchestrator** (`backend/app/services/ai_orchestrator.py`)
```python
Lines 79-80:
if settings.COPILOT_STUDIO_API_KEY:
    tasks.append(self._init_copilot())
```

### What It Powers (When Configured):
- 🔷 **Enterprise workflow automation**
- 🔷 **Microsoft integration**
- 🔷 **Business process automation**
- 🔷 **Workflow orchestration**

### Mock Mode (Without Key):
- ✅ EnhancedMockCopilotClient provides enterprise workflow templates
- ✅ All features work in mock mode

---

## 🔑 8. GITHUB_COPILOT_TOKEN (⚠️ OPTIONAL)

### Where It's Used:

#### A. **GitHubCopilotService** (`backend/app/services/github_copilot_service.py`)
```python
Uses GITHUB_COPILOT_TOKEN for GitHub API authentication
If not present: Uses EnhancedMockGitHubCopilotClient
If present: Uses RealGitHubCopilotClient
```

#### B. **AIOrchestrator** (`backend/app/services/ai_orchestrator.py`)
```python
Lines 81-82:
if settings.GITHUB_COPILOT_TOKEN:
    tasks.append(self._init_github_copilot())
```

### What It Powers (When Configured):
- 🔷 **GitHub repository management**
- 🔷 **CI/CD pipeline automation**
- 🔷 **Pull request automation**
- 🔷 **Code review automation**

### Mock Mode (Without Key):
- ✅ EnhancedMockGitHubCopilotClient provides repository management templates

---

## 📊 API Keys Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                     USER REQUEST                                │
│                  (via Frontend/API)                             │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                  AI ORCHESTRATOR                                │
│              (ai_orchestrator.py)                               │
└────────────────────────┬────────────────────────────────────────┘
                         ↓
         ┌───────────────┴───────────────┐
         ↓                               ↓
┌──────────────────────┐       ┌──────────────────────┐
│  MULTI-MODEL ROUTER  │       │  REAL ORCHESTRATOR   │
│(multi_model_router.py)│       │(real_orchestrator.py)│
└──────────┬───────────┘       └──────────┬───────────┘
           ↓                               ↓
    ┌──────┴──────┬──────────┬────────┐   │
    ↓             ↓          ↓        ↓   ↓
┌─────────┐ ┌──────────┐ ┌───────┐ ┌──────────┐
│ OpenAI  │ │Anthropic │ │Google │ │  Mem0.ai │
│ GPT-4   │ │ Claude   │ │Gemini │ │  Memory  │
│         │ │          │ │       │ │          │
│ Uses:   │ │ Uses:    │ │ Uses: │ │ Uses:    │
│ OPENAI_ │ │ANTHROPIC_│ │GOOGLE_│ │ MEM0_    │
│ API_KEY │ │ API_KEY  │ │GEMINI │ │ API_KEY  │
└─────────┘ └──────────┘ └───────┘ └──────────┘
                         ↓
┌─────────────────────────────────────────────────────────────────┐
│                  VPS DATABASE                                   │
│        (All results persisted to PostgreSQL)                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🎯 What Each Page Uses

### 1. **Chat Page** (`/chat`)
```
Uses:
  → OPENAI_API_KEY (GPT-3.5/GPT-4)
  → ANTHROPIC_API_KEY (Claude)
  → GOOGLE_GEMINI_API_KEY (Gemini)
  → MEM0_API_KEY (conversation memory)

Backend:
  → /api/v1/chat/message
    → RealOrchestrator._call_openai()
    → RealOrchestrator._call_anthropic()
    → RealOrchestrator._call_google()
    → Mem0Service.store_context()
```

### 2. **Orchestration Page** (`/orchestration`)
```
Uses:
  → OPENAI_API_KEY (strategic analysis)
  → ANTHROPIC_API_KEY (complex reasoning)
  → GOOGLE_GEMINI_API_KEY (cost-effective tasks)
  → MEM0_API_KEY (session context)
  → CREWAI_API_KEY (multi-agent) [optional]

Backend:
  → /api/v1/orchestration/execute
    → RealOrchestrator.execute_strategic_analysis()
    → MultiModelRouter.route_request()
    → CrewAIService.analyze_strategic_opportunity()
```

### 3. **Memory Page** (`/memory`)
```
Uses:
  → MEM0_API_KEY (memory operations)

Backend:
  → /api/v1/memory/store
  → /api/v1/memory/search
    → Mem0Service.store_context()
    → Mem0Service.retrieve_relevant_memories()
```

### 4. **Strategic Intelligence Page** (`/strategic`)
```
Uses:
  → OPENAI_API_KEY (strategic analysis)
  → ANTHROPIC_API_KEY (gap analysis)
  → MEM0_API_KEY (strategic context)

Backend:
  → /api/v1/strategic/*
    → StrategicIntelligenceService
    → MultiModelRouter.route_request()
```

### 5. **Revenue Integration Page** (`/revenue`)
```
Uses:
  → OPENAI_API_KEY (proposal generation)
  → ANTHROPIC_API_KEY (revenue analysis)
  → MEM0_API_KEY (revenue context)

Backend:
  → /api/v1/revenue/proposals/generate
    → AutonomousBRICKProposer
    → MultiModelRouter.route_request()
```

---

## 💡 Summary: What You Have vs What You Need

### ✅ YOU HAVE (Configured):
1. **OPENAI_API_KEY** ⭐ → Real AI analysis working!
2. **ANTHROPIC_API_KEY** ⭐ → Claude 3 working!
3. **GOOGLE_GEMINI_API_KEY** ⭐ → Gemini working!
4. **MEM0_API_KEY** ⭐ → Enhanced memory working!

### ⚠️ OPTIONAL (Not Needed):
5. **CREWAI_API_KEY** → Mock mode works great
6. **DEVIN_API_KEY** → Enhanced mock works
7. **COPILOT_STUDIO_API_KEY** → Enhanced mock works
8. **GITHUB_COPILOT_TOKEN** → Enhanced mock works

### 🎉 Result:
**You have ALL the critical keys needed for REAL AI Orchestration!**

The system is:
- ✅ Using real AI (not templates)
- ✅ Routing intelligently between models
- ✅ Optimizing costs automatically
- ✅ Storing enhanced context
- ✅ Learning from conversations
- ✅ Fully operational!

---

**Last Updated:** 2025-10-07  
**Status:** All critical API keys configured and working  
**System:** Real AI Orchestration ACTIVE

