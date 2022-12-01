import os
from flask import Flask, flash, request, redirect, jsonify
from werkzeug.utils import secure_filename
import config as conf
from data.classifier_image import  validaImagem


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify(
               status=200,
               msg='api rodando'
              )
    pass

@app.route('/validate-fish', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        try:
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(conf.UPLOAD_FOLDER, filename))
                ret,acc=validaImagem(os.path.join(conf.UPLOAD_FOLDER, filename))
                os.remove(os.path.join(conf.UPLOAD_FOLDER, filename))
                return jsonify(
                    type=ret,
                    accuracy=float(acc)
                )
        except Exception as e:
             return jsonify(
                    err=400,
                    msg=str(e.args[0])
                )       



if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=3000)
