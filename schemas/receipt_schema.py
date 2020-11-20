from flask_marshmallow import Marshmallow

ma = Marshmallow()


class ReceiptSchema(ma.Schema):
    class Meta:
        fields = ("number", "amount", "received", "provider_id")


receipt_schema = ReceiptSchema()
receipts_schema = ReceiptSchema(many=True)
