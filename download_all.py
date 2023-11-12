import os
import shutil
import datetime
from garmin import get_api, get_activities_date

logs_home = '/mnt/c/Users/yumilceh/Dropbox/Logs/Running/'
def download_all(date):

    while date <= datetime.date.today():
        run_path = logs_home + date.strftime('%Y-%m-%d')
        if os.path.isdir(run_path):
            print('Data already here here')
            date += datetime.timedelta(1)
            continue
        os.makedirs(run_path)

        api = get_api()         
        print(date)
        if get_activities_date(api, startdate=date, enddate=date, path=run_path + '/') == 0:
            print('No data here')
            shutil.rmtree(run_path)
        else:
            print('No data here')

        date += datetime.timedelta(1)
        

if __name__ == '__main__':

    date = datetime.datetime.strptime('2020-11-06', '%Y-%m-%d').date()
    download_all(date)
