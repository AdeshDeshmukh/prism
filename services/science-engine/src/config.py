import os

class Config:
    NOAA_SWPC_URL: str = os.getenv("NOAA_SWPC_URL", "https://services.swpc.noaa.gov/json")
    SCINDA_API_URL: str = os.getenv("SCINDA_API_URL", "https://api.scinda-network.org/v1")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

config = Config()
