from flask import Flask, jsonify, request
import pandas as pd
from scipy.stats import zscore
from flask_cors import CORS

app = Flask(__name__)

#Data Processing
players = pd.read_csv("Seasons_Stats.csv")
players18 = pd.read_csv("17-18.csv")
players19 = pd.read_csv("18-19.csv")
players20 = pd.read_csv("19-20.csv")
players21 = pd.read_csv("20-21.csv")
players22 = pd.read_csv("21-22.csv")
players23 = pd.read_csv("22-23.csv")
all_time_stats =  pd.concat([players, players18, players19, players20, players21, players22,players23], axis = 0)
all_time_stats = all_time_stats.drop('Unnamed: 0', axis = 1)

#Replace null values with 0s
all_time_stats.fillna(0, inplace=True)

top_75_names = ['Michael Jordan', 'LeBron James', 'Kareem Abdul-Jabbar', 'Magic Johnson', 'Wilt Chamberlain', 'Bill Russell', 'Larry Bird', 'Tim Duncan', 'Oscar Robertson', 'Kobe Bryant', "Shaquille O'Neal", 'Kevin Durant', 'Hakeem Olajuwon', 'Julius Erving', 'Moses Malone', 'Stephen Curry', 'Dirk Nowitzki', 'Giannis Antetokounmpo', 'Jerry West', 'Elgin Baylor', 'Kevin Garnett', 'Charles Barkley', 'Karl Malone', 'John Stockton', 'David Robinson', 'John Havlicek', 'Isiah Thomas', 'George Mikan', 'Chris Paul', 'Dwyane Wade', 'Allen Iverson', 'Scottie Pippen', 'Kawhi Leonard', 'Bob Cousy', 'Bob Pettit', 'Dominique Wilkins', 'Steve Nash', 'Rick Barry', 'Kevin McHale', 'Patrick Ewing', 'Walt Frazier', 'Jason Kidd', 'Bill Walton', 'Bob McAdoo', 'Jerry Lucas', 'Ray Allen', 'Wes Unseld', 'Nate Thurmond', 'James Harden', 'Reggie Miller', 'George Gervin', 'Clyde Drexler', 'Pete Maravich', 'Earl Monroe', 'James Worthy', 'Willis Reed', 'Elvin Hayes', 'Nate Archibald', 'Sam Jones', 'Dave Cowens', 'Paul Pierce', 'Robert Parish', 'Hal Greer', 'Lenny Wilkens', 'Paul Arizin', 'Dennis Rodman', 'Russell Westbrook', 'Carmelo Anthony', 'Dolph Schayes', 'Anthony Davis', 'Billy Cunningham', 'Dave DeBusschere', 'Dave Bing', 'Damian Lillard', 'Bill Sharman', 'Michael Jordan*', 'LeBron James*', 'Kareem Abdul-Jabbar*', 'Magic Johnson*', 'Wilt Chamberlain*', 'Bill Russell*', 'Larry Bird*', 'Tim Duncan*', 'Oscar Robertson*', 'Kobe Bryant*', "Shaquille O'Neal*", 'Kevin Durant*', 'Hakeem Olajuwon*', 'Julius Erving*', 'Moses Malone*', 'Stephen Curry*', 'Dirk Nowitzki*', 'Giannis Antetokounmpo*', 'Jerry West*', 'Elgin Baylor*', 'Kevin Garnett*', 'Charles Barkley*', 'Karl Malone*', 'John Stockton*', 'David Robinson*', 'John Havlicek*', 'Isiah Thomas*', 'George Mikan*', 'Chris Paul*', 'Dwyane Wade*', 'Allen Iverson*', 'Scottie Pippen*', 'Kawhi Leonard*', 'Bob Cousy*', 'Bob Pettit*', 'Dominique Wilkins*', 'Steve Nash*', 'Rick Barry*', 'Kevin McHale*', 'Patrick Ewing*', 'Walt Frazier*', 'Gary Payton*', 'Jason Kidd*', 'Bill Walton*', 'Bob McAdoo*', 'Jerry Lucas*', 'Ray Allen*', 'Wes Unseld*', 'Nate Thurmond*', 'James Harden*', 'Reggie Miller*', 'George Gervin*', 'Clyde Drexler*', 'Pete Maravich*', 'Earl Monroe*', 'James Worthy*', 'Willis Reed*', 'Elvin Hayes*', 'Nate Archibald*', 'Sam Jones*', 'Dave Cowens*', 'Paul Pierce*', 'Robert Parish*', 'Hal Greer*', 'Lenny Wilkens*', 'Paul Arizin*', 'Dennis Rodman*', 'Russell Westbrook*', 'Carmelo Anthony*', 'Dolph Schayes*', 'Anthony Davis*', 'Billy Cunningham*', 'Dave DeBusschere*', 'Dave Bing*', 'Damian Lillard*', 'Bill Sharman*']

