import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog
from ui_lecteurVideo import Ui_MainWindow
from PySide2.QtCore import QUrl, QTime
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow() # on veut utiliser qu'il y a dans le fichier généré
        self.ui.setupUi(self) # on charge tous les composants graphiques qui sont dedans

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.ui.videoWidget)

        self.ui.dial.setValue(50)
        self.mediaPlayer.setVolume(self.ui.dial.value())
        self.ui.volume.setText(f"{self.ui.dial.value()}%")
        # self.ui.lTempsCourant.setText("00:00:00")
        # self.ui.lTempsTotal.setText("00:00:00")


        self.ui.pbLecture.clicked.connect(self.lectureClicked)
        self.ui.pbPause.clicked.connect(self.pauseClicked)
        self.ui.pbStop.clicked.connect(self.stopClicked)
        self.ui.pbPrec.clicked.connect(self.precClicked)
        self.ui.pbSuiv.clicked.connect(self.suivClicked)
        self.ui.pbAjouter.clicked.connect(self.ajouterClicked)
        self.ui.pbSupprimer.clicked.connect(self.supprimerClicked)
        self.ui.dial.valueChanged.connect(self.displayVolume)
        self.mediaPlayer.durationChanged.connect(self.mediaDurationChanged)
        self.mediaPlayer.positionChanged.connect(self.mediaPositionChanged)
        self.ui.sTempsCourant.valueChanged.connect(self.changeSliderPosition)

        mediaContent = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        self.mediaPlayer.setMedia(mediaContent)

    def lectureClicked(self):
        print("Lecture !")
        self.mediaPlayer.play()

    def pauseClicked(self):
        print("Pause !")
        self.mediaPlayer.pause()

    def stopClicked(self):
        print("Stop !")
        self.mediaPlayer.stop()
        totalTimeMedia = QTime(0,0,0)

    def displayVolume(self):
        self.mediaPlayer.setVolume(self.ui.dial.value())
        self.ui.volume.setText(f"{self.ui.dial.value()}%")
        print(f"Volume modifié à {self.ui.dial.value()}%")

    def mediaDurationChanged(self):
        print("mediaLoaded")
        self.ui.lTempsCourant.setText("00:00:00")
        mediaDuration = self.mediaPlayer.duration()
        self.ui.sTempsCourant.setRange(0,mediaDuration)##########
        totalTimeMedia = QTime(0,0,0)
        totalTimeMedia = totalTimeMedia.addMSecs(mediaDuration)
        self.ui.lTempsTotal.setText(totalTimeMedia.toString("HH:mm:ss"))

    def mediaPositionChanged(self):
        mediaPosition = self.mediaPlayer.position()
        self.ui.sTempsCourant.setValue(mediaPosition)###########
        currentTimeMedia = QTime(0,0,0)
        currentTimeMedia = currentTimeMedia.addMSecs(mediaPosition)
        self.ui.lTempsCourant.setText(currentTimeMedia.toString("HH:mm:ss"))

    def changeSliderPosition(self):
        self.mediaPlayer.positionChanged.disconnect(self.mediaPositionChanged)
        self.mediaPlayer.setPosition(self.ui.sTempsCourant.value())
        self.mediaPlayer.positionChanged.connect(self.mediaPositionChanged)

    def precClicked(self):
        print("Morceau précédent !")

    def suivClicked(self):
        print("Morceau suivant !")

    def ajouterClicked(self):
        print("Élément ajouté !")

    def supprimerClicked(self):
        print("Élément supprimé !")



if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())