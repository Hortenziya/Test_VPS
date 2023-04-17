import time

from flask import Flask, request, render_template, send_from_directory, Response

from persistence import display_data, get_filename_for_filehash
from upload import save_file

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_file():
    file = request.files['file']
    if not file:
        return Response(response='Uploading file expected', status=400)

    start_time = time.perf_counter()
    content_length = int(request.headers.get('Content-Length', 0))
    try:
        file_doc = save_file(file, start_time, content_length)
        return render_template(
            'success.html',
            filename=file_doc['filename'],
            time=file_doc['upload_duration'],
            date=file_doc['upload_time'],
            hash=file_doc['filehash'],
        )
    except Exception as e:
        print(e)
        return "Ooops. Something is wrong. Give me some time to fix it!"


@app.route('/files/<filehash>')
def uploaded_file(filehash):
    display_data()
    filename = get_filename_for_filehash(filehash)

    return send_from_directory(
        app.config['UPLOAD_FOLDER'], filehash, download_name=filename
    )


if __name__ == '__main__':
    app.run()
