from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.types import Date
from marshmallow import Schema, fields
from dbconfig import Base

'''betmodel class'''
class BettingModel(Base):
    __tablename__ = 'bettingmodel'

    id = Column(Integer, primary_key=True, index=True)
    league = Column(String(80), nullable=False)
    home_team = Column(String(80), nullable=False) 
    away_team =Column(String(80), nullable=False)
    home_team_win_odds = Column(Float, nullable=False)
    away_team_win_odds = Column(Float, nullable=False)
    draw_odds = Column(Float, nullable=False)
    game_date = Column(Date)

    def __repr__(self):
        return 'id: {}, league: {}, home_team: {}, away_team: {}, home_team_win_odds: {}, away_team_win_odds: {},draw_odds: {}, game_date: {}'.format(
            self.id, 
            self.league,
            self.home_team,
            self.away_team,
            self.home_team_win_odds,
            self.away_team_win_odds,
            self.draw_odds,
            self.game_date)

'''betmodel schema to serialize objects to json'''
class BettingSchema(Schema):
    id = fields.Str()
    league = fields.Str()
    home_team = fields.Str()
    away_team = fields.Str()
    home_team_win_odds = fields.Float()
    away_team_win_odds = fields.Float()
    draw_odds = fields.Float()
    game_date = fields.Date()