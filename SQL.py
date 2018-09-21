import sqlite3

name = 'jamie'
score = 240

db = sqlite3.connect('scoreboard.db')
cursor = db.cursor()
def create_table():
    cursor.execute('CREATE TABLE Leaderboard(name string, score integer)')
    db.commit()

def add_score(Username, Userscore):
    cursor.execute('INSERT INTO Leaderboard(name, score) VALUES(?,?)',(Username, Userscore))

def display_table():
    cursor.execute('SELECT * FROM Leaderboard')
    for item in cursor:
        print(item)


