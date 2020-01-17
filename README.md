# Sudocool by team Flask Chained  

# Roster and Assignments
Jesse Hall (PM)

Ivan Galakhov
* Login/Database system
* Frontend Sudoku editor
* Frontend-Backend interaction
* Database design

Ayham Alnasser
* Sudoku puzzle generator
* Sudoku puzzle solver
* DB Initialization
* Video Maker

Hong Wei Chen
* Leaderboard functionality
* CSS design

# VIDEO
[Video Demo here](https://youtu.be/su9gPzbYzws)
# Project Overview
The classic logic game, Sudoku, in a portable website built with JavaScript. The puzzles are automatically generated in accordance with difficulty settings: easy, medium, hard, insane. Users can create an account to save finished puzzles and times or can play without an account. A set of weekly leaderboards is displayed on the page, ranking the users by the amount of time it took for them to finish the puzzle, differentiated by the difficulty setting. 

# Sounds like you'll do really well! what does this project use?

## Backend
* Server in python (flask)
* Flask-SQLalchemy
* Flask-WTForms
* Flask-Login

## Frontend
* Bootstrap
* Theme from [bootswatch](https://bootswatch.com/)
* jQuery (QaF post incoming)

# Wow! APIs?
* [Random Useless Facts API](https://uselessfacts.jsph.pl/) ([knowledge base document](https://docs.google.com/document/d/1AbBv9kVinKeExUQCl0Y3JHxyVVIjgmLV22VOxUb0Efo/edit)) which requires no API keys! The API will be used to give the user fun facts to look at while their sudoku puzzle is loading (which could take upwards of 30 seconds). 
* Our app also communicates internally with our own private API.

# Launch Codes 
1. Open Your Terminal and cd into the location of this project
2. Make sure you have [make](https://www.gnu.org/software/make/) installed (hint hint, you probably do)
2. Type: "pip install -r requirements.txt"
3. Then type: "make run"
4. Have fun playing sudoku!! 
5. Leave us 5 stars on the App Store or Google Play Store!
