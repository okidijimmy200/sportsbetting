from flask_injector import FlaskInjector
from injector import inject, singleton
from flask import Flask, request
from interface import SportsBettingInterface
from dbsystems.mysqlsystem import MYSQLDBSystem
from dbconfig import SessionLocal


app = Flask(__name__) 
db = SessionLocal()

class SportsBettingApp:
    @inject
    def __init__(self,  db_service_provider: SportsBettingInterface) -> None:
        self.db = db_service_provider

    def create(self, body):
        try:
            created, reason, status = self.db.create(body)
            if not created:
                print(reason)
                return False, reason, status
            return True, reason, status
        except Exception as e:
            result = (
                f"-Error "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            return result

    def read(self, body):
        try:
            result, reason, status = self.db.read(body)
            if not result:
                print(reason)
                return False, reason, status
            return True, reason, status
        except Exception as e:
            result = (
                f"-Error "
                + f"{type(e).__name__} {str(e)}"
            )
            print(result)
            return result

def configure(binder):
    binder.bind(SportsBettingApp, to=SportsBettingApp, scope=singleton)
    binder.bind(SportsBettingInterface, to=MYSQLDBSystem(db), scope=singleton)


@inject
@app.route('/createbet', methods=['POST'])
def create_item(service: SportsBettingApp):
    try:
        body = request.get_json()
        Boolean, response, status = service.create(body)
        print(response)
        return {
            "Boolean": Boolean,
            "msg": response,
            "status": status
        }
    except Exception as e:
        result = (
                f"-Error "
                + f"{type(e).__name__} {str(e)}"
            )
        print(result)
        return result

@inject
@app.route('/readbet', methods=['GET'])
def read_item(service: SportsBettingApp):
    try:
        data = {
            "league": f"{request.args.to_dict()['league']}",
            "start_date": f"{request.args.to_dict()['start_date']}",
            "end_date": f"{request.args.to_dict()['end_date']}"
        }
        Boolean, response, status = service.read(data)
        return {
            "Boolean": Boolean,
            "data": response,
            "status": status
        }
    except Exception as e:
        result = (
                f"-Error "
                + f"{type(e).__name__} {str(e)}"
            )
        print(result)
        return result

FlaskInjector(app=app, modules=[configure])




if __name__ == '__main__':
    app.run(debug=True)