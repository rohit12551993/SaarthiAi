from db import get_or_create_conversation, save_message

conversation_id = get_or_create_conversation("session123")

save_message(
    conversation_id,
    "user",
    "Hello Saarthi!"
)

print("Message saved successfully!")
