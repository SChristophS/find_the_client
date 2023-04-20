import os
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_from_directory
import flask
#from geoip import open_database
from PIL import Image

from geoip2.database import Reader


#from io import BytesIO

import maxminddb
from pathlib import Path

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['USER_DATA_FILE'] = 'user_data.txt'
app.config['THUMBNAIL_FOLDER'] = 'uploads_thumbnails'
app.config['ALLOWED_EXTENSIONS'] = {'jpg', 'jpeg', 'png', 'gif'}
app.config['USED_PORT'] = 80


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
    
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file selected')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            ext = os.path.splitext(file.filename)[1]
            image_id = f"{uuid.uuid4()}"
            unique_filename = f"{image_id}{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))

            # Create thumbnail
            img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], unique_filename))
            img.thumbnail((200, 200))  # Set the size of the thumbnail
            img.save(os.path.join(app.config['THUMBNAIL_FOLDER'], f"{image_id}_thumbnail{ext}"))

            return jsonify({'thumbnail_filename': f"{image_id}_thumbnail{ext}", 'image_id': image_id})
        else:
            return jsonify({'error': 'Invalid file type. Allowed file types are jpg, jpeg, png, gif.'})

    return render_template('index.html')


@app.route('/delete_image', methods=['POST'])
def delete_image():
    image_id = request.form['image_id']
    image_ext = request.form['image_ext']
    image_filename = f"{image_id}{image_ext}"
    thumbnail_filename = f"{image_id}_thumbnail{image_ext}"
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    thumbnail_path = os.path.join(app.config['THUMBNAIL_FOLDER'], thumbnail_filename)

    if os.path.exists(image_path):
        os.remove(image_path)
        print("Deleted image at: " + image_path)
    else:
        print("Unable to delete image at path:" + image_path)

    if os.path.exists(thumbnail_path):
        os.remove(thumbnail_path)
    else:
        print("Unable to delete thumbnail at path: " + thumbnail_path)

    return 'OK', 200


@app.route('/thumbnails/<path:filename>')
def thumbnail(filename):
    return flask.send_from_directory(app.config['THUMBNAIL_FOLDER'], filename)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    reader = Reader('GeoLite2-City.mmdb')

    ip = request.remote_addr
    
    
    try:
        location = reader.city(ip)
        country = location.country.name
        region = location.subdivisions.most_specific.name
        city = location.city.name
    except:
        country = "N/A"
        region = "N/A"
        city = "N/A"

    image_id = os.path.splitext(filename)[0]
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(app.config['USER_DATA_FILE'], 'a') as f:
        f.write(f"{image_id};{timestamp};{ip};{country};{region};{city}\n")

    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@app.route('/get_user_data')
def get_user_data():
    data = []
    with open(app.config['USER_DATA_FILE'], 'r') as f:
        for line in f:
            image_id, timestamp, ip, country, region, city = line.strip().split(';')
            data.append({
                'image_id': image_id,
                'timestamp': timestamp,
                'ip': ip,
                'country': country,
                'region': region,
                'city': city
            })
    return jsonify(data)

@app.route('/get_upload_data')
def get_upload_data():
    upload_dir = Path('uploads')
    image_ids = [{"id": f.stem, "ext": f.suffix} for f in upload_dir.glob('*')]
    return jsonify(image_ids)

@app.route('/delete_user_data', methods=['POST'])
def delete_user_data():
    image_id = request.form['image_id']
    timestamp = request.form['timestamp']
    lines_to_keep = []

    with open(app.config['USER_DATA_FILE'], 'r') as f:
        for line in f:
            if not (line.startswith(image_id) and line.split(';')[1] == timestamp):
                lines_to_keep.append(line)

    with open(app.config['USER_DATA_FILE'], 'w') as f:
        f.writelines(lines_to_keep)

    return 'OK', 200


if __name__ == '__main__':
    app.run(port=app.config['USED_PORT'])
