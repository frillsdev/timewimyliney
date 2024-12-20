from flask import Flask, request, render_template
import json
from datetime import datetime

app = Flask(__name__)
data_file = 'timeline_data.json'

def load_data():
    try:
        with open(data_file, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []  # Return empty list if the file doesn't exist


def save_data(data):
    with open(data_file, 'w') as file:
        json.dump(data, file, indent=4)

def calculate_contrast_colour(hex_colour):
    r = int(hex_colour[1:3], 16) / 255
    g = int(hex_colour[3:5], 16) / 255
    b = int(hex_colour[5:7], 16) / 255
    # Calculate luminance
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    # Return black for light backgrounds, white for dark backgrounds
    return '#000000' if luminance > 0.5 else '#ffffff'


@app.route('/')
def index():
    timeline = load_data()
    return render_template('index.html', timeline=timeline)

@app.route('/hello')
def test():
    return (load_data())


@app.route('/add', methods=['POST'])
def add_entry():
    data = load_data()
    status = request.form['status']
    emoji = request.form['emoji']
    colour = request.form['colour']
    contrast_colour = calculate_contrast_colour(colour)

    new_entry = {
        'status': status,
        'emoji': emoji,
        'colour': colour,
        'contrast_colour': contrast_colour,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    data.append(new_entry)
    save_data(data)
    return render_template('index.html', timeline=data)

if __name__ == '__main__':
    app.run(debug=True)
