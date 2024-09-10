from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for
import pyvista as pv
import geopandas as gpd
import vtk
import shapely
import pyvista as pv
import numpy as np
from vtk.util import numpy_support as VN
import io
import os
from model import getBaseMap, getHeightMap, render3d, render2d, compileModel
import shutil

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('modelMenu.html')

@app.route('/uploadfolder', methods=['POST'])
def uploafolder():
    if 'folder' not in request.files:
        return 'No folder part in the form!'
    folder = request.files['folder']
    if os.path.isdir('uploads'):
        shutil.rmtree('uploads')
    os.mkdir('uploads')
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(".shp") or file.endswith(".dbf") or file.endswith(".shx"):
                file_path = os.path.join(root, file)
                shutil.copy(file_path, 'uploads')
    return 'Folder uploaded successfully!'


@app.route('/upload', methods=['POST'])
def upload():
    
    dir_path = 'uploads'
    
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

    # Get the files from the request
    files = request.files.to_dict()

    # Iterate over the files and process each one
    for filename, file in files.items():
        # Save the file to disk
        file.save(os.path.join('uploads', filename))

    
    model = compileModel("uploads/Buildings.shp")
    
    # Show the plotter
    p = pv.Plotter()
    p.add_mesh(model)
    
    model.save("createdModels/model3d.stl")
    
    return 'File saved successfully', 200
    
    
@app.route('/download')
def download_file():
    # Set the file path and filename
    file_path = 'createdModels/model3d.stl'
    filename = 'model3d.stl'

    # Return the file to the client
    try:
        return send_file(file_path, as_attachment=True, download_name=filename)
    except Exception:
        return 'No file at that path' 

@app.route('/model3d')
def model3d():
    try:
        # 1. take the .shp file from uploads
        shapeData = "uploads/Buildings.shp"
        
        # 2. compile model
        modelfile = compileModel(shapeData)
        
        # 3. render model 
        image = render3d(modelfile)
        
        # 4. Return the HTML template with the image data
        return render_template('model3d.html', image=image)
    
    except Exception:
        # If a RuntimeError is raised, redirect the browser to the homepage
        return redirect(url_for('home'))

        

@app.route('/model2d')
def model2d():
    try:
        
        # 1. take shape data
        shapeData = "uploads/Buildings.shp"
        
        # 2. compile model
        modelfile = compileModel(shapeData)
        
        # 3. render model 
        image = render2d(modelfile)

        # Return the HTML template with the image data
        return render_template('model2d.html', image=image)
    
    except Exception:
        # If a RuntimeError is raised, redirect the browser to the homepage
        return redirect(url_for('home'))
    
    
if __name__ == '__main__':
    app.run(debug=True)