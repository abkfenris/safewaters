#!/usr/bin/env python
import time
import random
import requests
import pandas as pd

systems_url = "https://api.safewaters.com/api/riverSytems/all?limit=10&page={page}"
single_system_url = (
    "https://api.safewaters.com/api/facilities?limit=10&page=1&riverSystemId={system}"
)

headers = {
    "Origin": "https://www.safewaters.com",
    "Referer": "https://www.safewaters.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:98.0) Gecko/20100101 Firefox/98.0",
}


def find_systems():
    page = 0
    systems = []
    system_count = 20
    while len(systems) < system_count:
        page += 1
        r = requests.get(systems_url.format(page=page), headers=headers)
        system_data = r.json()
        system_count = system_data["totalCount"]
        systems += [s["slug"] for s in system_data["data"]]

    return systems


systems = [
    "androscoggin",
    "beaver",
    "black",
    "deep-creek",
    "deerfield",
    "hoosic",
    "kennebec",
    "little-tennessee",
    "new-river",
    "penobscot",
]


states_to_abbreviation = {
    "New Hampshire": "NH",
    "Maine": "ME",
    "Tennessee": "TN",
    "North Carolina": "NC",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "West Virgina": "WV",
    "Pennsylvania": "PA",
    "New York": "NY",
}

columns = [
    "Name",
    "Value",
    "Uom",
    "facilityName",
    "facilityId",
    "StoredAt",
    "StateAbbreviation",
]

rows = []

for system in systems:
    url = single_system_url.format(system=system)
    data = requests.get(url, headers=headers)
    data = data.json()

    for facility in data["data"]:
        for metric in facility["tb_facilityMatrices"]:
            rows.append(
                [
                    metric["description"],
                    metric["value"],
                    metric["unit"],
                    metric["facilityName"],
                    metric["facilityId"],
                    metric["time"],
                    states_to_abbreviation.get(facility["region"]),
                ]
            )

    time.sleep(random.random())

df = pd.DataFrame(rows, columns=columns)
df = df.sort_values(["StateAbbreviation", "facilityName", "Name"])

df.to_csv("safewaters.csv", index=False)
