# API Keys Setup Guide - Real AI Orchestration Intelligence

## 🎯 Overview

To run **Real AI Orchestration Intelligence** with actual AI capabilities (not just intelligent templates), you need to configure API keys for various AI services.

---

## 🚨 URGENTLY NEEDED API Keys (Priority 1)

These keys are **essential** for the Real AI Orchestration to work:

### 1. **OpenAI API Key** ⭐ MOST URGENT
```bash
OPENAI_API_KEY=sk-...
```

**Why urgent:**
- Powers GPT-4 and GPT-3.5 Turbo models
- Used by `RealOrchestrator` for strategic analysis
- Required by `MultiModelRouter` for intelligent routing
- Most widely supported and reliable AI service

**How to get:**
1. Visit: https://platform.openai.com/api-keys
2. Create account or sign in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

**Cost:**
- Pay-as-you-go: $0.01-$0.06 per 1K tokens
- Free trial: $5 credit for new accounts

---

### 2. **Anthropic API Key** (Claude) ⭐ HIGHLY RECOMMENDED
```bash
ANTHROPIC_API_KEY=sk-ant-...
```

**Why important:**
- Powers Claude 3 (Opus, Sonnet, Haiku) models
- Excellent for complex reasoning and strategic analysis
- Used by `MultiModelRouter` for quality-focused tasks
- Great for long-context understanding

**How to get:**
1. Visit: https://console.anthropic.com/
2. Create account or sign in
3. Go to "API Keys" section
4. Generate new key

**Cost:**
- Pay-as-you-go: $0.25-$15 per million tokens
- Free trial: Limited credits for testing

---

### 3. **Google Gemini API Key** ⭐ RECOMMENDED
```bash
GOOGLE_GEMINI_API_KEY=AIza...
```

**Why useful:**
- Powers Gemini Pro and Ultra models
- Used by `MultiModelRouter` for cost-effective tasks
- Good for general-purpose orchestration
- Free tier available

**How to get:**
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Get API Key"
4. Copy the key (starts with `AIza`)

**Cost:**
- Free tier: 60 requests per minute
- Paid: $0.00025-$0.125 per 1K tokens

---

## 💡 OPTIONAL API Keys (Priority 2)

These enhance specific features but are not required for basic operation:

### 4. **CrewAI API Key** (Multi-Agent Orchestration)
```bash
CREWAI_API_KEY=your-crewai-key
```

**What it does:**
- Enables advanced multi-agent collaboration
- Powers strategic analysis with specialized agents
- Used for complex BRICK development planning

**Status:** Optional - system works in mock mode without it

**How to get:**
1. Visit: https://crewai.com/
2. Sign up for account
3. Get API key from dashboard

---

### 5. **Mem0.ai API Key** (Memory Persistence)
```bash
MEM0_API_KEY=your-mem0-key
```

**What it does:**
- Enhanced AI memory and context storage
- Better long-term memory across sessions
- Improved context understanding

**Status:** Optional - system uses VPS database memory without it

**How to get:**
1. Visit: https://mem0.ai/
2. Create account
3. Get API key from settings

---

### 6. **Devin AI API Key** (Autonomous Coding)
```bash
DEVIN_API_KEY=your-devin-key
```

**What it does:**
- Autonomous code development
- Automatic code optimization
- Test generation

**Status:** Optional - system uses enhanced mock without it

**How to get:**
1. Visit: https://devin.ai/
2. Request access (waitlist)
3. Get API key when approved

---

### 7. **Microsoft Copilot Studio API Key** (Enterprise Workflows)
```bash
COPILOT_STUDIO_API_KEY=your-copilot-key
```

**What it does:**
- Enterprise workflow automation
- Microsoft integration
- Business process automation

**Status:** Optional - system uses enhanced mock without it

**How to get:**
1. Visit: https://copilotstudio.microsoft.com/
2. Sign in with Microsoft account
3. Get API credentials

---

### 8. **GitHub Copilot Token** (Development Pipeline)
```bash
GITHUB_COPILOT_TOKEN=gho_...
```

**What it does:**
- GitHub repository management
- CI/CD pipeline automation
- Code review automation

**Status:** Optional - system uses enhanced mock without it

**How to get:**
1. Visit: https://github.com/settings/tokens
2. Generate personal access token
3. Grant necessary permissions

---

## 🎯 Quick Start - Minimum Configuration

**To get Real AI working RIGHT NOW, you only need:**

```bash
# Minimum configuration (copy to .env or env.unified)
OPENAI_API_KEY=sk-your-openai-key-here
```

With just OpenAI, the system will:
- ✅ Use real AI for strategic analysis
- ✅ Generate actual AI-powered recommendations
- ✅ Perform intelligent task routing
- ✅ Create real strategic insights

---

## 📋 Recommended Configuration

**For best results, configure these 3:**

```bash
# Recommended configuration
OPENAI_API_KEY=sk-your-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here
GOOGLE_GEMINI_API_KEY=AIza-your-google-key-here
```

This gives you:
- ✅ Multiple AI models for redundancy
- ✅ Cost optimization (route to cheapest model)
- ✅ Quality optimization (route to best model)
- ✅ Fallback options if one service is down

---

## 🔧 How to Configure API Keys

### Method 1: Update env.unified (Recommended)

```bash
# Edit env.unified
nano env.unified

# Add your API keys
OPENAI_API_KEY=sk-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
GOOGLE_GEMINI_API_KEY=AIza-your-actual-key-here
```

### Method 2: Update .env directly

```bash
# Edit .env
nano .env

# Add your API keys
OPENAI_API_KEY=sk-your-actual-key-here
ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
GOOGLE_GEMINI_API_KEY=AIza-your-actual-key-here
```

### Method 3: Use environment variables

