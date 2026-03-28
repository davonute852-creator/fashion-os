import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'design-system-secret-key'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, 'static', 'images')
DESIGNS_DIR = os.path.join(BASE_DIR, 'static', 'designs')
UPLOAD_DIR = os.path.join(BASE_DIR, 'static', 'uploads')

for d in [IMAGES_DIR, DESIGNS_DIR, UPLOAD_DIR]:
    os.makedirs(d, exist_ok=True)

app.config['IMAGES_DIR'] = IMAGES_DIR
app.config['DESIGNS_DIR'] = DESIGNS_DIR
app.config['UPLOAD_DIR'] = UPLOAD_DIR

METADATA_FILE = os.path.join(BASE_DIR, 'data', 'images.json')
os.makedirs(os.path.dirname(METADATA_FILE), exist_ok=True)

def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_metadata(data):
    with open(METADATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    images = load_metadata()
    # 按上传时间倒序排列，最新的图片在最前面
    images.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
    lang = request.args.get('lang', 'en')
    return render_template('index.html', images=images, lang=lang)

@app.route('/library')
def library():
    images = load_metadata()
    # 按上传时间倒序排列，最新的图片在最前面
    images.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
    lang = request.args.get('lang', 'en')
    return render_template('library.html', images=images, lang=lang)

@app.route('/design')
def design():
    images = load_metadata()
    # 按上传时间倒序排列，最新的图片在最前面
    images.sort(key=lambda x: x.get('uploaded_at', ''), reverse=True)
    lang = request.args.get('lang', 'en')
    return render_template('design.html', images=images, lang=lang)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No image selected'}), 400
    
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png', '.webp', '.gif']:
        return jsonify({'error': 'Invalid image format'}), 400
    
    unique_name = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(app.config['UPLOAD_DIR'], unique_name)
    file.save(filepath)
    
    tags = request.form.get('tags', '').split(',')
    tags = [t.strip() for t in tags if t.strip()]
    
    metadata = load_metadata()
    image_data = {
        'id': uuid.uuid4().hex,
        'filename': unique_name,
        'original_name': filename,
        'tags': tags,
        'category': request.form.get('category', 'uncategorized'),
        'description': request.form.get('description', ''),
        'uploaded_at': datetime.now().isoformat()
    }
    metadata.append(image_data)
    save_metadata(metadata)
    
    return jsonify({'success': True, 'image': image_data})

@app.route('/search')
def search_images():
    query = request.args.get('q', '').lower()
    category = request.args.get('category', '')
    
    metadata = load_metadata()
    results = metadata
    
    if query:
        results = [img for img in results if 
                   query in img.get('tags', []).lower() or 
                   query in img.get('description', '').lower() or
                   query in img.get('original_name', '').lower()]
    
    if category:
        results = [img for img in results if img.get('category') == category]
    
    return jsonify(results)

@app.route('/generate', methods=['POST'])
def generate_design():
    data = request.json
    requirement = data.get('requirement', '')
    reference_images = data.get('reference_images', [])
    
    if not requirement:
        return jsonify({'error': 'No requirement provided'}), 400
    
    # TODO: Integrate with LLM to generate design
    # For now, return a placeholder
    
    return jsonify({
        'success': True,
        'design': {
            'id': uuid.uuid4().hex,
            'requirement': requirement,
            'references': reference_images,
            'generated_at': datetime.now().isoformat(),
            'status': 'pending'
        }
    })

@app.route('/style3d/send', methods=['POST'])
def send_to_style3d():
    data = request.json
    design_id = data.get('design_id')
    
    if not design_id:
        return jsonify({'error': 'No design_id provided'}), 400
    
    # TODO: Integrate with Style 3D API
    # This is a placeholder until user provides API documentation
    
    return jsonify({
        'success': True,
        'message': 'Design sent to Style 3D (placeholder)',
        'style3d_id': None
    })

@app.route('/api/images')
def api_images():
    return jsonify(load_metadata())

@app.route('/api/images/<image_id>', methods=['DELETE'])
def delete_image(image_id):
    metadata = load_metadata()
    metadata = [img for img in metadata if img['id'] != image_id]
    save_metadata(metadata)
    return jsonify({'success': True})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port)
