from collections import Counter
import json
import nltk
 
def checkEquality(word, target):
  word1 = word.strip().lower()
  word2 = target.strip().lower()
  
  if (word1 == word2):
    return 1
  return 0

# page = 'login_page.json'
page = 'broadcast_page.json'
with open(page, 'r') as file:
  data = json.load(file)

# test_data = {
#   "tag": "input",
#   "id": "new_user_email",
#   "type": "email",
#   "class": "form-control",
#   "name": "user[email]",
#   "aria-autocomplete": None,
#   "title": None,
#   "href": None,
#   "text": 'User Email',
#   "value": None,
#   "aria-label": None
# }

test_data = {
  "tag": "input",
  "id": None,
  "type": "text",
  "class": None,
  "name": None,
  "aria-autocomplete": None,
  "title": None,
  "href": None,
  "text": "Search recipient",
  "value": "Search recipient",
  "aria-label": None
}

useLevenshteinCalc = ['class', 'aria-autocomplete', 'href', 'title', 'text', 'value', 'aria-label']
new_result = {}

for x in data:
  new_result[x] = {}
  for attr, value in data[x].items():
    if (value != None) & (test_data[attr] != None):
      if (attr in useLevenshteinCalc):
        new_result[x][attr] = nltk.edit_distance(test_data[attr], value)
      else:
        new_result[x][attr] = checkEquality(test_data[attr], value)

# Weight
weight = {
  'id': 1,
  'tag': 1,
  'type': 0.5,
  'name': 0,
  'class': 0,
  'text': 1,
  'value': 0.25
}

score = []
for x in new_result:
  score_dict = {
    'name': x
  }
  score_dict['score'] = 0
  for attr, value in new_result[x].items():
    score_dict['score'] += (weight[attr]) * value
  score.append(score_dict)

sorted_data = sorted(score, key=lambda x: x['score'], reverse=False)
print(json.dumps(sorted_data))
print(json.dumps(sorted_data[0]))