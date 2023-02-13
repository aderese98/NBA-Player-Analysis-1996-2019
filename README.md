# NBA-Player-Analysis-1996-2019
The goal of this project was to analyze player data for the NBA from 1996 through 2019. I used a variety of Python features and integrations such as WordCloud, Matplotlib, Pandas and JSON.

## Detailed Description
The features my code makes use of are lists and dictionaries, one pandas dataframe, three web scrapers, one matplotlib graph and one wordcloud. All of these features are used to gather, analyze and visualize all the data I found. 

Most of my lists and dictionaries were used to hold data on teams and elo ratings. One struggle I can across was converting team names and abbreviations. I need this as some data on teams used their full name and some used abbreviations. I found a website on GitHub that contained team names and their abbreviations and stored that into a dictionary with key and values corresponding to names and abbreviations. 

I used three web scrapers in total. One to gather name to abbreviation data, one to get Elo Ratings for teams in the 2016-17 season and one to get team average net ratings as our dataset only included individual player net ratings and not team average net ratings.

I used a matplotlib bar graph to show the change in the current season being tracked, 2017-18 season, and my future projections for the 2018-19 season. It also shows the change in Elo Ratings for the top 10 potential teams for the future season.

I finally used a wordcloud to better visualize the data on all teams available with the teams having larger names showing a better chance at high performance in the future seasons.

### Matplot lib Usage
The challenges for the matplot lib for the colleges that have sent players to the NBA were 
1) 15% of the players listed had “None” listed as their college, so first I needed to eliminate that data and create a smaller panda that only included players recruited from college. 
2)  I needed to eliminate the duplicates: if players played more than 1 year.  
3)  I needed to pick a reasonable number of colleges to display.  Looking at the data, the top 101 produced a useful and readable chart.  The final 6 or so had the same number of players so it made sense to be inclusive. 
4)  Finally, I wanted to create a more interesting graphs so I generated a list of 101 random colors (generating r,g,b values 101 times).  I then fed this list into the matplot lib parameters to create a more colorful graph.  As a result, the graph is never quite the same twice.

### Age Graphing
The box plot on age went as expected. The youngest age is 18 and the oldest is 45.  Average age was 27.17.  The interesting thing on understanding this chart is that the players are averaged in at every age.  Given more time, it would be interesting to average each individual age and see how the box plot would change. 

### WordCloud Implementation
The wordCloud on length of careers proved challenging.  I needed to get the count for each player but I needed to keep their first & last names together.  I was able to cycle through and replace the “ “ with an underscore, but it did not work for all names.  Either JJ Reddick or JJ Berea has a random “J” showing up.  Additionally it took some finagling to figure out a good color mapping and the right number of players to include.  There was a tipping point where it was just too crowded and confusing.  Finding the correct parameters took some time.  Finally, I still can’t get my wordCloud to show up INSIDE my mask.  This is a consistent problem and I’m still trying to figure out how to fix it.  I did not mask the word cloud for the team abbreviations.  It was just a simple word cloud.

## Findings

### Net Rating Meaning
Net Rating is the offensive rating minus the defensive rating, but simply put it can be defined as how much better or worse the team is when a specific player is on the court. These ratings are usually on a per X possessions basis.

### Elo Rating Meaning and Formula
An elo rating is metric used to calculate the skill levels of players in various rating systems. It is regularly used in several competitive ranked leagues to determine the outcome of player vs. player or team vs. team matchups.

NBA Elo has a special calculation taking to consideration the unique aspects of the NBA. Factors such as a team being Home or Away and average League Elo Rating is taken into consideration.
![image](https://user-images.githubusercontent.com/101474440/218356966-c595a96f-fd28-4d32-9e24-40d554a09365.png)

### Most Games Played
![image](https://user-images.githubusercontent.com/101474440/218357144-8c2a01ba-751a-4f3a-957a-172f124798b6.png)

### Highest Averge Points per Game
![image](https://user-images.githubusercontent.com/101474440/218357179-967107b2-d97e-482f-9849-54a389c70cc0.png)

### Top Scorers
![image](https://user-images.githubusercontent.com/101474440/218357203-c89d0b9b-f86f-4d81-ad15-d1e850800bc4.png)

### Best Player Ratings in the NBA
![image](https://user-images.githubusercontent.com/101474440/218357235-79bd0c85-f8b7-4a23-95d7-8fbcb0c189b3.png)

## Elo Ratings

### 2016 - 2017
![image](https://user-images.githubusercontent.com/101474440/218357270-a28faba9-ccfe-4156-9515-1e4925fa4323.png)

### Translated Formula in Python
![image](https://user-images.githubusercontent.com/101474440/218357302-fd63a835-23aa-4274-a5f8-62eafb917280.png)

### 2017 - 2018
![image](https://user-images.githubusercontent.com/101474440/218357331-dae37d78-da4e-450e-9e2a-563a1ca6eaf0.png)

## Predictions
![image](https://user-images.githubusercontent.com/101474440/218357381-38f161c4-88a8-46cb-a81f-b6f39e31576c.png)

# Future Implementations
I would like to include being able to ask for user input and make this more of a usable app instead of just a data generating program.  I think there could be more done with the age analysis.  Finally, being able to find player salaries for each year and being able to do financial analysis would have been helpful.  Were the players worth the salaries paid? Are there players that should have been paid more?  I was also hoping to be able to break down stats by position but that was one piece of data missing from my dataset.  
