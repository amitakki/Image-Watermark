from app import app
from flask import request, render_template, url_for
import os
import cv2
import numpy as np
from PIL import Image
import random
import string


# Adding path to config
app.config['INITIAL_FILE_UPLOADS'] = "app/static/uploads"

# Route to home page
@app.route("/", methods=["GET", "POST"])

def index():

    # Execute if the request is GET
    if request.method == 'GET':
        full_filename = 'images/white_bg.jpg'
        return render_template("index.html", full_filename=full_filename)
    

    # Execute if the request if POST
    options = request.form['options']
    image_upload = request.files['image_upload']
    image_name = image_upload.filename
    image = Image.open(image_upload)
    image_logow = np.array(image.convert("RGB"))
    h_image, w_image, _ = image_logow.shape

    # printing lowercase
    letters = string.ascii_lowercase
    name = ''.join(random.choice(letters) for i in range(10)) + '.png'
    full_filename = 'uploads/' + name

    if options == 'logo_watermark':
        logo_upload = request.files['logo_upload']
        logoname = logo_upload.filename
        logo = Image.open(logo_upload)
        logo = np.array(logo.convert("RGB"))
        h_logo, w_logo, _ = logo.shape
        center_y = int(h_image/2)
        center_x = int(w_image/2)
        top_y = center_y - int(h_logo/2)
        left_x = center_x - int(w_logo/2)
        bottom_y = top_y + h_logo
        right_x = left_x + w_logo

        # Get ROI
        roi = image_logow[top_y:bottom_y, left_x:right_x]
        # Add logo to the ROI
        result = cv2.addWeighted(roi, 1, logo, 1, 0)
        # Drawing
        image_logow[top_y:bottom_y, left_x:right_x] = result

        img = Image.fromarray(image_logow, 'RGB')
        img.save(os.path.join(app.config[['INITIAL_FILE_UPLOADS'], name]))
        return render_template('index.html', full_filename = full_filename)
    else:
        text_mark = request.form['text_mark']

        cv2.putText(image_logow, text=text_mark, org=(w_image - 100, h_image - 10), 
                    fontFace=cv2.FONT_HERSHEY_COMPLEX, fontScale=0.5, color=(255, 255, 255), thickness=2, lineType=cv2.LINE_4)
        
        timg = Image.fromarray(image_logow, 'RGB')
        timg.save(os.path.join(app.config[['INITIAL_FILE_UPLOADS'], name]))
        return render_template('index.html', full_filename = full_filename)

        