from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import Qt, QModelIndex
from PyQt5.QtCore import QAbstractTableModel
import pandas as pd
import sys


class SeriesTableModel(QAbstractTableModel):
    def __init__(self, series):
        super(SeriesTableModel, self).__init__()
        self.series = series

    def rowCount(self, parent=QModelIndex()):
        return len(self.series)

    def columnCount(self, parent=QModelIndex()):
        return 1

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return str(self.series.iloc[index.row()])
        return None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Assume series is your Pandas Series
    series = pd.Series([1, 2, 3, 4])
    window = QTableView()
    model = SeriesTableModel(series)
    window.setModel(model)
    window.show()
    sys.exit(app.exec_())