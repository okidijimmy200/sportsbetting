from models.models import BettingModel
from interface import SportsBettingInterface
from dbconfig import Base, engine
from models.models import BettingSchema

class MYSQLDBSystem(SportsBettingInterface):
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db

    def connect(self):
        return super().connect()

    def disconnect(self):
        return super().disconnect()

    def create(self, data):
        try:
            print("Create data")
            Base.metadata.create_all(engine)
            new_data = BettingModel(**data)
            self.db.add(new_data)
            self.db.commit()
            print("data stored in db")
            result = 'Data stored successfully in MYSQL db'
            return True, result, 201
        except Exception as e:
            result = (
                f"-Failed to store data in MYSQL DB, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            reason = '-Failed to store data in MYSQL DB'
            return False, reason, 404

    def read(self, data):
        try:
            schema = BettingSchema()
            q = self.db.query(BettingModel).filter(BettingModel.league == data['league'], BettingModel.game_date.between(data['start_date'], data['end_date'])).first()
            print(q)
            reason = schema.dump([q], many=True)
            if q is None:
                return False, 'Data not found', 403
            return True,reason,200
        except Exception as e:
            result = (
                f"-Failed to store data in MYSQL DB, reason: "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            reason = '-Failed to read data from db'
            return False, reason, 500




