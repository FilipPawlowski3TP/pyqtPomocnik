import random
import sys
from itertools import count

from PyQt6.QtWidgets import QDialog, QApplication, QInputDialog, QMessageBox, QFileDialog

from layout import Ui_Dialog


class MyPizza(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.show()
        self.ui.spinWartoscN.setEnabled(False)
        self.ui.textLiczby.setEnabled(False)
        self.ui.btnGeneruj.clicked.connect(self.generuj)
        self.ui.btnWczytaj.clicked.connect(self.wczytajPlik)



    def generuj(self):
        liczbaN, ok = QInputDialog.getInt(self,"Liczba elementow",'Podaj liczbe elementow n od 0 do 100:')
        self.ui.spinWartoscN.setValue(liczbaN)
        wylosowaneLiczby = self.losuj_liczby(liczbaN)
        print(wylosowaneLiczby)
        tekstLiczby = ', '.join(map(str,wylosowaneLiczby))
        self.ui.textLiczby.setText(tekstLiczby)



    def losuj_liczby(self,n):
        liczby = []
        for i in range(n):
            liczba = random.randint(0,100)
            liczby.append(liczba)
        return liczby

    def wczytajPlik(self):
        nazwaPliku, _ = QFileDialog.getOpenFileName(self,"Otworz plik","","Pliki csv (*.csv)")
        if nazwaPliku:
            with open(nazwaPliku,'r') as f:
                dane = f.read()

            tekstDane = dane.split(';')
            wynik = ', '.join(map(str,tekstDane))
            self.ui.textLiczby.setText(wynik)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyPizza()
    sys.exit(app.exec())