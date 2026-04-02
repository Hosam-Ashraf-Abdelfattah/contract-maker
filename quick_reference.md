# Quick Reference Guide

## 🚀 Getting Started in 5 Minutes

### 1. Install Dependencies
```bash
# Telegram Bot
pip install python-telegram-bot==20.7 SpeechRecognition pydub gtts
sudo apt-get install ffmpeg  # or brew install ffmpeg on macOS

# Pricing Scraper
pip install selenium webdriver-manager
```

### 2. Run Standalone Bots
```bash
# FAQ Bot only
python telegram_bot.py

# Pricing Scraper only
python calculate_project_pricing.py

# Combined Bot (recommended)
python unified_pricing_bot.py
```

---

## 📚 Module Imports Cheat Sheet

### Telegram Bot
```python
from telegram_bot import (
    TelegramBot,           # Main bot class
    KnowledgeBase,         # FAQ management
    MessageLogger,         # Message logging
    VoiceProcessor        # Voice processing
)
```

### Pricing Scraper
```python
from calculate_project_pricing import (
    FreelancePriceScraper,  # Main scraper
    PriceExtractor,         # Price extraction
    UpworkScraper,          # Upwork only
    FreelancerScraper,      # Freelancer only
    FiverrScraper,          # Fiverr only
    ExchangeRateService    # Currency conversion
)
```

---

## 💡 Common Use Cases

### Use Case 1: Send Message to User
```python
from telegram_bot import TelegramBot
import threading

bot = TelegramBot()

# Start bot in background
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()

# Wait for bot to initialize
import time
time.sleep(5)

# Send message
chat_id = 123456789  # Get from bot logs
success = bot.send_message_sync(chat_id, "Hello from script!")

if success:
    print("✓ Message sent!")
```

### Use Case 2: Get Pricing Data
```python
from calculate_project_pricing import FreelancePriceScraper

scraper = FreelancePriceScraper(headless=True)

try:
    # Search platforms
    results = scraper.search_all("Python developer")
    
    # Get exchange rate
    rate = scraper.get_usd_to_egp_rate()
    
    # Print summary
    for result in results:
        if 'error' not in result:
            print(f"{result['platform']}: ${result['hourly_avg']:.2f}/hr")
    
    # Save to file
    scraper.save_to_json(results, rate)

finally:
    scraper.close()
```

### Use Case 3: Monitor Messages
```python
from telegram_bot import TelegramBot
import threading
import time

bot = TelegramBot()

# Start bot
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()
time.sleep(5)

# Monitor loop
while True:
    messages = bot.get_recent_messages(10)
    
    for msg in messages:
        if 'urgent' in msg.get('text', '').lower():
            chat_id = int(msg['user_id'])
            bot.send_message_sync(chat_id, "Urgent request received!")
    
    time.sleep(5)
```

### Use Case 4: Custom FAQ Bot
```python
from telegram_bot import TelegramBot, KnowledgeBase
import threading

# Create custom FAQ
faq = KnowledgeBase({
    "pricing": "Premium: $299/mo, Enterprise: $999/mo",
    "support": "Email: support@company.com, Phone: 555-0123",
    "trial": "14-day free trial available"
})

# Create bot with custom FAQ
bot = TelegramBot(knowledge_base=faq)

# Start bot
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()

print("Custom FAQ bot running!")
```

---

## 🔧 Method Quick Reference

### TelegramBot Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `start_background()` | None | None | Start bot (blocking) |
| `stop()` | None | None | Stop bot gracefully |
| `send_message_sync(chat_id, message)` | int, str | bool | Send text message |
| `send_voice_sync(chat_id, text, language='en')` | int, str, str | bool | Send voice message |
| `get_recent_messages(limit=10)` | int | List[Dict] | Get recent messages |

### FreelancePriceScraper Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `search_all(query, show_egp=False)` | str, bool | List[Dict] | Search all platforms |
| `get_usd_to_egp_rate()` | None | float | Get exchange rate |
| `save_to_json(results, rate, filename=None)` | List, float, str | Tuple[str, Dict] | Save to JSON |
| `close()` | None | None | Close browser |

---

## 🎯 Integration Patterns

### Pattern 1: Telegram Bot + Pricing Scraper
```python
from telegram_bot import TelegramBot
from calculate_project_pricing import FreelancePriceScraper
import threading
import time

# Initialize both
bot = TelegramBot()
scraper = FreelancePriceScraper(headless=True)

# Start bot
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()
time.sleep(5)

# Monitor for pricing requests
while True:
    messages = bot.get_recent_messages(5)
    
    for msg in messages:
        if 'price of' in msg.get('text', '').lower():
            # Extract project title
            text = msg['text'].lower()
            title = text.replace('price of', '').strip()
            
            # Get pricing
            chat_id = int(msg['user_id'])
            bot.send_message_sync(chat_id, f"Searching for {title}...")
            
            results = scraper.search_all(title)
            rate = scraper.get_usd_to_egp_rate()
            
            # Send results
            for result in results:
                if 'error' not in result:
                    msg_text = f"{result['platform']}: ${result['hourly_avg']:.2f}/hr"
                    bot.send_message_sync(chat_id, msg_text)
    
    time.sleep(5)
```

