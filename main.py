import sys
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QLabel, QApplication
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QMovie

class DesktopPet(QLabel):
    def __init__(self, gifFiles):
        super().__init__()
        self.gifFiles = gifFiles

        self.current_emote = 0 #index of the current emote

        #setting up the window
        self.setWindowFlags(
            Qt.FramelessWindowHint | 
            Qt.WindowStaysOnTopHint | #makes the pet stay on top of all other windows
            Qt.NoDropShadowWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("background: transparent; border: none;")

        self.pic_size = QSize(70,70)
        #making the gif animated
        self.movie = QMovie(self.gifFiles[self.current_emote])
        self.movie.setScaledSize(self.pic_size)
        self.setMovie(self.movie)
        self.setFixedSize(self.pic_size)
        self.movie.start()
        
        self.offset = None

    def next_emote(self, event=None):  
        print("displaying next emote")
        self.current_emote = (self.current_emote + 1) % len(self.gifFiles)
        self.movie.stop()
        self.movie = QMovie(self.gifFiles[self.current_emote])
        self.movie.setScaledSize(self.pic_size)
        self.setMovie(self.movie)
        self.setFixedSize(self.pic_size)
        self.movie.start()

    def mousePressEvent(self, ev):
        if (ev.button() == Qt.LeftButton):
            self.offset = ev.position().toPoint() #allows user to drag/move widget
        elif (ev.button() == Qt.RightButton):
            self.next_emote() #switch emotes
    
    def mouseMoveEvent(self, ev): #when the user drags
        if self.offset is not None:
            self.move(self.pos() + ev.position().toPoint() - self.offset)
    def mouseReleaseEvent(self, ev): 
        #when dragging stops it resets the offset
        self.offset = None
    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
        painter.fillRect(self.rect(), QtCore.Qt.transparent)
        super().paintEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pet = DesktopPet(["gifFiles/1.gif", "gifFiles/2.gif", "gifFiles/3.gif", "gifFiles/4.gif"])
    pet.show()
    sys.exit(app.exec())

