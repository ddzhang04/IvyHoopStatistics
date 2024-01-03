import requests
import pandas as pd
from cs50 import SQL
from bs4 import BeautifulSoup
import sqlite3


db = SQL("sqlite:///ncaa.db")


# Get the standings for a given year
def standings(year):
  connection = sqlite3.connect('ncaa.db')
  url = "https://www.sports-reference.com/cbb/conferences/ivy/men/{}.html#all_polls"
  placeholder = year
  formatted_url = url.format(placeholder)

  # Read HTML tables from the specified URL
  data_frame = pd.read_html(formatted_url, skiprows=0)
  standings_table = data_frame[0]
  school_stats_table = data_frame[2]

  year_rankings = "ranking" + str(placeholder)
  # dynamically name each year's table
  standings_table.columns = [
      "Rank", "School", "ConfWin", "ConfLoss", "ConfWL", "OvWin", "OvLoss",
      "OvWL", "Own", "Opp", "Srs", "Sos", "Notes"
  ]
  standings_table.to_sql(year_rankings, con=connection, if_exists='replace')

  return standings_table

# Get the roster for a given school and year.
def ivyTeams(school, year):
  connection = sqlite3.connect('ncaa.db')
  url = "https://www.sports-reference.com/cbb/schools/{}/men/{}.html"
  placeholder1 = school
  placeholder2 = year
  formatted_url_team = url.format(placeholder1, placeholder2)

  # Read HTML tables from the specified URL
  data_frame_team = pd.read_html(formatted_url_team)

  roster = data_frame_team[0]

  year_teams = "team" + str(placeholder1) + str(placeholder2)

  # dynamically name each year's table
  roster.to_sql(year_teams, con=connection, if_exists='replace')

  return roster


# Get the ivy league schedule for a year
def ivySchedule(year):
  connection = sqlite3.connect('ncaa.db')
  url = "https://www.sports-reference.com/cbb/conferences/ivy/men/{}-schedule.html"
  placeholder = year
  formatted_url_schedule = url.format(placeholder)

  # read HTML from the URL
  data_frame_schedule = pd.read_html(formatted_url_schedule)
  # Assuming the schedule is the first data frame
  schedule = data_frame_schedule[0]

  year_schedule = "schedule" + str(placeholder)

  # Dynamically name each year's table
  schedule.to_sql(year_schedule, con=connection, if_exists='replace')


def getNews():

    connection = sqlite3.connect('ncaa.db')
    url = "https://www.foxsports.com/college-basketball/ivy-league"

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all relevant <a> tags
        article_links = soup.find_all('a', class_='article-container news')

        # Limit the number of articles to scrape (e.g., the first 5)
        num_articles_to_scrape = 5

        # Create a list to store the data
        articles_data = []

        for article_link in article_links[:num_articles_to_scrape]:
            link = article_link['href']
            article_title = article_link.find('h3', class_='article-title').text.strip()
            article_description = article_link.find('span', class_='ff-h fs-xl-14 fs-13 lh-1pt43 cl-gr-7 article-description').text.strip() if article_link.find('span', class_='ff-h fs-xl-14 fs-13 lh-1pt43 cl-gr-7 article-description') else "Additional information not found"

            # Append the data to the list
            articles_data.append([link, article_title, article_description])

        # Convert the list to a DataFrame
        df = pd.DataFrame(articles_data, columns=['link', 'title', 'description'])

        # Connect to SQLite database and insert data

        df.to_sql('articles', con=connection, if_exists='replace')


