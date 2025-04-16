import sys
import typing

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget

from fretboard import Fret, FretboardNotes
from intervals import MajorScale


class Fretboard(QWidget):
    CANVAS_HEIGHT: int = 200
    CANVAS_WIDTH: int = 600
    CANVAS_PADDING: int = 5
    NUT_OFFSET: int = 30

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setSizePolicy(
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
            QtWidgets.QSizePolicy.Policy.MinimumExpanding,
        )

        self._fretboard_height = Fretboard.CANVAS_HEIGHT - (
            Fretboard.CANVAS_PADDING * 2
        )
        self._fretboard_width = Fretboard.CANVAS_WIDTH - (Fretboard.CANVAS_PADDING * 2)
        self._fret_spacing = (self._fretboard_width - Fretboard.NUT_OFFSET) / 12

        # TODO--parametrize
        self.key = "G"
        self.scale = MajorScale(self.key)
        self.fretboard_notes = FretboardNotes(self.scale)
        self.notes = self.fretboard_notes.filter_notes_by_position(Fret(1))

    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(Fretboard.CANVAS_WIDTH, Fretboard.CANVAS_HEIGHT)

    def _paintStrings(self, painter: QtGui.QPainter):
        painter.setPen(QtGui.QColorConstants.LightGray)
        for string in range(6):
            y1 = y2 = (
                int(string * self._fretboard_height / 5) + Fretboard.CANVAS_PADDING
            )
            painter.drawLine(0, y1, Fretboard.CANVAS_WIDTH, y2)

    def _paintFrets(self, painter: QtGui.QPainter):
        pen = QtGui.QPen()
        pen.setCapStyle(QtCore.Qt.PenCapStyle.RoundCap)
        pen.setColor(QtGui.QColorConstants.DarkGray)

        # draw nut
        pen.setWidth(5)
        painter.setPen(pen)
        painter.drawLine(
            Fretboard.NUT_OFFSET,
            Fretboard.CANVAS_PADDING,
            Fretboard.NUT_OFFSET,
            Fretboard.CANVAS_HEIGHT - Fretboard.CANVAS_PADDING,
        )

        # draw frets
        pen.setWidth(2)
        painter.setPen(pen)

        for fret in range(1, 13):
            x1 = x2 = Fretboard.NUT_OFFSET + (fret * self._fret_spacing)
            top = QtCore.QPointF()
            top.setX(x1)
            top.setY(Fretboard.CANVAS_PADDING)
            bottom = QtCore.QPointF()
            bottom.setX(x2)
            bottom.setY(Fretboard.CANVAS_HEIGHT - Fretboard.CANVAS_PADDING)
            painter.drawLine(top, bottom)

    def _paintNotes(self, painter: QtGui.QPainter):
        pen = QtGui.QPen()
        pen.setWidth(8)

        for string, notes in self.notes.items():
            y = (
                int((string - 1) * self._fretboard_height / 5)
                + Fretboard.CANVAS_PADDING
            )
            for fret, note in notes:
                if note == self.key:
                    pen.setColor(QtGui.QColorConstants.Red)
                    painter.setPen(pen)
                else:
                    pen.setColor(QtGui.QColorConstants.Blue)
                    painter.setPen(pen)

                if fret == 0:
                    x = int(Fretboard.NUT_OFFSET / 2)
                else:
                    x = int(
                        Fretboard.NUT_OFFSET
                        + (fret * self._fret_spacing)
                        - (self._fret_spacing / 2)
                    )

                painter.drawPoint(x, y)

    def paintEvent(self, a0) -> None:
        painter = QtGui.QPainter(self)
        self._paintStrings(painter)
        self._paintFrets(painter)
        self._paintNotes(painter)
        painter.end()


class Window(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self._fretboard = Fretboard()
        layout.addWidget(self._fretboard)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())
