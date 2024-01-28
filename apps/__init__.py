from flask import Blueprint

app = Blueprint('apps', __name__)

from .dbs import init_app,db,User,Futsal,Bookings

from . import index,session,booking
from . import staff,users,bookings,futsals

def init(main):
    init_app(main)