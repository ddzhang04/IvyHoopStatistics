INTRODUCTION:
Ivy Hoops Statistics is a website that provides information on the current and past Ivy League basketball seasons and teams. 

Video Link: https://youtu.be/SnUdyPg4ciM 

DEPENDENCIES:
The packages used:
 cs50:
Flask:
flask _session
werkzeug.security
datetime
requests
beautifulsoup4
pandas
sqlite3

WEBSITES SCRAPED:
https://www.sports-reference.com/cbb/
Sports-reference is a website that provides information on various sports leagues. This was used for Basketball Statistics to get the Ivy League schedule, standings, and team rosters.

https://www.foxsports.com/college-basketball/ivy-league
Fox Sports is a website that provides news and other information about Ivy League college basketball.  This website was used in order to get the most recent news.
HOW TO RUN:
Import the zip file into cs50.dev
Unzip the zip file
Flask run 

HOW TO USE:
For our project, we developed a webpage called Ivy Hoops Insights. We made a webpage that is easily navigable from any tab using the navbar implementation from Bootstrap. By using the different buttons in the navbar to navigate to various tabs in our webpage, the user is able to view Ivy League basketball standings for this year and past years, schedule for the current season, teams including roster for this season and past, recent news articles, convenient way to buy tickets within the webpage, and a tab to follow the users favorite teams. In each of the subpages, there is a large jumbotron, implemented from Bootstrap, explaining the premise of each subpage. Additionally, the navbar is displayed in the homepage as well as all of the subpages so the user can toggle between different pages within the webpage seamlessly. 

The user may access the homepage from the navbar by either clicking on the Ivy League athletics logo at the top left of the page or the title, “Ivy Hoops Insights.” The user is greeted by a large jumbotron explaining the purpose of our website. Scrolling down, the user can view this current year’s standings and the schedule for the next upcoming 5 games in the Ivy League. In the right column of the homepage, the user can easily access recent articles about various Ivy League teams by clicking the button, “Read More”.   

In the standings subpage, the user is directed to a subpage featuring this season's current standings. The user can access this from the navbar by selecting “Standings.” Depending on the time of year, there may or may not be differing standings if the teams have not yet started their season. In this page, a visual table of the standings among the Men’s Basketball teams in the Ivy League are displayed. The table features rank, school, conference win, conference loss, conference win/loss percentage, overall win, overall loss, overall win loss percentage, own points per game, opponent points per game, simple rating system, strength of schedule, and any notes. As the season progresses and games are completed, the standings will be updated accordingly. Additionally, in the tab, the user is able to search to view past year’s standings. By entering a valid year in the format YYYY, the standings table will display the according year. The only exception for the standings table is the year 2021, since the basketball season was canceled due to the COVID19 pandemic. To handle this case, if the user inputs 2021, the webpage will display an apology page. 

In the schedule subpage, the user is able to view the entire season’s schedule and the results from that game. This includes all the games where Ivy League teams are playing against each other for the current season. The schedule is displayed in a visually appealing table with different columns including the date of the game, visiting team, points scored by visiting team, home team, points scored by home team, overtime, and any notes from the game. By placing all these statistics from each game in an easy to read table, the user is able to quickly view a brief numerical summary of each game. 

When the user navigates to the team subpage from the navbar by selecting “Teams,” they are directed to the Teams subpage. If users have a registered account and are logged in, they are able to follow a team by clicking the “Follow” button on the top right corner of the image of each school. If users no longer wish to follow a certain team, they can simply click the “Following” button again to unfollow. 

Furthermore, each of the images are a button themselves, directing the user to the roster of each team. Although when clicked, the default displays the current season’s roster in a table format, the user is able to search with the format YYYY to view past year’s team rosters as well. For each player in the roster, the columns simply display the player’s name, jersey number, class, position, height, weight, hometown, high school, RSCI TOP 100, and a statistical summary. By placing all this information about various players from each school in a table, the user is able to easily find their favorite player on the roster from a particular year and learn new information about them in one place. 

The user can navigate to the news subpage from the navbar by selecting “News” from any other webpage or the homepage. In this page, users can view the latest news articles about Ivy League Basketball. These articles will constantly change and always have the latest news. This page displays the title of the article as well as a brief headline so the user can get an idea of what the article is about. If the user would like to view the article, they can navigate to the article by using the button, “Read More.” 

The user can navigate to the tickets subpage using the navbar by selecting “Tickets.” In this subpage, the user is able to view the Ivy League Team they would like to see in action. Using the Bootstrap accordion feature, users can dropdown their favorite team by selecting the particular accordion. From there, the webpage displays a frame of the SeatGeek website where the user should buy their ticket. By using an iframe, the user doesn't have to find the SeatGeek website but can buy their tickets directly from this section in the Ivy Hoops Insights webpage. 

