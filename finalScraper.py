import requests
import bs4
import mysql.connector
from datetime import datetime

countriesList = [{'name': 'australia', 'code': 2 }, {'name': 'england', 'code': 1}, {'name': 'ireland', 'code': 29}, {'name': 'pakistan', 'code': 7}, {'name': 'srilanka', 'code': 8}, {'name': 'zimbabwe', 'code': 9}, 
{'name': 'afghanistan', 'code': 40}, {'name': 'bangladesh', 'code': 25}, {'name': 'india', 'code': 6}, {'name': 'newzealand', 'code': 5}, {'name': 'southafrica', 'code': 3}, {'name': 'westindies', 'code': 4}]

count = 1

#connecting to MYSQL database
try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="your_password",
        auth_plugin='mysql_native_password',
        database='your_database_name'
    )
    print("\nConnected to database SUCCESSFULLY\n")
except Exception as e:
    print("\nERROR in connecting with database:\n", e)
mycursor = db.cursor()




###############################################################
#START SCRAPING PLAYERS DETAILS
###############################################################

for k in range(len(countriesList)):
    url = 'http://www.espncricinfo.com/' + countriesList[k].get('name') + '/content/player/country.html?country=' + str(countriesList[k].get('code'))
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text)

    #allPlayersList of a particular country 
    allPlayersList = soup.select('div[id="rectPlyr_Playerlistt20"] table a')
   
   
    for i in range(len(allPlayersList)):

        #particular player profile
        url = 'http://www.espncricinfo.com' + allPlayersList[i].get('href')
        res = requests.get(url)
        soup = bs4.BeautifulSoup(res.text)


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
       
                
        #batting details
        details = soup.find(text="T20Is").parent.parent.parent.parent
        matchsBT = details.next_sibling.next_sibling
        inningsBT = matchsBT.next_sibling.next_sibling
        notout = inningsBT.next_sibling.next_sibling
        runsBT = notout.next_sibling.next_sibling
        highestscore = runsBT.next_sibling.next_sibling
        battingAvg = highestscore.next_sibling.next_sibling
        ballFaced = battingAvg.next_sibling.next_sibling
        strikeRateBT = ballFaced.next_sibling.next_sibling
        Hundreds = strikeRateBT.next_sibling.next_sibling
        Fiftys = Hundreds.next_sibling.next_sibling
        fours = Fiftys.next_sibling.next_sibling
        sixs = fours.next_sibling.next_sibling
        catches = sixs.next_sibling.next_sibling
        stumpings = catches.next_sibling.next_sibling

        #bowling details
        details = soup.find_all(text="T20Is", limit=2)[1].parent.parent.parent.parent
        matchsBL = details.next_sibling.next_sibling
        inningsBL = matchsBL.next_sibling.next_sibling
        ballsBowled = inningsBL.next_sibling.next_sibling 
        runsBL = ballsBowled.next_sibling.next_sibling
        wickets = runsBL.next_sibling.next_sibling
        BBI = wickets.next_sibling.next_sibling
        BBM = BBI.next_sibling.next_sibling
        bowlingAvg = BBM.next_sibling.next_sibling
        economy = bowlingAvg.next_sibling.next_sibling
        strikeRateBL = economy.next_sibling.next_sibling

        
        ############################################################################
        country,name,age,playingRole,battingStyle,bowlingStyle = country.strip(),name.strip(),age.strip(),playingRole.strip(),battingStyle.strip(),bowlingStyle.strip()
        matchsBT,inningsBT,notout,runsBT,highestscore,battingAvg,ballFaced,strikeRateBT,Hundreds,Fiftys,fours,sixs = matchsBT.getText().strip(),inningsBT.getText().strip(),notout.getText().strip(),runsBT.getText().strip(),highestscore.getText().strip(),battingAvg.getText().strip(),ballFaced.getText().strip(),strikeRateBT.getText().strip(),Hundreds.getText().strip(),Fiftys.getText().strip(),fours.getText().strip(),sixs.getText().strip()
        matchsBL,inningsBL,ballsBowled,runsBL,wickets,BBI,BBM,bowlingAvg,economy,strikeRateBL,catches,stumpings = matchsBL.getText().strip(),inningsBL.getText().strip(),ballsBowled.getText().strip(),runsBL.getText().strip(),wickets.getText().strip(),BBI.getText().strip(),BBM.getText().strip(),bowlingAvg.getText().strip(),economy.getText().strip(),strikeRateBL.getText().strip(),catches.getText().strip(),stumpings.getText().strip()
        ############################################################################
        
        if (playingRole.find("rounder") != -1):
            playingRole = "Allrounder"
        if (playingRole.find("keeper") != -1):
            playingRole = "Wicketkeeper"
        if (playingRole.find("man") != -1):
            playingRole = "Batsman"        

       
        print("NO: ", count)
        count+=1


        #############################################################################
        #START ADDING PLAYERS AND BOWLERS DETAILS INTO DATABASE
        #############################################################################


        #adding player_details
        player_details = [name,country,playingRole,age]
        player_details.append(str(datetime.now()))
        player_details.append(str(datetime.now()))

        for i in range(len(player_details)):
            if player_details[i] == '-':
                player_details[i] = '00'

        try:
            sql = 'INSERT INTO player_details (player_name,player_country,player_type,player_age,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s)'
            mycursor.execute(sql, tuple(player_details))
            db.commit()
            print("Entry added SUCCESSFULLY to 'Player_details' TABLE")
        except Exception as e:
            print("Error in adding data to 'Player_details' TABLE:\n", e)



       #adding bowling_details
        bowling_details = [bowlingAvg,ballsBowled,economy,bowlingStyle,wickets,BBI,strikeRateBL,catches,stumpings,inningsBL]
        bowling_details.append(str(datetime.now()))
        bowling_details.append(str(datetime.now())) 

        for i in range(len(bowling_details)):
            if bowling_details[i] == '-':
                bowling_details[i] = '00'

        try:
            sql = 'INSERT INTO bowling_details (bowling_average,balls_bowled,economy,bowling_style,wickets_taken,best_bowling_figure,bowling_strike_rate,catches,stumpings,innings,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(sql, tuple(bowling_details))
            db.commit()
            print("Entry added SUCCESSFULLY to 'Bowling_details' TABLE")
        except Exception as e:
            print("ERROR in adding data to 'Bowling_details' TABLE:\n", e)    



        #adding batting_details
        batting_details = [battingAvg,strikeRateBT,runsBT,ballFaced,highestscore,Hundreds,sixs,fours,inningsBT]
        batting_details.append(str(datetime.now()))
        batting_details.append(str(datetime.now()))
        
        for i in range(len(batting_details)):
            if batting_details[i] == '-':
                batting_details[i] = '00'

        try:
            sql = 'INSERT INTO batting_details (batting_average,strike_rate,runs,balls_faced,highest,hundreds,sixes,fours,innings,created_at,updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(sql, tuple(batting_details))
            db.commit()
            print("Entry added SUCCESSFULLY to 'Batting_details' TABLE")
        except Exception as e:
            print("Error in adding data to 'Batting_details' TABLE:\n", e)



