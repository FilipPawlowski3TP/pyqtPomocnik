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
        self.liczby = []  # Inicjalizacja atrybutu self.liczby
        self.ui.spinWartoscN.setEnabled(False)
        self.ui.textLiczby.setEnabled(False)
        self.ui.btnGeneruj.clicked.connect(self.generuj)
        self.ui.btnWczytaj.clicked.connect(self.wczytajPlik)
        # Dodanie przycisku do obliczania średniej (zakładam, że istnieje w layoucie)
        # Jeśli przycisk nie istnieje, trzeba go dodać w layoucie
        try:
            self.ui.btnSrednia.clicked.connect(self.srednia_arytmetyczna)
        except AttributeError:
            pass  # Jeśli przycisk nie istnieje, pomiń

    def generuj(self):
        liczbaN, ok = QInputDialog.getInt(self, "Liczba elementów", 'Podaj liczbę elementów n od 0 do 100:')
        if ok and 0 <= liczbaN <= 100:
            self.ui.spinWartoscN.setValue(liczbaN)
            self.liczby = self.losuj_liczby(liczbaN)  # Zapisanie liczb do self.liczby
            print(self.liczby)
            tekstLiczby = ', '.join(map(str, self.liczby))
            self.ui.textLiczby.setText(tekstLiczby)
            self.uzupelnij()
        elif ok:
            QMessageBox.warning(self, "Błąd", "Podaj liczbę od 0 do 100!")

    def losuj_liczby(self, n):
        liczby = []
        for i in range(n):
            liczba = random.randint(0, 100)
            liczby.append(liczba)
        return liczby

    def wczytajPlik(self):
        nazwaPliku, _ = QFileDialog.getOpenFileName(self, "Otwórz plik", "", "Pliki csv (*.csv)")
        if nazwaPliku:
            try:
                with open(nazwaPliku, 'r') as f:
                    dane = f.read()
                tekstDane = dane.split(';')
                self.liczby = [int(element) for element in tekstDane if element.strip()]  # Zapisanie liczb do self.liczby
                self.ui.textLiczby.setText(', '.join(map(str, self.liczby)))
                self.uzupelnij()
            except (ValueError, FileNotFoundError):
                QMessageBox.critical(self, "Błąd", "Nie udało się wczytać pliku lub dane są nieprawidłowe!")

    def srednia_arytmetyczna(self):
        return sum(self.liczby) / len(self.liczby)
    def srednia_geomatryczna(self):
        iloczyn = 1
        for liczby in self.liczby:
            iloczyn *= liczby
        return iloczyn ** (1/len(self.liczby))

    def uzupelnij(self):
        self.ui.lineSredniaA.setText(f'{self.srednia_arytmetyczna():.2f}')
        self.ui.lineSredniaG.setText(f'{self.srednia_geomatryczna():.2f}')
        self.ui.lineMediana.setText((f'{self.mediana():.2f}'))
        self.ui.lineDominanta.setText(str(self.dominanta()))

    def mediana(self):
        dl = len(self.liczby)
        liczby_posortowane = sorted(self.liczby)
        if dl % 2 == 1:
            return liczby_posortowane[dl // 2]
        else:
            return (liczby_posortowane[dl//2-1]+liczby_posortowane[dl//2]) / 2

    def dominanta(self):
        wystapienia = {}
        for liczba in self.liczby:
            if liczba not in wystapienia.keys():
                wystapienia[liczba] = 1
            else:
                wystapienia[liczba] += 1
        max = 0
        max_arg = 0

        for k, v in wystapienia.items():
            if v > max:
                max = v
                max_arg = k

        return max_arg

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyPizza()
    sys.exit(app.exec())