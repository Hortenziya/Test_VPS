import datetime
import os
import time
import hashlib

from pymongo import MongoClient
from flask import Flask, request, render_template, send_from_directory
from datetime import datetime
from prettytable import PrettyTable

app = Flask(__name__)
app.config['ENV'] = 'production'
app.config['UPLOAD_FOLDER'] = 'uploads'

client = MongoClient("mongodb://localhost:27017/")
db = client.filedatabase
collection = db.savefile


def display_data():
    # Отримуємо всі документи з колекції
    documents = collection.find()
    # Створюємо таблицю
    table = PrettyTable()
    table.field_names = [
        "filename",
        "filehash",
        "upload_time",
        "upload_duration"
    ]
    for doc in documents:
        table.add_row(
            [
                doc['filename'],
                doc['filehash'],
                doc['upload_time'],
                doc['upload_duration']
            ]
        )
    print(table)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        start_time = time.perf_counter()

        content_length = int(request.headers.get('Content-Length', 0))
        try:
            check_free_space(content_length)
        except Exception as e:
            print(e)
            return "Ooops. Something is wrong. Give me some time to fix it!"

        if file:
            file_doc = save_file(file, start_time)
            return render_template(
                'success.html',
                filename=file_doc['filename'],
                time=file_doc['upload_duration'],
                date=file_doc['upload_time'],
                hash=file_doc['filehash'],

            )
    return render_template('index.html')


@app.route('/files/<filehash>')
def uploaded_file(filehash):
    display_data()
    #повернення документу(словники, які зберігаються в ноу скл бд)
    match = collection.find({'filehash': filehash})
    file_doc = match[0]
    filename = file_doc['filename']
    return send_from_directory(
        app.config['UPLOAD_FOLDER'], filehash, download_name=filename
    )


def check_free_space(file_size):
    free_space = os.statvfs('/')[0] * os.statvfs('/')[4]
    if file_size > free_space:
        raise Exception("Not enough disk space")


def save_file(file, start_time):
    # Генеруємо хешоване ім'я файлу
    real_filename = file.filename
    filename_hash = hashlib.md5(
        f'{real_filename}{str(start_time)}'.encode()
    ).hexdigest()

    # Зберігаємо файл на сервері
    file.save(os.path.join('uploads', filename_hash))

    end_time = time.perf_counter()
    time_taken = round(end_time - start_time, 4)
    # Додаємо інформацію про файл до бази даних
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_doc = {
        'filename': real_filename,
        'upload_time': current_time,
        'upload_duration': time_taken,
        'filehash': filename_hash,
    }
    collection.insert_one(file_doc)

    return file_doc


if __name__ == '__main__':
    app.run()
