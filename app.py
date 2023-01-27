"""

• Read data from an external data sources, e.g. txt, JSON, xlsx, csv or other formats.
• Allow users to view the datasets.
• Allow users to search the data based on some criterion.
• Allow users to see some statistics information based on the data.
• Allow users to export some results.
• Advanced features: you can identify your own way for pattern/anomaly detection,
prediction or other analyses using advanced data science libraries.
You need to design one user-friendly UI such that your program is easy to use.

NOTES:
• if you have new requirements.txt to add, do the following steps:
    - pip install pipreqs (don't use freeze)
    - pipreqs /path/to/project
• path to datasets: os.path.join(app.root_path, 'datasets', filename)

"""

from flask import *
from werkzeug.utils import secure_filename
import os
import time
import humanize

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload_files', methods=['GET', 'POST'])
def upload():
    global file_path

    if request.method == 'POST':
        # Get the list of files from webpage
        files = request.files.getlist("file")

        # Iterate for each file in the files List, and Save them
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.root_path, 'datasets', filename)
            file.save(file_path)

        while not os.path.exists(file_path):
            time.sleep(1)

        flash("Files uploaded successfully")

    # Display all current files into page
    files = dict()
    for filename in os.listdir('datasets'):
        file_path = os.path.join(app.root_path, 'datasets', filename)
        file_size = humanize.naturalsize(os.path.getsize(file_path))
        files[filename] = file_size
    return render_template('upload_files.html', files=files)


if __name__ == '__main__':
    app.run()
