import os
import json
import datetime
from flask import Flask, render_template, request, url_for
from garmin import get_api, get_activities_date

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = {
            'date': request.form['date'],
            'type_of_run': request.form['type_of_run'],
            'last_breakfast': request.form['last_breakfast'],
            'last_lunch': request.form['last_lunch'],
            'last_dinner': request.form['last_dinner'],
            'nutrition_during_run': request.form['nutrition_during_run'],
            'water_during_run': request.form['water_during_run'],
            'known_injuries': request.form['known_injuries'],
            'shoes': request.form['shoes'],
            'temperature': request.form['temperature'],
            'weight':  request.form['weight_'],
            'Notes': request.form['notes']
        }
        save_data(data,  request.form['date'])
    return render_template('index.html')

def save_data(data, date):
    try:
        date = datetime.date.fromisoformat(date)
    except ValueError:
        return
    i = 0 
    run_path = './logs/' + date.strftime('%Y%m%d') + '_' + str(i) 
    while os.path.isdir(run_path):
        i += 1
        run_path = './logs/' + date.strftime('%Y%m%d') + '_' + str(i) 
    os.makedirs(run_path)

    with open(run_path + '/details.json', 'w') as fp:
        json.dump(data, fp, indent=4, sort_keys=True)

    api = get_api()
    get_activities_date(api, startdate=date, enddate=date, path=run_path + '/')
    

if __name__ == '__main__':
    app.run(debug=True)


