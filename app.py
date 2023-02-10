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

import time
import os
import humanize
import plotly
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from plotly.colors import n_colors
from flask import *
import numpy as np

from function import *

import json

app = Flask(__name__)
app.secret_key = "super secret key"

factors = ['Consumer_Price_Index', 'Income_Polarization', 'Enrolment', 'Family', 'Poverty']
newfactor_data = {}


# main page - dashboard
@app.route('/', methods=['GET'])
def index():
    global factors, newfactor_data, Country, start_year, end_year, graphJSON, is_filter, factors_list, countries, factors_value
    # Filter values
    factors_list = list()
    # country
    Country = request.args.get('Country')

    countries = ['United States', 'Singapore', 'Japan', 'Brazil', 'Jamaica', 'France', 'Philippines', 'India',
                 'South Africa',
                 'Mexico']

    if not (Country in countries):
        Country = 'United States'

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

    # GRAPH
    # Rename dataframe keys so that x and y-axis names are more general
    # df.rename(columns={'Year': 'year', 'Lack_of_Educational_Opportunities': 'countries'}, inplace=True)
    # x = year, y = factor, output = country

    is_filter = True
    graphJSON = []

    # Factors
    factors_value = {}
    for factor in factors:
        if request.args.get(factor) is not None:
            factors_value[factor] = True

    # check if dict is empty -> no factors
    if bool(factors_value):
        # Show crimes rates graph
        clean_data = cleanCrimedata(
            "data/CrimeRates/" + Country.replace(" ", "-").lower() + "-crime-rate-statistics.csv", start_year, end_year)
        print(clean_data)

        columns = [col for col in clean_data.columns]
        column_1_values = [col for col in clean_data[columns[0]]]
        column_2_values = [col for col in clean_data[columns[1]]]

        df = pd.DataFrame(dict(x=column_1_values, y=column_2_values))

        fig1 = px.line(df, x='x', y='y', title="Crime Rates").update_layout(
            xaxis_title=columns[0],
            yaxis_title=columns[1])

        fig2 = px.histogram(df, "x", "y", opacity=0.4)
        fig2.update_traces(marker_color="green", showlegend=True, name="Crime Rates")

        '''fig2 = px.line(df, x='x', y='y', title="Crime Rates").update_layout(
            xaxis_title=columns[0],
            yaxis_title=columns[1])
        fig2['data'][0]['showlegend'] = True
        fig2['data'][0]['name'] = 'Crime Rates'''

        fig2.update_traces(yaxis="y2")

        graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
        graphJSON.append(graph1JSON)

        # Show graphs for different factors
        for factor in factors_value:
            print(factor)
            subfig = make_subplots(specs=[[{"secondary_y": True}]])
            if factor == 'Consumer_Price_Index':
                clean_data = cleanCPIdata("data/CosumerPriceIndex/CPI_" + convertname(Country) + ".xlsx", start_year,
                                          end_year)
                title = "Consumer Price Index"
                print(clean_data)
            elif factor == 'Income_Polarization':
                clean_data = cleanIncomedata("data/IncomePolarization/IncomeInequality_World.xls", Country, start_year,
                                             end_year)
                title = "Income Polarization"
                print(clean_data)
            elif factor == 'Enrolment':
                clean_data = cleanEnroldata("data/enrollment.csv", Country, start_year, end_year)
                title = "Enrolment"
                print(clean_data)
            elif factor == 'Family':
                clean_data = cleanFamilyData("data/family.csv", Country, start_year, end_year)
                title = "Family"
                print(clean_data)
            elif factor == 'Poverty':
                clean_data = cleanPovertydata("data/poverty-explorer.csv", Country, start_year, end_year)
                title = "Poverty"
                print(clean_data)
            else:
                title = factor
                if Country in newfactor_data[factor]:
                    filename = newfactor_data[factor][Country]
                    file_path = os.path.join(app.root_path, 'datasets_user', filename)
                    file_name, file_extension = os.path.splitext(filename)
                    if file_extension == '.csv' or file_extension == '.txt':
                        clean_data = cleanCSVTXTdata(file_path, Country, start_year, end_year)
                    elif file_extension == '.json':
                        clean_data = cleanJsondata(file_path, Country, start_year, end_year)

                    print(clean_data)
                else:
                    dict1 = {"Year": [], "No Data": []}
                    clean_data = pd.DataFrame(dict1)
            if clean_data.empty:
                dict1 = {"Year": [], "No Data": []}
                clean_data = pd.DataFrame(dict1)

            columns = [col for col in clean_data.columns]
            column_1_values = [col for col in clean_data[columns[0]]]
            column_2_values = [col for col in clean_data[columns[1]]]

            df = pd.DataFrame(dict(x=column_1_values, y=column_2_values))

            fig1 = px.line(df, x='x', y='y', title=title).update_layout(
                xaxis_title=columns[0],
                yaxis_title=columns[1])
            fig1['data'][0]['showlegend'] = True
            fig1['data'][0]['name'] = factor

            subfig.add_traces(fig2.data + fig1.data)
            subfig.layout.yaxis.title = factor.replace('_', ' ')
            subfig.layout.xaxis.title = "Time"
            subfig.layout.yaxis2.title = "Crime Rates"
            # subfig.for_each_trace(lambda t: t.update(line=dict(color=t.marker.color)))
            subfig.update_layout(legend_x=1, legend_y=1, showlegend=True)
            subfig.layout.update({'title': factor})
            graph1JSON = json.dumps(subfig, cls=plotly.utils.PlotlyJSONEncoder)
            graphJSON.append(graph1JSON)

            factors_list = list()
            factors_list.append('Crime_Rates')
            for key, value in factors_value.items():
                factors_list.append(key)

    else:
        is_filter = False

    # List of graphs
    print("A", factors_value, factors)
    return render_template('index.html', graphJSON=graphJSON, filter=is_filter, factors=factors,
                           factors_list=factors_list, country=Country, countries=countries, start_year=start_year, end_year=end_year, factors_value=factors_value)


