from flask import Flask, render_template, jsonify, request, send_file, redirect, url_for
import pyvista as pv
from vtk.util import numpy_support as VN
import os
from model import render3d, render2d, compileModel

app = Flask(__name__)

@app.route('/')
def home():
    
    # code for creating the 2d image at the homescreen
    # 1. take shape data
    #shapeData = "uploads/Buildings.shp"
        
    # 2. compile model
    #modelfile = compileModel(shapeData)
    
    # 3. save 2dmodel img  
    #render2d(modelfile)
    
    return render_template('modelMenu.html')


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