```bash
# Export in your shell
export OPENAI_API_KEY=sk-your-actual-key-here
export ANTHROPIC_API_KEY=sk-ant-your-actual-key-here
export GOOGLE_GEMINI_API_KEY=AIza-your-actual-key-here

# Then run
docker compose up -d
```

---

## 🔄 After Adding Keys

**Restart services to apply changes:**

```bash
# Stop services
docker compose down

# Rebuild and start
docker compose up -d --build

# Check logs to verify AI services are active
docker compose logs backend | grep "Real AI"
```

**You should see:**
```
✅ Real AI services configured: openai, anthropic, google
```

Instead of:
```
⚠️ No real AI services configured - using intelligent templates
```

---

## 🧪 Testing Your API Keys

### Test OpenAI:
```bash
curl -X POST http://localhost:8000/api/v1/orchestration/execute \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "Test OpenAI integration",
    "task_type": "strategic_analysis",
    "context": {}
  }'
```

Look for `"ai_powered": true` in the response.

### Check Multi-Model Router Status:
```bash
curl http://localhost:8000/api/v1/dashboard/services | jq '.services.multi_model_router'
```

Should show configured models:
```json
{
  "status": "operational",
  "configured_models": ["gpt-4", "claude-3-opus", "gemini-pro"],
  "available_ai_services": 3
}
```

---

## 💰 Cost Estimates

**Monthly costs for moderate usage (100K tokens/day):**

| Service | Model | Cost/Month |
|---------|-------|------------|
| OpenAI | GPT-3.5 Turbo | ~$30 |
| OpenAI | GPT-4 | ~$180 |
| Anthropic | Claude 3 Sonnet | ~$45 |
| Anthropic | Claude 3 Opus | ~$450 |
| Google | Gemini Pro | ~$7.50 |

**Recommended budget:** $50-100/month for development

---

## 🔐 Security Best Practices

1. **Never commit API keys to Git:**
   ```bash
   # .env is already in .gitignore
   # Double-check: cat .gitignore | grep .env
   ```

2. **Use environment variables:**
   - Store keys in `.env` file (not in code)
   - Use different keys for dev/prod

3. **Rotate keys regularly:**
   - Change keys every 90 days
   - Revoke old keys after rotation

4. **Set spending limits:**
   - OpenAI: Set usage limits in dashboard
   - Monitor usage regularly

5. **Restrict key permissions:**
   - Only grant necessary permissions
   - Use read-only keys where possible

---

## 🚀 What Happens Without API Keys?

**Current behavior (NO API keys):**
- ⚠️ System uses "intelligent templates"
- ⚠️ Responses are pre-generated based on patterns
- ⚠️ No actual AI reasoning or learning
- ⚠️ Limited adaptability to new scenarios

**With API keys (REAL AI):**
- ✅ Actual AI reasoning and analysis
- ✅ Dynamic responses to any situation
- ✅ Learning from context
- ✅ Adaptive recommendations
- ✅ True strategic intelligence

---

## 📊 Service Dependencies

```
Real AI Orchestration
├── OpenAI (REQUIRED) ⭐⭐⭐
│   ├── GPT-4 (strategic analysis)
│   └── GPT-3.5 Turbo (general tasks)
├── Anthropic (HIGHLY RECOMMENDED) ⭐⭐
│   └── Claude 3 (complex reasoning)
├── Google Gemini (RECOMMENDED) ⭐
│   └── Gemini Pro (cost-effective)
├── CrewAI (OPTIONAL)
│   └── Multi-agent orchestration
├── Mem0.ai (OPTIONAL)
│   └── Enhanced memory
├── Devin AI (OPTIONAL)
│   └── Autonomous coding
├── Microsoft Copilot (OPTIONAL)
│   └── Enterprise workflows
└── GitHub Copilot (OPTIONAL)
    └── Development pipeline
```

---

## 🆘 Troubleshooting

### Problem: "No real AI services configured"

**Solution:**
```bash
# 1. Check if keys are in .env
grep "OPENAI_API_KEY" .env

# 2. Verify key format (should start with sk-)
# OpenAI: sk-...
# Anthropic: sk-ant-...
# Google: AIza...

# 3. Restart services
docker compose restart backend

# 4. Check logs
docker compose logs backend | tail -50
```

### Problem: "API key invalid"

**Solution:**
- Verify key is correct (no extra spaces)
- Check key hasn't expired
- Ensure billing is set up on provider's dashboard
- Try generating a new key

### Problem: "Rate limit exceeded"

**Solution:**
- Upgrade to paid tier
- Implement request throttling
- Use multiple keys with load balancing

---

## 📞 Support Resources

- **OpenAI:** https://help.openai.com/
- **Anthropic:** https://support.anthropic.com/
- **Google AI:** https://ai.google.dev/docs
- **CrewAI:** https://docs.crewai.com/

---

## ✅ Checklist

- [ ] Get OpenAI API key ⭐ URGENT
- [ ] Get Anthropic API key (optional but recommended)
- [ ] Get Google Gemini API key (optional but recommended)
- [ ] Add keys to `env.unified` or `.env`
- [ ] Restart Docker services
- [ ] Verify "Real AI services configured" in logs
- [ ] Test with a simple orchestration request
- [ ] Monitor API usage and costs
- [ ] Set up spending limits

---

## 🎉 Ready to Go!

**With just OpenAI API key configured, you'll have:**
- Real AI-powered strategic analysis
- Intelligent task routing
- Adaptive recommendations
- True orchestration intelligence

**Get your OpenAI key now:** https://platform.openai.com/api-keys

Then add it to your configuration and restart! 🚀

---

**Last Updated:** 2025-10-07  
**Current Status:** System works with intelligent templates (no API keys required)  
**Recommended:** Add at least OpenAI API key for real AI capabilities

