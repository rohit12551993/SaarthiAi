from db import get_or_create_conversation

conversation_id = get_or_create_conversation("session123")

print("Conversation ID:", conversation_id)