#Create a list of the top 75 players (really 76 cuz idk why)
top_75 = all_time_stats[all_time_stats['Player'].isin(top_75_names)]

#cut down to the top 75 list
top_75_raw = all_time_stats[all_time_stats['Player'].isin(top_75_names)]

#Convert to int
top_75_raw["Year"] = top_75["Year"].astype(int)

#Select and aggregate by desired stats
top_75 = top_75_raw.groupby(['Player']).agg({
    'G' : 'sum',
    'PTS': 'sum',
    'AST': 'sum',
    'TRB': 'sum',
    'STL': 'sum',
    'BLK': 'sum'
}).reset_index()

# Get Averages
top_75['PTS/G'] = top_75['PTS'] / top_75['G']
top_75['AST/G'] = top_75['AST'] / top_75['G']
top_75['TRB/G'] = top_75['TRB'] / top_75['G']
top_75['STL/G'] = top_75['STL'] / top_75['G']
top_75['BLK/G'] = top_75['BLK'] / top_75['G']

#Calculate z-scores

# Define the columns to calculate z-scores
cols = ['PTS', 'AST', 'TRB', 'STL', 'BLK', 'PTS/G', 'AST/G', 'TRB/G', 'STL/G', 'BLK/G']

# Calculate the z-scores
top_75_zscore = top_75[cols].apply(zscore)

# Add back the 'Player' column
top_75_zscore['Player'] = top_75['Player']

# Reorder the columns
top_75_zscore = top_75_zscore[['Player'] + cols]

pd.read_csv("awards.csv")
pd.read_csv("allnbateams.csv")
championships = pd.read_csv("championships.csv")

team_abbreviations = {
    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BKN',
    'Charlotte Hornets': 'CHA',
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'Los Angeles Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Orleans Pelicans': 'NOP',
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHX',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Washington Wizards': 'WAS',
    'St. Louis Hawks': 'STL',
    'Seattle SuperSonics': 'SEA',
    'Washington Bullets': 'WSB',
    'Philadelphia Warriors': 'PHW',
    'Syracuse Nationals': 'SYR',
    'Minneapolis Lakers': 'MPL',
    'Rochester Royals': 'MPL'
    # Add more mappings if necessary
}

championships['Team'] = championships['Team'].replace(team_abbreviations)

#Calculate # of championships
all_championships = pd.merge(top_75_raw, championships, left_on=['Year', 'Tm'], right_on=['Year', 'Team'], how='left')
all_championships = all_championships[all_championships['Player'].isin(top_75_names)]
all_championships['Championships'] = all_championships['Adjusted SRS'].where(all_championships['Adjusted SRS'].isnull(), 1).fillna(0)

all_championships = all_championships.groupby("Player").sum()
all_championships

