# downloading-vk-music
Программа, которая может вам скачать всю музыку из вашего профиля ВКонтакте с помощью библиотеки selenium и сервиса vrit.me

Поддержка браузеров: Chrome, Edge

## Требования:
- Python 3.0+
- Selenium driver для используемого браузера

## Установка:
> Клонирование репозитория
>> `$ git clone https://github.com/ackn0wl3dgm3nt/downloading-vk-music`

> Создание виртуального окружения (необязательно):
>> `$ python -m venv venv` - для Windows
>
>> Для Linux:
>>
>> `$ sudo apt install python3-venv`
>> 
>>`$ python3 -m venv venv`
>>
>>
>
> Активация:
>> `$ venv\Scripts\activate.bat` - для Windows
>>
>> `$ source venv/bin/activate` -  для Linux и MacOS
>
> Деактивация:
>
>> `$ deactivate`

> Установка необходимых пакетов python
>> `$ pip install -r requirements.txt`

> Установка Selenium драйвера (скачивайте версию драйвера с такой же версией, как и ваш браузер!)
>> Chrome: https://chromedriver.chromium.org/downloads
>
>> Edge: https://developer.microsoft.com/ru-ru/microsoft-edge/tools/webdriver/

## Использование:
### Настройка config.txt
> `browser=chrome` - Браузер для запуска selenium
>
> `driver_path=C:\SeleniumDrivers\chromedriver\chromedriver.exe` - путь до selenium драйвера. Если вы используете PATH, оставьте параметр пустым
>
> `output_dir=%homepath%\Downloads\VK Music` - директория, где по завершению программы будут находиться скачанные треки. Для Linux замените `%homepath%` на `~`
### Запуск
> `$ python main.py`

> *Введите ваш полный url профиля ВК >>*
>
> *Рассортировать треки? (Да/Нет) >>*
>
> *Удалять треки более 9:59 по времени? (Да/Нет) >>*

При экстренном завершении программы её можно запустить заново и выполнение программы продолжится с того места, где она была завершена
> *Продолжить выполнение программы? (Да/Нет) >>*

