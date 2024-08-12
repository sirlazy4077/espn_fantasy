from pypdf import PdfReader
import re
import csv

#FIXME haven't quite gotten bye weeks to work yet

#global dict for player data we're sort later for csv loading
players_dict = {}

# input is the raw player text, the type of pattern (if 2 or 3 names, e.g. suffix included use 2), and the rank of the LAST player with double-digit values
def player_parser(players_raw,pattern_type,value_doubledigits):
    for p in players_raw:
        p_raw = p.split()
        
        #grab all the player details of name, team, and (for now) their auction value
        if (pattern_type == "1") or (pattern_type == "1b"):
            p_name = p_raw[2] + ' ' + p_raw[3].split(',')[0]
            p_team = p_raw[4]
            p_value_raw = p_raw[5].split('$')[1]

        elif (pattern_type == "2") or (pattern_type == "2b"):
            p_name = p_raw[2] + ' ' + p_raw[3] + ' ' + p_raw[4].split(',')[0]
            p_team = p_raw[5]
            p_value_raw = p_raw[6].split('$')[1]
        
        #get their rank, position, and positional ranking
        p_rank = int(p_raw[0].split('.')[0])

        pattern_pos = r'[A-Za-z]+'
        p_position = re.findall(pattern_pos,p_raw[1])[0]
        
        pattern_pos_rank = r'[0-9]+'
        p_position_rank = int(re.findall(pattern_pos_rank,p_raw[1])[0])

        #sort out if the player's line had the auction value and bye week concatenated to split them up
        if (pattern_type == "1") :
            p_value = p_value_raw
            # p_bye = p_raw[6] #FIXME
            
        elif (pattern_type == "2"):
            p_value = p_value_raw
            # p_bye = p_raw[7] #FIXME
                
        elif (pattern_type == "1b") or (pattern_type == "2b"):
                
            if (p_rank < value_doubledigits):
                p_value = p_value_raw[0:2]
                # p_bye = p_value_raw[2:] #FIXME
            else:
                p_value = p_value_raw[0]
                # p_bye = p_value_raw[1:] #FIXME
            
        #check if the player's bye exists after the logic, if not then they already existed and don't write to the dict
        # if p_bye == '': #FIXME
        #     continue
        
        int(p_value)
        # int(p_bye) #FIXME
    
        # players_dict.update({p_name:[p_rank,p_position,p_position_rank,p_team,p_value,p_bye]}) #FIXME
        players_dict.update({p_name:[p_rank,p_position,p_position_rank,p_team,p_value]})

# what is essentially the main of the program, TODO make this a proper program
#strip the ESPN top 300 rankings pdf for player data
reader = PdfReader('PPR300.pdf')
page = reader.pages[0]
text = page.extract_text()
text_lower = text.lower()

#find players with a first and last name including . and - and ', including defenses with their /, ignores newline char
pattern_1 = r'[0-9]+\. \([^)]*\) [A-Za-z0-9\-\.\']+ [A-Za-z0-9\-\.\'\/]+, [A-Za-z]+ \$[0-9]+ [0-9]+'
players_raw_1 = re.findall(pattern_1, text_lower)

#find players with a first and last name including . and - and ', including defenses with their /, ignores newline char, but player value and bye week were combined
pattern_1b = r'[0-9]+\. \([^)]*\) [A-Za-z0-9\-\.\']+ [A-Za-z0-9\-\.\'\/]+, [A-Za-z]+ \$[0-9]+'
players_raw_1b = re.findall(pattern_1b, text_lower)

#find players with a first and last name WITH suffix including . and - and ', including defenses with their /, ignores newline char, but player value and bye week were combined
pattern_2 = r'[0-9]+\. \([^)]*\) [A-Za-z0-9\-\.\']+ [A-Za-z0-9\-\.\'\/]+ [A-Za-z0-9\-\.\'\/]+, [A-Za-z]+ \$[0-9]+ [0-9]+'
players_raw_2 = re.findall(pattern_2, text_lower)

#find players with a first and last name WITH suffix including . and - and ', including defenses with their /, ignores newline char, but player value and bye week were combined
pattern_2b = r'[0-9]+\. \([^)]*\) [A-Za-z0-9\-\.\']+ [A-Za-z0-9\-\.\'\/]+ [A-Za-z0-9\-\.\'\/]+, [A-Za-z]+ \$[0-9]+'
players_raw_2b = re.findall(pattern_2b, text_lower)

#run the player data to be cleaned
player_parser(players_raw_1,"1",57)
player_parser(players_raw_1b,"1b",57)
player_parser(players_raw_2,"2",57)
player_parser(players_raw_2b,"2b",57)

# print(players_dict) #DEBUG

#sort on overall rank and load the data to a csv
players_dict_sorted = {key: value for key, value in sorted(players_dict.items(),key=lambda item: item[1][0],reverse=False)}

# header = ['player_name','overall_rank','position','position_rank','team','auction_value','bye_week'] #FIXME
header = ['player_name','overall_rank','position','position_rank','team','auction_value']
with open('test.csv','w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    
    for key,val in players_dict_sorted.items():
        load = []
        load.append(key)
        for v in val:
            load.append(v)
        
        writer.writerow(load)