import os
from datetime import datetime

from flask import Flask, request
from paths import envPath
from dotenv import load_dotenv

load_dotenv()

# OR, the same with increased verbosity
load_dotenv(verbose=True)

load_dotenv(dotenv_path=envPath)

from src.pkg.utils.common import init_logger
from src.services.script.router import image_blueprint

app = Flask(__name__)
app.register_blueprint(image_blueprint)

init_logger('./out.log')


@app.route('/', methods=['GET'])
def status():
    return "Active: " + str(datetime.now())


# @app.route('/image/process', methods=['POST'])
# def processImage():
#     # Validating image file
#     if 'file' not in request.files:
#         abort(400, 'File not found in request')
#     image_file = request.files['file']
#     if image_file.filename == '':
#         abort(400, 'No selected file')
#     if image_file and not allowedFile(image_file.filename):
#         abort(400, 'File extension not supported: ' + image_file.filename)
#
#     # Getting data
#     data = parseJson(request.form.get("data"))
#     if not data:
#         abort(400, 'Data block is not a valid json')
#
#     # Validating the data with schema
#     schema_path = os.path.join(schemaPath, 'processImage.json')
#     if os.path.isfile(schema_path):
#         with open(schema_path, 'r') as schema_file:
#             schema = json.loads(schema_file.read())
#             try:
#                 validate(data, schema)
#             except ValidationError as e:
#                 abort(400, "Schema validation failed: " + str(e))
#     else:
#         abort(500, 'Schema file not found: ' + schema_path)
#
#     # Processing the image
#     processed_image = getProcessedImage(io.BytesIO(image_file.read()), data)
#     myprint(processed_image.getbuffer().nbytes)
#     processed_image.seek(0)
#     encoded_image = base64.b64encode(processed_image.read()).decode("utf-8")
#     return encoded_image
#
#
# @app.route('/image/process/base64', methods=['POST'])
# def processBase64Image():
#     # Validating image file
#     if 'file' not in request.form:
#         abort(400, 'File not found in request')
#     image_file = request.form.get("file")
#     im = Image.open(io.BytesIO(base64.b64decode(image_file)))
#     myprint(im.size)
#     # Getting data
#     data = parseJson(request.form.get("data"))
#     if not data:
#         abort(400, 'Data block is not a valid json')
#
#     # Validating the data with schema
#     schema_path = os.path.join(schemaPath, 'processImage.json')
#     if os.path.isfile(schema_path):
#         with open(schema_path, 'r') as schema_file:
#             schema = json.loads(schema_file.read())
#             try:
#                 validate(data, schema)
#             except ValidationError as e:
#                 abort(400, "Schema validation failed: " + str(e))
#     else:
#         abort(500, 'Schema file not found: ' + schema_path)
#
#     # Processing the image
#     processed_image = getProcessedImage(io.BytesIO(base64.b64decode(image_file)), data)
#     myprint(processed_image.getbuffer().nbytes)
#     processed_image.seek(0)
#     encoded_image = base64.b64encode(processed_image.read()).decode("utf-8")
#     return encoded_image


# def allowedFile(filename):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
#
# def getProcessedImage(image_file, data: Dict):
#     image_instance = ImageProcessing().load_from_memory(image_file)
#     for v in data["text"]:
#         text_type = TextType(v["msg"], v["font_family"], v["font_size"], v["color"])
#         if v["coordinates"] is not None:
#             text_type.set_coordinates(TextCoordinates(
#                 v["coordinates"]["type"],
#                 v["coordinates"]["unit"],
#                 v["coordinates"]["points"]
#             ))
#         image_instance.add_text(text_type)
#     processed_image = image_instance.image_in_bytes()
#     return processed_image


@app.before_request
def log_request_info():
    if os.getenv("FLASK_ENV") == "development":
        app.logger.debug('Headers: %s', request.headers)
        app.logger.debug('Body: %s', request.get_data())


if __name__ == '__main__':
    port = 4501
    if os.getenv("port") is not None and len(os.getenv("port")) > 0:
        port = os.getenv("port")

    debug = True
    if os.getenv("debug") is not None and os.getenv("debug").lower() == "n":
        debug = False
    app.run(debug=debug, host='127.0.0.1', port=4501)
