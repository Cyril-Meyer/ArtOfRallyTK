import sys
import os

from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import QFile, QTimer, SIGNAL
from PySide2.QtUiTools import QUiLoader

import dashboard


class Dashboard(QWidget):
    def __init__(self):
        super(Dashboard, self).__init__()
        self.ui = self.load_ui()
        self.setWindowTitle('ArtOfRallyTK - Dashboard')

        self.pm = dashboard.open_aor_process()
        self.addresses = dashboard.get_addresses('./cheat-table/artofrally.CT', self.pm)

        '''
        self.ui.label_1.setText(list(addresses.keys())[0])
        self.ui.label_2.setText(list(addresses.keys())[1])
        self.ui.label_3.setText(list(addresses.keys())[2])
        self.ui.label_4.setText(list(addresses.keys())[3])
        '''
        self.ui.label_1.setText('Speed')
        self.ui.label_2.setText('RPM')
        self.ui.label_3.setText('Gear')
        self.ui.label_4.setText('Steering')

        self.ui.progressBar_1.setRange(0, 200)
        self.ui.progressBar_2.setRange(0, 10000)
        self.ui.progressBar_3.setRange(0, 1)
        self.ui.progressBar_4.setRange(-1000, 1000)

        self.QTimerUpdateUI = QTimer(self)
        self.connect(self.QTimerUpdateUI, SIGNAL("timeout()"), self.updateUI)
        self.QTimerUpdateUI.start(10)

    def updateUI(self):
        k = 'Speed pointer 1'
        self.ui.progressBar_1.setValue(dashboard.get_value(self.addresses[k][0], self.addresses[k][1], self.pm))
        self.ui.lcdNumber_1.display(str(round(dashboard.get_value(self.addresses[k][0], self.addresses[k][1], self.pm), 1)))
        k = 'RPM pointer 1'
        self.ui.progressBar_2.setValue(dashboard.get_value(self.addresses[k][0], self.addresses[k][1], self.pm))
        self.ui.lcdNumber_2.display(int(dashboard.get_value(self.addresses[k][0], self.addresses[k][1], self.pm)))
        k = 'Gear pointer 1'
        self.ui.progressBar_3.setValue(dashboard.get_value(self.addresses[k][0], self.addresses[k][1], self.pm))
        self.ui.lcdNumber_3.display(int(dashboard.get_value(self.addresses[k][0], self.addresses[k][1], self.pm)-1))
        k = 'Steering pointer 1'
        self.ui.progressBar_4.setValue(dashboard.get_value(self.addresses[k][0], self.addresses[k][1], self.pm)*1000)
        self.ui.lcdNumber_4.display(int(dashboard.get_value(self.addresses[k][0], self.addresses[k][1], self.pm)*1000))
        return

    def load_ui(self):
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "dashboard_viewer.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        ui = loader.load(ui_file, self)
        ui_file.close()
        return ui

if __name__ == "__main__":
    app = QApplication([])
    widget = Dashboard()
    widget.show()
    sys.exit(app.exec_())
