from sqlalchemy.orm import Session
from Domain.models.log import LogModel
from datetime import datetime, timedelta

class LogRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_log(self, user_id: int, group_id: str, action: str):
        new_log = LogModel(user_id=user_id, group_id=group_id, action=action)
        self.db.add(new_log)
        self.db.commit()

    def count_recent_deletions(self, user_id: int, minutes: int = 1):
        time_threshold = datetime.utcnow() - timedelta(minutes=minutes)
        return self.db.query(LogModel).filter(
            LogModel.user_id == user_id,
            LogModel.action.ilike("%DELETED%"),
            LogModel.timestamp >= time_threshold
        ).count()