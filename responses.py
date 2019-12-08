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

# Writes the question headings as row headings in a csv
with open('mycsv.csv', 'w', newline='') as f:
    thewriter = csv.writer(f, delimiter = ',')
    for x in survey_questions['data']:
        for (y,z) in x.items():
            if y == 'heading':
                colHeading = [z]
                thewriter.writerow(colHeading)
            #elif y == 'id':
             #   print(z)

#gets list of questions and corresponding choices

questions = []
answers = []

for x in survey_responses['data']:
    for (y, z) in x.items():
        if y == 'pages':
            for a in z:
                for b,c in a.items():
                    if b == 'questions':
                        for d in c:
                            for e,f in d.items():
                                if e == 'id':
                                    questions.append(f)
                                else:
                                    #answers.append(f)
                                    for g in f:
                                        for h, i in g.items():
                                            if h == 'choice_id':
                                                answers.append(i)                                    
#zips questions and answers together
matches = list(zip(questions, answers))

d = defaultdict(list)

#combines like values
for k, *v in matches:
    d[k].append(v)
    
sorted_matches = []

sorted_matches = list(d.items())

#puts sorted matches into datafram
df = pd.DataFrame(sorted_matches)

df

#separates out answers into multiple columns
df0 = pd.DataFrame(df[0])
df1 = pd.DataFrame(df[1].tolist())

#puts the dataframe back together
result = pd.concat([df0, df1], axis=1)
df2 = pd.DataFrame(result)
df2
