from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QFileDialog, QSlider, QVBoxLayout, QHBoxLayout
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import Qt, QUrl, QTimer
from mutagen.easyid3 import EasyID3
from mutagen.mp3 import MP3
import random
import os


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.current_folder = None
        self.current_file = None 
        self.song_list = []
        self.current_index = -1
        self.shuffle_mode = False
        self.loop_mode = False
        self.timer = QTimer()
        self.settings()
        self.ui()
        self.event_handler()


    def settings(self):
        self.setWindowTitle("Music Player")
        self.resize(600, 150)


    def ui(self):
        self.file_list = QListWidget()
        self.btn_opener = QPushButton("➕")
        self.btn_delete = QPushButton("✖️")
        self.btn_back = QPushButton("⏪")
        self.btn_play_or_pause = QPushButton("▶️")
        self.btn_reset = QPushButton("🔄️")
        self.btn_skip = QPushButton("⏩")
        self.btn_shuffle_or_loop = QPushButton("🔀")
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(80)
        self.slider_left_text = QLabel("-")
        self.slider_right_text = QLabel("+")  
        self.song_title_label = QLabel("🎵 Title: ...")
        self.song_time_label = QLabel("⏱️ 00:00 / 00:00")
        self.album_label = QLabel("💿 Album: ...")
        self.artist_label = QLabel("🎤 Artist: ...")
        self.bitrate_label = QLabel("🔊 Bitrate: ...")
        self.btn_back.setDisabled(True)
        self.btn_play_or_pause.setDisabled(True)
        self.btn_reset.setDisabled(True)
        self.btn_skip.setDisabled(True)
        self.btn_shuffle_or_loop.setDisabled(True)
        self.btn_delete.setDisabled(True)

        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.btn_back)
        controls_layout.addWidget(self.btn_play_or_pause)
        controls_layout.addWidget(self.btn_reset)
        controls_layout.addWidget(self.btn_skip)
        controls_layout.addWidget(self.btn_shuffle_or_loop)

        title_artist_layout = QHBoxLayout()
        title_artist_layout.addWidget(self.artist_label)
        title_artist_layout.addStretch(1)
        title_artist_layout.addWidget(self.album_label)

        bitrate_layout = QVBoxLayout()
        bitrate_layout.addWidget(self.bitrate_label)

        info_layout = QVBoxLayout()
        info_layout.addWidget(self.song_time_label)
        info_layout.addWidget(self.song_title_label)
        info_layout.addLayout(title_artist_layout)
        info_layout.addLayout(bitrate_layout)
        info_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        info_layout.addStretch(1)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(self.slider_left_text)
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.slider_right_text)

        add_or_delete_file_layout = QHBoxLayout()
        add_or_delete_file_layout.addWidget(self.btn_opener)
        add_or_delete_file_layout.addWidget(self.btn_delete)

        slider_and_btns_layout = QHBoxLayout()
        slider_and_btns_layout.addLayout(slider_layout, 1)
        slider_and_btns_layout.addLayout(add_or_delete_file_layout, 1)

        right_layout = QVBoxLayout()
        right_layout.addLayout(info_layout)
        right_layout.addLayout(slider_and_btns_layout)
        right_layout.addLayout(controls_layout)

        center_layout = QHBoxLayout()
        center_layout.addWidget(self.file_list, 2)
        center_layout.addLayout(right_layout, 3)

        self.master = QVBoxLayout()
        self.master.addLayout(center_layout)

        self.setLayout(self.master)

        self.audio_output = QAudioOutput()
        self.audio_output.setVolume(self.slider.value() / 100)
        self.media_player = QMediaPlayer()
        self.media_player.setAudioOutput(self.audio_output)


    def event_handler(self):
        self.btn_opener.clicked.connect(self.open_file)
        self.btn_play_or_pause.clicked.connect(self.play_and_pause_audio)
        self.btn_reset.clicked.connect(self.reset)
        self.file_list.itemClicked.connect(self.choose_audio)
        self.slider.valueChanged.connect(self.change_volume)
        self.timer.timeout.connect(self.update_time)        
        self.btn_delete.clicked.connect(self.delete_song)
        self.btn_skip.clicked.connect(self.next_song)
        self.btn_back.clicked.connect(self.previous_song)
        self.btn_shuffle_or_loop.clicked.connect(self.toggle_shuffle_or_loop)
        self.media_player.mediaStatusChanged.connect(self.handle_media_status)


    def open_file(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")

        if path:
            self.current_folder = path
            self.file_list.clear()
            self.song_list = []
            for file_name in os.listdir(path):
                if file_name.endswith(".mp3"):
                    self.file_list.addItem(file_name)
                    self.song_list.append(file_name)
                    print(self.song_list)
            self.current_index = -1
        else:
            file, _ = QFileDialog.getOpenFileName(self, "Select File", filter="Audio Files (*.mp3)")
            if file:
                self.current_folder = os.path.dirname(file)
                self.file_list.clear()
                self.file_list.addItem(os.path.basename(file))
                self.song_list.append(os.path.basename(file))
                print(self.song_list)


    def choose_audio(self):
        if self.file_list.selectedItems():
            self.current_file = self.file_list.selectedItems()[0].text()
            self.current_index = self.song_list.index(self.current_file)
            print(self.current_index)
            file_path = os.path.join(self.current_folder, self.current_file)
            file_url = QUrl.fromLocalFile(file_path)
            self.media_player.setSource(file_url)
            self.media_player.play()
            self.btn_play_or_pause.setText("⏸️")

            self.read_metadata(file_path)            
            self.timer.start()

            if len(self.song_list) == 1:
                self.btn_back.setDisabled(True)
                self.btn_play_or_pause.setDisabled(False)
                self.btn_reset.setDisabled(False)
                self.btn_skip.setDisabled(True)
                self.btn_shuffle_or_loop.setDisabled(True)
                self.btn_delete.setDisabled(True)
            else:
                self.btn_back.setDisabled(False)
                self.btn_play_or_pause.setDisabled(False)
                self.btn_reset.setDisabled(False)
                self.btn_skip.setDisabled(False)
                self.btn_shuffle_or_loop.setDisabled(False)
                self.btn_delete.setDisabled(False)


    def play_and_pause_audio(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.btn_play_or_pause.setText("▶️")
            self.timer.stop()
        else:
            self.media_player.play()
            self.btn_play_or_pause.setText("⏸️")
            self.timer.start()


    def reset(self):
        self.media_player.setPosition(0)
        self.media_player.play()


    def update_time(self):
        if self.media_player.source().isEmpty():
            return
        
        self.timer.setInterval(1000)

        duration = self.media_player.duration() / 1000
        position = self.media_player.position() / 1000  

        duration_str = f"{int(duration // 60):02}:{int(duration % 60):02}"
        position_str = f"{int(position // 60):02}:{int(position % 60):02}"

        self.song_time_label.setText(f"⏱️ {position_str} / {duration_str}")

    
    def change_volume(self, value):
        volume = value / 100
        self.audio_output.setVolume(volume)


    def read_metadata(self, file_path):
        try:
            audio = MP3(file_path, ID3=EasyID3)
           
            title = audio.get("title")[0]
            artist = audio.get("artist")[0]
            album = audio.get("album")[0]

            bitrate = int(audio.info.bitrate / 1000)
            duration = int(audio.info.length)
            duration_str = f"{duration // 60:02}:{duration % 60:02}"

            self.song_title_label.setText(f"🎵 {title}")
            self.artist_label.setText(f"🎤 {artist}")
            self.album_label.setText(f"💿 {album}")
            self.song_time_label.setText(f"⏱️ 00:00 / {duration_str}")
            self.bitrate_label.setText(f"🔊 {bitrate} kb/s")

        except Exception:
            self.song_title_label.setText("🎵 Tytuł: ...")
            self.artist_label.setText("🎤 Artysta: ...")
            self.album_label.setText("💿 Album: ...")
            self.song_time_label.setText("⏱️ 00:00 / 00:00")
            self.bitrate_label.setText("🔊 Bitrate: ...")


    def delete_song(self):
        if self.current_file and len(self.song_list) > 1:
            self.song_list.remove(self.current_file) 
            self.next_song()
            self.file_list.takeItem(self.file_list.row(self.file_list.selectedItems()[0]))


    def next_song(self):
        if not self.song_list:
            return
        
        if self.shuffle_mode:
            self.current_index = random.randint(0, len(self.song_list) - 1)
        elif self.loop_mode:
            self.media_player.setPosition(0) 
            self.media_player.play()
            return
        else:
            self.current_index = (self.current_index + 1) % len(self.song_list)
        
        self.current_file = self.song_list[self.current_index]

        file_path = os.path.join(self.current_folder, self.current_file)
        file_url = QUrl.fromLocalFile(file_path)
        self.media_player.setSource(file_url)
        self.media_player.play()
        self.btn_play_or_pause.setText("⏸️")

        self.read_metadata(file_path)
        self.timer.start()


    def previous_song(self):
        if not self.song_list:
            return
        
        self.current_index = (self.current_index - 1) % len(self.song_list)
        self.current_file = self.song_list[self.current_index]

        file_path = os.path.join(self.current_folder, self.current_file)
        file_url = QUrl.fromLocalFile(file_path)
        self.media_player.setSource(file_url)
        self.media_player.play()
        self.btn_play_or_pause.setText("⏸️")

        self.read_metadata(file_path)
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


    def handle_media_status(self, status):
        if status == QMediaPlayer.MediaStatus.EndOfMedia:        
            if len(self.song_list) > 1:
                self.next_song()
            else:
                self.media_player.setPosition(0)
                self.media_player.play()


if __name__ in "__main__":
    app = QApplication([])
    main = MusicPlayer()
    main.show()
    app.exec()
