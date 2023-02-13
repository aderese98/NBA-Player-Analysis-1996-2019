import pandas as pd
import requests
from bs4 import BeautifulSoup as soup
from matplotlib import pyplot as plt
import numpy as np
import random
from PIL import Image
from wordcloud import WordCloud,STOPWORDS

def Abraham_Code():
    #CSV Read
    nba_data = pd.read_csv('nba_17-18_win_loss.csv')
    
    #Pandas DataFrame 1
    nba_elo_df = pd.DataFrame()
    
    #All Dictionaries Used
    past_elo=dict()
    present_elo=dict()
    future_elo=dict()
    team_elo=dict()
    name_to_abb = dict()
    name_ratings=dict()
    
    #All Lists Used
    team_abb=list()
    rate_list=list()
    elo_list = list()
    
    '''
    Method to get information on past NBA Elo Ratings from websites,
    get conversions for NBA abbreviations to team names and get NBA team
    net rating averages for the future season
    '''
    def get_elo():
        url = 'https://projects.fivethirtyeight.com/2017-nba-predictions/'
    
        page = requests.get(url)
        page_soup = soup(page.content, 'html.parser')
        results = page_soup.find(id='standings-table')
        elo = results.find_all('td', class_='num elo original desktop')
        team_name1 = results.find_all('td', class_='team')
        
        for rating,name in zip(elo,team_name1):
            for num,team in zip(rating,name):
                for nm in team:
                    team_elo[nm]=num
        
        url2 = 'https://gist.github.com/Tgemayel/e6e282b9aa538bb8b8b7'
        
        page2 = requests.get(url2)
        page_soup2 = soup(page2.content, 'html.parser')
        results2 = page_soup2.find(id='file-gistfile1-txt')
        abb = results2.find_all('table', class_='highlight tab-size js-file-line-container')
        
        for val in abb:
            team_abb = val.text.split('\n')
            while("" in team_abb):
                team_abb.remove("")
        for team in team_abb:
            abb = team[:3]
            name = team[6:]
            name_to_abb[abb] = name
            for name in team_elo:
                if name in team:
                    past_elo[abb] = team_elo[name]
        url3 = 'https://www.basketball-reference.com/leagues/NBA_2019_ratings.html'
        
        page3 = requests.get(url3)
        page_soup3 = soup(page3.content, 'html.parser')
        results3 = page_soup3.find(id='ratings')
        team_name2 = results3.find_all('td', class_='left')
        ratings = results3.find_all('td', class_='right')
        
        for rating in ratings:
            if 'net_rtg_adj' in str(rating):
                rate_list.append(rating.text)
        for name,rating in zip(team_name2,rate_list):
            name_ratings[name.text] = rating
    
    '''Writes to present Elo using past Elo data to make new Elo Ratings for the'''
    #new season
    def get_past_elo():
        for elo in past_elo:
            old_elo = int(past_elo[elo])
            present_elo[elo] = calc_elo(old_elo)
     
    '''Calculates new starting Elo'''
    def calc_elo(team_elo):
        equation = (int(team_elo) * .75) + (.25*1505)
        return round(equation)
    
    ''''Calculates a team's win probability against another team using their Elo scores'''
    def win_prob(team_elo,opp_elo):
        win_probability = 1/(1+(10**((op_elo-team_elo)/400)))
        return win_probability
    
    '''Calculates final Elo prediction for a given season'''
    def final_elo(k,win_loss,win_p,elo):
        final_elo = k*(win_loss-win_p)+elo
        return round(final_elo)
    
    '''Calculates future Elo Prediction for the next seasons'''
    def get_future_elo(cur_elo,net):
        net_rating = (net/100)*cur_elo
        f_elo = net_rating + cur_elo
        return round(f_elo)
    
    '''Call get methods for dictionairies and lists to be used'''
    get_elo()
    get_past_elo()
    
    '''Use prediction algorithm to estimate 2017-18 Elo Rating Based on 2016-17 Elo Rating
    And 2017-18 Game by Game performance'''
    for index, row in nba_data.iterrows():
        if row['Team'] in past_elo and row['Opponent'] in past_elo:
            w_or_l = 0
            tm_elo = float(present_elo[row['Team']])
            op_elo = float(present_elo[row['Opponent']])
            if 'W' in row['WINorLOSS']:
                elo_diff = tm_elo - op_elo
                margin_of_victory = int(row['TeamPoints'])-int(row['OpponentPoints'])
                numerator = abs((margin_of_victory + 3)**.8)
                denominator = 7.5+.006*elo_diff
                k = 20*(numerator/denominator)
                w_or_l = 1
            elif 'L' in row['WINorLOSS']:
                elo_diff = op_elo - tm_elo
                margin_of_victory = int(row['OpponentPoints'])-int(row['TeamPoints'])
                numerator = abs((margin_of_victory + 3)**.8)
                denominator = 7.5+.006*elo_diff
                k = 20*(numerator/denominator)
        if row['Team'] in past_elo:
            present_elo[row['Team']] = final_elo(k,w_or_l,win_prob(tm_elo,op_elo),tm_elo)
            future_elo[row['Team']] = final_elo(k,w_or_l,win_prob(tm_elo,op_elo),tm_elo)
    
    '''Make DataFrame to store past and present Elo Ratings'''
    for elo in future_elo:
        for abb in name_to_abb:
            if elo in abb:
                name = name_to_abb[abb]    
        data = [[name,elo,past_elo[elo],future_elo[elo]]]
        nba_elo_df = nba_elo_df.append(pd.DataFrame(data,
                     columns=['Name','Abbr.','2016-17 Elo Rating','2017-18 Elo Rating']),
                     ignore_index=True)
    
    '''Calculate and add future Elo Rating predictions for 2018-19 to the DataFrame
    using 2017-18 data'''
    for index,rows in nba_elo_df.iterrows():
        if rows['Name'] in name_ratings:
            rating = name_ratings[rows['Name']]
            elo = rows['2017-18 Elo Rating']
            f_elo = get_future_elo(int(elo),float(rating))
        elo_list.append(f_elo)
    nba_elo_df['2018-19 Elo Rating'] = pd.Series(elo_list,
                                       index=nba_elo_df.index)
    
    '''Make a bar graph of the change in Elo Rating of the top 10 teams in 2018 to 2019'''
    def make_bar():
        x_indexes = np.arange(len(nba_elo_df['Abbr.'].head(10)))
        width=.25
        data = nba_elo_df.sort_values(by='2017-18 Elo Rating',ascending=False)
        plt.bar(x_indexes,data['2017-18 Elo Rating'].head(10),width=width
                ,color='#e5ae38', label='2017-18')
        plt.xticks(x_indexes-width,data['Abbr.'].head(10))
        
        plt.bar(x_indexes+width,data['2018-19 Elo Rating'].head(10),width=width
                ,color = "#008fd5", label='2018-19')
        plt.legend()
        plt.xlabel('Team Names(Abbreviated)')
        plt.ylabel('Elo Rating')
        plt.title('2018 and 2019 Season Final NBA Elo Ratings')
        plt.show()
    
    '''Make a WordCloud to visualize possible 2018-19 NBA Season team performance'''
    def make_cloud():
        temp_list = []
        for index, rows in nba_elo_df.iterrows():
            nm = rows['Name']
            elo = rows['2018-19 Elo Rating']/100
            temp_list += ([nm]*int(elo))
        wc = WordCloud(
            background_color = 'gray',
            height = 600,
            width = 400)
        text = ''
        for word in temp_list:
            text += word + ' '
        wc.generate(text)
        plt.imshow(wc)
        wc.to_file('wc.png')
    
    print('This section of the project is capable of taking past NBA team data')
    print('and predicts their future performance by calculating Elo Ratings.\n')
    print('Here are the past Elo Ratings for NBA Teams in the 2016-17 Season')
    for elo in past_elo:
        print(name_to_abb[elo],'---',past_elo[elo])
    
    print('\nThis is the final Elo Prediction for the 2017-18 Season based on the')
    print('year''s game performance.\n')
    for elo in future_elo:
        print(name_to_abb[elo],'---',future_elo[elo])
    make_bar()
    print('\nThis graph visualizes the possible change in team performance between the years')
    
    print('\nThis DataFrame compiles present year and potential future year performance')
    print(nba_elo_df)
    
    print('Finally, this WordCloud uses change in Elo from the present and future')
    print('year to visualize further performance predictions for later years')
    make_cloud()
    
