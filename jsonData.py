import requests
import bs4

countriesList = [{'name': 'australia', 'code': 2 }, {'name': 'england', 'code': 1}, {'name': 'ireland', 'code': 29}, {'name': 'pakistan', 'code': 7}, {'name': 'srilanka', 'code': 8}, {'name': 'zimbabwe', 'code': 9}, 
{'name': 'afghanistan', 'code': 40}, {'name': 'bangladesh', 'code': 25}, {'name': 'india', 'code': 6}, {'name': 'newzealand', 'code': 5}, {'name': 'southafrica', 'code': 3}, {'name': 'westindies', 'code': 4}]

finalString = ""
f = open('output', 'w')
count = 1

finalString += "Country," + "Name," + "Age," + "PlayingRole," + "BattingStyle," + "BowlingStyle,"
finalString += "Matches," + "Innings," + "Notout," + "Runs," +"HighestScore," + "BattingAvg," + "BallsFaced," +"StrikeRate," + "Hundreds," + "Fiftys," + "Fours," + "Sixs," 
finalString += "Matches," + "Innings," + "BallsBowled," + "Runs," + "Wickets," + "BBI," + "BBW," + "BowlingAvg," + "Economy," + "StrikeRate" +"\n"  

for k in range(len(countriesList)):
    url = 'http://www.espncricinfo.com/' + countriesList[k].get('name') + '/content/player/country.html?country=' + str(countriesList[k].get('code'))
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, features="html.parser")

    #allPlayersList of a particular country 
    allPlayersList = soup.select('div[id="rectPlyr_Playerlistt20"] table a')
   

    for i in range(len(allPlayersList)):

        #particular player profile
        url = 'http://www.espncricinfo.com' + allPlayersList[i].get('href')
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text, features="html.parser")


        #player details 
        country  = soup.select('div[class="pnl490M"] h3 > b')[0].getText()
        name = soup.select('div[class="pnl490M"] h1')[0].getText()
        age = soup.find(text="Current age").parent.next_sibling.next_sibling.getText()[0:3]
        try:
            playingRole = soup.find(text="Playing role").parent.next_sibling.next_sibling.getText()
        except: 
            playingRole = "_"    
        try:
            battingStyle = soup.find(text="Batting style").parent.next_sibling.next_sibling.getText()
        except:
            battingStyle = "_"  
        try:      
            bowlingStyle = soup.find(text="Bowling style").parent.next_sibling.next_sibling.getText()
        except:
            bowlingStyle = "_"    
       
        finalString += country.strip() + "," + name.strip() + "," + age.strip() + "," + playingRole.strip() + "," + battingStyle.strip() + "," + bowlingStyle.strip() + ","
        
        #batting details
        details = soup.find(text="T20Is").parent.parent
        matchs = details.next_sibling.next_sibling
        innings = matchs.next_sibling.next_sibling
        notout = innings.next_sibling.next_sibling
        runs = notout.next_sibling.next_sibling
        highestscore = runs.next_sibling.next_sibling
        battingAvg = highestscore.next_sibling.next_sibling
        ballFaced = battingAvg.next_sibling.next_sibling
        strikeRate = ballFaced.next_sibling.next_sibling
        Hundreds = strikeRate.next_sibling.next_sibling
        Fiftys = Hundreds.next_sibling.next_sibling
        fours = Fiftys.next_sibling.next_sibling
        sixs = fours.next_sibling.next_sibling

        finalString += matchs.getText().strip() + "," + innings.getText().strip() + "," + notout.getText().strip() + "," + runs.getText().strip() + "," +highestscore.getText().strip() + "," + battingAvg.getText().strip() + "," + ballFaced.getText().strip() + "," + strikeRate.getText().strip() + "," + Hundreds.getText().strip() + "," + Fiftys.getText().strip() + "," + fours.getText().strip() + "," +sixs.getText().strip() + ","

        #bowling details
        details = soup.find_all(text="T20Is", limit=2)[1].parent.parent
        matchs = details.next_sibling.next_sibling
        innings = matchs.next_sibling.next_sibling
        balls = innings.next_sibling.next_sibling 
        runs = balls.next_sibling.next_sibling
        wickets = runs.next_sibling.next_sibling
        BBI = wickets.next_sibling.next_sibling
        BBM = BBI.next_sibling.next_sibling
        bowlingAvg = BBM.next_sibling.next_sibling
        economy = bowlingAvg.next_sibling.next_sibling
        strikeRate = economy.next_sibling.next_sibling

        finalString += matchs.getText().strip() + "," + innings.getText().strip() + "," + balls.getText().strip() + "," + runs.getText().strip() + "," + wickets.getText().strip() + "," + BBI.getText().strip() + "," + BBM.getText().strip() + "," + bowlingAvg.getText().strip() + "," + economy.getText().strip() + "," + strikeRate.getText().strip() + "\n"
        
        count+=1
        print("No:", count)
f.write(finalString)