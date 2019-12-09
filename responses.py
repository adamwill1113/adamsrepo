import pandas as pd
import requests
import csv
import json
from collections import defaultdict


headers={
"Authorization": "Bearer %s" % "MY_ACCESS_TOKEN",
"Content-Type": "application/json"
}

#gets question details
url1 = "https://api.surveymonkey.net/v3/surveys/274000446/pages/104874047/questions/387014905"
response1 = requests.get(url1, headers=headers)
question_details = response1.json()

#gets survey bulk data
url2 = "https://api.surveymonkey.net/v3/surveys/274000446/responses/bulk"
response2 = requests.get(url2, headers=headers)
survey_responses = response2.json()

#gets survey questions
url3 = "https://api.surveymonkey.net/v3/surveys/274000446/pages/104874047/questions"
response3 = requests.get(url3, headers=headers)
survey_questions = response3.json()

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
                                    #questions.append(f)
                                    #pass
                                    temp = f
                                else:
                                    for g in f:
                                        for h, i in g.items():
                                            if h == 'choice_id':
                                                answers.append(i)
                                                questions.append(temp)

temp = defaultdict(list)

for key, value in zip(questions, answers):
    temp[key].append(value)
    
adict = (dict(temp))

df = pd.DataFrame({ key:pd.Series(value) for key, value in adict.items()})

qtitle = []
qid = []

for x in survey_questions['data']:
        for (y,z) in x.items():
            if y == 'id':
                qid.append(z)
            elif y == 'heading':
                qtitle.append(z)
                
qdict = dict(zip(qid, qtitle))

#gets question details
ctext = []
cid = []

for i in qid:
    url1 = "https://api.surveymonkey.net/v3/surveys/274000446/pages/104874047/questions/%s" % i
    response1 = requests.get(url1, headers=headers)
    question_details = response1.json()
    #print(question_details)
    for j, k in question_details.items():
        if j == 'answers':
            for l, m in k.items():
                if l == 'choices':
                    for n in m:
                        for z, x in n.items():
                            if z == 'text':
                                ctext.append(x)
                            elif z == 'id':
                                cid.append(x)

#replaces ids with text values                                
cdict = dict(zip(cid, ctext))

temp = qdict
temp2 = adict

df1 = pd.DataFrame(df)

qtitle.pop()
qtitle.pop()

df1.columns = qtitle

df2 = df1.replace(cdict)

#write to file
df2.to_csv(r'results.csv')
