import asyncio
import random
from faker import Faker
from Domain.models.Review import ReviewModel

fake = Faker()

class FakerService():
    def __init__(self, review_service, sma_repo, ws_manager):
        self.review_service = review_service
        self.sma_repo = sma_repo
        self.ws_manager = ws_manager
        self.is_running = False
        self._bg_task = None

    async def start_loop(self):
        if not self.is_running:
            self.is_running = True
            self._bg_task = asyncio.create_task(self._run_generator())

    def stop_loop(self):
        self.is_running = False
        if self._bg_task:
            self._bg_task.cancel()
            self._bg_task = None

    async def _run_generator(self):
        SYSTEM_USER_ID = 1
        try:
            while self.is_running:
                movies = self.sma_repo.get_all()
                if movies:
                    movie = random.choice(movies)

                    data = ReviewModel(
                        movie_id=movie.id,
                        text=fake.paragraph(nb_sentences=2),
                        rating=random.choice([0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5])
                    )

                    await self.review_service.add_review(data, user_id=SYSTEM_USER_ID)

                    await self.ws_manager.broadcast({
                        "type": "NEW_DATA_ALERT",
                        "message": f"Added review for {movie.name}"
                    })

                await asyncio.sleep(60)
        except asyncio.CancelledError:
            pass


