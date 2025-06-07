import sys
from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtCore import Qt 
from PySide6.QtGui import QMovie

class DesktopPet(QLabel):
    def __init__(self, gifFiles):
        super().__init__()
        self.gifFiles = gifFiles

        self.current_emote = 0 #index of the current emote

        #setting up the window
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | 
            Qt.Tool
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        #making the gif animated
        self.movie = QMovie(self.gifFiles[self.current_emote])
        self.setMovie(self.movie)
        self.movie.start()
        
        self.offset = None

    def next_emote(self, event=None):  
        print("displaying next emote")
        self.current_emote = (self.current_emote + 1) % len(self.emotes)
        self.movie.stop()
        self.movie = QMovie(self.gif_files[self.current_emote])
        self.setMovie(self.movie)
        self.movie.start()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet(["gifFiles/1.gif"])
    pet.show()
    sys.exit(app.exec())

