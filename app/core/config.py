import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central configuration. Every value is overridable via environment
    variables (or a .env file), so no secret ever needs to be hardcoded
    in source.
    """

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # SECURITY WARNING: this random fallback is fine for local dev, but a
    # real deployment MUST set SECRET_KEY explicitly so tokens stay valid
    # across restarts and workers, and so a leaked default can't be used
    # to forge tokens.
    secret_key: str = secrets.token_hex(32)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    # Basic brute-force protection on /auth/login (see AuthService).
    max_login_attempts: int = 5
    login_lockout_minutes: int = 15


settings = Settings()
