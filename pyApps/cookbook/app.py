from flask import Flask, request, jsonify, render_template
import json
from jsonschema import validate, ValidationError
import os

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the uploads directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Load the JSON schema
# with open('schema.json') as f:
#     recipe_schema = json.load(f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        # Parse JSON data
        data = request.form.to_dict()
        data['ingredients'] = data['ingredients'].splitlines()
        data['steps'] = data['steps'].splitlines()

        # Validate against the schema
        # validate(instance=data, schema=recipe_schema)

        # Handle photo upload
        photo = request.files.get('photo')
        if photo:
            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], photo.filename)
            photo.save(photo_path)
            data['photo'] = photo_path

        # Save to a JSON file
        with open('recipes.json', 'a') as f:
            json.dump(data, f)
            f.write('\n')

        return jsonify({"message": "Recipe submitted successfully!"}), 200

    except ValidationError as e:
        return jsonify({"error": str(e)}), 400

    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)