def Itai_Code():
    # printing the all players net ratings using my first feature- panda.
    df = pd.read_csv("all_seasons.csv")
    print(df)
    
    # printing the the players with the net ratings using my second feature-  still panda, now, in descending order.
    sort = df.sort_values(by=['net_rating'], ascending=False).head(10)
    print("the top 10 players, with the best net rating are :\n", sort)
    
    # 1 Data Analyses using Lists & Dictionaries
    
    player_name = input('Enter the player name:')
    player_season = input('Enter the season you wish to know about the player, please enter the year in this format: '
                          'xxxx-xx, '
                          ' where xxxx is the full year the season began and the xx is the shortened of the 2nd year: ')
    check = False
    
    for i, row in df.iterrows():
        if row['player_name'] in player_name and row['season'] in player_season:
            print(player_name + ": His net rating for the season was", row['net_rating'])
            check = True
            break
    if not check:
        print('This player does not exist')
    
    # second time - Data Analyses using Lists & Dictionaries
    player_season = input('Enter the season you wish to know which player had the best net rating, please enter the year '
                          'in this format: '
                          'xxxx-xx, '
                          ' where xxxx is the full year the season began and the xx is the shortened of the 2nd year: ')
    high = 0
    name = ''
    for i, row in df.iterrows():
        if row['season'] == player_season and row['net_rating'] > high:
            high = row['net_rating']
            name = row['player_name']
    print("The best net rating for the season was", high, "by the player", name)
    
    
    # display this information in bar graph using my third feature - matplotlib library
    plt.bar('player_name', 'net_rating', data=sort)
    plt.xlabel("player_name", size=35)
    plt.ylabel("net_rating", size=25)
    plt.grid(color='#95a5a6', linestyle='--', linewidth=2, axis='y', alpha=0.7)
    plt.title("Net rating in the NBA since 1966-2019", size=12)
    plt.show()
    
    
    # display this information in word cloud using my fifth feature - wordcloud library
    check = df['country'].value_counts(ascending=False).head(10)
    wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="black").generate(str(check))
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

