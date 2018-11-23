# ppl cricketer details scraper

import requests
import bs4

countriesList = [{'name': 'australia', 'code': 2 }, {'name': 'england', 'code': 1}, {'name': 'ireland', 'code': 29}, {'name': 'pakistan', 'code': 7}, {'name': 'srilanka', 'code': 8}, {'name': 'zimbabwe', 'code': 9}, 
{'name': 'afghanistan', 'code': 40}, {'name': 'bangladesh', 'code': 25}, {'name': 'india', 'code': 6}, {'name': 'newzealand', 'code': 5}, {'name': 'southafrica', 'code': 3}, {'name': 'westindies', 'code': 4}]

resultData = []

for k in range(len(countriesList)):
    url = 'http://www.espncricinfo.com/' + countriesList[k].get('name') + '/content/player/country.html?country=' + str(countriesList[k].get('code'))
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text)
    tempList = []
    playersList = soup.select('div[id="rectPlyr_Playerlistt20"] table a')
   
    for i in range(len(playersList)):
        tempList.append({'name': playersList[i].getText(), 'profile': playersList[i].get('href')})
    resultData.append({countriesList[k].get('name'): tempList})
 
count= 0

for i in range(len(countriesList)):
    countryPlayersList = resultData[i].get(countriesList[i].get('name'))
    for j in range(len(countryPlayersList)):
        playerName = countryPlayersList[j].get('name')
        url = 'http://www.espncricinfo.com' + countryPlayersList[j].get('profile')
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text)
        detailsField = soup.select('table[class=engineTable] thead tr')[0] 
        individualDetails = soup.select('table[class=engineTable] tbody tr')[0]
        print('#'.rjust(120, '#'))
        print(count, playerName)
        count += 1
        print('#'.rjust(120, '#'))
        print(detailsField)
        print(individualDetails)
        print('#'.rjust(120, '#'))
 