import io
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, send_file
from scipy.io import loadmat
from mpl_toolkits.mplot3d import Axes3D
import os
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_file = request.files['file']
    azimuth = int(request.form['azimuth'])
    elevation = int(request.form['elevation'])
    
    if uploaded_file.filename != '':
        # Save the uploaded file temporarily
        uploaded_file_path = "temp.mat"
        uploaded_file.save(uploaded_file_path)

        # Load the .mat file
        mat_data = loadmat(uploaded_file_path)

        # Delete the temporary file
        # Note: Make sure to handle this properly in a production environment
        os.remove(uploaded_file_path)

        V = mat_data['V']
        F = mat_data['F']

        # Plot the 3D mesh
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_trisurf(V[:, 0], V[:, 1], V[:, 2], triangles=F)

        # Adjust the viewpoint (azimuth and elevation angles)
        ax.view_init(azim=azimuth, elev=elevation)

        # Save the plot to a BytesIO object
        img_bytes_io = io.BytesIO()
        plt.savefig(img_bytes_io, format='png')
        img_bytes_io.seek(0)
        plt.close()

        return send_file(img_bytes_io, mimetype='image/png')
    else:
        return 'No file uploaded'


if __name__ == '__main__':
    app.run(debug=True)
