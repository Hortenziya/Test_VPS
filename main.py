from flask import Flask, request, redirect, url_for, render_template
import os
import time

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        content_length = int(request.headers.get('Content-Length', 0))
        try:
            check_free_space(content_length)
        except Exception as e:
            print(e)
            return "Ooops. Something is wrong. Give me some time to fix it!"
        if file:
            filename = file.filename
            start_time = time.time()
            file.save(os.path.join('static/uploads', filename))
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            return render_template(
                'success.html',
                filename=filename,
                time=time_taken
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
    app.run(host='0.0.0.0')
