import pandas as pd
import requests

def get_submission_data():
    url = 'https://api-dev.bikespace.ca/api/v2/submissions'
    headers = {'accept': 'application/json'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        # Handle the error, raise an exception, or return an empty list, depending on your use case.
        return []

def submissions_to_dataframe(submissions):
    data = []
    for submission in submissions:
        row = {
            'id': submission['id'],
            'comments': submission['comments'],
            'issues': ', '.join(submission['issues']),
            'latitude': submission['latitude'],
            'longitude': submission['longitude'],
            'parking_duration': submission['parking_duration'],
            'parking_time': pd.to_datetime(submission['parking_time'])
        }
        data.append(row)
    return pd.DataFrame(data)

# Fetch data and convert to DataFrame
submissions_data = get_submission_data()
df = submissions_to_dataframe(submissions_data)

# Now, 'df' is your Pandas DataFrame containing the submission data.
print(df)
