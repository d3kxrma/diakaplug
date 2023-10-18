# Бібліотека DiakaPlug

DiakaPlug - це бібліотека Python, яка надає набір інструментів для взаємодії з сервісом пожертвувань Diaka. Вона дозволяє надсилати тестові сповіщення та аналізувати вхідні сповіщення з потоків Diaka. Цей файл README.md пропонує огляд бібліотеки та її основних можливостей.

[README.md англійською мовою](https://github.com/d3kxrma/diakaplug/blob/main/README.md).

## Зміст
- [Встановлення](#встановлення)
- [Використання](#використання)
  - [Синхронний клас Diaka](#synchronous-diaka-class)
  - [Асинхронний клас AsyncDiaka](#asynchronous-asyncdiaka-class)
- [Ліцензія](#ліцензія)

## Встановлення

Для використання бібліотеки Diakaplug вам потрібно встановити її за допомогою pip:

```bash
pip install diakaplug
```
## Використання

### Синхронний клас Diaka

Клас `Diaka` надає синхронні методи для взаємодії з сервісом Diaka.

#### Ініціалізація

```python
from diakaplug import Diaka

# Ініціалізуємо клас Diaka URL-адресою сповіщення Diaka
diaka = Diaka("https://c.diaka.ua/notification_url")
```
### Відправлення тестового повідомлення
```python
# Надіслати тестове сповіщення
status_code = diaka.send_test_notification(
    target="TargetName",
    amount=54,
    name="DiakaPlug",
    message="Привіт від Python",
    source="SourceName",
    show="Show",
    additional="AdditionalInfo"
)
```
### Розбір повідомлення
```python
# Розбір повідомлення за ідентифікатором транзакції та хешем
notification_data = diaka.parse_notification(transaction_id=123, hash="notification_hash")
```
### Отримати останні пожертви
```python
# Отримати останні пожертви з необов'язковими параметрами
last_donations = diaka.get_last_donations(limit=10, test=2)
```
### Отримати найбільші пожертви
```python
# Отримати найбільші пожертви з необов'язковими параметрами
largest_donations = diaka.get_largest_donations(offset=86400, limit=10, test=2)
```
### Отримати суму пожертвувань
```python
# Отримати суму пожертвувань з необов'язковими параметрами
amount_of_donations = diaka.get_amount_of_donations(offset=86400, test=2)
```
### Створення сеансу
```python
# Встановлення сеансу з SSE-сервером та отримання обробленого повідомлення
for notification in diaka.session():
    print(notification)
```

### Асинхронний клас AsyncDiaka

Клас `AsyncDiaka` надає асинхронні методи для взаємодії з сервісом Diaka.

#### Ініціалізація

```python
from diakaplug import AsyncDiaka

# Ініціалізуємо клас AsyncDiaka URL-адресою сповіщення Diaka
async_diaka = AsyncDiaka("https://c.diaka.ua/notification_url")
```
### Відправлення тестового повідомлення
```python
# Надіслати тестове сповіщення
status_code = await async_diaka.send_test_notification(
    target="TargetName",
    amount=54,
    name="DiakaPlug",
    message="Привіт від Python",
    source="SourceName",
    show="ShowName",
    additional="AdditionalInfo"
)
```
### Розбір повідомлення
```python
# Розбір повідомлення за ідентифікатором транзакції та хешем
notification_data = await async_diaka.parse_notification(transaction_id=123, hash="notification_hash")
```
### Отримати останні пожертви
```python
# Отримати останні пожертви з необов'язковими параметрами
last_donations = diaka.get_last_donations(limit=10, test=2)
```
### Отримати найбільші пожертви
```python
# Отримати найбільші пожертви з необов'язковими параметрами
largest_donations = diaka.get_largest_donations(offset=86400, limit=10, test=2)
```
### Отримати суму пожертвувань
```python
# Отримати суму пожертвувань з необов'язковими параметрами
amount_of_donations = diaka.get_amount_of_donations(offset=86400, test=2)
```
### Створення сесії
```python
# Встановлення сеансу з SSE-сервером та отримання обробленого повідомлення
async for notification in async_diaka.session():
    print(notification)
```

# Ліцензія
Цей проект поширюється на умовах [MIT License](https://github.com/d3kxrma/diakaplug/blob/main/LICENSE).