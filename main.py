import sys, os
from PySide6 import QtGui, QtCore
from PySide6.QtWidgets import QLabel, QApplication, QDialog, QVBoxLayout, QPushButton, QSystemTrayIcon, QMenu
from PySide6.QtCore import Qt, QSize, QTimer
from PySide6.QtGui import QMovie, QIcon, QAction

def showInfoBox (app, pet):
    screen = app.primaryScreen()
    geometry = screen.availableGeometry() #getting the geometry of the screen
    x = geometry.left()
    y = geometry.bottom() - pet.height()

    # Show the info box
    infoBox = InfoBox(pet)
    infoBox.move(x + (infoBox.width()/4), y - infoBox.height())
    infoBox.exec()
#to make the file paths availible in the final application
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

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
    #when pet is double clicked info box will show
    def mouseDoubleClickEvent(self, event):
        print("Double-click detected!")
        if event.button() == Qt.LeftButton:
            print("left button")
            showInfoBox(app, self)

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


class InfoBox(QDialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setWindowTitle("Desktop Pet Instructions")
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setModal(True)
        self.setFixedSize(260, 180)
        #adding instructions to layout
        layout = QVBoxLayout()
        instructions = QLabel(
            "🐾 Desktop Pet Controls 🐾\n\n"
            "• Drag with left mouse button\n"
            "• Right-click to change emote\n"
            "• Double-click to view controls again\n"
            "• Click 'Close Pet' to exit"
        )
        instructions.setWordWrap(True)
        layout.addWidget(instructions)

        closeBtn = QPushButton("Close Pet")
        closeBtn.setStyleSheet("""
            QPushButton {
                background-color: #ececec;
                border: 1px solid #888;
                border-radius: 6px;
                padding: 6px 12px;
                color: #222;
            }
            QPushButton:hover {
                background-color: #d6d6d6;
            }
        """)
        closeBtn.clicked.connect(self.closePet)

        layout.addWidget(closeBtn)
        self.setLayout(layout)

    def closePet(self):
        #closes program
        print("closing program")
        QApplication.instance().quit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    logo = resource_path("gifFiles/logo.png")
    app.setWindowIcon(QIcon(logo))
    app.setQuitOnLastWindowClosed(False)
    # Create the system tray icon that allows logo to stay even when program is closed
    tray = QSystemTrayIcon(QIcon("gifFiles/logo.png"), parent=app)
    menu = QMenu()
    quit_action = QAction("Quit")
    quit_action.triggered.connect(app.quit)
    menu.addAction(quit_action)
    tray.setContextMenu(menu)
    tray.show()

    gif_paths = [
    resource_path("gifFiles/1.gif"),
    resource_path("gifFiles/2.gif"),
    resource_path("gifFiles/3.gif"),
    resource_path("gifFiles/4.gif"),
    ]   
    pet = DesktopPet(gif_paths)
    pet.show()
    #moving the pet to make it spawn in lower left
    screen = app.primaryScreen()
    geometry = screen.availableGeometry() #getting the geometry of the screen
    x = geometry.left()
    y = geometry.bottom() - pet.height()
    pet.move(x, y)

    # will show the info box after the main event loop starts
    #if the info box was shown before, the functions inside it that rely on the pet would not work
    QTimer.singleShot(0, lambda: showInfoBox(app, pet))

    sys.exit(app.exec())

