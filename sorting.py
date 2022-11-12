import os
import shutil
import re
from pathlib import Path
from progress.bar import IncrementalBar

class Sorting:
    def __init__(self, output_dir):
        self.output_dir = output_dir
        self.downloads_dir = str(Path().home()) + "\\Downloads\\VK Music"
        self.performers = []

    def sort(self):
        tracks = list(filter(self._isSongFile, os.listdir(self.downloads_dir)))
        bar = IncrementalBar('Countdown', max=len(tracks))
        for track in tracks:
            bar.next()
            self._moveTrack(track)
        self._removeRepeatingTracks()
        os.remove(self.downloads_dir)
        print("\nСортировка завершена")

    def continue_sort(self):
        for performer in os.listdir(self.output_dir):
            self.performers.append(performer)
        self.sort()

    def _removeRepeatingTracks(self):
        dirs = os.listdir(self.output_dir)
        for dir in dirs:
            files = os.listdir(self.output_dir + f"\\{dir}")
            for filename in files:
                if re.search(r"\(\d+\)", filename):
                    os.remove(self.output_dir+f"\\{dir}\\{filename}")

    def _moveTrack(self, filename):
        performer = self._getPerformer(filename)
        performer_dir = f"{self.output_dir}/{performer}"
        if performer not in self.performers:
            self.performers.append(performer)
            try: os.mkdir(performer_dir)
            except: pass
        try: shutil.move(self.downloads_dir + "\\" + filename, performer_dir)
        except: pass

    def _isSongFile(self, name):
        if name[-3:] == "mp3":
            return True
        else:
            return False

    def _getPerformer(self, name):
        return name[:name.find(" - ")].strip()
