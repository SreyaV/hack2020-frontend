from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
import datetime
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import os, csv, uuid

from werkzeug.utils import secure_filename
from Hack2020.music import parse_input, write_midi, process_midi

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'output'
ALLOWED_EXTENSIONS = {'csv'}


try:
    __import__(mailing_list_info)
except:
    mailing_list_name = None
    mailing_list_password = None

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 
#########
# Links #
#########
@app.route('/output/<path:filename>')
def download_file(filename):
    return send_from_directory('output', filename)
@app.route('/playback')
def play_wav():
    uuid_str = request.args.get('uuid')
    return render_template("playback.html", uuid=uuid_str)
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            uuid_str = uuid.uuid1().hex
            filename = secure_filename(uuid_str + '.csv')
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            input_data = parse_input('uploads/' + uuid_str + '.csv')
            output_file = 'output/' + uuid_str + '.midi'
            write_midi(input_data, output_file)
            process_midi(output_file, play=False, output_wav='output/' + uuid_str + '.wav')
            return redirect('/playback?uuid=' + uuid_str)
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True)
