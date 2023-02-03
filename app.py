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
import json
import time

import humanize
import plotly
import plotly.express as px
from flask import *
from werkzeug.utils import secure_filename

from function import *

app = Flask(__name__)
app.secret_key = "super secret key"


@app.route('/')
def index():
    # Filter values

    # country
    Country = request.args.get('Country')

    countries = ['USA', 'Singapore', 'Japan', 'Brazil', 'Jamaica', 'France', 'Philippines', 'India', 'South Afrcia',
                 'Mexico']

    if not (Country in countries):
        Country = 'USA'

    # start and end year
    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    if start_year is not None and end_year is not None:
        try:
            if int(start_year) < 1990:
                start_year = 1990
            else:
                start_year = int(start_year)

            if int(end_year) > 2020:
                end_year = 2020
            else:
                end_year = int(end_year)
        except:
            start_year = 1990
            end_year = 2020
    else:
        start_year = 1990
        end_year = 2020

    # Factors
    Consumer_Price_Index = request.args.get('Consumer_Price_Index')
    Income_Polarization = request.args.get('Income_Polarization')
    Enrolment = request.args.get('Enrolment')
    Family = request.args.get('Family')
    Poverty = request.args.get('Poverty')

    # GRAPH
    # Rename dataframe keys so that x and y-axis names are more general
    # df.rename(columns={'Year': 'year', 'Lack_of_Educational_Opportunities': 'countries'}, inplace=True)
    # x = year, y = factor, output = country

    is_filter = True
    graphJSON = []

    if Consumer_Price_Index == 'T':
        clean_data = cleanCPIdata(file2, 1980, 2010)
        print(clean_data)

        columns = [col for col in clean_data.columns]
        column_1_values = [col for col in clean_data[columns[0]]]
        column_2_values = [col for col in clean_data[columns[1]]]

        df = pd.DataFrame(dict(x=column_1_values, y=column_2_values))

        fig1 = px.line(df, x='x', y='y', title="Consumer Price Index").update_layout(
            xaxis_title=columns[0],
            yaxis_title=columns[1])

        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON.append(graph1JSON)

    if Income_Polarization == 'T':
        clean_data = cleanIncomedata(file3, "Brazil", 2000, 2010)
        print(clean_data)

        columns = [col for col in clean_data.columns]
        column_1_values = [col for col in clean_data[columns[0]]]
        column_2_values = [col for col in clean_data[columns[1]]]

        df = pd.DataFrame(dict(x=column_1_values, y=column_2_values))

        fig1 = px.line(df, x='x', y='y', title="Income Polarization").update_layout(
            xaxis_title=columns[0],
            yaxis_title=columns[1])

        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON.append(graph1JSON)

    if Enrolment == 'T':
        clean_data = cleanEnroldata(file5, "Brazil", 1999, 3005)
        print(clean_data)

        columns = [col for col in clean_data.columns]
        column_1_values = [col for col in clean_data[columns[0]]]
        column_2_values = [col for col in clean_data[columns[1]]]

        df = pd.DataFrame(dict(x=column_1_values, y=column_2_values))

        fig1 = px.line(df, x='x', y='y', title="Enrolment").update_layout(
            xaxis_title=columns[0],
            yaxis_title=columns[1])

        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON.append(graph1JSON)

    if Family == 'T':
        clean_data = cleanFamilyData(file7, "Brazil", 1000, 2012)
        print(clean_data)

        columns = [col for col in clean_data.columns]
        column_1_values = [col for col in clean_data[columns[0]]]
        column_2_values = [col for col in clean_data[columns[1]]]

        df = pd.DataFrame(dict(x=column_1_values, y=column_2_values))

        fig1 = px.line(df, x='x', y='y', title="Family").update_layout(
            xaxis_title=columns[0],
            yaxis_title=columns[1])

        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON.append(graph1JSON)

    if Poverty == 'T':
        clean_data = cleanPovertydata(file6, "Brazil", 2000, 2005)
        print(clean_data)

        columns = [col for col in clean_data.columns]
        column_1_values = [col for col in clean_data[columns[0]]]
        column_2_values = [col for col in clean_data[columns[1]]]

        df = pd.DataFrame(dict(x=column_1_values, y=column_2_values))

        fig1 = px.line(df, x='x', y='y', title="Poverty").update_layout(
            xaxis_title=columns[0],
            yaxis_title=columns[1])

        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON.append(graph1JSON)

    else:
        is_filter = False

    # List of graphs
    return render_template('index.html', graphJSON=graphJSON, filter=is_filter)


@app.route('/upload_files', methods=['GET', 'POST'])
def upload():
    global file_path

    if request.method == 'POST':
        # Get the list of files from webpage
        files = request.files.getlist("file")

        # Iterate for each file in the files List, and Save them
        for file in files:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.root_path, 'datasets_user', filename)
            file.save(file_path)

        while not os.path.exists(file_path):
            time.sleep(1)

        flash("Files uploaded successfully")

    # Display all current files into page
    files = dict()
    for filename in os.listdir('datasets_user'):
        file_path = os.path.join(app.root_path, 'datasets_user', filename)
        file_size = humanize.naturalsize(os.path.getsize(file_path))
        file_c_time = os.path.getctime(file_path)
        files[filename] = [file_size, time.ctime(file_c_time)]
    return render_template('upload_files.html', files=files)


@app.route('/delete_file/<filename>', methods=['GET', 'POST'])
def delete_file(filename):
    # TODO: NOT WORKING REMEMBER DO
    os.remove(os.path.join(app.root_path, 'datasets_user', filename))
    return redirect(url_for("upload"))


@app.route('/display_file/<filename>', methods=['GET'])
def display(filename):
    # if file size too big, may take a long time or crash
    try:
        file_path = os.path.join(app.root_path, 'datasets_user', filename)
        file_name, file_extension = os.path.splitext(filename)

        pd.set_option('colheader_justify', 'center')

        if file_extension == '.csv':
            df = pd.read_csv(file_path)
            df_html = df.to_html(classes='mystyle')
        elif file_extension == '.xlsx':
            df = pd.read_excel(file_path)
            df_html = df.to_html(classes='mystyle')
        elif file_extension == '.json':
            df = pd.read_json(file_path)
            df_html = df.to_html(classes='mystyle')
        elif file_extension == '.txt':
            df = pd.read_csv(file_path)
            df_html = df.to_html(classes='mystyle')
        else:
            df_html = "<h5>File extension not supported</h5>"
    except Exception as e:
        print(e)
        df_html = "<h5>Error in displaying File contents</h5>"
    # except ValueError:
    #     df_html = "<h5>Error in displaying File contents</h5>"
    return render_template('display.html', data_var=df_html, filename=filename)


if __name__ == '__main__':
    app.run()
