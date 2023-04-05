import datetime

from flask import Flask, request, redirect, url_for, render_template
import os
import time
from datetime import datetime


app = Flask(__name__)


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
            filename = file.filename
            file.save(os.path.join('static/uploads', filename))
            end_time = time.perf_counter()
            time_taken = round(end_time - start_time, 4)
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return render_template(
                'success.html',
                filename=filename,
                time=time_taken,
                date=current_time,
            )
    return render_template('index.html')


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename=f'uploads/{filename}'), code=301)


def check_free_space(file_size):
    free_space = os.statvfs('/')[0] * os.statvfs('/')[4]
    if file_size > free_space:
        raise Exception("Not enough disk space")


if __name__ == '__main__':
    app.run()
