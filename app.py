# app.py

from flask import Flask, request, jsonify, render_template
from image_processing import process_image
from ai_model import recommend_size
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('upload.html')


@app.route('/upload-image', methods=['POST'])
def upload_image():
    # Gather uploaded image file
    image_file = request.files.get('image')
    if not image_file:
        return jsonify({'error': 'No image uploaded'}), 400

    # Save the uploaded image
    image_path = os.path.join('static', 'images', image_file.filename)
    image_file.save(image_path)

    # Collect user input for height, weight, and reference object dimensions
    gender = request.form.get('gender')
    if gender not in ['male', 'female']:
        return jsonify({'error': 'Invalid gender provided'}), 400

    try:
        height = float(request.form.get('height'))
        weight = float(request.form.get('weight'))
        ref_length = float(request.form.get('ref_length'))
        ref_width = float(request.form.get('ref_width'))
    except ValueError:
        return jsonify({'error': 'Invalid numeric input for height, weight, or reference object dimensions'}), 400

    # Process the image to extract measurements using the reference object
    measurements = process_image(image_path, ref_length, ref_width)
    if not measurements:
        return jsonify({'error': 'Failed to process image'}), 400

    # Include height and weight in the measurements
    measurements["Height"] = height
    measurements["Weight"] = weight

    # Recommend size based on gender and extracted measurements
    recommended_size = recommend_size(gender, measurements)

    return jsonify({
        'measurements': measurements,
        'recommended_size': recommended_size
    })


if __name__ == '__main__':
    app.run(debug=True)
