import pandas as pd
import requests
import csv
import json


headers={
"Authorization": "Bearer %s" % "eaP1DmlrVqcdtnhOS8csezAcxolrQmL1u8k2XiuuF7qL5.Qy5jDitlLCjGIaK76W.zGsd6-88a3JiDIJn7SSBG67JS99GSWirimCfWRkK4fIERLhTGfnbjPxT-fob1N8",
"Content-Type": "application/json"
}

#gets survey details
url1 = "https://api.surveymonkey.net/v3/surveys/274000446/details"
response1 = requests.get(url1, headers=headers)
survey_details = response1.json()

#gets survey bulk data
url2 = "https://api.surveymonkey.net/v3/surveys/274000446/responses/bulk"
response2 = requests.get(url2, headers=headers)
survey_responses = response2.json()

#gets survey questions
url3 = "https://api.surveymonkey.net/v3/surveys/274000446/pages/104874047/questions"
response3 = requests.get(url3, headers=headers)
survey_questions = response3.json()

#prints question headings
for x in survey_questions['data']:
    for (y,z) in x.items():
        if y == 'heading':
            print(z)
