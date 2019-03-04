import sqlite3

db = sqlite3.connect('scoreboard.db')
cursor = db.cursor()
scores = []

def create_table():
    cursor.execute('CREATE TABLE Leaderboard(name TEXT, score INTEGER)')
    db.commit()

def add_score(Username, Userscore):
    cursor.execute('INSERT INTO Leaderboard(name, score) VALUES(?,?)',(Username, Userscore))
    db.commit()



def display_table():
    cursor.execute('SELECT * FROM Leaderboard ORDER BY score DESC')

    for item in cursor:
        scores.append(item)
    #print(scores)
    return(scores)

def reset_leaderboard():
    cursor.execute('DELETE FROM Leaderboard')
    scores = []




