import numpy as np
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from werkzeug.utils import secure_filename
import cv2
import glob
import os
from vehicle_detector import VehicleDetector

UPLOAD_FOLDER = 'C:/Users/kvard/OneDrive/Desktop/CiSTUP-IISc/Web Dev/uplods'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load Veichle Detector
vd = VehicleDetector()


@app.route('/uploaded-image/<filename>')
def uploaded_image(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            vehicles_folder_count = analyze_image(filepath)
            annotated_image_path = vehicle_count(filepath)
            filename1 = os.path.basename(annotated_image_path)
            return render_template('uploaded.html', filename=filename, count=vehicles_folder_count, annotated_image=filename1)
    return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def vehicle_count(image_path):
    # Load the image
    img = cv2.imread(image_path)

    # Perform vehicle detection
    vehicle_boxes = vd.detect_vehicles(img)

    # Draw bounding boxes around detected vehicles
    for box in vehicle_boxes:
        x, y, w, h = box
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Add vehicle count text
    vehicle_count = len(vehicle_boxes)
    cv2.putText(img, f"Vehicles: {vehicle_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Convert the image to RGB format
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    filename = os.path.basename(image_path)
    annotated_image_path = os.path.join(
        app.config['UPLOAD_FOLDER'], 'annotated_' + filename)
    cv2.imwrite(annotated_image_path, img)

    # Return the processed image
    return annotated_image_path


def analyze_image(filepath):
    img = cv2.imread(filepath)

    vehicle_boxes = vd.detect_vehicles(img)
    vehicle_count = len(vehicle_boxes)

    for box in vehicle_boxes:
        x, y, w, h = box

        cv2.rectangle(img, (x, y), (x + w, y + h), (25, 0, 180), 3)

        cv2.putText(img, "Vehicles: " + str(vehicle_count),
                    (20, 50), 0, 2, (100, 200, 0), 3)

    cv2.imshow("Cars", img)
    cv2.waitKey(1)

    return vehicle_count


if __name__ == '__main__':
    app.run(debug=True)