In order to view the “Your Teams” subpage, the user navigates there through the navbar. To view the “Your Teams” subpage, users must be logged in. When users are logged in, they are able to see all the teams they have followed. Users have the ability to follow their favorite teams and they can also choose to stop following any teams they no longer wish to track. When they follow a team, they are able to see the next three upcoming games against other Ivy League teams in the “Your Teams" subpage. 

Lastly, if the user is logged in, they will be able to easily logout using the “Log Out” button in the navbar. When the user clicks this button the session is cleared and the user can either continue using the website as a visitor or log in again. 

If a user is not logged in, they can still access many features of the webpage including the subpages standings, schedule, teams, news and tickets. They must be logged in to view “Your Teams.” 

A new user, if they wish to, may register an account. By selecting register, users can easily create an account with Ivy Hoops Insights by creating a username and password. From there they will automatically be logged in and can start following their favorite Ivy League teams. 


CODE DOCUMENTATION:
HELPERS.PY:

standings(year):
- This function takes a year as the parameter and creates a sql table for the Ivy League standings associated with that year

ivyTeams(schools, year):
- This function takes a year and school as the parameter and creates a sql table for the roster of the school that was passed in for the year that was passed in.

getNews():
- This function scrapes “https://www.foxsports.com/college-basketball/ivy-league” and gets the title, description and link of the first five news articles.
MAIN.PY:

home():
- This function gets the standings of the current year, schedule and news and renders them on the homepage template.

login():
-  This function works so that if the request method is get, render the login template and if the method was post, log out the user, then check all login fields and if successful, redirect to homepage, or else return an apology.

logout():
- This function clears the session id and redirects to the homepage

standingsIvy(year):
- This function gets the Ivy League standings for the parameter year passed in and renders the standings template. On first call this will be the current year.

schedule():
- This function renders the schedule template with the schedule of the current year.

roster(school, year):
- This function renders the roster template with the roster information for a school in a specific year. On first call this will be the current year.

team():
- This function renders the team template.

news():
- This function renders the news template with the updated news information.

tickets():
- This function renders the page to buy tickets.

yourTeams():
- If the user is not logged in, the function returns the user back to the login page. If the user is logged in, display the information associated with the teams that this user follows.

TEMPLATES:


layout.html:
- This template is the basic layout of the website. It contains a navigation bar with the different options based on if the user is logged in or not.

login.html: 
- Jinja template for the login page that contains a field for the username, a field for the password, and a button to submit the inputted username and password.

home.html:
-  Jinja template for the home page. This contains a jumbotron with a background image and text. It also contains a section with the current standings and abridged schedule and a sidebar containing recent news.

news.html:
-  Base Jinja template for ivy League news. This template contains five buttons formatted with the article title, description, and a button that redirects to the actual article.

newsMain.html:
-  Jinja template for the news page. This includes the news.html and renders it in the layout.html format.

register.html:
- Jinja template for the login page that contains a field for the username, a field for the password, a field for confirmation password  and a button to submit the inputted username, password,  and confirmation password.

roster.html:
- Jinja template for the team roster pages that display the roster information of a team in a table. This template also includes a search bar that on search redirects to the roster page based on the year inputted through the script component on submission prevents empty search and calls the redirectToYear function
  - redirectToYear():
    - Takes the year input from the searchbar and then of the year is a valid year,
       redirect to the link that displays the roster information of that school of that the
       inputted year.
    -  Handles the case where the year is 2021 due to the covid 19 cancellation and 
        redirects to the special case template.

schedule.html:
- Jinja template for abridged version of the schedule. Used for rendering in the home page as an inclusion.

scheduleMain.html:
- Jinja template for the main schedule page. Displays a table of the schedule information from the information passed to it when rendering.

standingsIvy.html:
- Jinja template for an abridged version of the standings. Used for rendering in the home page as an inclusion.

standingsMain.html:
- Jinja template for the standings pages that display the standings of the Ivy League Mens’ Basketball conference for a given year. This template also includes a search bar that on search redirects to the roster page based on the year inputted through the script component on submission prevents empty search and calls the redirectToYear function
  - redirectToYear():
    - Takes the year input from the searchbar and then of the year is a valid year,
       redirect to the link that displays the standings for that given year.
    -  Handles the case where the year is 2021 due to the covid 19 cancellation and 
        redirects to the special case template.

team.html:
-  Jinja template that displays 8 buttons, one for each Ivy League team. When the button is clicked, the roster page for the corresponding team in the current year is displayed.

tickets.html:
- Jinja template that displays an accordion table that contains the ticketing site as an iframe for each team.










