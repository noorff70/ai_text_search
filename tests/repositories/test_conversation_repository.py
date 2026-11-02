from repositories.conversation_repository import ConversationRepository


def test_create_conversation():
    repo = ConversationRepository("data/chatbot.db")
    conversation_id = repo.create_conversation()
    assert conversation_id> 0

def test_add_message():
    repo = ConversationRepository("data/chatbot.db")
    conversation_id = repo.create_conversation()
    repo.add_message(conversation_id, "user", "hello")
    messages = repo.get_messages(
        conversation_id
    )
    assert len(messages) == 1

def test_get_messages():

    repo = ConversationRepository(
        "data/chatbot.db"
    )

    conversation_id = repo.create_conversation()

    repo.add_message(
        conversation_id,
        "user",
        "What is FastAPI?"
    )

    messages = repo.get_messages(
        conversation_id
    )

    assert messages[0]["role"] == "user"
    assert messages[0]["content"] == "What is FastAPI?"