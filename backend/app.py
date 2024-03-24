from flask import Flask, request
import cv2
import base64
import io
import numpy as np

app = Flask(__name__)


@app.route('/process', methods=['POST'])
def process_image():
    image = request.files['image'].read()
    img = cv2.imdecode(np.frombuffer(image, np.uint8), cv2.IMREAD_COLOR)

    # Apply filter to the image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (15, 15), 0)

    # Convert back to RGB and encode as base64
    processed_img = cv2.cvtColor(blurred, cv2.COLOR_GRAY2RGB)
    _, buffer = cv2.imencode('.png', processed_img)
    processed_image = base64.b64encode(buffer).decode()

    return {'processedImage': f'data:image/png;base64,{processed_image}'}


if __name__ == '__main__':
    app.run(debug=True)
