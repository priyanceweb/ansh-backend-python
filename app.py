# import necessary libraries and functions 
from flask import Flask, jsonify, request 
import conversion
from paddleocr import PaddleOCR
import os

# creating a Flask app 
app = Flask(__name__) 

ocr = PaddleOCR(use_angle_cls=True, lang='en') # need to run only once to download and load model into memory

  
# on the terminal type: curl http://127.0.0.1:5000/ 
# returns hello world when we use GET. 
# returns the data that we send when we use POST. 
@app.route('/upload-image', methods = ['POST']) 
def home(): 

    f = request.files['file'] 
    f.save(f.filename)   

    
    # Perform OCR on the cropped bottom left portion
    result = ocr.ocr(f.filename, cls=True)

    # for idx in range(len(result)):
    #     res = result[idx]
    #     for line in res:
    #         print(line)

    parsed_data = result[0]

    # Extract the text values
    text_values = [item[1][0] for item in parsed_data if isinstance(item[1], tuple) and isinstance(item[1][0], str)]

    return conversion.search_tracking_and_invoice(text_values)
# driver function 
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
  
    app.run(debug = True) 