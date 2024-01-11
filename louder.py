import os
import wave
import audioop

def amplify_wav(input_dir, output_dir, factor):
    # Убедимся, что выходная директория существует, если нет - создадим её
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Перебор всех файлов в директории
    for filename in os.listdir(input_dir):
        if filename.endswith('.wav'):
            # Создание полного пути к исходному и выходному файлам
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)

            # Открытие WAV файла
            with wave.open(input_path, 'rb') as wav_file:
                # Считывание параметров аудиофайла
                params = wav_file.getparams()
                # Чтение данных (как байты)
                audio_data = wav_file.readframes(params.nframes)

            # Увеличение громкости
            amplified_audio_data = audioop.mul(audio_data, params.sampwidth, factor)
            
            # Создание нового WAV файла с увеличенной громкостью
            with wave.open(output_path, 'wb') as amplified_wav_file:
                amplified_wav_file.setparams(params)
                amplified_wav_file.writeframes(amplified_audio_data)

# Использование функции
input_directory = '/Users/aleksejzubel/Documents/work/преобразование данных гироскопа от колонок в аудиофайл /honor50_gyro_samples_speakers/1' 
output_directory = '/Users/aleksejzubel/Documents/work/преобразование данных гироскопа от колонок в аудиофайл /honor50_gyro_samples_speakers/loudX16/1' 
amplification_factor = 16 # Увеличение громкости в 16 раз

amplify_wav(input_directory, output_directory, amplification_factor)