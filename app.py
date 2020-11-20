import os
from flask import Flask
from flask_restful import Api

from resources.receipt_resource import ReceiptListResource, ReceiptResource

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL", os.environ.get("SQLALCHEMY_DATABASE_URI")
)
SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")


def create_app():
    _app = Flask(__name__)
    _app.config["DEBUG"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    _app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    _app.config["RECEIPTS_URL"] = os.environ.get("RECEIPTS_URL")
    api = Api(_app)

    api.add_resource(ReceiptResource, "/receipt/<string:uniq_str>")
    api.add_resource(ReceiptListResource, "/receipts")

    @_app.route("/index")
    @_app.route("/")
    def index():  # pylint: disable=unused-variable
        return "Welcome to Receipts App"

    return _app


if __name__ == "__main__":

    from db import db
    from schemas.receipt_schema import ma

    app = create_app()
    db.init_app(app)
    with app.app_context():
        db.create_all()

    ma.init_app(app)
    app.run(port=os.environ.get("RECEIPTS_PORT"), debug=True)
