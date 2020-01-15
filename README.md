# Sudocool by team Flask Chained  

# Roster and Assignments
Jesse Hall (PM)

Ivan Galakhov
* Login/Database system [done]
* Frontend Sudoku editor [in progress]
* Frontend-Backend interaction

Ayham Alnasser
* Sudoku puzzle generator [done]
* Sudoku puzzle solver [done]
* Backend DB [done]

Hong Wei Chen
* Leaderboard functionality
* CSS design


# Project Overview
The classic logic game, Sudoku, in a portable website built with JavaScript. The puzzles are automatically generated in accordance with difficulty settings: easy, medium, hard, killer. Users can create an account to save finished puzzles and times or can play without an account. A set of weekly leaderboards is displayed on the page, ranking the users by the amount of time it took for them to finish the puzzle, differentiated by the difficulty setting. If the user is stuck, they can request hints, with a certain penalty being added to their time setting. We would also like to add functionality to allow users to export PDFs into various forms, and maybe even have them emailed to the user if necessarry. 

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
* [Random Useless Facts API](https://uselessfacts.jsph.pl/) which requires no API keys! The API will be used to give the user fun facts to look at while their sudoku puzzle is loading (which could take upwards of 30 seconds). 


# Launch Codes 
1. Open Your Terminal and cd into the location of this project
2. Make sure you have [make](https://www.gnu.org/software/make/) installed (hint hint, you probably do)
2. Type: "pip install -r requirements.txt"
3. Then type: "make run"
4. Have fun playing sudoku!! 
5. Leave us 5 stars on the App Store or Google Play Store!
