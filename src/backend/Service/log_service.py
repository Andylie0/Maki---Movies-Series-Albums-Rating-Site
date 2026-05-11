from Repository.log_repository import LogRepository
from Domain.models.observation import ObservationModel


class LogService:
    def __init__(self, log_repo: LogRepository):
        self.log_repo = log_repo
        self.db = log_repo.db

    def log_and_check(self, user_id: int, group_id: str, action: str):
        self.log_repo.add_log(user_id, group_id, action)
        deletion_count = self.log_repo.count_recent_deletions(user_id)
        if deletion_count >= 5:
            self.place_in_observation_list(user_id, f"Mass deletion: {deletion_count} in 1min")

    def place_in_observation_list(self, user_id: int, reason: str):
        exists = self.db.query(ObservationModel).filter_by(user_id=user_id).first()
        if not exists:
            new_entry = ObservationModel(user_id=user_id, reason=reason, severity="High")
            self.db.add(new_entry)
            self.db.commit()