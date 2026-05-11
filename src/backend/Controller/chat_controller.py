from fastapi import APIRouter, Body

from Service.chat_service import ChatService
from Service.websocket_manager import ws_manager

router = APIRouter(prefix="/chat", tags=["Chat"])
chat_service = ChatService()

@router.get("/history")
async def get_chat_history():
    chat_service.get_history()


@router.post("/send")
async def send_message(payload: dict = Body(...)):
    username = payload.get("username", "Guest")
    text = payload.get("text", "")
    chat_service.save_message(username, text)
    await ws_manager.broadcast({
        "type": "CHAT_MESSAGE",
        "data": {"username": username, "text": text}
    })
    return {"status": "success"}