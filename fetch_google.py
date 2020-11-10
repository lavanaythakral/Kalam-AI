import yake
import requests

API_KEY = '4e1eb040-18e7-11eb-a969-4d03007837e9'

def keys(query):
  kw_extractor = yake.KeywordExtractor()
  keywords = kw_extractor.extract_keywords(query)
  txt = "A P J Abdul Kalam"
  for kw in keywords:
    # print(kw[1])
    txt += " "
    txt += kw[1]
  return txt,keywords

def get_ans(question):
  headers = { 'apikey': API_KEY }
  params = (
    ("q",question),
    ("device","desktop"),
    ("gl","IN"),
    ("hl","en"),
    ("location","Navi Mumbai,Maharashtra,India"),
    ("num","50"),
  )

  response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)
  data = response.json()
  if 'answer_box' in data.keys():
    res = data['answer_box']['answer']
  else:
    res = "No clue"
  return res

def master(query):
  txt,keywords = keys(query)
  # print(txt)
  res = get_ans(txt)
  return res