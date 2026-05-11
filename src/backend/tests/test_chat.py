from Service.chat_service import ChatService


def test_chat_nosql_persistence():
    service = ChatService()
    # Test saving
    service.save_message("Kobe", "Job's not done")

    # Test retrieving
    history = service.get_history()
    assert any(m["username"] == "Kobe" for m in history)