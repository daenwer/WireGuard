#!/home/dmitry/PycharmProjects/WireGuard/venv/bin/python3
# -*- coding: utf-8 -*-
import sys
from subprocess import Popen, PIPE

from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, \
    QInputDialog, QLineEdit, QDesktopWidget


class Example(QMainWindow):

    def __init__(self):
        self.wight = 290
        self.height = 150
        self.enabled = False
        self.sudo = None
        super().__init__()

        self.initUI()

    # def clear_color(self):
    #     self.statusBar().setStyleSheet()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        cp.setY(cp.y() - self.height/2)
        qr.moveCenter(cp)

        self.move(qr.topLeft())

    def initUI(self):

        self.btn = QPushButton("Run VPN", self)
        self.btn.move(95, 55)
        self.btn.clicked.connect(self.button_clicked)

        self.statusBar()

        self.resize(self.wight, self.height)
        self.center()

        self.setWindowTitle('WideGuard')
        # self.setStyleSheet('background: rgb(255,0,0);')

        self.show()

    def get_sudo(self):
        sudo, ok = QInputDialog.getText(
            None, 'Auth', 'Input sudo:', QLineEdit.Password
        )
        if ok:
            self.sudo = sudo
            return sudo

    def run_vpn(self, sudo):
        command = 'sudo wg-quick up wg0'.split()
        p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE,
                  universal_newlines=True)
        sudo_prompt = p.communicate(sudo + '\n')[1]
        if 'incorrect password attempt' in p.communicate()[1]:
            return sudo_prompt

    def stop_vpn(self, sudo):
        command = 'sudo wg-quick down wg0'.split()
        p = Popen(['sudo', '--stdin'] + command, stdin=PIPE, stderr=PIPE,
                  universal_newlines=True)
        sudo_prompt = p.communicate(sudo + '\n')[1]
        if 'incorrect password attempt' in p.communicate()[1]:
            return sudo_prompt

    def button_clicked(self):

        sender = self.sender()

        message = sender.text()
        if message == 'Run VPN':
            sudo = self.get_sudo() if self.sudo is None else self.sudo
            if sudo:
                self.statusBar().showMessage('sudo: ' + sudo)
                error = self.run_vpn(sudo)
                if error:
                    self.statusBar().showMessage('Invalid sudo!')
                    self.sudo = None
                else:
                    self.sudo = sudo
                    self.enabled = True
                    self.statusBar().showMessage('VPN is running!')
                    self.btn.setText('Stop VPN')
                    # self.btn.setStyleSheet('background: rgb(255,0,0);')

        else:
            # sudo = self.get_sudo()
            sudo = self.sudo
            if sudo:
                error = self.stop_vpn(sudo)
                if error:

                    self.statusBar().showMessage('Invalid sudo!')
                else:
                    self.enabled = False
                    self.btn.setText('Run VPN')
                    # self.statusBar().setStyleSheet('color: rgb(255,0,0);')
                    self.statusBar().showMessage('VPN stopped')

    def closeEvent(self, event):
        if self.enabled:
            # self.statusBar().setStyleSheet('color: rgb(255,0,0);')
            self.statusBar().showMessage('Turn off VPN first!')
            event.ignore()
        else:
            event.accept()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
