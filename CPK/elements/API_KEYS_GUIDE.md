# API Keys Configuration Guide

## Overview
This application requires API keys from three services. Follow the steps below to obtain and configure them.

## 1. OpenAI API Key (Required)

### Why It's Needed
- Powers the AI chemistry assistant
- Enables intelligent element analysis and recommendations
- Provides natural language processing for user queries

### How to Get It

1. **Go to OpenAI Platform**
   - Visit: https://platform.openai.com/api-keys

2. **Sign In or Create Account**
   - Use existing account or create new one
   - Verify email if needed

3. **Create API Key**
   - Click "Create new secret key"
   - Copy the key (you won't see it again)
   - Save it securely

4. **Add to `.env.local`**
   ```env
   OPENAI_API_KEY=sk_test_4eC39HqLyjWDarhtT1l9K5Y
   ```

### Usage Tier
- **Free Trial**: $5 credit for 3 months
- **Pay as you go**: $0.03 per 1K input tokens, $0.06 per 1K output tokens
- **Recommended**: Start with free trial

### Rate Limits
- Requests: 3,500 requests per minute
- Tokens: 200,000 tokens per minute
- Good for this application ✓

---

## 2. CopilotKit API Key (Already Provided)

### Why It's Needed
- Integrates AI capabilities into the UI
- Manages agent-frontend communication
- Handles streaming responses

### Configuration

**The key is already provided:**
```env
NEXT_PUBLIC_COPILOT_KIT_PUBLIC_API_KEY=ck_pub_336d5ab8498da237aaccefc683ed17e7
```

### What You Can Do (Optional)
- Create your own CopilotKit workspace for production
- Visit: https://copilotkit.ai
- Create account and get organization key
- Replace the public key with yours

### Features Enabled
- Frontend actions
- Backend tool integration  
- Streaming responses
- State management

---

## 3. Google Maps API Key (Optional)

### Why It's Needed
- Can be used for location-based element discovery
- Enables location visualization features
- (Currently not used in base implementation)

### Configuration

**The key is already provided:**
```env
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyDK7BXtZz4ypjq0yr-7FrrAcl3oCoPpxK8
```

### How to Get Your Own

1. **Google Cloud Console**
   - Go to: https://console.cloud.google.com

2. **Create Project**
   - Click "Create Project"
   - Name it "Periodic Table"
   - Wait for creation

3. **Enable APIs**
   - Search "Maps API"
   - Enable "Maps JavaScript API"
   - Enable "Places API" (if needed)

4. **Create API Key**
   - Go to "Credentials"
   - Click "Create Credentials"
   - Select "API Key"
   - Restrict to your domain

5. **Add to `.env.local`**
   ```env
   NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyD...
   ```

### Usage Limits
- Free: $200 monthly credit
- Includes $0.50 per 1000 requests
- Good for demos and testing

---

## Environment File Setup

### Create `.env.local`

**Location:** Project root directory `/Users/jesse/Desktop/Company/Tools/PeriodicTable/CPK/elements/`

**File:**
```env
# ========================================
# REQUIRED - OpenAI Configuration
# ========================================
OPENAI_API_KEY=sk_YOUR_KEY_HERE

# ========================================
# PROVIDED - CopilotKit Configuration
# ========================================
NEXT_PUBLIC_COPILOT_KIT_PUBLIC_API_KEY=ck_pub_336d5ab8498da237aaccefc683ed17e7

# ========================================
# OPTIONAL - Google Maps Configuration
# ========================================
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=AIzaSyDK7BXtZz4ypjq0yr-7FrrAcl3oCoPpxK8

# ========================================
# Development Settings
# ========================================
NODE_ENV=development
NEXT_PUBLIC_DEBUG=false
```

### Important Notes
- ⚠️ **Never commit `.env.local` to git**
- ⚠️ **Never share API keys publicly**
- ✓ Add to `.gitignore` (already done if setup correctly)
- ✓ Create per environment (`.env.local`, `.env.production`, etc.)

---

## Verification

### Test Configuration

Run this to verify keys are loaded:

```bash
# Check environment variables are accessible
npm run dev

# In browser console:
console.log(process.env.NEXT_PUBLIC_COPILOT_KIT_PUBLIC_API_KEY)
```

### Test OpenAI Connection

```bash
# Test API key validity
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer sk_YOUR_KEY_HERE"
```

Expected response: List of available models

### Test CopilotKit

- Open app in browser
- Check if AI assistant loads
- Send a test message
- Verify response appears

---

## Cost Estimates

### Monthly Usage Estimate

**Light Usage (10 queries/day, ~500 tokens each):**
- OpenAI: ~$0.15/month
- Google Maps: Free (under limit)
- **Total: ~$0.15/month**

**Medium Usage (50 queries/day, ~1000 tokens each):**
- OpenAI: ~$1.50/month
- Google Maps: Free (under limit)
- **Total: ~$1.50/month**

**Heavy Usage (200 queries/day, ~2000 tokens each):**
- OpenAI: ~$12/month
- Google Maps: Free (under limit)
- **Total: ~$12/month**

### Cost Optimization Tips
1. Use GPT-3.5 for simpler queries
2. Implement caching for repeated queries
3. Monitor usage dashboard
4. Set up billing alerts
5. Use batch API for high volume

---

## Troubleshooting

### Problem: "Invalid API Key"

**Solution:**
1. Double-check key is correctly copied
2. Verify no extra spaces or characters
3. Ensure key is for correct service
4. Check key hasn't been revoked
5. Restart development server

### Problem: "Rate Limit Exceeded"

**Solution:**
1. Implement exponential backoff
2. Add request queuing
3. Cache responses
4. Upgrade API tier
5. Contact support for higher limits

### Problem: "API Key Not Found"

**Solution:**
1. Check `.env.local` exists
2. Verify file path is correct
3. Ensure no typos in variable names
4. Restart npm server
5. Check `process.env.OPENAI_API_KEY` in console

### Problem: "CORS Error"

**Solution:**
1. API keys should be in `.env.local` (backend only)
2. Only public keys should be in `NEXT_PUBLIC_*`
3. Move sensitive keys to server-side only
4. Check allowed origins in API settings

---

## Security Best Practices

### Do's ✓
- ✓ Store keys in `.env.local`
- ✓ Add `.env.local` to `.gitignore`
- ✓ Rotate keys periodically
- ✓ Use separate keys per environment
- ✓ Monitor usage regularly
- ✓ Set up billing alerts

### Don'ts ✗
- ✗ Don't commit keys to git
- ✗ Don't share keys in Slack/Email
- ✗ Don't use production keys in development
- ✗ Don't expose keys in client code (unless marked NEXT_PUBLIC_)
- ✗ Don't keep unused keys active
- ✗ Don't use the same key across projects

---

## Production Deployment

### Before Going Live

1. **Rotate All Keys**
   - Generate new production keys
   - Test thoroughly before deploying
   - Revoke old keys

2. **Secure Secrets**
   ```bash
   # Use environment variables in deployment
   OPENAI_API_KEY=sk_prod_...
   NEXT_PUBLIC_COPILOT_KIT_PUBLIC_API_KEY=ck_prod_...
   ```

3. **Set Rate Limits**
   - Configure in API dashboards
   - Implement application-level limits
   - Monitor for abuse

4. **Monitor Usage**
   - Set up billing alerts
   - Review API logs
   - Track token usage

---

## Getting Help

### Resources
- **OpenAI Documentation**: https://platform.openai.com/docs
- **CopilotKit Documentation**: https://docs.copilotkit.ai
- **Google Maps Documentation**: https://developers.google.com/maps
- **Project Issues**: Check GitHub issues

### Support Contacts
- OpenAI Support: support@openai.com
- CopilotKit Support: support@copilotkit.ai
- Google Cloud Support: https://cloud.google.com/support

---

## Quick Start Checklist

- [ ] Copy `.env.local.example` to `.env.local`
- [ ] Get OpenAI API key from https://platform.openai.com/api-keys
- [ ] Add OpenAI key to `.env.local`
- [ ] Verify CopilotKit key is present
- [ ] Verify Google Maps key is present
- [ ] Run `npm install`
- [ ] Run `npm run dev`
- [ ] Open http://localhost:3000
- [ ] Test AI assistant with a message
- [ ] Check console for errors

---

**Last Updated:** November 2025
**Version:** 1.0.0
