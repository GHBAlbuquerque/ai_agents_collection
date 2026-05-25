import os

from dotenv import load_dotenv
load_dotenv()

class Config:
    """
    Central configuration manager
    """
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OMDB_API_KEY = os.getenv("OMDB_API_KEY")
    
    @classmethod
    def validate(cls):
        """
        Validates if required env variables were correctly defined.
        """
        
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is not defined in .env")
        
        if not cls.OMDB_API_KEY:
            raise ValueError("OMDB_API_KEY is not defined in .env")
        
    @classmethod
    def get_openai_key(cls):
        cls.validate()
        return cls.OPENAI_API_KEY
    
    @classmethod
    def get_omdb_key(cls):
        cls.validate()
        return cls.OMDB_API_KEY