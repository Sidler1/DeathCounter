import os

from flask import Flask
from sqlalchemy import Column, Integer, String, create_engine, insert
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///deathcounter.db'
engine = create_engine('sqlite:///deathcounter.db', echo=True, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


@app.route('/')
def index():
    return 'Pew, Pew Motherfucker!'


@app.route('/create/user/<username>')
def createuser(username: str):
    user = session.query(f'id FROM users WHERE username="' + username + '"').first()
    if user:
        return f'{username} ist bereits angelegt mit der id: {user[0]}.'
    session.add(User(username=username))
    session.commit()
    user = session.query(f'id FROM users WHERE username="' + username + '"').first()
    return f'ok {username} wurde angelegt mit der id: {user[0]}.'


@app.route('/create/game/<gamename>')
def creategame(gamename: str):
    game = session.query(f'id FROM games WHERE game="' + gamename + '"').first()
    if game:
        return f'{gamename} ist bereits angelegt mit der id: {game[0]}.'
    session.add(Games(game=gamename))
    session.commit()
    game = session.query(f'id FROM games WHERE game="' + gamename + '"').first()
    return f'ok {gamename} wurde angelegt mit der id: {game[0]}.'


@app.route('/create/counter/<uid>/<gid>')
def createcounter(uid: int, gid: int):
    game = session.query(f'game FROM games WHERE id=' + str(gid) + '')
    user = session.query(f'username FROM users WHERE id=' + str(uid) + '')
    if game and user:
        return "Beides da ... alles gut :D"
        # session.add(Counter(userid=uid, gameid=gid))


@app.route('/getDC/<user>/<game>')
def deathcounter(user: str, game: int):
    pass


class User(Base):
    """Model for user accounts."""
    __tablename__ = 'users'

    id = Column(Integer,
                primary_key=True)
    username = Column(String,
                      nullable=False,
                      unique=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Games(Base):
    __tablename__ = 'games'
    id = Column(Integer,
                primary_key=True)
    game = Column(String, nullable=False, unique=True)

    def __repr__(self):
        return '<Spiel {}>'.format(self.game)


class Counter(Base):
    __tablename__ = 'counter'
    id = Column(Integer,
                primary_key=True, autoincrement=True)
    userid = Column(Integer, nullable=False, default=0)
    gameid = Column(Integer, nullable=False, default=0)
    counter = Column(Integer, nullable=False, default=0)


if __name__ == '__main__':
    app.run()
