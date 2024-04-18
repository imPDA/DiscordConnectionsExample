import environ
from pydantic import BaseModel

env = environ.Env()


class MongoDBSettings(BaseModel):
    host: str = env.str("MONGO_DB_HOST")
    port: int = env.int("MONGO_DB_PORT")
    username: int = env.str("MONGO_DB_USERNAME")
    password: int = env.str("MONGO_DB_PASSWORD")
    db_name: str = env.str("MONGO_DB_DB_NAME")
    tokens_collection_name: str = env.str("MONGO_DB_TOKENS_COLLECTION_NAME")
    users_collection_name: str = env.str("MONGO_DB_USERS_COLLECTION_NAME")
    metadata_collection_name: str = env.str("MONGO_DB_METADATA_COLLECTION_NAME")

    @property
    def connection_uri(self) -> str:
        return f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}/{self.db_name}"


class KafkaSettings(BaseModel):
    bootstrap_servers: str = env.str("KAFKA_BOOTSTRAP_SERVERS")
    group_id: str = env.str("KAFKA_GROUP_ID")
    new_metadata_topic: str = env.str("KAFKA_NEW_METADATA_TOPIC")
    update_metadata_topic: str = env.str("KAFKA_UPDATE_METADATA_TOPIC")


class Settings(BaseModel):
    client_id: str = env.str("CLIENT_ID")
    client_secret: str = env.str("CLIENT_SECRET")
    oauth_redirect_uri: str = env.str("OAUTH_REDIRECT_URL")
    discord_token: str = env.str("TOKEN")

    linked_roles_uri: str = env.str("LINKED_ROLES_URL")

    mongo_db: MongoDBSettings = MongoDBSettings()

    kafka: KafkaSettings = KafkaSettings()
