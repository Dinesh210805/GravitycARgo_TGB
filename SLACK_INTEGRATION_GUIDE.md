# 🚛 OptiGenix Slack Integration Setup Guide

## Step 1: Complete Slack App Configuration

### A. Enable Bot User (REQUIRED FIRST!)

1. **Go to your Slack App dashboard**: https://api.slack.com/apps/A096HEE7TGD
2. **Navigate to "App Home"** in the left sidebar
3. **Scroll down to "Your App's Presence in Slack"**
4. **Toggle "Always Show My Bot as Online"** to ON
5. **Add Display Information**:
   - **Display Name**: `OptiGenix Bot`
   - **Default Username**: `optigenix`
   - **Description**: `AI-powered container optimization assistant`
6. **Click "Save Changes"**

### B. Configure OAuth Scopes (BEFORE Slash Commands)

1. **Go to "OAuth & Permissions"** in the left sidebar
2. **Add these Bot Token Scopes**:
   - `chat:write` - Send messages
   - `commands` - Handle slash commands
   - `incoming-webhook` - Send notifications
   - `app_mentions:read` - Read mentions
   - `channels:read` - Read channel information
3. **Save Changes**

### C. Configure Slash Commands

1. **Navigate to "Slash Commands"** in the left sidebar
2. **Click "Create New Command"**

**Command 1: Status Check**
- **Command**: `/optigenix-status`
- **Request URL**: `http://localhost:5000/slack/commands` (for demo)
- **Short Description**: `Check OptiGenix server status and health`
- **Usage Hint**: `No parameters needed`

**Command 2: Start Optimization**
- **Command**: `/optigenix-optimize`
- **Request URL**: `http://localhost:5000/slack/commands` (for demo)
- **Short Description**: `Start container optimization process`
- **Usage Hint**: `[urgent|normal] - Priority level`

### D. Install App to Workspace

1. **Go to "Install App"** in the left sidebar
2. **Click "Install to Workspace"** (should now work with bot user enabled)
3. **Authorize the app**
4. **Copy the Bot User OAuth Token** (starts with `xoxb-`)

### E. Configure Incoming Webhooks (Optional)

1. **Go to "Incoming Webhooks"**
2. **Activate Incoming Webhooks**: Toggle to "On"
3. **Add New Webhook to Workspace**
4. **Choose channel** for notifications (e.g., #logistics-team)
5. **Copy the Webhook URL**

## Step 2: Set Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:
```bash
# Required - Get from Slack App dashboard
SLACK_BOT_TOKEN=xoxb-your-actual-bot-token-here
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/your/actual/webhook

# Already configured
SLACK_CLIENT_SECRET=ac2f422216c0682f10278d2550f9f902
SLACK_SIGNING_SECRET=e2475a30a09640d4055a5d5efa834084
```

## Step 3: Update Slack App URLs

After deploying to Render, update these URLs in your Slack app:

1. **Slash Commands Request URLs**:
   - Change to: `https://your-app.onrender.com/slack/commands`

2. **OAuth Redirect URLs**:
   - Add: `https://your-app.onrender.com/slack/oauth`

## Step 4: Test Integration

### Local Testing:
```bash
python hackathon_start.py
```

### Test Slack Commands:
1. In your Slack workspace, try:
   - `/optigenix-status`
   - `/optigenix-optimize urgent`

### Test API Endpoints:
```bash
# Test integration
curl -X POST http://localhost:5000/slack/test

# Test notification (when optimization completes)
curl -X POST http://localhost:5000/slack/notify/optimization-complete \
  -H "Content-Type: application/json" \
  -d '{
    "volume_utilization": 87.3,
    "items_packed": 145,
    "total_items": 150,
    "cost_savings": 45000,
    "user_name": "john.doe"
  }'
```

## Step 5: Hackathon Demo Flow

### Live Demo Script:

1. **Open Slack on screen**
   ```
   Type: /optigenix-status
   Shows: Real-time server status with metrics
   ```

2. **Show Command Recognition**
   ```
   Type: /optigenix-optimize urgent
   Shows: Optimization started notification
   ```

3. **Switch to Web App**
   - Upload demo CSV file
   - Show optimization running
   - Display 3D container visualization

4. **Back to Slack**
   - Show completion notification
   - Display results and metrics

5. **Highlight Enterprise Features**
   - Team collaboration
   - Real-time status monitoring
   - Integrated workflow

## Troubleshooting

### Slash Commands Not Working:
- Check Request URL in Slack app settings
- Verify signing secret in environment variables
- Check server logs for errors

### Notifications Not Sending:
- Verify webhook URL is correct
- Check bot token permissions
- Ensure webhook channel exists

### Server Issues:
- Check port configuration
- Verify environment variables
- Review application logs

## Environment Variables Reference

```bash
# Required for Slack Integration
SLACK_BOT_TOKEN=xoxb-...           # From OAuth & Permissions
SLACK_WEBHOOK_URL=https://hooks... # From Incoming Webhooks

# Pre-configured
SLACK_CLIENT_SECRET=ac2f422216c0682f10278d2550f9f902
SLACK_SIGNING_SECRET=e2475a30a09640d4055a5d5efa834084

# Optional
FLASK_ENV=development              # or production
SECRET_KEY=your-secret-key
MAIN_APP_PORT=5000
```

## Demo Commands

### Slack Commands:
```
/optigenix-status
/optigenix-optimize urgent
/optigenix-optimize normal
```

### Expected Responses:
- Status: Server health, recent activity, AR URLs
- Optimize: Confirmation with progress tracking
- Notifications: Automatic completion alerts

## Success Criteria

✅ **Slash commands respond correctly**
✅ **Server status shows real metrics**
✅ **Optimization commands trigger workflows**
✅ **Notifications sent on completion**
✅ **Team collaboration demonstrated**
✅ **Enterprise WorkOS features highlighted**

Ready for your hackathon presentation! 🏆
