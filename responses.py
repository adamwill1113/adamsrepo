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

# Creates dictionary of question ids and titles for later remapping
qtitle = []
qid = []

for x in survey_questions['data']:
        for (y,z) in x.items():
            if y == 'id':
                qid.append(z)
            elif y == 'heading':
                qtitle.append(z)
                
qdict = dict(zip(qid, qtitle))

# Creates dictionary of choice ids and text for later remapping
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

cdict = dict(zip(cid, ctext))


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

#puts questions and answers into a dictionary and then into a dataframe
temp = defaultdict(list)

for key, value in zip(questions, answers):
    temp[key].append(value)
    
adict = (dict(temp))

df = pd.DataFrame({ key:pd.Series(value) for key, value in adict.items()})

df
