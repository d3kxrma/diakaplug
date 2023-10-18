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
        self.__topic = url.split('/')[-1]
    
    def __get_auth_token(self) -> str:
        """
        Sends a GET request to the Diaka API to retrieve an authorization token for the current topic.

        Returns:
            str: The authorization token as a string.
        """
        response = requests.get(f"{DIAKA_URL}/stream/{self.__topic}")
        raw_token = re.findall(r"'authorization',\s*'([^']+)'", response.text)
        return raw_token[0]
    
    def send_test_notification(self, target:str, amount:float = 54, name:str="DiakaPlug", message:str="Hi from Python", source:str="", show:bool=True, additional:str="") -> int:
        """
        Sends a test notification to the specified target.

        Args:
            target (str): The target of the notification.
            amount (float): The amount of the notification (default 54).
            name (str): Benefactor's name (default "DiakaPlug").
            message (str): Message from the benefactor (default "Hi from Python").
            source (str): Identifier of the system from which the donation was made (default "").
            show (bool): whether to display notifications (default True).
            additional (str): The additional information of the notification (default "").

        Returns:
            int: The status code of the response.
        """
        response = requests.get(f"{API_URL}/message/create?key={self.__topic}&amount={amount}&name={name}&message={message}&target={target}&source={source}&additional={additional}&show={show}")
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
    
    def get_last_donations(self, limit:int = 10, test:int = 1):
        """
        Returns the last donations.

        Args:
            limit (int): number of last donations to retrieve (default: 10)
            test (int): to receive test or paid donations, 1 - only test, 2 - only paid. (default: 1)

        Returns:
            A list object containing the last donations.
        """
        url = f"https://diaka.ua/api/v1/message/stats?action=recent&conveyorHash={self.__topic}&params%5Blimit%5D={limit}&params%5Btest%5D={test}"
        return requests.get(url).json()
    
    def get_largest_donations(self, offset:int, limit:int = 10, test:int = 1):
        """
        Returns the largest donations.

        Args:
            offset (int): the offset in seconds. For example, to get the largest donations in one day, the value should be 60*60*24=86400.
            limit (int): number of last donations to retrieve. (default: 10)
            test (int): to receive test or paid donations, 1 - only test, 2 - only paid. (default: 1)

        Returns:
            A list object containing the largest donations.
        """
        url = f"https://diaka.ua/api/v1/message/stats?action=top&conveyorHash={self.__topic}&params%5Blimit%5D={limit}&params%5Btest%5D={test}&params%5Boffset%5D={offset}"
        return requests.get(url).json()
    
    def get_amount_of_donations(self, offset:int, test:int = 1):
        """
        Returns the sum of donations for a given time offset.

        Args:
            offset (int): time offset in seconds. For example, to get the amount of donations in one day, the value should be 60*60*24=86400.
            test (int): to receive test or paid donations, 1 - only test, 2 - only paid. (default: 1)

        Returns:
            dict object containing the sum of donations.
        """
        url = f"https://diaka.ua/api/v1/message/stats?action=sum&conveyorHash={self.__topic}&params%5Btest%5D={test}&params%5Btime%5D={offset}"
        return requests.get(url).json()
    
    def session(self):
        """
        Establishes a session with the SSE server and yields parsed notifications.

        Returns:
            generator: A generator that yields parsed notifications.
        """
        params = {'topic': self.__topic, 'authorization' : self.__get_auth_token()}
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
        self.__topic = url.split('/')[-1]
        
    async def __get_auth_token(self) -> str:
        """
        Sends a GET request to the Diaka API to retrieve an authorization token for the current topic.

        Returns:
            str: The authorization token as a string.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{DIAKA_URL}/stream/{self.__topic}") as response:
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
            async with session.get(f"{API_URL}/message/create?key={self.__topic}&amount={amount}&name={name}&message={message}&target={target}&source={source}&additional={additional}&show={show}") as response:
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

    async def get_last_donations(self, limit:int = 10, test:int = 1):
        """
        Returns the last donations.

        Args:
            limit (int): number of last donations to retrieve (default: 10)
            test (int): to receive test or paid donations, 1 - only test, 2 - only paid. (default: 1)

        Returns:
            A list object containing the last donations.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://diaka.ua/api/v1/message/stats?action=recent&conveyorHash={self.__topic}&params%5Blimit%5D={limit}&params%5Btest%5D={test}") as response:
                response = await response.text()
                return json.loads(response)
    
    async def get_largest_donations(self, offset:int, limit:int = 10, test:int = 1):
        """
        Returns the largest donations.

        Args:
            offset (int): the offset in seconds. For example, to get the largest donations in one day, the value should be 60*60*24=86400.
            limit (int): number of last donations to retrieve. (default: 10)
            test (int): to receive test or paid donations, 1 - only test, 2 - only paid. (default: 1)

        Returns:
            A list object containing the largest donations.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://diaka.ua/api/v1/message/stats?action=top&conveyorHash={self.__topic}&params%5Blimit%5D={limit}&params%5Btest%5D={test}&params%5Boffset%5D={offset}") as response:
                response = await response.text()
                return json.loads(response)
    
    async def get_amount_of_donations(self, offset:int, test:int = 1):
        """
        Returns the sum of donations for a given time offset.

        Args:
            offset (int): time offset in seconds. For example, to get the amount of donations in one day, the value should be 60*60*24=86400.
            test (int): to receive test or paid donations, 1 - only test, 2 - only paid. (default: 1)

        Returns:
            dict object containing the sum of donations.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://diaka.ua/api/v1/message/stats?action=sum&conveyorHash={self.__topic}&params%5Btest%5D={test}&params%5Btime%5D={offset}") as response:
                response = await response.text()
                return json.loads(response)
    
    async def session(self):
        """
        Establishes a session with the SSE server and yields parsed notifications.

        Returns:
            generator: A generator that yields parsed notifications.
        """
        params = {'topic': self.__topic, 'authorization' : await self.__get_auth_token()}
        async for event in aiosseclient(SSE_URL, params=params):
            data = json.loads(event.data)["data"]
            transaction_id = data["transaction"]["id"]
            hash = data["widget"]["hash"]
            yield await self.parse_notification(transaction_id, hash)