#Calculate championship difficulty
top_75_names = ['Michael Jordan', 'LeBron James', 'Kareem Abdul-Jabbar', 'Magic Johnson', 'Wilt Chamberlain', 'Bill Russell', 'Larry Bird', 'Tim Duncan', 'Oscar Robertson', 'Kobe Bryant', "Shaquille O'Neal", 'Kevin Durant', 'Hakeem Olajuwon', 'Julius Erving', 'Moses Malone', 'Stephen Curry', 'Dirk Nowitzki', 'Giannis Antetokounmpo', 'Jerry West', 'Elgin Baylor', 'Kevin Garnett', 'Charles Barkley', 'Karl Malone', 'John Stockton', 'David Robinson', 'John Havlicek', 'Isiah Thomas', 'George Mikan', 'Chris Paul', 'Dwyane Wade', 'Allen Iverson', 'Scottie Pippen', 'Kawhi Leonard', 'Bob Cousy', 'Bob Pettit', 'Dominique Wilkins', 'Steve Nash', 'Rick Barry', 'Kevin McHale', 'Patrick Ewing', 'Walt Frazier', 'Jason Kidd', 'Bill Walton', 'Bob McAdoo', 'Jerry Lucas', 'Ray Allen', 'Wes Unseld', 'Nate Thurmond', 'James Harden', 'Reggie Miller', 'George Gervin', 'Clyde Drexler', 'Pete Maravich', 'Earl Monroe', 'James Worthy', 'Willis Reed', 'Elvin Hayes', 'Nate Archibald', 'Sam Jones', 'Dave Cowens', 'Paul Pierce', 'Robert Parish', 'Hal Greer', 'Lenny Wilkens', 'Paul Arizin', 'Dennis Rodman', 'Russell Westbrook', 'Carmelo Anthony', 'Dolph Schayes', 'Anthony Davis', 'Billy Cunningham', 'Dave DeBusschere', 'Dave Bing', 'Damian Lillard', 'Bill Sharman', 'Michael Jordan*', 'LeBron James*', 'Kareem Abdul-Jabbar*', 'Magic Johnson*', 'Wilt Chamberlain*', 'Bill Russell*', 'Larry Bird*', 'Tim Duncan*', 'Oscar Robertson*', 'Kobe Bryant*', "Shaquille O'Neal*", 'Kevin Durant*', 'Hakeem Olajuwon*', 'Julius Erving*', 'Moses Malone*', 'Stephen Curry*', 'Dirk Nowitzki*', 'Giannis Antetokounmpo*', 'Jerry West*', 'Elgin Baylor*', 'Kevin Garnett*', 'Charles Barkley*', 'Karl Malone*', 'John Stockton*', 'David Robinson*', 'John Havlicek*', 'Isiah Thomas*', 'George Mikan*', 'Chris Paul*', 'Dwyane Wade*', 'Allen Iverson*', 'Scottie Pippen*', 'Kawhi Leonard*', 'Bob Cousy*', 'Bob Pettit*', 'Dominique Wilkins*', 'Steve Nash*', 'Rick Barry*', 'Kevin McHale*', 'Patrick Ewing*', 'Walt Frazier*', 'Gary Payton*', 'Jason Kidd*', 'Bill Walton*', 'Bob McAdoo*', 'Jerry Lucas*', 'Ray Allen*', 'Wes Unseld*', 'Nate Thurmond*', 'James Harden*', 'Reggie Miller*', 'George Gervin*', 'Clyde Drexler*', 'Pete Maravich*', 'Earl Monroe*', 'James Worthy*', 'Willis Reed*', 'Elvin Hayes*', 'Nate Archibald*', 'Sam Jones*', 'Dave Cowens*', 'Paul Pierce*', 'Robert Parish*', 'Hal Greer*', 'Lenny Wilkens*', 'Paul Arizin*', 'Dennis Rodman*', 'Russell Westbrook*', 'Carmelo Anthony*', 'Dolph Schayes*', 'Anthony Davis*', 'Billy Cunningham*', 'Dave DeBusschere*', 'Dave Bing*', 'Damian Lillard*', 'Bill Sharman*']


championships_difficulty = pd.merge(top_75_raw, championships, left_on=['Year', 'Tm'], right_on=['Year', 'Team'], how='left')
championships_difficulty = championships_difficulty[["Player", "Adjusted SRS"]]
#championships_difficulty[championships_difficulty['Player'] == "Kareem Abdul-Jabbar*"]
championships_difficulty = championships_difficulty[championships_difficulty['Player'].isin(top_75_names)] 



championships_difficulty = championships_difficulty[championships_difficulty["Adjusted SRS"] != 'None']
championships_difficulty = championships_difficulty.dropna()

#championships_difficulty["Adjusted SRS"] = championships_difficulty["Adjusted SRS"].astype(int)  
#championships_difficulty.groupby("Player").mean().reset_index().sort_values("Adjusted SRS")
championships_difficulty = championships_difficulty.rename(columns={'Adjusted SRS': 'Championship Difficulty'})

championships_difficulty = championships_difficulty.groupby("Player").mean().reset_index()

championships_difficulty
# Find the minimum value in the 'SRS' column
min_SRS = championships_difficulty['Championship Difficulty'].min()

# Add the absolute value of min_value to all values in the 'SRS' column
championships_difficulty['new Championship Difficulty'] = championships_difficulty['Championship Difficulty'] + abs(min_SRS)
championships_difficulty.sort_values("new Championship Difficulty", ascending = True)
#championships_difficulty =championships_difficulty.dropna()
#championships_difficulty.groupby("Player")
#championships_difficulty.sort_values("Adjusted SRS")

championships["Championships"] = 1
all_championships
all_championships = pd.merge(top_75_raw, championships, left_on=['Year', 'Tm'], right_on=['Year', 'Team'], how='left')
all_championships = all_championships[all_championships['Player'].isin(top_75_names)]
#all_championships =all_championships.fillna(0)
#all_championships.groupby("Player").mean()
#all_championships.sort_values("Adjusted SRS")
#all_championships['Adjusted SRS'] = all_championships['Adjusted SRS'].astype(int)
#all_championships.groupby("Player").sum()


