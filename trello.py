import json
import datetime

a =json.load(open('trello.dat','rb'))
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


version = {}
latestDate = None
for card in cards:
  if 'Done' in card['list']:
    versionNum = float(find_between(card['list'],'Version',')').strip())
    newAddition = '*   [:feature:`Feature`]: ' + card['name']
    for l in card['labels']:
        newAddition =  newAddition + '  (:' + l.lower().split()[0].replace('-','') + ':`' + l + '`)'    
    newAddition += '\n'
    if versionNum in version:
      version[versionNum] = version[versionNum] + newAddition
    else:
      version[versionNum] = newAddition
    cardDate = datetime.datetime.strptime(card['date'], '%Y-%m-%d')
    if latestDate is None:
      latestDate = cardDate
    else:
      if latestDate < cardDate:
        latestDate = cardDate

currentVersion = max(version.keys())
currentDate = datetime.datetime.strftime(latestDate,'%Y-%m-%d')
for card in cards:
  if 'Done' not in card['list']:
    newAddition = '*   [:' + card['list'].lower().split()[0].replace('-','') + ':`' + card['list'] + '`]: '
    newAddition = newAddition + card['name'] 
    for l in card['labels']:
      newAddition =  newAddition + '  (:' + l.lower().split()[0].replace('-','') + ':`' + l + '`)'
    version[currentVersion] = version[currentVersion] + newAddition + "\n"

for i in sorted(version,reverse=True):
  print ':version:`Version ' + str(i) + ' (' + currentDate + ')`\n'
  print version[i]
  