### Pattern 2: Custom Message Handler
```python
from telegram_bot import TelegramBot
import threading

async def custom_handler(bot_instance, update, context):
    """Custom logic for specific messages"""
    text = update.message.text.lower()
    
    if text == '/vip':
        await update.message.reply_text("🌟 VIP mode activated!")
        return True  # Handled
    
    if 'premium' in text:
        await update.message.reply_text("Premium plans start at $299/mo")
        return True
    
    return False  # Not handled, use default FAQ

# Create bot with custom handler
bot = TelegramBot(custom_message_handler=custom_handler)

# Start bot
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()

print("Bot with custom handler running!")
```

---

## ⚠️ Common Pitfalls

### ❌ DON'T: Run bot in main thread
```python
# This blocks everything!
bot = TelegramBot()
bot.start_background()  # Main thread stuck here
```

### ✅ DO: Run in separate thread
```python
import threading

bot = TelegramBot()
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()  # Main thread continues
```

---

### ❌ DON'T: Forget to close scraper
```python
scraper = FreelancePriceScraper(headless=True)
results = scraper.search_all("Python")
# Memory leak! Browser still running
```

### ✅ DO: Always close
```python
scraper = FreelancePriceScraper(headless=True)
try:
    results = scraper.search_all("Python")
finally:
    scraper.close()  # Always cleanup
```

---

### ❌ DON'T: Ignore user_id type
```python
# user_id from messages is string!
messages = bot.get_recent_messages()
chat_id = messages[0]['user_id']  # This is a STRING
bot.send_message_sync(chat_id, "Hi")  # ERROR!
```

### ✅ DO: Convert to int
```python
messages = bot.get_recent_messages()
chat_id = int(messages[0]['user_id'])  # Convert to int
bot.send_message_sync(chat_id, "Hi")  # Works!
```

---

## 📊 Data Structures

### Message Dictionary
```python
{
    'timestamp': '2026-01-14 10:30:00',
    'user': 'john_doe',
    'user_id': '123456789',  # STRING!
    'first_name': 'John',
    'type': 'TEXT',
    'text': 'Price of Python developer',
    'content': 'Price of Python developer'
}
```

### Pricing Result Dictionary
```python
{
    'platform': 'Upwork',
    'url': 'https://www.upwork.com/...',
    'hourly_rates': [25.0, 30.0, 35.0, 40.0],
    'fixed_prices': [500.0, 750.0, 1000.0],
    'hourly_avg': 32.5,
    'fixed_avg': 750.0
}
```

---

## 🧪 Testing Your Integration

```python
# test_integration.py

from telegram_bot import TelegramBot
from calculate_project_pricing import FreelancePriceScraper
import threading
import time

print("Starting integration test...")

# 1. Test bot creation
bot = TelegramBot()
print("✓ Bot created")

# 2. Test scraper creation
scraper = FreelancePriceScraper(headless=True)
print("✓ Scraper created")

# 3. Start bot
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()
time.sleep(5)
print("✓ Bot started")

# 4. Test messaging
print("\nSend a message to your bot now!")
time.sleep(10)

messages = bot.get_recent_messages(5)
if messages:
    print(f"✓ Received {len(messages)} messages")
    
    # Test sending response
    for msg in messages:
        if msg['user_id'] not in ['SYSTEM', 'API']:
            chat_id = int(msg['user_id'])
            success = bot.send_message_sync(chat_id, "Integration test successful!")
            print(f"✓ Sent response: {success}")
            break
else:
    print("⚠ No messages received")

# 5. Test scraper
print("\nTesting pricing scraper...")
results = scraper.search_all("Python", show_egp=False)
print(f"✓ Scraped {len(results)} platforms")

# 6. Cleanup
scraper.close()
print("✓ Scraper closed")

print("\n✓ Integration test complete!")
```

Run:
```bash
python test_integration.py
```

---

## 📞 Support Checklist

Before asking for help:

- [ ] All dependencies installed?
- [ ] FFmpeg installed (for voice)?
- [ ] ChromeDriver installed (for scraping)?
- [ ] Bot token is valid?
- [ ] Running bot in separate thread?
- [ ] Closing scraper with `close()`?
- [ ] Converting user_id to int?
- [ ] Checked error messages in console?
- [ ] Reviewed test scripts?
- [ ] Read the documentation?

---

## 📖 Full Documentation Links

- **Telegram Bot**: See `telegram_bot_docs.md`
- **Pricing Scraper**: See `pricing_scraper_docs.md`
- **Test Scripts**: Included in each documentation file

---

## 🎓 Next Steps

1. Run test scripts to verify setup
2. Read full documentation for your use case
3. Start with simple examples
4. Build custom integrations
5. Add your own features!

Happy coding! 🚀
