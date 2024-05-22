import os
import torch
import torchvision.transforms as transforms
from PIL import Image
import torch.nn as nn
import tkinter as tk
from tkinter import filedialog
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import sounddevice as sd
import soundfile as sf
from tqdm import tqdm
import numpy as np

# CNN - ээр 2 ангилалд сургасан моделийг тест хийх

# Ангилал
classes = ['Эрүүл', 'Хатгаатай']

output_image_directory = os.path.join(os.getcwd(), 'Spectrogram_Output')
output_audio_directory = os.path.join(os.getcwd(), 'Recorded_audio_Output')

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

        probabilities = torch.softmax(output, dim=1)[0]

        return output

# Сургасан модель
model = ConvNet(num_classes=2)
model.load_state_dict(torch.load('best_checkpoint_2_class_masked_5_17.model'))

model.eval()

# Хувиргалт
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])


def predict_image(image_path):
    image = Image.open(image_path)

    if image.mode == 'RGBA':
        image = image.convert('RGB')

    image_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)[0]
        confidence_scores = probabilities.tolist()
        predicted_class = torch.argmax(probabilities).item()
    predicted_label = classes[predicted_class]
    return predicted_label, confidence_scores


def generate_spectrogram(audio_path, output_directory):

    audio, sample_rate = librosa.load(audio_path, sr=None)
    spectrogram = librosa.feature.melspectrogram(y=audio, sr=sample_rate)

    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

    y_min = 0  # Minimum frequency (in Hz)
    y_max = 2048  # Maximum frequency (in Hz)

    freqs = librosa.mel_frequencies(n_mels=spectrogram.shape[0], fmin=0, fmax=8000)
    y_min_idx = np.argmin(np.abs(freqs - y_min))
    y_max_idx = np.argmin(np.abs(freqs - y_max))
    spectrogram_db = spectrogram_db[y_min_idx:y_max_idx, :]


    plt.figure(figsize=(2.56, 2.56))  # 256x256 зураг
    plt.axis('off')
    plt.imshow(spectrogram_db, aspect='auto', cmap='viridis')  # Плот хийх
    plt.tight_layout()

    # Спектрограмыг зураг болгон хадгалах
    filename = os.path.basename(audio_path).split('.')[0] + '.png'
    output_path = os.path.join(output_directory, filename)
    plt.savefig(output_path, format='png', bbox_inches='tight', pad_inches=0, transparent=True, dpi=256)
    plt.close()
    return output_path


def choose_audio():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose an audio file", filetypes=[("WAV files", "*.wav")])
    print("Selected audio file:", file_path)
    return file_path

def record_audio(output_directory, output_filename, duration=10, sample_rate=44100, channels=1):
    output_file = os.path.join(output_directory, output_filename)
    print("Бичиж байна...")
    frames = int(duration * sample_rate)
    audio = sd.rec(frames, samplerate=sample_rate, channels=channels, dtype='float32')
    sd.wait()  # 10 секунд бичлэг хийгдтэл хүлээнэ
    sf.write(output_file, audio, sample_rate)  # Аудио файлыг хадгалах
    print("Цээжний чимээний өгөгдөл хадгалагдлаа:", output_file)


# Main function
def main():
    while True:
        print("\nХийх үйлдлээ сонгоно уу:")
        print("1. Цээжний чимээний өгөгдөл сонгох")
        print("2. Цээжний чимээний өгөгдөл бичих")
        choice = input("Сонголтоо оруулна уу (1/2): ")

        if choice == '1':
            audio_path = choose_audio()

        elif choice == '2':
            record_audio(output_audio_directory, "recorded_audio.wav", duration=10, sample_rate=44100, channels=1)
            audio_path = os.path.join(output_audio_directory, "recorded_audio.wav")
        else:
            print("1 эсвэл 2 гэж оруулна уу.")
            continue

        if audio_path:
            spectrogram_path = generate_spectrogram(audio_path, output_image_directory)

            spectrogram_image = Image.open(spectrogram_path)

            plt.imshow(spectrogram_image)
            plt.axis('off')
            plt.show()

            spectrogram_image.close()
            predicted_label, confidence_scores = predict_image(spectrogram_path)
            print("\nТаамаглаж буй ангилал:", predicted_label)
            print("Таамагласан оноо [Эрүүл, Хатгаатай]:", confidence_scores)

if __name__ == "__main__":
    main()
