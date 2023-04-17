from datetime import datetime
import hashlib
import os
import time

from persistence import collection


#перевірити чи достатньо місця на диску
def check_free_space(file_size):
    free_space = os.statvfs('/')[0] * os.statvfs('/')[4]
    if file_size > free_space:
        raise Exception("Not enough disk space")


#зберегти файл на диск
def save_file(file, start_time, file_size):
    check_free_space(file_size)
    # Генеруємо хешоване ім'я файлу
    real_filename = file.filename
    filename_hash = hashlib.md5(
        f'{real_filename}{str(start_time)}'.encode()
    ).hexdigest()

    # Зберігаємо файл на сервері
    file.save(os.path.join('uploads', filename_hash))

    end_time = time.perf_counter()
    time_taken = round(end_time - start_time, 4)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Додаємо інформацію про файл до бази даних
    file_doc = {
        'filename': real_filename,
        'upload_time': current_time,
        'upload_duration': time_taken,
        'filehash': filename_hash,
    }
    collection.insert_one(file_doc)

    return file_doc
