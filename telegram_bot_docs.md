# Telegram Bot Module Documentation

## Overview
A modular Telegram bot with FAQ support, voice processing, and extensible message handling.

---

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Classes](#classes)
4. [API Reference](#api-reference)
5. [Examples](#examples)
6. [Testing](#testing)

---

## Installation

### Dependencies
```bash
pip install python-telegram-bot==20.7
pip install SpeechRecognition
pip install pydub
pip install gtts
```

### System Requirements
- Python 3.8+
- FFmpeg (for audio processing)

```bash
# Install FFmpeg on Ubuntu/Debian
sudo apt-get install ffmpeg

# Install FFmpeg on macOS
brew install ffmpeg
```

---

## Quick Start

### Standalone Mode
```python
# Run as standalone bot
python telegram_bot.py
```

### Import as Module
```python
from telegram_bot import TelegramBot

# Create bot instance
bot = TelegramBot()

# Start in background thread
import threading
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()

# Use bot API
bot.send_message_sync(chat_id=123456789, message="Hello!")
messages = bot.get_recent_messages(limit=10)
```

---

## Classes

### 1. MessageLogger

**Purpose**: Logs all bot messages to console and queue

#### Constructor
```python
MessageLogger()
```

**Parameters**: None

**Returns**: MessageLogger instance

#### Methods

##### `log(user_info: Dict, message_type: str, content: str)`

**Description**: Log a message to console and add to queue

**Parameters**:
- `user_info` (dict): User information
  - `username` (str): Telegram username
  - `id` (int): User ID
  - `first_name` (str): User's first name
- `message_type` (str): Type of message (TEXT, VOICE, COMMAND, etc.)
- `content` (str): Message content

**Returns**: None

**Example**:
```python
logger = MessageLogger()
logger.log(
    user_info={'username': 'john', 'id': 123, 'first_name': 'John'},
    message_type='TEXT',
    content='Hello bot!'
)
```

##### `get_recent_messages(limit: int = 10) -> List[Dict]`

**Description**: Retrieve recent messages from queue

**Parameters**:
- `limit` (int, optional): Maximum messages to retrieve. Default: 10

**Returns**: List of message dictionaries
```python
[
    {
        'timestamp': '2026-01-14 10:30:00',
        'user': 'john',
        'user_id': '123',
        'first_name': 'John',
        'type': 'TEXT',
        'text': 'Hello!',
        'content': 'Hello!'
    }
]
```

**Example**:
```python
logger = MessageLogger()
recent = logger.get_recent_messages(5)
for msg in recent:
    print(f"{msg['user']}: {msg['text']}")
```

---

### 2. VoiceProcessor

**Purpose**: Process voice messages and convert text to speech

#### Constructor
```python
VoiceProcessor()
```

**Parameters**: None

**Returns**: VoiceProcessor instance

#### Methods

##### `async process_voice(voice_file, user_id: int) -> Optional[str]`

**Description**: Convert voice message to text (async)

**Parameters**:
- `voice_file`: Telegram voice file object
- `user_id` (int): User ID for temporary file naming

**Returns**: 
- `str`: Transcribed text
- `None`: If transcription failed

**Example**:
```python
processor = VoiceProcessor()

# Inside async handler
voice = await update.message.voice.get_file()
text = await processor.process_voice(voice, user_id=123)

if text:
    print(f"User said: {text}")
```

**Dependencies**: SpeechRecognition, pydub, FFmpeg

##### `text_to_speech(text: str, user_id: int, language: str = 'en') -> str` (static)

**Description**: Convert text to speech MP3 file

**Parameters**:
- `text` (str): Text to convert
- `user_id` (int): User ID for file naming
- `language` (str, optional): Language code. Default: 'en'

**Returns**: `str` - Path to generated MP3 file

**Example**:
```python
voice_file = VoiceProcessor.text_to_speech(
    text="Hello, this is a test",
    user_id=123,
    language='en'
)
# voice_file = "response_voice_123.mp3"

# Remember to delete the file after use
import os
os.remove(voice_file)
```

**Dependencies**: gtts

---

### 3. KnowledgeBase

**Purpose**: Manage FAQ data and search functionality

#### Constructor
```python
KnowledgeBase(data: Optional[Dict[str, str]] = None)
```

**Parameters**:
- `data` (dict, optional): Custom FAQ data. Default: Uses built-in FAQ

**Returns**: KnowledgeBase instance

**Example**:
```python
# Use default FAQ
kb = KnowledgeBase()

# Use custom FAQ
custom_faq = {
    "refund": "Refunds processed within 7 days",
    "warranty": "1-year warranty on all products"
}
kb = KnowledgeBase(data=custom_faq)
```

#### Methods

##### `search(query: str) -> List[Tuple[str, str]]`

**Description**: Search FAQ for matching topics

**Parameters**:
- `query` (str): Search query

**Returns**: List of (topic, answer) tuples

**Example**:
```python
kb = KnowledgeBase()
matches = kb.search("shipping")

for topic, answer in matches:
    print(f"{topic}: {answer}")
# Output: shipping: Free shipping on orders over $50...
```

##### `get_all_topics() -> List[str]`

**Description**: Get all available topics

**Parameters**: None

**Returns**: List of topic names

**Example**:
```python
kb = KnowledgeBase()
topics = kb.get_all_topics()
print(topics)
# ['support', 'hours', 'return_policy', 'shipping', ...]
```

---

### 4. TelegramBot

**Purpose**: Main bot orchestrator with public API

#### Constructor
```python
TelegramBot(
    token: str = BOT_TOKEN,
    knowledge_base: Optional[KnowledgeBase] = None,
    custom_message_handler: Optional[Callable] = None
)
```

**Parameters**:
- `token` (str, optional): Bot token from BotFather. Default: Uses module constant
- `knowledge_base` (KnowledgeBase, optional): Custom knowledge base. Default: Creates new instance
- `custom_message_handler` (Callable, optional): Custom message handler function. Default: None

**Returns**: TelegramBot instance

**Example**:
```python
# Default bot
bot = TelegramBot()

# Custom knowledge base
custom_kb = KnowledgeBase({"pricing": "Starts at $99/month"})
bot = TelegramBot(knowledge_base=custom_kb)

# Custom message handler
async def my_handler(bot_instance, update, context):
    if "special" in update.message.text:
        await update.message.reply_text("Special response!")
        return True  # Handled
    return False  # Not handled

bot = TelegramBot(custom_message_handler=my_handler)
```

#### Methods

##### `start_background()`

**Description**: Start bot in background thread (blocking)

**Parameters**: None

**Returns**: None (runs forever until stopped)

**Example**:
```python
import threading

bot = TelegramBot()

# Run in separate thread
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()

# Main thread continues...
print("Bot running in background")
```

**Note**: This method blocks. Always run in a separate thread.

##### `stop()`

**Description**: Stop the bot gracefully

**Parameters**: None

**Returns**: None

**Example**:
```python
bot = TelegramBot()
# ... bot running ...
bot.stop()
print("Bot stopped")
```

##### `async send_message(chat_id: int, message: str) -> bool`

**Description**: Send text message to user (async)

**Parameters**:
- `chat_id` (int): Telegram user ID
- `message` (str): Message text

**Returns**: 
- `True`: Message sent successfully
- `False`: Failed to send

**Example**:
```python
# Inside async function
success = await bot.send_message(
    chat_id=123456789,
    message="Hello from bot!"
)

if success:
    print("Message sent!")
```

##### `send_message_sync(chat_id: int, message: str) -> bool`

**Description**: Send text message to user (synchronous)

**Parameters**:
- `chat_id` (int): Telegram user ID
- `message` (str): Message text

**Returns**: 
- `True`: Message sent successfully
- `False`: Failed to send

**Example**:
```python
bot = TelegramBot()
# Start bot first...

success = bot.send_message_sync(
    chat_id=123456789,
    message="Hello!"
)

if success:
    print("Message sent!")
else:
    print("Failed to send")
```

##### `async send_voice(chat_id: int, text: str, language: str = 'en') -> bool`

**Description**: Send voice message to user (async)

**Parameters**:
- `chat_id` (int): Telegram user ID
- `text` (str): Text to convert to speech
- `language` (str, optional): Language code. Default: 'en'

**Returns**: 
- `True`: Voice sent successfully
- `False`: Failed to send

**Example**:
```python
# Inside async function
success = await bot.send_voice(
    chat_id=123456789,
    text="This is a voice message",
    language='en'
)
```

##### `send_voice_sync(chat_id: int, text: str, language: str = 'en') -> bool`

**Description**: Send voice message to user (synchronous)

**Parameters**:
- `chat_id` (int): Telegram user ID
- `text` (str): Text to convert to speech
- `language` (str, optional): Language code. Default: 'en'

**Returns**: 
- `True`: Voice sent successfully
- `False`: Failed to send

**Example**:
```python
bot = TelegramBot()
# Start bot first...

success = bot.send_voice_sync(
    chat_id=123456789,
    text="Welcome to our service!",
    language='en'
)
```

##### `get_recent_messages(limit: int = 10) -> List[Dict]`

**Description**: Get recent messages from logger

**Parameters**:
- `limit` (int, optional): Maximum messages. Default: 10

**Returns**: List of message dictionaries

**Example**:
```python
bot = TelegramBot()
messages = bot.get_recent_messages(5)

for msg in messages:
    print(f"{msg['user']}: {msg['text']}")
```

---

## Complete Examples

### Example 1: Basic Bot with Custom FAQ

```python
from telegram_bot import TelegramBot, KnowledgeBase
import threading
import time

# Create custom FAQ
faq = KnowledgeBase({
    "pricing": "Premium: $299/month, Enterprise: $999/month",
    "support": "24/7 support at support@company.com",
    "trial": "Free 14-day trial available"
})

# Create bot
bot = TelegramBot(knowledge_base=faq)

# Start in background
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()

print("Bot running! Send messages...")
time.sleep(3600)  # Run for 1 hour
```

### Example 2: Monitor Messages and Auto-Respond

```python
from telegram_bot import TelegramBot
import threading
import time

bot = TelegramBot()

# Start bot
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()

# Monitor loop
while True:
    messages = bot.get_recent_messages(10)
    
    for msg in messages:
        # Check for keyword
        if msg['user_id'] != 'SYSTEM' and 'urgent' in msg.get('text', '').lower():
            # Auto-respond
            chat_id = int(msg['user_id'])
            bot.send_message_sync(
                chat_id,
                "⚠️ Urgent request detected! Support team notified."
            )
    
    time.sleep(5)
```

### Example 3: Custom Message Handler

```python
from telegram_bot import TelegramBot
import threading

# Define custom handler
async def handle_special_commands(bot_instance, update, context):
    text = update.message.text.lower()
    
    if text.startswith('/broadcast'):
        # Custom broadcast command
        await update.message.reply_text("Broadcasting feature coming soon!")
        return True  # Handled
    
    if 'vip' in text:
        await update.message.reply_text("🌟 VIP support activated!")
        return True
    
    return False  # Not handled, use default FAQ

# Create bot with custom handler
bot = TelegramBot(custom_message_handler=handle_special_commands)

# Start bot
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()

print("Bot with custom handler running!")
```

---

## Testing Script

Save as `test_telegram_bot.py`:

```python
"""
Test script for telegram_bot module
"""

from telegram_bot import TelegramBot, KnowledgeBase, MessageLogger, VoiceProcessor
import threading
import time

def test_knowledge_base():
    """Test KnowledgeBase functionality"""
    print("\n=== Testing KnowledgeBase ===")
    
    kb = KnowledgeBase()
    
    # Test search
    results = kb.search("shipping")
    assert len(results) > 0, "Should find shipping info"
    print(f"✓ Search found {len(results)} results")
    
    # Test get all topics
    topics = kb.get_all_topics()
    assert len(topics) > 0, "Should have topics"
    print(f"✓ Found {len(topics)} topics")
    
    print("✓ KnowledgeBase tests passed!\n")

def test_message_logger():
    """Test MessageLogger functionality"""
    print("=== Testing MessageLogger ===")
    
    logger = MessageLogger()
    
    # Log a message
    logger.log(
        user_info={'username': 'test', 'id': 123, 'first_name': 'Test'},
        message_type='TEST',
        content='Test message'
    )
    
    # Get recent messages
    messages = logger.get_recent_messages(1)
    assert len(messages) == 1, "Should have 1 message"
    assert messages[0]['text'] == 'Test message', "Message content should match"
    
    print("✓ MessageLogger tests passed!\n")

def test_voice_processor():
    """Test VoiceProcessor text-to-speech"""
    print("=== Testing VoiceProcessor ===")
    
    import os
    
    # Test text to speech
    voice_file = VoiceProcessor.text_to_speech(
        text="This is a test",
        user_id=999,
        language='en'
    )
    
    assert os.path.exists(voice_file), "Voice file should exist"
    print(f"✓ Voice file created: {voice_file}")
    
    # Cleanup
    os.remove(voice_file)
    print("✓ VoiceProcessor tests passed!\n")

def test_bot_creation():
    """Test TelegramBot creation"""
    print("=== Testing TelegramBot Creation ===")
    
    # Test default creation
    bot = TelegramBot()
    assert bot.knowledge_base is not None, "Should have knowledge base"
    assert bot.logger is not None, "Should have logger"
    print("✓ Default bot created")
    
    # Test with custom knowledge base
    custom_kb = KnowledgeBase({"test": "Test answer"})
    bot2 = TelegramBot(knowledge_base=custom_kb)
    assert bot2.knowledge_base == custom_kb, "Should use custom KB"
    print("✓ Bot with custom KB created")
    
    print("✓ TelegramBot creation tests passed!\n")

def test_bot_integration():
    """Test bot with actual Telegram (requires manual verification)"""
    print("=== Integration Test (Manual) ===")
    print("This test requires manual interaction:")
    print("1. Bot will start")
    print("2. Send a message to your bot")
    print("3. Bot will respond automatically")
    print("\nStarting bot in 3 seconds...")
    time.sleep(3)
    
    bot = TelegramBot()
    
    # Start in background
    bot_thread = threading.Thread(target=bot.start_background, daemon=True)
    bot_thread.start()
    
    print("\n✓ Bot started! Now send a test message...")
    print("Waiting 10 seconds for messages...\n")
    time.sleep(10)
    
    # Check for messages
    messages = bot.get_recent_messages(5)
    print(f"\nCaptured {len(messages)} messages:")
    for msg in messages:
        print(f"  - {msg['user']}: {msg['text']}")
    
    bot.stop()
    print("\n✓ Integration test complete!")

if __name__ == "__main__":
    print("="*60)
    print("TELEGRAM BOT MODULE - TEST SUITE")
    print("="*60)
    
    try:
        test_knowledge_base()
        test_message_logger()
        test_voice_processor()
        test_bot_creation()
        
        # Ask for integration test
        response = input("\nRun integration test with actual Telegram? (y/n): ")
        if response.lower() == 'y':
            test_bot_integration()
        
        print("\n" + "="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
```

Run tests:
```bash
python test_telegram_bot.py
```

---

## Error Handling

### Common Errors

**1. Bot token invalid**
```python
# Error: telegram.error.InvalidToken
# Solution: Check BOT_TOKEN in telegram_bot.py
```

**2. Bot not started**
```python
# Error: send_message_sync returns False
# Solution: Ensure bot.start_background() was called first
```

**3. FFmpeg not found**
```python
# Error: FileNotFoundError: ffmpeg
# Solution: Install FFmpeg (see Installation section)
```

**4. Voice recognition failed**
```python
# Returns: None from process_voice
# Causes: Unclear audio, no internet, unsupported language
# Solution: Check audio quality and internet connection
```

---

## Best Practices

1. **Always run bot in separate thread**
```python
# Good
bot_thread = threading.Thread(target=bot.start_background, daemon=True)
bot_thread.start()

# Bad - blocks main thread
bot.start_background()
```

2. **Clean up voice files**
```python
voice_file = VoiceProcessor.text_to_speech("Hello", 123)
# ... use file ...
os.remove(voice_file)  # Always delete
```

3. **Check bot is running before sending**
```python
if bot.app and bot.loop:
    bot.send_message_sync(chat_id, "Hello")
else:
    print("Bot not running!")
```

4. **Use custom handlers for extensions**
```python
# Don't modify telegram_bot.py
# Instead, use custom_message_handler
async def my_handler(bot, update, context):
    # Your custom logic
    pass

bot = TelegramBot(custom_message_handler=my_handler)
```

---

## Support

For issues or questions:
- Check error messages in console
- Review test script for examples
- Ensure all dependencies are installed
- Verify FFmpeg is installed for voice processing
