# DiakaPlug Library

The DiakaPlug library provides a set of tools for interacting with the Diaka donation service, allowing you to send test notifications and parse incoming notifications from Diaka streams. This README.md file offers an overview of the library and its main features.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Synchronous Diaka Class](#synchronous-diaka-class)
  - [Asynchronous AsyncDiaka Class](#asynchronous-asyncdiaka-class)
- [License](#license)

## Installation

To use the Diaka Python library, you'll need to install it via pip:

```bash
pip install diakaplug
```
## Usage

### Synchronous Diaka Class

The `Diaka` class provides synchronous methods for interacting with the Diaka service.

#### Initialization

```python
from diakaplug import Diaka

# Initialize the Diaka class with a Diaka notification URL
diaka = Diaka("https://c.diaka.ua/notification_url")
```
### Sending a Test Notification
```python
# Send a test notification with optional parameters
status_code = diaka.send_test_notification(
    target="TargetName",
    amount=54,
    name="DiakaPlug",
    message="Hi from Python",
    source="SourceName",
    show="Show",
    additional="AdditionalInfo"
)
```
### Parsing a Notification
```python
# Parse a notification using a transaction ID and hash
notification_data = diaka.parse_notification(transaction_id=123, hash="notification_hash")
```
### Establishing a Session
```python
# Establish a session with the SSE server and yield parsed notifications
for notification in diaka.session():
    print(notification)
```

### Asynchronous AsyncDiaka Class

The `AsyncDiaka` class provides asynchronous methods for interacting with the Diaka service.

#### Initialization

```python
from diakaplug import AsyncDiaka

# Initialize the AsyncDiaka class with a Diaka notification URL
async_diaka = AsyncDiaka("https://c.diaka.ua/notification_url")
```
### Sending a Test Notification
```python
# Send a test notification with optional parameters
status_code = await async_diaka.send_test_notification(
    target="TargetName",
    amount=54,
    name="DiakaPlug",
    message="Hi from Python",
    source="SourceName",
    show="ShowName",
    additional="AdditionalInfo"
)
```
### Parsing a Notification
```python
# Parse a notification using a transaction ID and hash
notification_data = await async_diaka.parse_notification(transaction_id=123, hash="notification_hash")
```
### Establishing a Session
```python
# Establish a session with the SSE server and yield parsed notifications
async for notification in async_diaka.session():
    print(notification)
```

# License
This project is licensed under the [MIT License](ttps://github.com/d3kxrma/diakaplug/blob/main/LICENSE).
