import os
from dotenv import load_dotenv
from telegram import Bot
import asyncio

load_dotenv()
TOKEN = os.getenv("API_TOKEN")
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

async def test_send():
    bot = Bot(token=TOKEN)
    
    test_message = "🧪 Test message from HunTech Bot!\n\nIf you receive this, notifications are working! ✅"
    
    print(f"Token: {TOKEN[:10]}...")
    print(f"Admin Username: {ADMIN_USERNAME}")
    print(f"Admin Chat ID: {ADMIN_CHAT_ID}")
    print("\nTrying to send test message...\n")
    
    # Try username first
    if ADMIN_USERNAME:
        try:
            username = ADMIN_USERNAME.lstrip('@')
            result = await bot.send_message(
                chat_id=f"@{username}",
                text=test_message
            )
            print(f"✅ SUCCESS! Message sent to @{username}")
            print(f"Message ID: {result.message_id}")
            return
        except Exception as e:
            print(f"❌ Failed to send to @{username}")
            print(f"Error: {e}")
            print("\n💡 This usually means:")
            print("   1. You haven't sent /start to the bot yet")
            print("   2. Username is incorrect")
            print("   3. Bot was blocked by user")
    
    # Try chat ID
    if ADMIN_CHAT_ID:
        try:
            result = await bot.send_message(
                chat_id=ADMIN_CHAT_ID,
                text=test_message
            )
            print(f"\n✅ SUCCESS! Message sent to Chat ID: {ADMIN_CHAT_ID}")
            print(f"Message ID: {result.message_id}")
            return
        except Exception as e:
            print(f"\n❌ Failed to send to Chat ID: {ADMIN_CHAT_ID}")
            print(f"Error: {e}")
    
    if not ADMIN_USERNAME and not ADMIN_CHAT_ID:
        print("❌ No admin contact configured!")
        print("Add ADMIN_USERNAME or ADMIN_CHAT_ID to .env file")

if __name__ == "__main__":
    asyncio.run(test_send())
