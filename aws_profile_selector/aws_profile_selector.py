from PyQt5.QtWidgets import *
import sys
import os

app = QApplication([])


def get_screen_size():
    screen = app.primaryScreen()
    size = screen.size()
    return size.width(), size.height()


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.main_lyt = None
        self.SECRET_KEY = None
        self.ACCESS_KEY = None
        self.__aws_sec_key = None
        self.__acc_add_btn = None
        self.__aws_access_key = None
        self.__aws_acc_disp_name = None
        self.__account_list = None
        self.__account_app = None
        # self.__account_count = 0
        self.__s_width, self.__s_height = get_screen_size()
        self.setGeometry(int(self.__s_width / 4), int(self.__s_height / 4), 600, 400)
        self.UI()

    def UI(self):
        self.setWindowTitle("AWS Account Selector")
        account_wid = QWidget()
        lay = QVBoxLayout()
        acc_list_lay = QHBoxLayout()
        self.__account_list = QListWidget()
        self.add_accounts()
        acc_list_lay.addWidget(self.__account_list)

        btn_list = QVBoxLayout()
        sel_account = QPushButton("Select")
        sel_account.clicked.connect(self.set_account)
        btn_list.addWidget(sel_account)
        del_account = QPushButton("Delete")
        del_account.clicked.connect(self.del_account)
        btn_list.addWidget(del_account)
        btn_list.addStretch()

        acc_list_lay.addLayout(btn_list)

        lay.addWidget(QLabel("Display Name:"))
        self.__aws_acc_disp_name = QLineEdit()
        lay.addWidget(self.__aws_acc_disp_name)
        lay.addWidget(QLabel("Access Key:"))
        self.__aws_access_key = QLineEdit()
        lay.addWidget(self.__aws_access_key)
        lay.addWidget(QLabel("Secret Key:"))
        self.__aws_sec_key = QLineEdit()
        lay.addWidget(self.__aws_sec_key)
        btn_lay = QHBoxLayout()
        self.__acc_add_btn = QPushButton("Add")
        self.__acc_add_btn.clicked.connect(self.add_aws_account)
        btn_lay.addWidget(self.__acc_add_btn)
        cancel_acc_window = QPushButton("Cancel")
        cancel_acc_window.clicked.connect(self.close_acc_window)
        btn_lay.addWidget(cancel_acc_window)
        lay.addLayout(btn_lay)
        lay.addStretch()
        lay.addLayout(acc_list_lay)
        close = QHBoxLayout()
        close_but = QPushButton("Close")
        close_but.clicked.connect(self.close_acc_window)
        close.addStretch()
        close.addWidget(close_but)
        close.addStretch()
        lay.addLayout(close)
        account_wid.setLayout(lay)
        self.setCentralWidget(account_wid)
        self.show()

    def add_aws_account(self):
        with open("accounts/" + self.__aws_acc_disp_name.text() + ".txt", "w") as f:
            # f.write(self.__aws_acc_disp_name.text() + "\n")
            f.write(self.__aws_access_key.text() + "\n")
            f.write(self.__aws_sec_key.text() + "\n")
        self.__aws_acc_disp_name.clear()
        self.__aws_access_key.clear()
        self.__aws_sec_key.clear()
        self.add_accounts()

    def close_acc_window(self):
        exit()

    def add_accounts(self):
        self.__account_list.clear()
        aws_files = os.listdir("accounts")
        if len(aws_files) > 0:
            self.__account_list.addItems([x.split(".")[0] for x in aws_files])

    def del_account(self):
        if len(self.__account_list.selectedItems()):
            os.remove("accounts\\"+self.__account_list.selectedItems()[0].text()+".txt")
        self.add_accounts()

    def set_account(self):
        if len(self.__account_list.selectedItems()) == 1:
            with open("accounts/" + self.__account_list.selectedItems()[0].text() + ".txt", "r") as f:
                data = f.readlines()
            self.ACCESS_KEY = data[0].replace("\n", "")
            self.SECRET_KEY = data[1].replace("\n", "")
            with open("C:\\Users\\" + os.getlogin() + "\\.aws\\config", "w") as f:
                f.write("[default]\n")
                f.write("aws_access_key_id = "+data[0])
                f.write("aws_secret_access_key = "+data[1])


if __name__ == "__main__":
    window = Window()
    sys.exit(app.exec_())
