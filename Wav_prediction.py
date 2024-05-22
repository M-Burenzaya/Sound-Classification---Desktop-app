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

# Define the class labels
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

# Load the trained model
model = ConvNet(num_classes=2)
model.load_state_dict(torch.load('best_checkpoint_2_class_masked_5_17.model'))
model.eval()

# Define image transformation
transform = transforms.Compose([
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])

# Function to predict class label of the input image
def predict_image(image_path):
    image = Image.open(image_path)
    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)[0]
        confidence_score, predicted_class = torch.max(probabilities, 0)
    predicted_label = classes[predicted_class]
    return predicted_label, confidence_score.item()

# Function to ask the user to choose an image file
# Function to predict class label of the input image
def predict_image(image_path):
    image = Image.open(image_path)

    # Convert RGBA image to RGB if it has an alpha channel
    if image.mode == 'RGBA':
        image = image.convert('RGB')

    image_tensor = transform(image).unsqueeze(0)  # Add batch dimension
    with torch.no_grad():
        output = model(image_tensor)
        probabilities = torch.softmax(output, dim=1)[0]
        confidence_scores = probabilities.tolist()  # Convert tensor to list
        predicted_class = torch.argmax(probabilities).item()
    predicted_label = classes[predicted_class]
    return predicted_label, confidence_scores
# Main function

# Function to generate and save spectrogram image for a single audio file
def generate_spectrogram(audio_path, output_directory):
    # Load the audio file
    audio, sample_rate = librosa.load(audio_path, sr=None)

    # Generate the spectrogram
    spectrogram = librosa.feature.melspectrogram(y=audio, sr=sample_rate)

    # Convert to decibels
    spectrogram_db = librosa.power_to_db(spectrogram, ref=np.max)

    # Crop and scale the spectrogram
    y_min = 0  # Minimum frequency (in Hz) to display
    y_max = 2048  # Maximum frequency (in Hz) to display
    freqs = librosa.mel_frequencies(n_mels=spectrogram.shape[0], fmin=0, fmax=8000)
    y_min_idx = np.argmin(np.abs(freqs - y_min))
    y_max_idx = np.argmin(np.abs(freqs - y_max))
    spectrogram_db = spectrogram_db[y_min_idx:y_max_idx, :]

    # Plot the spectrogram without axis labels or color bar
    plt.figure(figsize=(2.56, 2.56))  # Set the size of the figure to 256x256 pixels
    plt.axis('off')  # Turn off axis labels
    plt.imshow(spectrogram_db, aspect='auto', cmap='viridis')  # Plot the spectrogram
    plt.tight_layout()

    # Save the spectrogram image as a PNG
    filename = os.path.basename(audio_path).split('.')[0] + '.png'
    output_path = os.path.join(output_directory, filename)
    plt.savefig(output_path, format='png', bbox_inches='tight', pad_inches=0, transparent=True, dpi=256)  # Set DPI to 256 for 256x256 resolution
    plt.close()
    return output_path

# Function to ask the user to choose an audio file
def choose_audio():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Choose an audio file", filetypes=[("WAV files", "*.wav")])
    print("Selected audio file:", file_path)  # Debugging print statement
    return file_path

def record_audio(output_directory, output_filename, duration=10, sample_rate=44100, channels=1):
    output_file = os.path.join(output_directory, output_filename)
    print("Бичиж байна...")
    frames = int(duration * sample_rate)
    audio = sd.rec(frames, samplerate=sample_rate, channels=channels, dtype='float32')
    sd.wait()  # Wait until recording is finished
    sf.write(output_file, audio, sample_rate)  # Save the recorded audio to a file
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
