import datetime
from api.models.__init__ import db


class ScrapperBooks(db.Model):
    '''Modelo de dados para a tabela de Books.'''
    __tablename__ = 'scrapper_books'
    id              = db.Column(db.Integer, primary_key=True)
    title           = db.Column(db.String(120), nullable=False)
    genre           = db.Column(db.String(80), nullable=False)
    price           = db.Column(db.Float, nullable=False) 
    availability    = db.Column(db.Integer, nullable=False)
    rating          = db.Column(db.String(20), nullable=False)
    upc             = db.Column(db.String(100), nullable=False)
    description     = db.Column(db.Text, nullable=False)
    url             = db.Column(db.String(200), nullable=False)
    product_type    = db.Column(db.String(15), nullable=False)
    price_excl_tax  = db.Column(db.Float, nullable=False)
    price_incl_tax   = db.Column(db.Float, nullable=False)
    tax             = db.Column(db.Float, nullable=False)
    number_of_reviews  = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f'<Title {self.title}>'
