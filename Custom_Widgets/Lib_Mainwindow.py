# ---------- Base libraries -------------------------------------------------------------------------------------------
import os

# from os import PathLike
import sys
import tempfile
import logging

# import subprocess
import platform
from datetime import datetime
from pathlib import Path

# import shutil
import pyqtgraph as pg
# import time

# ---------- Numerical Visual packages---------------------------------------------------------------------------------
import numpy as np
from numpy.typing import NDArray
from scipy.io import wavfile
import wave
import pyaudio

# ---------- GUI libraries --------------------------------------------------------------------------------------------
from PySide6.QtWidgets import QMainWindow, QWidget, QFileDialog
# from PySide6.QtGui import QKeySequence, QShortcut, QColor
from PySide6.QtCore import Qt #pQModelIndex, QDir,

# ---------- Custom libs ----------------------------------------------------------------------------------------------
from Custom_UIs.UI_Mainwindow import Ui_MainWindow


# from Custom_Libs.Lib_DataDirTree import DataDirTree
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")


system_str = platform.system()

logging.basicConfig(
    filename=Path(tempfile.gettempdir()) / datetime.now().strftime("%Y%m%d_%H%M%S.log"),
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG,
)


class TheMainWindow(QMainWindow):
    # Home_dir: str = QDir.homePath()
    audio_wav_data: NDArray[np.int16]
    audio_wav_rate: int

    def __init__(self, parent: QWidget | None = None) -> None:
        super(TheMainWindow, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pb_load_audio_file.clicked.connect(self.callback_load_from_existing_file)
        self.ui.pb_start_record.clicked.connect(self.callback_record_button)

    def callback_load_from_existing_file(self) -> None:
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.FileMode.AnyFile)
        # dlg.setFilter("Text files (*.txt)")
        dlg.setNameFilters(["Other File (*)", "Audio (*.wav)"])
        dlg.selectNameFilter("Audio (*.wav)")

        if dlg.exec_():
            selected_file_path = dlg.selectedFiles()[0]
            self.load_audio_file(selected_file_path)

    def load_audio_file(self, file_path_to_wav) -> None:
        self.audio_wav_rate, self.audio_wav_data = wavfile.read(file_path_to_wav)
        print(self.audio_wav_rate, self.audio_wav_data)
        self.ui.l_loaded_file_rate.setNum(self.audio_wav_rate)
        self.ui.l_loaded_file_dur.setNum(self.audio_wav_data.shape[0] / self.audio_wav_rate)
        self.update_graph()

    def update_graph(self) -> None:
        """updates graph from self.audio_wav_data"""
        time = np.linspace(start=0, stop=self.audio_wav_data.shape[0] * self.audio_wav_rate, num=self.audio_wav_data.shape[0])

        self.ui.pyqt_graph_audio.clear()
        if len(self.audio_wav_data.shape) == 1:  # 1 channel audio
            self.ui.pyqt_graph_audio.plot(time, self.audio_wav_data, pen=pg.mkPen("k", width=1, style=Qt.PenStyle.SolidLine) )
        elif len(self.audio_wav_data.shape) == 2:  # 2 channel audio
            self.ui.pyqt_graph_audio.plot(time, self.audio_wav_data[:, 0], pen=pg.mkPen("r", width=1, style=Qt.PenStyle.SolidLine) )
            self.ui.pyqt_graph_audio.plot(time, self.audio_wav_data[:, 1], pen=pg.mkPen("b", width=1, style=Qt.PenStyle.SolidLine))

    def callback_record_button(self) -> None:
        tmp_file_path = os.path.join(tempfile.gettempdir(), datetime.now().strftime("%Y%m%d_%H%M%S.wav"))
        #self.ui.l_rec_state.setText(f"Recording for {self.ui.sp_audio_rec_duration.value():.1f}s")
        self.ui.pb_start_record.setText("Recording")

        self.record_a_wav_file(
            save_file_path=tmp_file_path,
            rate=self.ui.sp_audio_rec_rate.value(),
            rec_duration=self.ui.sp_audio_rec_duration.value(),
        )
        self.ui.l_rec_state.setText(f"Record saved at {tmp_file_path}")
        self.load_audio_file(tmp_file_path)
        self.ui.pb_start_record.setText("Start New Record")

    def record_a_wav_file(self, save_file_path: str, chunk: int = 1024, channels: int = 2, format=pyaudio.paInt16, rate: int = 44100, rec_duration: float = 10.0) -> None:
        # https://people.csail.mit.edu/hubert/pyaudio/
        channels = 1 if sys.platform == "darwin" else 2
        # takes 2 channels for windows/linux takes 1 channel for mac? not sure why

        with wave.open(save_file_path, "wb") as wf:
            p = pyaudio.PyAudio()
            wf.setnchannels(channels)
            wf.setsampwidth(p.get_sample_size(format))
            wf.setframerate(rate)

            stream = p.open(format=format, channels=channels, rate=rate, input=True)

            print("Recording...")
            for _ in range(0, int(rate / chunk * rec_duration)):
                wf.writeframes(stream.read(chunk))
            print("Done")

            stream.close()
            p.terminate()
