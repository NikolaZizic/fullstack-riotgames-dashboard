import logging
import sys, os
from enum import Enum
from dataclasses import dataclass
from typing import Any
from pathlib import Path
import requests
from requests import HTTPError, RequestException
import json
import time

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)



sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from creds import headers



class Tier(Enum):
    """Enum for valid tiers"""
    IRON = "IRON"
    BRONZE = "BRONZE"
    SILVER = "SILVER"
    GOLD = "GOLD"
    PLATINUM = "PLATINUM"
    DIAMOND = "DIAMOND"


class Division(Enum):
    """Enum for valid divisions"""
    I = "I"
    II = "II"
    III = "III"
    IV = "IV"


@dataclass
class APIResponse: 
    """Data class for API responses"""
    data : Any
    status_code : int
    success: bool


class RiotAPIError(Exception):
    """Custom exception for Riot API errors"""
    pass


class RiotAPIClient:
    """
    A client for interacting with the Riot Games API
    """

    BASE_URLS = {
        'euw1': 'https://euw1.api.riotgames.com',
        'europe': 'https://europe.api.riotgames.com'
    }

    RATE_LIMIT_DELAY = 2  # seconds
    MAX_RETRIES = 3
    TIMEOUT = 30  # seconds


    def __init__(self, headers, data_dir: str = "backend/data"): # add header type
        """
        Initialize the API client
        
        Args:
            headers: API headers including authentication
            data_dir: Directory to save data files
        """
        self.headers = headers
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()


    def _make_request(self, url: str, retries: int = 0) -> APIResponse:
        """
        Make HTTP request with error handling and retries
        
        Args:
            url: The URL to request
            retries: Current retry count
            
        Returns:
            APIResponse object
            
        Raises:
            RiotAPIError: If request fails after max retries
        """
        try:
            logger.info(f"Making request to: {url}")
            response = self.session.get(url, timeout=self.TIMEOUT,headers=self.headers)
            response.raise_for_status()
            
            return APIResponse(
                data=response.json(),
                status_code=response.status_code,
                success=True
            )
        
        except requests.exceptions.Timeout:
                logger.warning(f"Request timeout for URL: {url}")
                if retries < self.MAX_RETRIES:
                    time.sleep(self.RATE_LIMIT_DELAY * (retries + 1))
                    return self._make_request(url, retries + 1)
                raise RiotAPIError(f"Request timed out after {self.MAX_RETRIES} retries")
                
        except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:  # Rate limit
                    logger.warning("Rate limit hit, waiting...")
                    time.sleep(self.RATE_LIMIT_DELAY * 2)
                    if retries < self.MAX_RETRIES:
                        return self._make_request(url, retries + 1)
                
                logger.error(f"HTTP error {e.response.status_code}: {e}")
                raise RiotAPIError(f"HTTP error {e.response.status_code}: {e}")
                
        except RequestException as e:
                logger.error(f"Request failed: {e}")
                if retries < self.MAX_RETRIES:
                    time.sleep(self.RATE_LIMIT_DELAY)
                    return self._make_request(url, retries + 1)
                raise RiotAPIError(f"Request failed after {self.MAX_RETRIES} retries: {e}")
        


    def _save_data(self, filename : str, data : Any) -> None: # change Any
        """
        Save data to JSON file
        
        Args:
            filename: Name of the file to save
            data: Data to save
        """
        filepath = self.data_dir / f"{filename}.json"
        try:
            with open(filepath, 'w', encoding='utf-8', errors='igonre') as f:
                json.dump(data, f, indent=4) #ensure_ascii=False
            logger.info(f"Data saved to {filepath}")
        except IOError as e:
            logger.error(f"Failed to save data to {filepath}: {e}")
            raise RiotAPIError(f"Failed to save data: {e}")


    def get_player_puuid(self, username : str, tagline :str) -> Any : # change Any later
        """
        Get player PUUID by username and tagline
        
        Args:
            username: Player's username
            tagline: Player's tagline/region
            
        Returns:
            Player's PUUID
        """
        url = f"{self.BASE_URLS['europe']}/riot/account/v1/accounts/by-riot-id/{username}/{tagline}"
        response = self._make_request(url)

        if not response.success :
            raise RiotAPIError(f"Failed to get PUUID for {username}#{tagline}")
        
        # Saving the response
        self._save_data(f"{username}_{tagline}", response.data)

        return response.data.get('puuid')
    

    def close(self) -> None:
        """Close the session"""
        self.session.close()


# Example usage
def main():
    """Example usage of the RiotAPIClient"""
    
    # Initialize client
    client = RiotAPIClient(headers)
    
    try:
        # Get player PUUID
        puuid = client.get_player_puuid("somePlayerName", "NA")
        print(f"Player PUUID: {puuid}")
        
        # Get player matches
       
        
        # Get league entries
       
        
    except RiotAPIError as e:
        logger.error(f"API error: {e}")
    
    finally:
        client.close()


# if __name__ == "__main__":
#     main()

