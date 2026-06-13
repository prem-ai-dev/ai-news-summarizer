from pydantic_settings import BaseSettings,SettingsConfigDict

class AccessKey(BaseSettings):
    GEMINI_API_KEY:str
    NEW_API_KEY:str

    model_config=SettingsConfigDict(env_file=".env")

access=AccessKey()