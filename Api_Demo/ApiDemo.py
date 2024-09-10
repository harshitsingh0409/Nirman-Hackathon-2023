## Demo file to showcase the api 

import requests
import pyvista as pv
import os
import webbrowser

# Define the file path and the API endpoint URL
dir_path = "data"
url = "http://127.0.0.1:5000/upload"

# Send the file to the API endpoint
files = {}
for filename in os.listdir(dir_path):
    file_path = os.path.join(dir_path, filename)
    with open(file_path, "rb") as f:
        files[filename] = f.read()

# Send the dictionary of files to the API endpoint
response = requests.post(url, files=files)

import requests

# Define the server URL and filename for the downloaded file
server_url = 'http://localhost:5000/download'
filename = 'model3d.stl'

# Send a GET request to the server to download the file
response = requests.get(server_url)

# Save the file to disk
with open(filename, 'wb') as f:
    f.write(response.content)

# Print a success message
print(f"File '{filename}' downloaded successfully.")



url = "http://127.0.0.1:5000/"
webbrowser.open_new_tab(url)
 
#mesh = pv.read('model3d.stl')

#p = pv.Plotter()

# Create the PyVista plot
#p.add_mesh(mesh)

# Render the plot
#p.show()
    
    