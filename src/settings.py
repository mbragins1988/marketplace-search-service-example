import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BROKERS", "localhost:9092")
    kafka_topic_ads: str = os.getenv(
        "KAFKA_TOPIC_ADS", "student_mbragins1988-marketplace.ads"
    )
    kafka_consumer_group: str = os.getenv("KAFKA_CONSUMER_GROUP", "search-service")
    ad_service_url: str = os.getenv(
        "AD_SERVICE_URL",
        "http://student-mbragins1988-marketplace-ad-service-web.student-mbragins1988-marketplace-ad-service.svc.cluster.local:8000",
    )

    @property
    def database_url(self) -> str:
        # Получаем переменную из окружения.
        pg_conn = os.getenv("POSTGRES_CONNECTION_STRING")

        if pg_conn:
            # Если строка начинается с postgres:// или postgresql://
            if pg_conn.startswith("postgres://"):
                pg_conn = pg_conn.replace("postgres://", "postgresql+asyncpg://", 1)
            elif pg_conn.startswith("postgresql://") and "+asyncpg" not in pg_conn:
                pg_conn = pg_conn.replace("postgresql://", "postgresql+asyncpg://", 1)
            return pg_conn

        # Fallback для локальной разработки.
        return "postgresql+asyncpg://postgres:postgres@localhost:5433/auth_db"
