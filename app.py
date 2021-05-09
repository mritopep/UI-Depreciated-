from flask import Flask, render_template, request, redirect, url_for
from mri2pet import Mri2Pet
from os import path, mkdir, listdir, unlink
from flask_ngrok import run_with_ngrok
from werkzeug.utils import secure_filename
from shutil import rmtree

from server_util import *

app_root = path.dirname(path.abspath(__file__))

app = Flask(__name__)

run_with_ngrok(app)

model = Mri2Pet()

print(bcolors.BOLD, model, bcolors.ENDC, flush=True)

# initialization
skull_strip = False
denoise = False
bias_field_correction = False
file_upload_start = False
file_upload_end = False
preprocess_start = False
process_status = True
preprocess_end = False
generate_start = False
generate_end = False
saving_start = False
saving_end = False
start = False
end = False


@app.route("/")
def index():
    start = True
    end = False
    return render_template("index.html")


@app.route("/upload", methods=['GET', 'POST'])
def upload():
    file_upload_start = True
    global model
    if request.method == 'POST':
        if request.files:
            f = request.files['mri_file']
            if not supported_file(f.filename):
                print("File not supported")
                return redirect(request.url)
            else:
                create_folders()
                filename = secure_filename(f.filename)
                f.save(path.join(app_root, 'input', 'nii', filename))
                print("uploaded")
                file_upload_end = True

    return render_template("index.html")


@app.route("/next", methods=['GET', 'POST'])
def next():
    global model
    print(bcolors.OKBLUE + "Starting" + bcolors.ENDC)

    input_folder = path.join(app_root, 'input', 'nii')
    file_path = input_folder + '/' + listdir(input_folder)[0]

    print(f"File path : {file_path}")

    preprocess_start = True
    process_status = model.process(file_path, Skull_Strip=skull_strip,
                  Denoise=denoise, Bais_Correction=bias_field_correction)
    preprocess_end = True

    generate_start = True
    model.generate()
    generate_end = True

    saving_start = True
    model.save()
    saving_end = True

    print(bcolors.OKGREEN + 'Pet saved' + bcolors.ENDC)

    start = False
    end = True

    return render_template("index.html")


@app.route("/download", methods=['GET', 'POST'])
def download():

    file_path = path.join(app_root, 'output/nii/pet.nii.gz')

    def generate():
        with open(file_path, "rb") as file:
            yield from file

        delete_contents('./output')
        delete_contents('./input')

        # initialization
        skull_strip = False
        denoise = False
        bias_field_correction = False
        file_upload_start = False
        file_upload_end = False
        preprocess_start = False
        process_status = True
        preprocess_end = False
        generate_start = False
        generate_end = False
        saving_start = False
        saving_end = False
        start = True
        end = False

        print(bcolors.OKBLUE + "All files deleted" + bcolors.ENDC)

    response = app.response_class(generate(), mimetype='application/x-gzip')
    response.headers.set('Content-Disposition',
                         'attachment', filename="pet.nii.gz")
    return response


@app.route("/test", methods=['GET', 'POST'])
def test():
    global model
    model.load_test_data()
    model.test()
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
