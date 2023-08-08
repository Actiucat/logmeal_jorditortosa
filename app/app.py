from flask import Flask, request, jsonify, render_template
import os
import uuid
import PIL.Image

app = Flask(__name__, static_folder='uploads')
app.config['UPLOAD_FOLDER'] = 'uploads'  # Ruta de la carpeta de almacenamiento de imágenes



# Endpoint para cargar una imagen
@app.route('/upload_image', methods=['POST'])
def upload_image():
    # Comprobación de errores
    if 'image' not in request.files:
        return jsonify({'success': False, 'error': 'No se ha proporcionado una imagen'}), 400

    image_file = request.files['image']
    if image_file.filename == '':
        return jsonify({'success': False, 'error': 'Nombre de archivo incorrecto'}), 400

    image_id = str(uuid.uuid4())  # Genera un ID único para la imagen
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_id)
    image_file.save(image_path)

    return jsonify({'success': True, 'image_id': image_id}), 201



# Endpoint para analizar una imagen por su image_id
@app.route('/analyse_image/<string:image_id>', methods=['GET'])
def analyse_image(image_id):
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_id)
    # Comprobación de errores
    if not os.path.exists(image_path):
        return jsonify({'success': False, 'error': 'Image not found'}), 404

    try:
        image = PIL.Image.open(image_path)  # Utilizar el módulo PIL.Image
        width, height = image.size
        return jsonify({'success': True, 'width': width, 'height': height}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



# Endpoint para listar todas las imágenes y sus image_ids
@app.route('/list_images', methods=['GET'])
def list_images():
    image_list = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.isfile(image_path):
            image_list.append({'image_id': filename})
    
    return jsonify({'success': True, 'images': image_list}), 200

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)