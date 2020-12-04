import os
from app import app
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename

from main import *

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'files[]' not in request.files:
		flash('No file part')
		return redirect(request.url)
	files = request.files.getlist('files[]')
	file_names = []
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			# file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#else:
		#	flash('Allowed image types are -> png, jpg, jpeg, gif')
		#	return redirect(request.url)
	print('upload image...'+ file_names[0])
	# return render_template('upload.html', filenames=file_names)
	return redirect(url_for('display_image', filename=file_names[0]))

@app.route('/display/<filename>', methods=['GET'])
def display_image(filename):
	print('display_image filename: ' + filename)
	input_path = './static/uploads/' + filename
	output_path = 'static/output/'
	model_name = 'u2net'
	preprocessing_method_name = 'bbd-fastrcnn'
	postprocessing_method_name = 'rtb-bnb'
	save_file_name = filename.split('.')[0] + '.png'
	if model_name == "test":
		print(input_path, output_path, model_name, preprocessing_method_name, postprocessing_method_name)
	else:
		process(input_path, output_path, model_name, preprocessing_method_name, postprocessing_method_name)
		# print("saving {}".format(save_file_name))
	# return render_template('result.html', filenames=file_name)
	return redirect(url_for('static', filename='output/' + save_file_name), code=301)#send_from_directory("static/output", filename)# #

if __name__ == "__main__":
	app.run(debug = True)