# view individual dataset
@app.route('/view_individual_dataset/<dataset>', methods=['GET'])
def view_individual_dataset(dataset):
    # Get dataset from url, the rest is from global variables
    if dataset == "Crime_Rates":
        clean_data = cleanCrimedata(
            "data/CrimeRates/" + Country.replace(" ", "-").lower() + "-crime-rate-statistics.csv", start_year, end_year)
    elif dataset == 'Consumer_Price_Index':
        clean_data = cleanCPIdata("data/CosumerPriceIndex/CPI_" + convertname(Country) + ".xlsx", start_year, end_year)
    elif dataset == 'Income_Polarization':
        clean_data = cleanIncomedata("data/IncomePolarization/IncomeInequality_World.xls", Country, start_year,
                                     end_year)
    elif dataset == 'Enrolment':
        clean_data = cleanEnroldata("data/enrollment.csv", Country, start_year, end_year)
    elif dataset == 'Family':
        clean_data = cleanFamilyData("data/family.csv", Country, start_year, end_year)
    elif dataset == 'Poverty':
        clean_data = cleanPovertydata("data/poverty-explorer.csv", Country, start_year, end_year)
    elif dataset in factors:

        try:
            filename = newfactor_data[dataset][Country]

            file_name, file_extension = os.path.splitext(filename)
            file_path = os.path.join(app.root_path, 'datasets_user', filename)
            if file_extension in [".csv", ".txt"]:
                clean_data = cleanCSVTXTdata(file_path, Country, start_year, end_year)
            elif file_extension == ".json":
                clean_data = cleanJsondata(file_path, Country, start_year, end_year)
        except:
            flash("Dataset not found")
            return render_template('index.html', graphJSON=graphJSON, filter=is_filter, factors=factors,
                                   factors_list=factors_list, country=Country, countries=countries,
                                   start_year=start_year, end_year=end_year, factors_value=factors_value)

    if clean_data.empty:
        flash("Dataset not found")
        return render_template('index.html', graphJSON=graphJSON, filter=is_filter, factors=factors,
                           factors_list=factors_list, country=Country, countries=countries, start_year=start_year, end_year=end_year, factors_value=factors_value)

    columns = [col for col in clean_data.columns]
    column_1_values = [col for col in clean_data[columns[0]]]
    column_2_values = [col for col in clean_data[columns[1]]]

    # Used plotly graphs, and color (Simple table heatmap)
    # Plotly colors each row based on incremental value (i.e. start from 0 to end value)
    # https://plotly.com/python/table/
    # However, our dataset doesn't start from 0,
    # so I needed to create an order the numbers based on how big the values are (i.e. 0 = smallest, 27 = biggest)
    # After that rearrange them back to the original list so that plotly knows which number is the biggest in the
    # dataset and which is the smallest.

    # Example:
    # values = [200, 100, 500, 300, 400]
    # reposition = [100, 200, 300, 400, 500]
    # assign index = [0, 1, 2, 3, 4]
    # assign index to values = [1, 0, 4, 3, 2]

    column_1_rgb_value = list()
    for i in range(len(column_1_values)):
        column_1_rgb_value.append(i)

    # Rearranging the values and giving each an index number according to size of value
    column_2_rgb_value_dict = dict()
    count = 0
    for i in sorted(column_2_values):
        column_2_rgb_value_dict[count] = i
        count += 1

    # Append the index numbers based on where the original values were
    column_2_rgb_value = []
    for i in column_2_values:
        for key, value in column_2_rgb_value_dict.items():
            if value == i:
                column_2_rgb_value.append(key)

    # Color values, len(column_1_values) tells where the highlight color should be (i.e. red)
    colors = n_colors('rgb(255, 213, 128)', 'rgb(255, 0, 0)', len(column_1_values), colortype='rgb')

    a = np.asarray(column_1_rgb_value)
    b = np.asarray(column_2_rgb_value)

    fig = go.Figure(data=[go.Table(
        header=dict(
            values=[f'<b>{columns[0]}<b>', f'<b>{columns[1]}<b>'],
            line_color='white', fill_color='white',
            align='center', font=dict(color='black', size=18)
        ),
        cells=dict(
            values=[column_1_values, column_2_values],
            line_color=[np.array(colors)[a], np.array(colors)[b]],
            fill_color=[np.array(colors)[a], np.array(colors)[b]],
            align='center', font=dict(color='black', size=15)
        ))
    ])

    fig.show()

    return render_template('index.html', graphJSON=graphJSON, filter=is_filter, factors=factors,
                           factors_list=factors_list, country=Country, countries=countries, start_year=start_year, end_year=end_year, factors_value=factors_value)