all_championships['Championships'] = all_championships['Championships'].where(all_championships['Championships'].isnull(), 1).fillna(0)


all_championships['Championships'] = all_championships['Championships'].astype(int)
all_championships = all_championships.groupby("Player")[['Player', 'Championships']].sum().reset_index()
all_championships

awards = pd.read_csv("awards.csv")
MVP = awards['MVP'].value_counts().reset_index()
MVP.columns = ['Player', 'MVP']

DPOY = awards['DPOY'].value_counts().reset_index()
DPOY.columns = ['Player', 'DPOY']


FMVP = awards['FMVP'].value_counts().reset_index()
FMVP.columns = ['Player', 'FMVP']


all_nba = pd.read_csv("allnbateams.csv")


allawards = pd.merge(MVP, DPOY, on='Player', how = 'outer')
allawards = pd.merge(allawards, FMVP, on='Player', how = 'outer')
allawards = pd.merge(allawards, all_nba, on='Player', how = 'outer')
allawards.fillna(0, inplace=True)
allawards[['MVP', 'DPOY', 'FMVP', 'All NBA Teams']] = allawards[['MVP', 'DPOY', 'FMVP', 'All NBA Teams']].astype(int)

allawards
# final_table = pd.merge(final_table, allawards, how = "left")
# final_table.sort_values("MVP")


final_table = pd.merge(top_75, all_championships, left_on=['Player'], right_on=['Player'], how='left')
final_table = pd.merge(final_table, championships_difficulty, left_on=['Player'], right_on=['Player'], how='left')
final_table['Championship Difficulty'] = final_table['Championship Difficulty'].fillna(final_table['Championship Difficulty'].median())
final_table['Player'] = final_table['Player'].str.replace('*', '', regex=True)

final_table = pd.merge(final_table, MVP, left_on=['Player'], right_on=['Player'], how='left')
final_table = pd.merge(final_table, allawards, how = "left")
final_table = final_table.fillna(0)

# final_table["Championship Difficulty"] = final_table["Championship Difficulty"] * final_table["Championships"]

# final_table.sort_values("Championship Difficulty", ascending = False)
final_table["new Championship Difficulty"] = final_table["new Championship Difficulty"] * final_table["Championships"]

final_table.sort_values("MVP")

#Calculate z-scores

# Define the columns to calculate z-scores
cols = ['PTS', 'AST', 'TRB', 'STL', 'BLK', 'PTS/G', 'AST/G', 'TRB/G', 'STL/G', 'BLK/G', 'Championships', 'new Championship Difficulty', 'Championship Difficulty', 'MVP', 'DPOY', 'FMVP', 'All NBA Teams']

# Calculate the z-scores
final_table_z = final_table[cols].apply(zscore)

# Add back the 'Player' column
final_table_z['Player'] = final_table['Player']

# Reorder the columns
final_table_z = final_table_z[['Player'] + cols]

#stabilize outliers
cols = [col for col in final_table_z.columns if col != 'Player']
#final_table_z[cols] = final_table_z[cols].where(final_table_z[cols] <= 2.5, other=2.5)

# #stabilize outliers
# cols = [col for col in final_table_z.columns if col != 'Player']
# final_table_z[cols] = final_table_z[cols].where(final_table_z[cols] <= 2.5, other=2.5)

final_table_z.head(30)

import pandas as pd

# Custom function for robust scaling
def robust_scale(data):
    median = data.median()
    iqr = data.quantile(0.75) - data.quantile(0.25)
    return (data - median) / iqr

# Define the columns to calculate robust scaled values
cols = ['PTS', 'AST', 'TRB', 'STL', 'BLK', 'PTS/G', 'AST/G', 'TRB/G', 'STL/G', 'BLK/G', 'Championships', 'new Championship Difficulty', 'Championship Difficulty', 'MVP', 'DPOY', 'FMVP', 'All NBA Teams']

# Calculate the robust scaled values
final_table_robust = final_table[cols].apply(robust_scale)

# Add back the 'Player' column
final_table_robust['Player'] = final_table['Player']

# Reorder the columns
final_table_robust = final_table_robust[['Player'] + cols]

# Stabilize outliers (set values above 2.5 to 2.5)
cols = [col for col in final_table_robust.columns if col != 'Player']
final_table_robust[cols] = final_table_robust[cols].where(final_table_robust[cols] <= 2.5, other=2.5)

