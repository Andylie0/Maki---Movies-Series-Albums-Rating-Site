import redis

REDIS_URL="rediss://default:gQAAAAAAAb-9AAIgcDFkMDUzODIwNjQ3ODg0YjA2OTE0MDM4Y2E1MjBkOTI0ZA@eager-hamster-114621.upstash.io:6379"

try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    print("Connected to Cloud Redis!")
except Exception as e:
    print(f"Connection Failed: {e}")


def get_redis():
    return redis_client