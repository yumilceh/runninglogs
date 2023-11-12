import datetime
import json
import logging
import os
import sys

import requests
import pwinput
import readchar
from garth.exc import GarthHTTPError

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)
    
# Configure debug logging
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables if defined
email = os.getenv("GARMINEMAIL")
password = os.getenv("GARMINPASSWORD")
tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
api = None


def display_json(api_call, output):
    """Format API output for better readability."""

    dashed = "-"*20
    header = f"{dashed} {api_call} {dashed}"
    footer = "-"*len(header)

    print(header)
    print(json.dumps(output, indent=4))
    print(footer)

def display_text(output):
    """Format API output for better readability."""

    dashed = "-"*60
    header = f"{dashed}"
    footer = "-"*len(header)

    print(header)
    print(json.dumps(output, indent=4))
    print(footer)

def get_credentials():
    """Get user credentials."""
    email = input("Login e-mail: ")
    password = pwinput.pwinput(prompt='Password: ')

    return email, password

def get_api(email=email, password=password):
    """Initialize Garmin API with your credentials."""

    try:
        print(
            f"Trying to login to Garmin Connect using token data from '{tokenstore}'...\n"
        )
        garmin = Garmin()
        garmin.login(tokenstore)
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        print(
            "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        )
        try:
            # Ask for credentials if not set as environment variables
            if not email or not password:
                email, password = get_credentials()

            garmin = Garmin(email, password)
            garmin.login()
            # Save tokens for next login
            garmin.garth.dump(tokenstore)

        except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError, requests.exceptions.HTTPError) as err:
            logger.error(err)
            return None

    return garmin

# Get last activity
def get_last_activity(api):
    display_json("api.get_last_activity()", api.get_last_activity())

def get_activities_date(api, startdate=None, enddate=None, activitytype='running', path=''):
    # Get activities data from startdate 'YYYY-MM-DD' to enddate 'YYYY-MM-DD', with (optional) activitytype
    # Possible values are: cycling, running, swimming, multi_sport, fitness_equipment, hiking, walking, other 
    startdate =  datetime.date.today() if startdate is None else startdate
    enddate =  datetime.date.today() if enddate is None else enddate

    activities = api.get_activities_by_date(
        startdate.isoformat(), enddate.isoformat(), activitytype
    )


    # Download activities
    for activity in activities:

        activity_id = activity["activityId"]
        display_text(activity)

        print(f"api.download_activity({activity_id}, dl_fmt=api.ActivityDownloadFormat.GPX)")
        gpx_data = api.download_activity(
            activity_id, dl_fmt=api.ActivityDownloadFormat.GPX
        )
        output_file = f"{path}{str(activity_id)}.gpx"
        with open(output_file, "wb") as fb:
            fb.write(gpx_data)
        print(f"Activity data downloaded to file {output_file}")

        print(f"api.download_activity({activity_id}, dl_fmt=api.ActivityDownloadFormat.TCX)")
        tcx_data = api.download_activity(
            activity_id, dl_fmt=api.ActivityDownloadFormat.TCX
        )
        output_file = f"{path}{str(activity_id)}.tcx"
        with open(output_file, "wb") as fb:
            fb.write(tcx_data)
        print(f"Activity data downloaded to file {output_file}")

        print(f"api.download_activity({activity_id}, dl_fmt=api.ActivityDownloadFormat.ORIGINAL)")
        zip_data = api.download_activity(
            activity_id, dl_fmt=api.ActivityDownloadFormat.ORIGINAL
        )
        output_file = f"{path}{str(activity_id)}.zip"
        with open(output_file, "wb") as fb:
            fb.write(zip_data)
        print(f"Activity data downloaded to file {output_file}")

        print(f"api.download_activity({activity_id}, dl_fmt=api.ActivityDownloadFormat.CSV)")
        csv_data = api.download_activity(
            activity_id, dl_fmt=api.ActivityDownloadFormat.CSV
        )
        output_file = f"{path}{str(activity_id)}.csv"
        with open(output_file, "wb") as fb:
            fb.write(csv_data)
        print(f"Activity data downloaded to file {output_file}")

    return len(activities)