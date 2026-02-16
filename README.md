# Google-Lighthouse-website-auditing-script
A short script for auditing any specified URL with Google Lighthouse web and saving performance results to csv

# Running
To run the script you will need the Lighthouse [CLI tool](https://github.com/GoogleChrome/lighthouse?tab=readme-ov-file#using-the-node-cli) installed
Before running the script, define at least the URL, OUTPUT_FILE and OPTIMIZATION_TOOL.
The script will run TEST_RUN amount of times and write the results of the tests (Overall performance score and scores for the METRICS) and save the ressults in a csv file named with the OUTPUT_FILE constant.
