from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Skolotajs(db.Model):
    __tablename__ = 'skolotaji'
    id = db.Column(db.Integer, primary_key=True)
    vards = db.Column(db.String(100), nullable=False)
    uzvards = db.Column(db.String(100), nullable=False)
    epasts = db.Column(db.String(120), unique=True, nullable=False)

    lietojumi = db.relationship('Lietojums', back_populates='skolotajs')

    def __repr__(self):
        return f"{self.vards} {self.uzvards}"


class Dators(db.Model):
    __tablename__ = 'datori'
    id = db.Column(db.Integer, primary_key=True)
    nosaukums = db.Column(db.String(100), nullable=False)
    statuss = db.Column(db.String(20), default='pieejams')

    lietojumi = db.relationship('Lietojums', back_populates='dators')

    def __repr__(self):
        return f"{self.nosaukums} ({self.statuss})"


class Lietojums(db.Model):
    __tablename__ = 'lietojumi'
    id = db.Column(db.Integer, primary_key=True)
    dators_id = db.Column(db.Integer, db.ForeignKey('datori.id'), nullable=False)
    skolotajs_id = db.Column(db.Integer, db.ForeignKey('skolotaji.id'), nullable=False)
    sakums = db.Column(db.DateTime, default=datetime.utcnow)
    beigas = db.Column(db.DateTime, nullable=True)

    dators = db.relationship('Dators', back_populates='lietojumi')
    skolotajs = db.relationship('Skolotajs', back_populates='lietojumi')

    def __repr__(self):
        return f"Lietojums: {self.dators.nosaukums} - {self.skolotajs.vards}"
