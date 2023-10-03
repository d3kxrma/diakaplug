from sseclient import SSEClient
from aiosseclient import aiosseclient
import json, re, requests, aiohttp
from bs4 import BeautifulSoup

DIAKA_URL = "https://c.diaka.ua"
API_URL = "https://diaka.ua/api/v1"
SSE_URL = "https://e.diaka.ua/sse"

class Diaka():
    """
    The Diaka class provides methods for interacting with the diaka.ua synchronously.
    
    Args:
        url (str): This is the link from the notification page that diaka provides to display the donation on the stream
    """
    def __init__(self, url: str):
        self.topic = url.split('/')[-1]
        self.token = self.__get_auth_token()
    
    def __get_auth_token(self) -> str:
        """
        Sends a GET request to the Diaka API to retrieve an authorization token for the current topic.

        Returns:
            str: The authorization token as a string.
        """
        response = requests.get(f"{DIAKA_URL}/stream/{self.topic}")
        raw_token = re.findall(r"'authorization',\s*'([^']+)'", response.text)
        return raw_token[0]
    
    def send_test_notification(self, target:str, amount:int = 54, name:str="DiakaPlug", message:str="Hi from Python", source:str="", show:str="", additional:str="") -> int:
        """
        Sends a test notification to the specified target.

        Args:
            target (str): The target of the notification.
            amount (int): The amount of the notification (default 54).
            name (str): The name of the notification (default "DiakaPlug").
            message (str): The message of the notification (default "Hi from Python").
            source (str): The source of the notification (default "").
            show (str): The show of the notification (default "").
            additional (str): The additional information of the notification (default "").

        Returns:
            int: The status code of the response.
        """
        response = requests.get(f"{API_URL}/message/create?key={self.topic}&amount={amount}&name={name}&message={message}&target={target}&source={source}&additional={additional}&show={show}")
        return response.status_code
    
    def parse_notification(self, transaction_id: int, hash:str) -> dict:
        """
        Parses a notification from the Diaka API using the provided transaction ID and hash.

        Args:
            transaction_id (int): The ID of the transaction to retrieve the notification for.
            hash (str): The hash of the widget to retrieve the notification for.

        Returns:
            dict: A dictionary containing the parsed notification data, including the start music URL, voice music URL, image URL, message header, and message body.
        """
        response = requests.get(f"{DIAKA_URL}/api/v1/widget/get-html?widgetHash={hash}&transactionId={transaction_id}")
        soup = BeautifulSoup(response.text, 'lxml')
        
        message = {"start_music" : DIAKA_URL+soup.find('audio', id = "startMusic").get("src"), 
                   "voice_music": DIAKA_URL+soup.find('audio', id = "voiceMusic").get("src"), 
                   "image": DIAKA_URL+soup.find('img').get('src'), 
                   "message_header": soup.find('p', class_ = "header").text, 
                   "message_body": soup.find('p', class_ = "message").text}
        
        return message
    
    def session(self):
        """
        Establishes a session with the SSE server and yields parsed notifications.

        Returns:
            generator: A generator that yields parsed notifications.
        """
        params = {'topic': self.topic, 'authorization' : self.token}
        for event in SSEClient(SSE_URL, params=params):
            data = json.loads(event.data)["data"]
            transaction_id = data["transaction"]["id"]
            hash = data["widget"]["hash"]
            yield self.parse_notification(transaction_id, hash)

class AsyncDiaka():
    """
    The AsyncDiaka class provides asynchronous methods for interacting with the Diaka service.
    
    Args:
        url (str): This is the link from the notification page that diaka provides to display the donation on the stream
    """
    def __init__(self, url:str):
        self.topic = url.split('/')[-1]
        
    async def __get_auth_token(self) -> str:
        """
        Sends a GET request to the Diaka API to retrieve an authorization token for the current topic.

        Returns:
            str: The authorization token as a string.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{DIAKA_URL}/stream/{self.topic}") as response:
                html = await response.text()
                raw_token = re.findall(r"'authorization',\s*'([^']+)'", html)
        return raw_token[0]
        
    async def send_test_notification(self, target:str, amount:int = 54, name:str="DiakaPlug", message:str="Hi from Python", source:str="", show:str="", additional:str="") -> int:
        """
        Sends a test notification to the specified target.

        Args:
            target (str): The target of the notification.
            amount (int): The amount of the notification (default 54).
            name (str): The name of the notification (default "DiakaPlug").
            message (str): The message of the notification (default "Hi from Python").
            source (str): The source of the notification (default "").
            show (str): The show of the notification (default "").
            additional (str): The additional information of the notification (default "").

        Returns:
            int: The status code of the response.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/message/create?key={self.topic}&amount={amount}&name={name}&message={message}&target={target}&source={source}&additional={additional}&show={show}") as response:
                return response.status

    async def parse_notification(self, transaction_id: int, hash:str) -> dict:
        """
        Parses a notification from the Diaka API using the provided transaction ID and hash.

        Args:
            transaction_id (int): The ID of the transaction to retrieve the notification for.
            hash (str): The hash of the widget to retrieve the notification for.

        Returns:
            dict: A dictionary containing the parsed notification data, including the start music URL, voice music URL, image URL, message header, and message body.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{DIAKA_URL}/api/v1/widget/get-html?widgetHash={hash}&transactionId={transaction_id}") as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                
                message = {"start_music" : DIAKA_URL+soup.find('audio', id = "startMusic").get("src"), 
                           "voice_music": DIAKA_URL+soup.find('audio', id = "voiceMusic").get("src"), 
                           "image": DIAKA_URL+soup.find('img').get('src'), 
                           "message_header": soup.find('p', class_ = "header").text, 
                           "message_body": soup.find('p', class_ = "message").text}
                
                return message

    async def session(self):
        """
        Establishes a session with the SSE server and yields parsed notifications.

        Returns:
            generator: A generator that yields parsed notifications.
        """
        params = {'topic': self.topic, 'authorization' : await self.__get_auth_token()}
        async for event in aiosseclient(SSE_URL, params=params):
            data = json.loads(event.data)["data"]
            transaction_id = data["transaction"]["id"]
            hash = data["widget"]["hash"]
            yield await self.parse_notification(transaction_id, hash)