import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from ui_lecteurVideo import Ui_MainWindow
from PySide2.QtCore import QUrl, QTime, QFileInfo
from PySide2.QtMultimedia import QMediaPlayer, QMediaContent


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow() # on veut utiliser qu'il y a dans le fichier généré
        self.ui.setupUi(self) # on charge tous les composants graphiques qui sont dedans

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.ui.videoWidget)

        self.ui.dial.setValue(50) # pour avoir le son à 50% de base
        self.mediaPlayer.setVolume(self.ui.dial.value())
        self.ui.volume.setText(f"{self.ui.dial.value()}%")

        self.ui.pbLecture.clicked.connect(self.lectureClicked)
        self.ui.pbPause.clicked.connect(self.pauseClicked)
        self.ui.pbStop.clicked.connect(self.stopClicked)

        self.ui.dial.valueChanged.connect(self.displayVolume)

        self.mediaPlayer.durationChanged.connect(self.mediaDurationChanged)
        self.mediaPlayer.positionChanged.connect(self.mediaPositionChanged)
        self.ui.sTempsCourant.valueChanged.connect(self.sliderPositionChanged)

        self.ui.pbAjouter.clicked.connect(self.ajouterMedia2)
        self.ui.pbSupprimer.clicked.connect(self.supprMedia)
        self.ui.listeLecture.itemDoubleClicked.connect(self.mediaSelected2)

        self.ui.pbPrec.clicked.connect(self.precClicked)
        self.ui.pbSuiv.clicked.connect(self.suivClicked)

        # mediaContent = QMediaContent(QUrl.fromLocalFile("big_buck_bunny.avi"))
        # self.mediaPlayer.setMedia(mediaContent)

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
        self.ui.lTempsTotal.setText(totalTimeMedia.toString("HH:mm:ss"))

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
        self.ui.sTempsCourant.valueChanged.disconnect(self.sliderPositionChanged)
        mediaPosition = self.mediaPlayer.position()
        self.ui.sTempsCourant.setValue(mediaPosition)###########
        currentTimeMedia = QTime(0,0,0)
        currentTimeMedia = currentTimeMedia.addMSecs(mediaPosition)
        self.ui.lTempsCourant.setText(currentTimeMedia.toString("HH:mm:ss"))
        self.ui.sTempsCourant.valueChanged.connect(self.sliderPositionChanged)

    def sliderPositionChanged(self): # comment ça marche ???
        self.mediaPlayer.positionChanged.disconnect(self.mediaPositionChanged)
        self.mediaPlayer.setPosition(self.ui.sTempsCourant.value())
        self.mediaPlayer.positionChanged.connect(self.mediaPositionChanged)

    def ajouterMedia(self):
        nomMedia = QFileDialog.getOpenFileName(self, "Choix Film", "c:/", "Movie Files (*.mp4 *.avi)")
        item = QListWidgetItem(nomMedia[0])
        self.ui.listeLecture.addItem(item)
        print("Média ajouté !")

    def ajouterMedia2(self):
        nomMedia = QFileDialog.getOpenFileName(self, "Choix Film", "c:/", "Movie Files (*.avi *.mp4)")
        if nomMedia[0] == "": #si aucun fichier selectionné (si "Annuler" est sélectionné)
            return        # return + vide => sortie de la fonction

        fInfo = QFileInfo(nomMedia[0])
        fShortName = fInfo.baseName()
        item = QListWidgetItem(fShortName)
        item.setToolTip(nomMedia[0])
        self.ui.listeLecture.addItem(item)

    def supprMedia(self):
        rowItem = self.ui.listeLecture.currentRow()
        if rowItem != -1:
            self.ui.listeLecture.takeItem(rowItem)
        print("Média supprimé !")
        self.stopClicked()

    def mediaSelected(self):
        currentItem = self.ui.listeLecture.currentItem()
        mediaContent = QMediaContent(QUrl.fromLocalFile(currentItem.text()))
        self.mediaPlayer.setMedia(mediaContent)
        self.lectureClicked()
        print("Média sélectionné !")

    def mediaSelected2(self):
        currentItem = self.ui.listeLecture.currentItem()
        mediaContent = QMediaContent(QUrl.fromLocalFile(currentItem.toolTip()))
        self.mediaPlayer.setMedia(mediaContent)
        self.lectureClicked()

    def suivClicked(self):
        currentItemRow = self.ui.listeLecture.currentRow()
        if currentItemRow == -1:
            return
        totalItems = self.ui.listeLecture.count()
        self.ui.listeLecture.setCurrentRow((currentItemRow+1)%totalItems)
        print("Morceau suivant !")
        self.mediaSelected2()

    def precClicked(self):
        currentItemRow = self.ui.listeLecture.currentRow()
        if currentItemRow == -1:
            return
        totalItems = self.ui.listeLecture.count()
        self.ui.listeLecture.setCurrentRow((currentItemRow-1)%totalItems)
        print("Morceau précédent !")
        self.mediaSelected2()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())