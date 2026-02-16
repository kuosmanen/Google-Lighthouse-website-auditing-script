import subprocess
import json
import csv
from datetime import datetime
import os

timestamp = datetime.now().strftime("%d-%m-%Y_%H.%M.%S")




TEST_COUNT = 100
URL = "http://test.local/" #Change this to the URL you want to test
OUTPUT_FILE = "testpage.csv" #Change this to the desired output file name (will be created if it doesn't exist)
OPTIMIZATION_TOOL = "WP Rocket" #Change this to the optimization tool you are testing, e.g. "WP Rocket", "Autoptimize", "LiteSpeed Cache", "No Optimization" etc. This will be used in the CSV file to identify which results belong to which optimization tool.
METRICS = [
    "server-response-time",
    "first-contentful-paint",
    "largest-contentful-paint",
    "speed-index",
    "total-blocking-time",
    "cumulative-layout-shift"
]

fileExists = os.path.isfile(OUTPUT_FILE)
#Opening the file in append mode and writing the header only if it doesn't exist
with open(OUTPUT_FILE, "a", newline="") as file:
    writer = csv.writer(file)
    if not fileExists:
        writer.writerow(["URL", URL])
        writer.writerow(["Timestamp", timestamp])
        writer.writerow(["Run", "Optimization Tool", "Performance Score"] + [metric.title() for metric in METRICS])
    else:
        writer.writerow("")
        writer.writerow("")
        writer.writerow("")




def run_lighthouse(runNumber):
    print(f"Running Lighthouse test {runNumber}/{TEST_COUNT} with {OPTIMIZATION_TOOL}")

    command = f"lighthouse {URL} --quiet --chrome-flags='--headless' --output=json\
         --only-categories=performance --screenEmulation.desktop\
         --screenEmulation.width=1920 --screenEmulation.height=1080\
         --screenEmulation.deviceScale Factor=2"
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        errorMSG = f"Error running Lighthouse: {result.stderr}"
        print(errorMSG)
        return errorMSG

    data = json.loads(result.stdout)
    audits = data["audits"]

    #Getting the METRICS' data from the json
    results = []
    for metric in METRICS:
        value = audits[metric]["numericValue"]
        results.append(value)

    #Also overall performance score and adding it first in results
    performanceScore = round(data["categories"]["performance"]["score"] * 100)
    results.insert(0, performanceScore)

    #Writing the results to the csv
    with open(OUTPUT_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([runNumber, OPTIMIZATION_TOOL] + results)
    print(f"Test {runNumber} complete")



def calculate_averages():
    with open(OUTPUT_FILE, "r", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

        #Finding the index where actual data starts (skip headers)
        data_start_index = next(i for i, row in enumerate(rows) if row and row[0].isdigit())

        #Extracting only the last `TEST_COUNT` rows
        recent_data = rows[data_start_index:][-TEST_COUNT:]

        #Converting numeric columns (skip "Run" and "Optimization Tool")
        numeric_data = [list(map(float, row[2:])) for row in recent_data if len(row) > 2]

        #Calculating averages
        averages = [sum(col) / len(col) for col in zip(*numeric_data)]

    #Appending the averages to the CSV file
    with open(OUTPUT_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([])
        writer.writerow(["Averages", OPTIMIZATION_TOOL] + [round(avg, 5) for avg in averages])

    print(f"Averages for the last {TEST_COUNT} runs calculated and appended.")



 #for desktop with network and CPU throttling
    #lighthouse {URL} --quiet --output json --chrome-flags="--headless --" --only-categories=performance --screenEmulation.desktop 
    # --screenEmulation.width=1920 --screenEmulation.height=1080 --screenEmulation.deviceScale Factor=2

    #for default mobile device
    #lighthouse {URL} --quiet --chrome-flags='--headless' --output=json --only-categories=performance





def main():
    #Running the test TEST_COUNT amount of times
    for i in range(TEST_COUNT):
        if run_lighthouse(i+1) != None:
            print("EXITING")
            return None
    calculate_averages()
    print("----------------------------------------------------------------------------------------------------------------")

main()