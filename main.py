from download import Downloading
from sorting import Sorting
from logger import Logger
from pathlib import Path
import os

def answered_yes(text):
    return text.lower().find("д") > -1 or text.lower().find("y") > -1

def createTempLogFile(vk_url, sorting, remove_long_files):
    Path("temp_log.txt").touch()
    log_file = Logger("temp_log.txt")
    log_file.set_parameter("vk_url", vk_url)
    log_file.set_parameter("sorting", answered_yes(sorting))
    log_file.set_parameter("remove_long_files", answered_yes(remove_long_files))
    log_file.set_parameter("downloaded_tracks", 0)

def removeTempLogFile():
    Path("temp_log.txt").unlink()

if __name__ == "__main__":
    if os.path.isfile("temp_log.txt") == False:
        vk_url = input("Введите ваш полный url профиля ВК >> ")
        sorting = input("Рассортировать треки? (Да/Нет) >> ")
        remove_long_files = input("Удалять треки более 9:59 по времени? (Да/Нет) >> ")
        createTempLogFile(vk_url, sorting, remove_long_files)
    else:
        ask_to_continue = input("Продолжить выполнение программы? (Да/Нет) >> ")
        if answered_yes(ask_to_continue) == False:
            removeTempLogFile()
            exit(0)
    config = Logger("config.txt")
    log_file = Logger("temp_log.txt")
    Downloading(log_file.vk_url, config.browser, config.driver_path,
                log_file.remove_long_files).download()
    if log_file.sorting.lower() == "true":
        Sorting(config.output_dir).sort()
    removeTempLogFile()
    print("Программа завершена!")
