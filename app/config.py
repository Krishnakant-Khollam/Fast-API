# SET FOLLOWING VARIABLES IN ENVIRONMENT VARIABLES IN ALL CAPS w.r.t THEIR VALUES AND DELETE VALUES THAT SET OVER HERE

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_hostname: str = "localhost"
    # database_port: str = ""
    database_username: str = "postgres"
    database_password: str = "123456789ten!!"
    database_name: str = "mydb"
    secret_key: str = "W]E\5%(tIatX3p5g!,UD6UYs>F-|3;4{~OoDYR9/"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30


settings = Settings()
