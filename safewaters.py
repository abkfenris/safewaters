#!/usr/bin/env python
import requests
import pandas as pd

rows = []

for i in range(26):
    response = requests.get(f"https://brookfieldwaterpublishingapi.azurewebsites.net/riversystems/{i}/facilities?withEverything=false")
    data = response.json()
    for facility in data:
        if facility['WaterData']:
            for measurement in facility['WaterData']['Data']:
                measurement['facilityName'] = facility['Name']
                measurement['facilityId'] = facility['FacilityId']
                measurement['StoredAt'] = facility['WaterData']['StoredAt']
                measurement['StateAbbreviation'] = facility['StateAbbreviation']
                rows.append(measurement)
            
df = pd.DataFrame(rows)
df = df.sort_values(['StateAbbreviation', 'facilityName', 'Name'])

df.to_csv("safewaters.csv", index=False)
