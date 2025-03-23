import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QSpinBox, QComboBox
from PyQt5.QtCore import QThread, pyqtSignal
from auto_game import GameBot

class BotThread(QThread):
    update_status = pyqtSignal(str)

    def __init__(self, mode="mining", target_level=48):
        super().__init__()
        self.bot = GameBot()
        self.mode = mode
        self.target_level = target_level

    def run(self):
        self.bot.set_target_level(self.target_level)
        if self.mode == "mining":
            self.bot.start_mining()
        else:
            self.bot.start_module()

    def stop(self):
        if self.bot:
            self.bot.stop()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.bot_thread = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('림버스 컴퍼니 자동화')
        self.setGeometry(100, 100, 400, 200)

        # 중앙 위젯 생성
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # 모드 선택 콤보박스
        self.mode_combo = QComboBox()
        self.mode_combo.addItem("채광", "mining")
        self.mode_combo.addItem("모듈 제작", "module")
        layout.addWidget(QLabel('작업 선택:'))
        layout.addWidget(self.mode_combo)

        # 레벨 선택 (채광 모드용)
        self.level_label = QLabel('목표 레벨:')
        self.level_spin = QSpinBox()
        self.level_spin.setRange(1, 100)
        self.level_spin.setValue(48)
        layout.addWidget(self.level_label)
        layout.addWidget(self.level_spin)

        # 모드 변경 시 레벨 선택 위젯 표시/숨김
        self.mode_combo.currentIndexChanged.connect(self.on_mode_changed)

        # 시작/정지 버튼
        self.start_button = QPushButton('시작')
        self.start_button.clicked.connect(self.start_bot)
        layout.addWidget(self.start_button)

        self.stop_button = QPushButton('정지')
        self.stop_button.clicked.connect(self.stop_bot)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        # 상태 표시 레이블
        self.status_label = QLabel('대기 중...')
        layout.addWidget(self.status_label)

        self.show()

    def on_mode_changed(self, index):
        # 채광 모드일 때만 레벨 선택 표시
        is_mining = self.mode_combo.currentData() == "mining"
        self.level_label.setVisible(is_mining)
        self.level_spin.setVisible(is_mining)

    def start_bot(self):
        if self.bot_thread is None or not self.bot_thread.isRunning():
            mode = self.mode_combo.currentData()
            target_level = self.level_spin.value()
            
            self.bot_thread = BotThread(mode=mode, target_level=target_level)
            self.bot_thread.update_status.connect(self.update_status)
            self.bot_thread.start()
            
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.mode_combo.setEnabled(False)
            self.level_spin.setEnabled(False)
            self.status_label.setText(f'실행 중... (모드: {"채광" if mode == "mining" else "모듈 제작"})')

    def stop_bot(self):
        if self.bot_thread and self.bot_thread.isRunning():
            self.bot_thread.stop()
            self.bot_thread.quit()
            self.bot_thread.wait()
            
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            self.mode_combo.setEnabled(True)
            self.level_spin.setEnabled(True)
            self.status_label.setText('중지됨')

    def update_status(self, status):
        self.status_label.setText(status)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_()) 