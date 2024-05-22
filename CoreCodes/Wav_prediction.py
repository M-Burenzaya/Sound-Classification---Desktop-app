import sys
import os
from typing import Tuple, List
from numpy.typing import NDArray
import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn

import tempfile
import tkinter as tk
from tkinter import filedialog

import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
# from tqdm import tqdm
# CNN - ээр 2 ангилалд сургасан моделийг тест хийх


class ConvNet(nn.Module):
    def __init__(self, num_classes=2):
        super(ConvNet, self).__init__()

        self.conv1 = nn.Conv2d(in_channels=3, out_channels=12, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(num_features=12)
        self.relu1 = nn.ReLU()
        self.pool = nn.MaxPool2d(kernel_size=2)

        self.conv2 = nn.Conv2d(in_channels=12, out_channels=20, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(num_features=20)
        self.relu2 = nn.ReLU()

        self.conv3 = nn.Conv2d(in_channels=20, out_channels=32, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(num_features=32)
        self.relu3 = nn.ReLU()

        self.fc = nn.Linear(in_features=32 * 128 * 128, out_features=num_classes)

    def forward(self, input):
        output = self.conv1(input)
        output = self.bn1(output)
        output = self.relu1(output)

        output = self.conv2(output)
        output = self.bn2(output)
        output = self.relu2(output)
        output = self.pool(output)

        output = self.conv3(output)
        output = self.bn3(output)
        output = self.relu3(output)

        output = output.view(-1, 32 * 128 * 128)
        output = self.fc(output)

        # probabilities = torch.softmax(output, dim=1)[0]   # unused
        return output


class InfluenzaClassifier:
    audio: NDArray[np.float32]  # self.audio's     type hinting
    sample_rate: int | float  # self.sample_rate type hinting: int or float
    spectrogram: NDArray[np.float32]  # self.spectrogram
    spectrogram_db: NDArray[np.float32]  # self.spectrogram_db
    output_path_spectrogram_img: str

    def __init__(
        self,
        pre_trained_model_path: str = "best_checkpoint_2_class_masked_5_17.model",
    ) -> None:
        self.classes = ["Эрүүл", "Хатгаатай"]
        self.load_pre_trained_model(pre_trained_model_path, using_cpu=True)  # load pretrained model

        # Хувиргалт
        self.transform = transforms.Compose([transforms.Resize((256, 256)), transforms.ToTensor(), transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])])

    def load_pre_trained_model(self, fpath: str, using_cpu: bool = False) -> None:
        # Сургасан модель
        self.model = ConvNet(num_classes=2)
        if not using_cpu:
            self.model.load_state_dict(torch.load(fpath))
            # when with GPU??
        else:
            self.model.load_state_dict(torch.load(fpath, map_location="cpu"))
            # I needed to create this because my laptop don't have GPU
        self.model.eval()

    def generate_spectrogram_from_wav_file(
        self,
        audio_path: str,
        output_directory: str,
        y_min_freq: int = 0,  # Minimum frequency (in Hz)
        y_max_freq: int = 2048,  # Maximum frequency (in Hz)
    ) -> str:
        """Load .wav file and creates and saves"""

        self.audio, self.sample_rate = librosa.load(audio_path, sr=None, dtype=np.float32)
        self.spectrogram = librosa.feature.melspectrogram(y=self.audio, sr=self.sample_rate)
        self.spectrogram_db = librosa.power_to_db(self.spectrogram, ref=np.max)
        self.time = np.linspace(start=0, stop=self.audio.shape[0] * self.sample_rate, num=self.audio.shape[0])  # just for Plotting purposes

        self.freqs = librosa.mel_frequencies(n_mels=self.spectrogram.shape[0], fmin=0, fmax=8000)
        y_min_idx = np.argmin(np.abs(self.freqs - y_min_freq))
        y_max_idx = np.argmin(np.abs(self.freqs - y_max_freq))
        self.spectrogram_db = self.spectrogram_db[y_min_idx:y_max_idx, :]

        plt.figure(figsize=(2.56, 2.56))  # 256x256 зураг
        plt.axis("off")
        plt.imshow(self.spectrogram_db, aspect="auto", cmap="viridis")  # Плот хийх
        plt.tight_layout()

        # Спектрограмыг зураг болгон хадгалах
        filename = os.path.basename(audio_path).split(".")[0] + ".png"
        self.output_path_spectrogram_img = os.path.join(output_directory, filename)
        plt.savefig(self.output_path_spectrogram_img, format="png", bbox_inches="tight", pad_inches=0, transparent=True, dpi=256)
        plt.close()
        return self.output_path_spectrogram_img

    def record_audio(
        self,
        output_directory: str,
        output_filename: str,
        duration: float = 10.0,
        sample_rate: int = 44100,
        channels: int = 1,
    ) -> str:
        """Records Audio, and saves as file"""
        output_recorded_wav_file = os.path.join(output_directory, output_filename)
        print("Бичиж байна...")

        frames = int(duration * sample_rate)
        audio = sd.rec(frames, samplerate=sample_rate, channels=channels, dtype=np.float32)
        sd.wait()  # {duration} секунд бичлэг хийгдтэл хүлээнэ
        sf.write(output_recorded_wav_file, audio, sample_rate)  # Аудио файлыг хадгалах
        print("Цээжний чимээний өгөгдөл хадгалагдлаа:", output_recorded_wav_file)
        return output_recorded_wav_file

    def predict_image(self, image_path: str) -> Tuple[str, List[float]]:
        image = Image.open(image_path)

        if image.mode == "RGBA":
            image = image.convert("RGB")

        image_tensor = self.transform(image).unsqueeze(0)  # type: ignore
        with torch.no_grad():
            output = self.model(image_tensor)
            probabilities = torch.softmax(output, dim=1)[0]
            confidence_scores = probabilities.tolist()
            predicted_class = torch.argmax(probabilities).item()
        predicted_label = self.classes[predicted_class]  # type: ignore
        return predicted_label, confidence_scores

    def playback_loaded_audio_data(self) -> None:
        sd.play(self.audio, self.sample_rate)

def choose_audio() -> str:
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose an audio file", filetypes=[("WAV files", "*.wav")])
    print("Selected audio file:", file_path)
    return file_path


def main() -> None:
    """When using from terminal"""
    output_image_directory = tempfile.gettempdir() # os.path.join(os.getcwd(), "Spectrogram_Output")
    output_audio_directory = tempfile.gettempdir() # os.path.join(os.getcwd(), "Recorded_audio_Output")
    # tempfile.gettempdir() is used for make it work for both windows and linux

    inf_classifier = InfluenzaClassifier()

    while True:
        print("\nХийх үйлдлээ сонгоно уу:")
        print("1. Цээжний чимээний өгөгдөл сонгох")
        print("2. Цээжний чимээний өгөгдөл бичих")
        print("3. exit")
        choice = input("Сонголтоо оруулна уу (1/3): ")

        if choice == "1":
            audio_path = choose_audio()

        elif choice == "2":
            inf_classifier.record_audio(output_audio_directory, "recorded_audio.wav", duration=10, sample_rate=44100, channels=1)
            audio_path = os.path.join(output_audio_directory, "recorded_audio.wav")
            print(f"saved at: {audio_path}")
        elif choice == "3":
            sys.exit(0)
        else:
            print("1, 2 эсвэл  3 гэж оруулна уу.")
            continue

        if audio_path:
            spectrogram_img_path = inf_classifier.generate_spectrogram_from_wav_file(audio_path, output_image_directory)
            spectrogram_image = Image.open(spectrogram_img_path)

            plt.imshow(spectrogram_image)
            plt.axis("off")
            plt.show()

            spectrogram_image.close()
            predicted_label, confidence_scores = inf_classifier.predict_image(spectrogram_img_path)
            print("\nТаамаглаж буй ангилал:", predicted_label)
            print("Таамагласан оноо [Эрүүл, Хатгаатай]:", confidence_scores)


if __name__ == "__main__":
    main()
