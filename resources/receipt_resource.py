from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from models.receipt_model import Receipt
from db import db
from schemas.receipt_schema import receipt_schema, receipts_schema


class ReceiptResource(Resource):
    def get(self, number):
        try:
            _receipt = Receipt.query.filter_by(number=number).one()
            return {"receipt": receipt_schema.dump(_receipt)}
        except NoResultFound:
            return {"receipt": None}, 404

    def post(self, number):
        if Receipt.query.filter_by(number=number).count():
            return {"message": "Receipt with number={number} already exists"}, 400

        data = request.get_json()
        new_receipt = Receipt(
            number=number,
            amount=data["service_type"],
        )
        try:
            db.session.add(new_receipt)
            db.session.commit()
            return {"receipt": receipt_schema.dump(new_receipt)}
        except IntegrityError as exc:
            return {"message": str(exc)}

    def put(self, number):
        data = request.get_json()
        try:
            _receipt = Receipt.query.filter_by(number=number).one()
            _receipt.amount = data["amount"]
            return {"message": "Receipt updated"}
        except NoResultFound:
            new_receipt = Receipt(
                number=number,
                amount=data["amount"],
            )
            db.session.add(new_receipt)
            db.session.commit()
            return {"receipt": receipt_schema.dump(new_receipt)}, 201

    def delete(self, number):
        try:
            _receipt = Receipt.query.filter_by(number=number).one()
            db.session.delete(_receipt)
            db.session.commit()
            return {"message": "Receipt Deleted"}
        except NoResultFound:
            return {"message": f"Receipt with number={number} does not exist"}, 400


class ReceiptListResource(Resource):
    def get(self):
        return {"receipts": receipts_schema.dump(Receipt.query.all())}