def Heather_Code():
    plt.rcParams.update({'font.size': 20, 'figure.figsize': (10, 8)}) # set font and plot size to be larger
    
    # read the file and check that it read in correctly
    NBA_Player_df = pd.read_csv('all_seasons.csv')
    #print(NBA_Player_df.head())
    #print(NBA_Player_df.head(10))
    #print(NBA_Player_df.tail(2))
    
    #print(NBA_Player_df.info())
    #print(NBA_Player_df.shape)
    
    #rename column 0 to be the index and set it as the index
    NBA_Player_df = NBA_Player_df.rename(columns={'Unnamed: 0': "Index"})
    NBA_Player_df = NBA_Player_df.set_index('Index')
    
    #player_J = NBA_Player_df[NBA_Player_df['player_name'] == "J_"]
    #print(player_J)
    
    #generate list of random colors for bar chart
    color_list=[]
    for i in range(0,99):
        rgb=(random.random(),random.random(),random.random(),1)
        color_list.append(rgb)
    
    #print(color_list[:10])
    print()
    #create subset df, eliminate all players with college listed as "none", create df that is only player name & college
    #eliminate duplicates, bar graph of top 100 colleges who have sent players to the NBA
    college_df = NBA_Player_df[NBA_Player_df['college'] !='None']
    college_df_reduce = college_df[['player_name','college']]
    #my_cmap = cm.get_cmap('seismic')
    #my_norm = Normalize(vmin=0,vmax=100)
    
    #print(college_df_reduce.shape)
    college_df_no_dupes = college_df_reduce.drop_duplicates()
    #print(sub_college_df.shape)
    college_df_no_dupes['college'].value_counts()[:101].plot(kind='bar',fontsize=6, color = color_list, edgecolor='silver', title = "# of Players by College")
    plt.savefig("Colleges to NBA.png")
    plt.show()
    
    
    #create word cloud of top 250 players based on length of NBA career
    names=NBA_Player_df.player_name[0]
    player_season_count = NBA_Player_df['player_name'].value_counts(ascending=False)
    print(player_season_count)
    #with open('season_count','w') as f:
        #print(player_season_count, file=f)
    
    
    names = ";".join(names for names in NBA_Player_df.player_name)
    ball_mask=np.array(Image.open("basketball.png"))
    ball_mask = ball_mask.reshape((ball_mask.shape[0],-1), order='F')
    
    stopwords = set(STOPWORDS)
    #print(names)
    name_string = names.replace(" ","_")
    
    
    #text=df.description[0]
    wordcloud = WordCloud(collocations=False, max_words = 250, height = 700, width = 700, colormap="winter", background_color = "whitesmoke", mask = ball_mask, scale = .5, contour_width=.5, contour_color='cornflowerblue').generate(name_string)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    wordcloud.to_file("NBA_Players.png")
    
    #Create word cloud for teams
    
    teams=NBA_Player_df.team_abbreviation[0]
    team_count = NBA_Player_df['team_abbreviation'].value_counts(ascending=False)
    print(team_count)
    #with open('season_count','w') as f:
        #print(player_season_count, file=f)
    
    
    teams = ";".join(teams for teams in NBA_Player_df.team_abbreviation)
    ball_mask=np.array(Image.open("basketball.png"))
    ball_mask = ball_mask.reshape((ball_mask.shape[0],-1), order='F')
    
    stopwords = set(STOPWORDS)
    #print(names)
    #team_string = team.replace(" ","_")
    
    
    #text=df.description[0]
    wordcloud = WordCloud(collocations=False, max_font_size = 200, max_words = 250, height = 1000, width = 500, colormap="seismic", background_color = "slategrey", scale = .5).generate(teams)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    wordcloud.to_file("NBA_teams.png")
    
    print("\nTop 10 players with the most games played.\n")
    
    games_played_df = NBA_Player_df[['player_name','gp']]
    games_sum_df = games_played_df.groupby('player_name').sum()
    print(games_sum_df.sort_values(by=['gp'],ascending = False)[:10])
    
    print("\nTop 10 highest average points per game.\n")
    
    points_scored_df = NBA_Player_df[['player_name','pts']]
    points_sum_df = points_scored_df.groupby('player_name').mean()
    print(points_sum_df.sort_values(by=['pts'],ascending = False)[:10])
    
    total_points_df=NBA_Player_df[['player_name','gp','pts','reb','ast']]
    total_points_df['season_points'] = (total_points_df['gp'] * total_points_df['pts'])
    total_points_df['season_ast'] = (total_points_df['gp'] * total_points_df['ast'])
    total_points_df['season_reb'] = (total_points_df['gp'] * total_points_df['reb'])
    top_total_points = total_points_df[['player_name','season_points']]
    top_total_points_df = top_total_points.groupby('player_name').sum()
    print('\nTop 10 Points Scorers\n')
    print(top_total_points_df.sort_values(by=['season_points'], ascending=False)[:10])
    
    top_total_reb = total_points_df[['player_name','season_reb']]
    top_total_reb_df = top_total_reb.groupby('player_name').sum()
    print('\nTop 10 Rebounders\n')
    print(top_total_reb_df.sort_values(by=['season_reb'], ascending=False)[:10])
    
    top_total_ast = total_points_df[['player_name','season_ast']]
    top_total_ast_df = top_total_ast.groupby('player_name').sum()
    print('\nTop 10 Assists\n')
    top_total_ast_df['season_ast'].apply(np.ceil)
    print(top_total_ast_df.sort_values(by=['season_ast'], ascending=False)[:10])
    
    print(NBA_Player_df['age'].describe())
    
    NBA_Player_df['age'].plot(kind="box")
    plt.savefig("Age_Boxplot.png")
    plt.show()    


print("Welcome to the Group 6 NBA Analysis Project.")
print("Each group members code can be found in their respective function.")

while input("Do You Want To Continue? [y/n]") == "y":
    print("\n====This is Abrahams section====\n")
    Abraham_Code()
    if input("Do You Want To Continue? [y/n]") == 'n':
        break
    print("\n====This is Itais section====\n")
    Itai_Code()
    if input("Do You Want To Continue? [y/n]") == 'n':
        break
    print("\n====This is Heathers section====\n")
    Heather_Code()