# Print the final_table_robust
final_table_robust.head(50)

final_table_z.sort_values('new Championship Difficulty', ascending = False).head(10)

def rankAllTimePlayer(PTS, AST, STL, BLK, Championships, new_Championship_Difficulty, MVP, DPOY, FMVP, All_NBA):
    final_table_z["Rankings"] = (PTS * final_table_z["PTS"] 
    + AST * final_table_z["AST"] 
    + STL * final_table_z["STL"] 
    + BLK * final_table_z["BLK"]
    + Championships * final_table_z["Championships"] 
    + new_Championship_Difficulty * final_table_z["new Championship Difficulty"]
    +  MVP * final_table_z["MVP"]
    +  DPOY * final_table_z["DPOY"]
    +  FMVP * final_table_z["FMVP"]
    +  All_NBA * final_table_z["All NBA Teams"])
    
    return final_table_z.sort_values("Rankings", ascending = False) 

final_table_z.sort_values("Championship Difficulty").head(50)

top_75_names = ["Michael Jordan", "LeBron James", "Kareem Abdul-Jabbar", "Magic Johnson", "Wilt Chamberlain",
                "Bill Russell", "Larry Bird", "Tim Duncan", "Oscar Robertson", "Kobe Bryant", "Shaquille O'Neal",
                "Kevin Durant", "Hakeem Olajuwon", "Julius Erving", "Moses Malone", "Stephen Curry", "Dirk Nowitzki",
                "Giannis Antetokounmpo", "Jerry West", "Elgin Baylor", "Kevin Garnett", "Charles Barkley", "Karl Malone",
                "John Stockton", "David Robinson", "John Havlicek", "Isiah Thomas", "George Mikan", "Chris Paul",
                "Dwyane Wade", "Allen Iverson", "Scottie Pippen", "Kawhi Leonard", "Bob Cousy", "Bob Pettit",
                "Dominique Wilkins", "Steve Nash", "Rick Barry", "Kevin McHale", "Patrick Ewing", "Walt Frazier",
                "Gary Payton", "Jason Kidd", "Bill Walton", "Bob McAdoo", "Jerry Lucas", "Ray Allen", "Wes Unseld",
                "Nate Thurmond", "James Harden", "Reggie Miller", "George Gervin", "Clyde Drexler", "Pete Maravich",
                "Earl Monroe", "James Worthy", "Willis Reed", "Elvin Hayes", "Nate Archibald", "Sam Jones",
                "Dave Cowens", "Paul Pierce", "Robert Parish", "Hal Greer", "Lenny Wilkens", "Paul Arizin",
                "Dennis Rodman", "Russell Westbrook", "Carmelo Anthony", "Dolph Schayes", "Anthony Davis",
                "Billy Cunningham", "Dave DeBusschere", "Dave Bing", "Damian Lillard", "Bill Sharman"]

# Double the size of the list by duplicating every player with a "*" added to the end of their name
doubled_list = [name + '*' for name in top_75_names]

# Combine the original list and the doubled list
full_list = top_75_names + doubled_list

# example below 
rankAllTimePlayer(15, 15, 5, 5, 25, 30, 8, 1, 15, 10)

def rankAllTimePlayer(PTS, AST, STL, BLK, Championships, new_Championship_Difficulty, MVP, DPOY, FMVP, All_NBA):
    final_table_z["Rankings"] = (PTS * final_table_z["PTS"] 
    + AST * final_table_z["AST"] 
    + STL * final_table_z["STL"] 
    + BLK * final_table_z["BLK"]
    + Championships * final_table_z["Championships"] 
    + new_Championship_Difficulty * final_table_z["new Championship Difficulty"]
    +  MVP * final_table_z["MVP"]
    +  DPOY * final_table_z["DPOY"]
    +  FMVP * final_table_z["FMVP"]
    +  All_NBA * final_table_z["All NBA Teams"])
    
    return final_table_z.sort_values("Rankings", ascending = False).head(10)


CORS(app)


@app.route("/", methods=['POST'])
def rank_players():
    try:
        # Get the values array from the JSON request
        values_array = request.get_json()['values']
        print(values_array)
        results = rankAllTimePlayer(*values_array)
        # Ranking function here
        
        # Convert the DataFrame to a list of dictionaries
        ranked_players_data = results.to_dict(orient="records")

        # Return the ranked players' data as JSON response
        return jsonify(ranked_players_data)
    except Exception as e:
        return jsonify({"error": str(e)})

# Run the Flask app if executed as the main script
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)

