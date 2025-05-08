import os
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
import random

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.current_folder = None
        self.current_file = None 
        self.current_index = -1
        self.shuffle_mode = False
        self.loop_mode = False
        self.song_list = []
        self.timer = QTimer()
        self.settings()
        self.ui()
        self.event_handler()


    def settings(self):
        self.setWindowTitle("Music Player")
        self.resize(500, 250)


    def ui(self):
        self.file_list = QListWidget()
        
        self.btn_opener = QPushButton("ℹ️")
        self.btn_back = QPushButton("⏪")
        self.btn_play_or_pause = QPushButton("▶️")
        self.btn_skip = QPushButton("⏩")
        self.btn_shuffle_or_loop = QPushButton("🔀")

        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(80)

        self.slider_text = QLabel("🔈")
        self.slider_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.song_name_label = QLabel("Tytuł: brak")
        self.song_time_label = QLabel("00:00 / 00:00")

        self.btn_back.setDisabled(True)
        self.btn_play_or_pause.setDisabled(True)
        self.btn_skip.setDisabled(True)
        self.btn_shuffle_or_loop.setDisabled(True)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.btn_back)
        controls_layout.addWidget(self.btn_play_or_pause)
        controls_layout.addWidget(self.btn_skip)
        controls_layout.addWidget(self.btn_shuffle_or_loop)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.song_name_label)
        info_layout.addWidget(self.song_time_label)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider_text)
        slider_layout.addWidget(self.slider)

        add_file_layout = QHBoxLayout()
        add_file_layout.addWidget(self.btn_opener)

        right_layout = QVBoxLayout()
        right_layout.addLayout(info_layout)
        right_layout.addLayout(slider_layout)
        right_layout.addLayout(add_file_layout)

        center_layout = QHBoxLayout()
        center_layout.addWidget(self.file_list, 3)
        center_layout.addLayout(right_layout, 2)

        self.master = QVBoxLayout()
        self.master.addLayout(center_layout)
        self.master.addLayout(controls_layout)

        self.setLayout(self.master)

        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(self.slider.value() / 100)

        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)


    def event_handler(self):
        self.btn_opener.clicked.connect(self.open_file)
        self.btn_play_or_pause.clicked.connect(self.play_and_pause_audio)
        self.file_list.itemClicked.connect(self.choose_audio)
        self.slider.valueChanged.connect(self.change_volume)
        self.timer.timeout.connect(self.update_time)
        self.btn_skip.clicked.connect(self.next_song)
        self.btn_back.clicked.connect(self.previous_song)
        self.btn_shuffle_or_loop.clicked.connect(self.toggle_shuffle_or_loop)


    def open_file(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")

        if path:
            self.current_folder = path
            self.file_list.clear()
            for file_name in os.listdir(path):
                if file_name.endswith(".mp3"):
                    self.file_list.addItem(file_name)
        else:
            file, _ = QFileDialog.getOpenFileName(self, "Select File", filter="Audio Files (*.mp3)")
            if file:
                self.current_folder = os.path.dirname(file)
                self.file_list.clear()
                self.file_list.addItem(os.path.basename(file))


    def choose_audio(self):
        if self.file_list.selectedItems():
            self.current_file = self.file_list.selectedItems()[0].text()
            file_path = os.path.join(self.current_folder, self.current_file)
            file_url = QUrl.fromLocalFile(file_path)
            self.media_player.setSource(file_url)
            self.media_player.play()
            self.btn_play_or_pause.setText("⏸️")

            self.song_name_label.setText(f"Tytuł: {self.current_file}")
            self.timer.start()

            self.btn_back.setDisabled(False)
            self.btn_play_or_pause.setDisabled(False)
            self.btn_skip.setDisabled(False)
            self.btn_shuffle_or_loop.setDisabled(False)


    def play_and_pause_audio(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.btn_play_or_pause.setText("▶️")
            self.timer.stop()

        else:
            self.media_player.play()
            self.btn_play_or_pause.setText("⏸️")
            self.timer.start()


    def update_time(self):
        if self.media_player.source().isEmpty():
            return
        
        self.timer.setInterval(1000)

        duration = self.media_player.duration() / 1000
        position = self.media_player.position() / 1000  

        duration_str = f"{int(duration // 60):02}:{int(duration % 60):02}"
        position_str = f"{int(position // 60):02}:{int(position % 60):02}"

        self.song_time_label.setText(f"{position_str} / {duration_str}")

    
    def change_volume(self, value):
        volume = value / 100
        self.audio_output.setVolume(volume)


    def next_song(self):
        if len(self.song_list) == 0:
            return  

        if self.shuffle_mode:
            self.current_index = random.randint(0, len(self.song_list) - 1)
        else:
            self.current_index = (self.current_index + 1) % len(self.song_list)

        self.current_file = self.song_list[self.current_index]
        file_path = os.path.join(self.current_folder, self.current_file)
        file_url = QUrl.fromLocalFile(file_path)
        self.media_player.setSource(file_url)
        self.media_player.play()
        self.btn_play_or_pause.setText("⏸️")
        self.song_name_label.setText(f"Tytuł: {self.current_file}")
        self.timer.start()


    def previous_song(self):
        self.current_index = (self.current_index - 1) % len(self.song_list)
        self.current_file = self.song_list[self.current_index]
        file_path = os.path.join(self.current_folder, self.current_file)
        file_url = QUrl.fromLocalFile(file_path)
        self.media_player.setSource(file_url)
        self.media_player.play()
        self.btn_play_or_pause.setText("⏸️")
        self.song_name_label.setText(f"Tytuł: {self.current_file}")
        self.timer.start()


    def toggle_shuffle_or_loop(self):
        if not self.shuffle_mode and not self.loop_mode:
            self.shuffle_mode = True
            self.btn_shuffle_or_loop.setText("🔁")
        elif self.shuffle_mode and not self.loop_mode:
            self.shuffle_mode = False
            self.loop_mode = True
            self.btn_shuffle_or_loop.setText("🔂")
        else:
            self.shuffle_mode = False
            self.loop_mode = False
            self.btn_shuffle_or_loop.setText("🔀")


if __name__ in "__main__":
    app = QApplication([])
    main = MusicPlayer()
    main.show()
    app.exec()
