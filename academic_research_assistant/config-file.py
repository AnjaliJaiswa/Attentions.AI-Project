from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # LLM Configuration
    LLM_BASE_URL: str = "http://localhost:11434/api"
    LLM_MODEL: str = "llama2"  # or other models available in Ollama
    
    # Neo4j Configuration
    NEO4J_URI: str = "neo4j://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"  # Change in production
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    class Config:
        env_file = ".env"

settings = Settings()
