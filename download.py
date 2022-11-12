from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from progress.counter import Counter
from pathlib import Path
from logger import Logger
import time
import re


class Downloading:
    def __init__(self, vk_url, browser="chrome", driver_path="", remove_long_tracks=False):
        self.vk_url = vk_url
        self.browser = browser
        self.driver_path = driver_path
        self.remove_long_tracks = remove_long_tracks
        self.driver = None
        self.download_path = str(Path().home()) + "\\Downloads\\VK Music"

    def _initial(self):
        args = {}
        if self.driver_path != "":
            args["executable_path"] = self.driver_path
        if self.browser == "chrome":
            chrome_options = Options()
            chrome_options.add_argument("--log-level=3")
            chrome_options.add_argument("--disable-notification")
            prefs = {
                "download.default_directory": self.download_path,
                "download.prompt_for_download": False
            }
            chrome_options.add_experimental_option("prefs", prefs)
            args["options"] = chrome_options
            self.driver = webdriver.Chrome(**args)
        else:
            raise Exception("Browser are not supported")
        self.driver.get("https://vrit.me/settings")
        self._auth()

        print("Инициализация завершена")

    def _auth(self):
        wait = WebDriverWait(self.driver, 20)
        input_url = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".block_links input")))
        input_url.send_keys(self.vk_url)
        self.driver.find_elements(By.CLASS_NAME, "control_button_wrapper")[1].click()
        self.driver.find_element(By.CLASS_NAME, "search_send").click()

        current_link = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".info .title")))
        current_link.click()
        page_loaded = wait.until(EC.invisibility_of_element_located((By.CLASS_NAME, "spinner")))

    def download(self):
        self._initial()
        counter = Counter("Downloaded tracks: ")
        c = self._getStartingNumber(counter)
        while self._isAudioOnPage():
            if c % 30 == 0:
                self._loadMoreButtons()
            self._downloadAudio()
            counter.next()
            c += 1
        self.driver.quit()
        self._clearLogFile()
        print("Скачивание треков завершено")

    def _downloadAudio(self):
        is_long_track = self._isLongTrack() if self.remove_long_tracks else False
        if self._isAudioUnavailable() or is_long_track:
            self.driver.execute_script("document.querySelector('.audio').remove()")
            return

        self.driver.find_element(By.CLASS_NAME, "download").click()
        while self._getLoadingButton():
            pass
        self.driver.execute_script("document.querySelector('.audio').remove()")
        self._updateLogFile()

    def _isAudioUnavailable(self):
        if self.driver.find_element(By.CLASS_NAME, "audio").get_attribute("class").find("unavailable") != -1:
            return True
        else:
            return False

    def _isLongTrack(self):
        track_duration = self.driver.find_element(By.CLASS_NAME, "duration").text
        match1 = re.fullmatch(r"\d:\d{2}:\d{2}", track_duration)
        match2 = re.fullmatch(r"\d{2}:\d{2}", track_duration)
        return match1 or match2

    def _getLoadingButton(self):
        try:
            self.driver.find_element(By.CLASS_NAME, "downloaded")
            return False
        except:
            return True

    def _loadMoreButtons(self):
        self._scrollTo("bottom")
        while self._getLoader():
            pass
        self._scrollTo("top")
        time.sleep(0.5)

    def _scrollTo(self, type):
        actions = ActionChains(self.driver)
        scrolling_element = None
        if type == "top":
            scrolling_element = self.driver.find_element(By.CLASS_NAME, "search")
        elif type == "bottom":
            scrolling_element = self.driver.find_element(By.CLASS_NAME, "footer")
        actions.move_to_element(scrolling_element).perform()

    def _getLoader(self):
        try:
            loading = self.driver.find_element(By.CLASS_NAME, "loading")
            return True
        except:
            return False

    def _isAudioOnPage(self):
        try:
            self.driver.find_element(By.CLASS_NAME, "audio")
            return True
        except:
            return False

    def _getStartingNumber(self, counter_obj):
        downloaded_count = self._getDownloadedTracksCount()
        c = 0
        while c < downloaded_count:
            if c % 30 == 0:
                self._loadMoreButtons()
            self.driver.execute_script("document.querySelector('.audio').remove()")
            counter_obj.next()
            c += 1
        return c

    def _getDownloadedTracksCount(self):
        return int(Logger("temp_log.txt").get_parameter("downloaded_tracks"))

    def _updateLogFile(self):
        last_downloaded_track = int(Logger("temp_log.txt").get_parameter("downloaded_tracks"))
        Logger("temp_log.txt").set_parameter("downloaded_tracks", last_downloaded_track + 1)

    def _clearLogFile(self):
        Logger("temp_log.txt").set_parameter("downloaded_tracks", 0)
