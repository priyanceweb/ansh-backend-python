from flask import Flask, jsonify, request
import conversion
from paddleocr import PaddleOCR
import os
from PIL import Image
import io
import numpy as np

app = Flask(__name__)

# Initialize the PaddleOCR model once, outside of the request handler
ocr = PaddleOCR(use_angle_cls=True, lang='en', cpu_threads=2, use_gpu=False)

@app.route('/', methods=['GET'])
def health_check():
    return "Ok"

@app.route('/upload-image', methods=['POST'])
def process_image():
    # Get the uploaded file from the request
    file = request.files['file']

    # Load the image using Pillow and convert to numpy array
    image = np.array(Image.open(io.BytesIO(file.read())))

    # Get dimensions
    height = image.shape[0]

    # Extract bottom half of the image
    bottom_half = image[height//2:, :]

    # Perform OCR on the image in smaller chunks
    result = []
    for i in range(0, bottom_half.shape[0], 128):
        chunk = bottom_half[i:i+128]
        result.extend(ocr.ocr(chunk, cls=True)[0])

    # Extract the text values
    text_values = [item[1][0] for item in result if isinstance(item[1], tuple) and isinstance(item[1][0], str)]

    return conversion.search_tracking_and_invoice(text_values)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)