import datetime, pytest
from dbsystems.mysqlsystem import MYSQLDBSystem
from sqlalchemy import create_engine
from sqlalchemy.types import Date
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Table, Column, Integer, String, Float, DateTime


@pytest.fixture(scope='function')
def db_session():
    """Session for SQLAlchemy."""
    Base = declarative_base()  
    meta = Base.metadata
    engine = create_engine('sqlite://')
    Table('bettingmodel', meta, Column('id',Integer, primary_key=True, index=True), 
    Column('league',String(100), index=True),
    Column('home_team',String(100), index=True),
    Column('away_team',String(100), index=True),
    Column('home_team_win_odds',Float, index=True),
    Column('away_team_win_odds',Float, index=True),
    Column('draw_odds',Float, index=True),
    Column('game_date',Date, index=True),
    )
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create(db_session):
    data = {"league": "primier league", "home_team": "man u", "away_team": "arsenal", "home_team_win_odds": 2.0, "away_team_win_odds": 1.2, "draw_odds":2, "game_date": datetime.date(2022, 10, 10)}
    data_2 = {"league": "primier league", "home_team": "man u", "away_team": "arsenal", "home_team_win_odds": 2.0, "away_team_win_odds": 1.2, "draw_odds":2, "game_date": 2022-10-10}
    test_cases = [
        {
            "name": "pass",
            "input": data,
            "output": (True, "Data stored successfully in MYSQL db", 201)
        },
        {
            "name": "fail",
            "input": data_2,
            "output": (False, "-Failed to store data in MYSQL DB", 404)
        }
    ]    
    for test_case in test_cases:
        result = MYSQLDBSystem(db_session).create(test_case["input"])
        assert result == test_case["output"]

def test_read(db_session):
    data = {
        'league': 'premier league', 'start_date': "2022-03-12", "end_date": "2022-12-12"
    }
    data_2 = {
        'league': 'la liga', 'start_date': "2022-10-8", "end_date": "2022-10-12"
    }
    create = {"league": "premier league", "home_team": "man u", "away_team": "arsenal", "home_team_win_odds": 2.0, "away_team_win_odds": 1.2, "draw_odds":2, "game_date": datetime.date(2022, 10, 10)}
    test_cases = [
    {
            "name": "pass",
            "input": data,
            "create": create,
            "output": (True, [{'home_team': 'man u', 'league': 'premier league', 'game_date': '2022-10-10', 'draw_odds': 2.0, 'away_team': 'arsenal', 'id': '1', 'home_team_win_odds': 2.0, 'away_team_win_odds': 1.2}], 200)
        },
        {
            "name": "fail",
            "input": data_2,
            "create": create,
            "output": (False, 'Data not found', 403)
        },
        {
            "name": "error",
            "input": '',
            "create": create,
            "output": (False, '-Failed to read data from db', 500)
        }
    ]
    for test_case in test_cases:
        MYSQLDBSystem(db_session).create(test_case["create"])
        result = MYSQLDBSystem(db_session).read(test_case["input"])
        assert result == test_case["output"]