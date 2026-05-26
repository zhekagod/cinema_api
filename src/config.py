from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    port: int

    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    @property
    def db_url(self) -> str:
        return (
            f"postgresql+psycopg2://"
            f"{self.db_username}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    model_config = SettingsConfigDict(env_file=".env")


config = Config()