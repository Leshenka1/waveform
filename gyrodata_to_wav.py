import os
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import resample

def txt_to_wav(input_directory, output_directory, gyro_fs, audio_fs=8000):
    # Создаем выходные директории для каждой оси в указанной выходной директории
    output_dirs = ['1', '2', '3']
    for dir_name in output_dirs:
        os.makedirs(os.path.join(output_directory, dir_name), exist_ok=True)
    
    # Обходим все файлы в директории
    for file_name in os.listdir(input_directory):
        if file_name.endswith('.txt'):
            # Чтение данных из файла
            file_path = os.path.join(input_directory, file_name)
            data = np.loadtxt(file_path)
            
            # Извлекаем данные для каждой оси
            x_data = data[:, 1]
            y_data = data[:, 2]
            z_data = data[:, 3]
            
            # x_data_mean = np.mean(x_data)
            # y_data_mean = np.mean(y_data)
            # z_data_mean = np.mean(z_data)
            
            
            # # Привести данные к одному и тому же диапазону для аудиофайла
            # x_data_centered = x_data - x_data_mean
            # y_data_centered = y_data - y_data_mean
            # z_data_centered = z_data - z_data_mean
            
            # x_data_normalized = np.interp(x_data_centered, (x_data_centered.min(), x_data_centered.max()), (-1, 1))
            # y_data_normalized = np.interp(y_data_centered, (y_data_centered.min(), y_data_centered.max()), (-1, 1))
            # z_data_normalized = np.interp(z_data_centered, (z_data_centered.min(), z_data_centered.max()), (-1, 1))
            
            
            # Передискретизация данных с частоты гироскопа на конечную частоту дискретизации аудио
            num_samples = int(len(x_data) * float(audio_fs) / gyro_fs)
            x_resampled = resample(x_data, num_samples)
            y_resampled = resample(y_data, num_samples)
            z_resampled = resample(z_data, num_samples)
            
            # Преобразование данных в аудиоформат для каждой оси и сохранение файлов
            for axis_data, dir_name in zip([x_resampled, y_resampled, z_resampled], output_dirs):
                # Имя файла для аудио
                wav_file_name = os.path.splitext(file_name)[0] + '.wav'
                wav_file_path = os.path.join(output_directory, dir_name, wav_file_name)
                
                # Запись WAV-файла
                scaled_data = np.int16(axis_data/np.max(np.abs(axis_data)) * 32767)  # приводим к 16-битным значениям
                write(wav_file_path, audio_fs, scaled_data)
            

# Пример использования функции
input_directory = '/Users/aleksejzubel/Documents/work/преобразование данных гироскопа от колонок в аудиофайл /данные гироскопа/honor50'  # Укажите путь к вашей директории с текстовыми файлами
output_directory = '/Users/aleksejzubel/Documents/work/преобразование данных гироскопа от колонок в аудиофайл /honor50_gyro_samples_speakers/python'  # Укажите путь к директории для сохранения .wav файлов
gyro_fs = 400  # Частота дискретизации данных гироскопа, указанная пользователем (Гц)
txt_to_wav(input_directory, output_directory, gyro_fs)