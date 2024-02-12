import os
import numpy as np
from scipy.io.wavfile import write
from scipy.signal import resample

def txt_to_wav(input_directory, output_directory, gyro_fs, audio_fs=8000):
    
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
            
            # Инициализация списка для сохранения евклидовых норм
            evklid_data = []
            
            # Вычисление евклидовой нормы для каждой тройки (x, y, z)
            for x, y, z in zip(x_data, y_data, z_data):
                norm = np.linalg.norm([x, y, z])
                evklid_data.append(norm)
            
            
            # Передискретизация данных с частоты гироскопа на конечную частоту дискретизации аудио
            num_samples = int(len(evklid_data) * float(audio_fs) / gyro_fs)
            evklid_data_resampled = resample(evklid_data, num_samples)
            
            
            # Преобразование данных в аудиоформат для каждой оси и сохранение файлов
            for axis_data, dir_name in zip([evklid_data_resampled], output_directory):
                # Имя файла для аудио
                wav_file_name = os.path.splitext(file_name)[0] + '.wav'
                wav_file_path = os.path.join(output_directory, wav_file_name)
                
                # Запись WAV-файла
                scaled_data = np.int16(axis_data/np.max(np.abs(axis_data)) * 32767)  # приводим к 16-битным значениям
                write(wav_file_path, audio_fs, scaled_data)
            

# Пример использования функции
input_directory = '/Users/aleksejzubel/Documents/work/преобразование данных гироскопа от колонок в аудиофайл /данные гироскопа/voiced_numbers(1-5)/samsungS21'  # Укажите путь к вашей директории с текстовыми файлами
output_directory = '/Users/aleksejzubel/Documents/work/преобразование данных гироскопа от колонок в аудиофайл /samsungS21_gyro_samples_speakers/python/voicedSegments(1-5)/evklid'  # Укажите путь к директории для сохранения .wav файлов
gyro_fs = 400  # Частота дискретизации данных гироскопа, указанная пользователем (Гц)
txt_to_wav(input_directory, output_directory, gyro_fs)