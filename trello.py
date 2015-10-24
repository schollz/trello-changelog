import json
import datetime
import sys
import random

a =json.load(open(sys.argv[1],'rb'))
def find_between( s, first, last ):
  try:
    start = s.index( first ) + len( first )
    end = s.index( last, start )
    return s[start:end]
  except ValueError:
    return ""
    
# BOARDS
boards  = {} 
for board in a['lists']:
  boards[board['id']] = board['name']

# CARDS
cards = []
for i in a['cards']:
  name = i['name']
  labels = i['labels']
  ls = []
  for j in labels:
    ls.append(j['name'])
  boardID = i['idList']
  board = boards[boardID]
  card = {}
  card['name']=name
  card['labels']=ls
  card['list']=board
  card['date']=datetime.datetime.strptime(i['dateLastActivity'].split('.')[0], '%Y-%m-%dT%H:%M:%S').strftime('%Y-%m-%d')
  cards.append(card)


availableColors = []
with open('colors.txt','r') as f:
  for line in f:
    availableColors.append(line.decode('utf-8').strip())

random.shuffle(availableColors)

changelog = {}
dates = {}
colors = {}
latestDate = None
for card in cards:
  if 'Done' in card['list']:
    version = card['list']
    if version not in changelog:
      changelog[version] = {}
      changelog[version]['date'] = card['date']
      changelog[version]['features'] = []
      dates[changelog[version]['date']] = version

    dat = {'feature':card['name'], 'categories': card['labels']}
    changelog[version]['features'].append(dat)
    for category in card['labels']:
      if category not in colors:
        colors[category] = availableColors.pop()


versionOrdering = []
for k in sorted(dates.keys(),reverse=True):
  versionOrdering.append(dates[k])



changelist = {}
for version in versionOrdering:
  heading = changelog[version]['date'] + ' ' + version.replace('Done ','').replace('(','').replace(')','')
  changelist[heading] = []
  for feature in changelog[version]['features']:
    line = '- '
    for category in feature['categories']:
      line += '<span style="color:' + colors[category] + '; font-family: Courier New;">[' + category + '] </span>'
    line += '<span style="font-family: Courier New;">' + feature['feature'] + '</span>'
    changelist[heading].append(line)

print "\n\n\n\n\n\n\n# Changelog \n"
for version in versionOrdering:
  heading = changelog[version]['date'] + ' ' + version.replace('Done ','').replace('(','').replace(')','')
  print "\n\n## " + heading
  for line in sorted(changelist[heading]):
    print line
  print "\n"