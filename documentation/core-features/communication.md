# Communication - Email Management

OPSIIE provides comprehensive email capabilities through Gmail integration for sending, receiving, and managing emails.

## 📧 Overview

- **Send Emails**: Natural language email composition
- **Read Inbox**: View unread messages
- **Reply**: Respond to emails
- **Multi-Recipient**: Up to 5 recipients
- **Contact Mapping**: Automatic name resolution from kun.py
- **HTML Templates**: Professional ARPA-branded emails

## 📤 Sending Emails

### /mail Command

**Basic Syntax:**
```bash
/mail <emails> subject "<subject>" content "<message>"
```

**Examples:**
```bash
# Single recipient
/mail john@gmail.com subject "Meeting" content "Let's meet at 2 PM"

# Multiple recipients
/mail john@gmail.com and alice@example.com subject "Update" content "Here's the info"

# Using contact names
/mail Ross subject "Hello" content "How are you?"
```

### Email Parsing

OPSIIE extracts:
- **Email Addresses**: `name@domain.com` format
- **Contact Names**: From kun.py profiles
- **Subject**: Keywords: subject, sub, theme, title
- **Content**: Keywords: content, body, message, saying

### Contact Resolution

Names automatically map to emails from kun.py:
```python
'Ross': {'mail': 'ross@example.com'}
```

## 📥 Reading Emails

### /mail inbox

View unread emails:
```bash
/mail inbox
```

**Select email number to read:**
```
[INPUT] Select email number or 'exit': 1
```

**Commands in email view:**
- `reply` - Reply to email
- `inbox` - Return to inbox list  
- `exit` - Return to main interface

## 💬 Replying

1. Open email from inbox
2. Type `reply`
3. Compose message
4. Reply sent with "Re:" prefix

## 🔧 Configuration

**Gmail Setup:**
1. Enable 2-Factor Authentication
2. Generate App Password
3. Configure .env:

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

## 🚨 Troubleshooting

**Authentication Failed:**
- Use app password, not regular password
- Enable 2FA
- Regenerate app password

**Cannot Send:**
- Check internet connection
- Verify Gmail SMTP access
- Check recipient addresses

**Cannot Read Inbox:**
- Enable IMAP in Gmail
- Verify credentials
- Check connection

---

**OPSIIE keeps you connected.** 📧