# allow users to upload their data files
@app.route('/upload_files', methods=['GET', 'POST'])
def upload():
    global file_path, newfactor_data

    if request.method == 'POST':
        # get new factor to add
        newfactor = request.form.get("newfactor")
        if not newfactor in factors:
            factors.append(newfactor)

        # get country to add to
        country = request.form.get("Country")

        # Get the list of files from webpage
        files = request.files.getlist("file")

        # Iterate for each file in the files List, and Save them
        for file in files:
            temp, ext = os.path.splitext(file.filename)
            filename = newfactor + "_" + country + ext

            if newfactor in newfactor_data.keys():
                newfactor_data[newfactor][country] = filename
            else:
                newfactor_data[newfactor] = {country: filename}
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


# allow users to delete their data file
@app.route('/delete_file/<filename>', methods=['GET', 'POST'])
def delete_file(filename):
    global newfactor_data

    try:
        os.remove(os.path.join(app.root_path, 'datasets_user', filename))
        file_name, file_extension = os.path.splitext(filename)
        file_name = file_name.split("_")
        factor = file_name[0]
        country = file_name[1]
        del newfactor_data[factor][country]

        if newfactor_data[factor] == {}:
            del newfactor_data[factor]
            factors.remove(factor)
        return redirect(url_for("upload"))

    except:
        print('No factor')
        return redirect(url_for("upload"))


# allow users to display the files they upload
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
    return render_template('display.html', data_var=df_html, filename=filename)
       
# allow users to export specific dataset
@app.route('/export_dataset/<file_type>/<dataset>', methods=['GET'])
def export_dataset(dataset,file_type):
     # Get dataset from url, the rest is from global variables
    if dataset == "Crime_Rates":
        clean_data = cleanCrimedata(
            "data/CrimeRates/" + Country.replace(" ", "-").lower() + "-crime-rate-statistics.csv", start_year, end_year)
    elif dataset == 'Consumer_Price_Index':
        clean_data = cleanCPIdata("data/CosumerPriceIndex/CPI_" + convertname(Country) + ".xlsx", start_year, end_year)
    elif dataset == 'Income_Polarization':
        clean_data = cleanIncomedata("data/IncomePolarization/IncomeInequality_World.xls", Country, start_year, end_year)
    elif dataset == 'Enrolment':
        clean_data = cleanEnroldata("data/enrollment.csv", Country, start_year, end_year)
    elif dataset == 'Family':
        clean_data = cleanFamilyData("data/family.csv", Country, start_year, end_year)
    elif dataset == 'Poverty':
        clean_data = cleanPovertydata("data/poverty-explorer.csv", Country, start_year, end_year)
    elif dataset in factors:
        if not Country in newfactor_data[dataset]:
            flash("Dataset not found")
            return render_template('index.html', graphJSON=graphJSON, filter=is_filter, factors=factors,
                           factors_list=factors_list, country=Country, countries=countries, start_year=start_year, end_year=end_year, factors_value=factors_value)
        filename = newfactor_data[dataset][Country]
        
        file_name, file_extension = os.path.splitext(filename)
        file_path = os.path.join(app.root_path, 'datasets_user', filename)
        if file_extension in [".csv",".txt"]:
            clean_data = cleanCSVTXTdata(file_path,Country,start_year,end_year)
        elif file_extension == ".json":
            clean_data = cleanJsondata(file_path,Country,start_year,end_year)
    filename = dataset+"_"+Country+"."+file_type
    filename = os.path.join(app.root_path, 'Exports', filename)

    if file_type == "csv":
        clean_data.to_csv(filename, index=False, header=True)
    
    elif file_type == "xlsx":
        clean_data.to_excel(filename, index=False)

    return send_file(filename)

# run the app
if __name__ == '__main__':
    app.run()
