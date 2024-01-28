from . import db,User,Futsal,Bookings
from utils.closest_futsal import FutsalFinder
from datetime import datetime,timedelta

startTime=8
endTime=21
open_times = [i for i in range(startTime, endTime)]

locked=[]


def refund():
    pass

def getFutsals(location):
    futsals = Futsal.query.all()
    # sort and filter here
    return futsals

def getOpenDays(futsal):
    days = [(datetime.now().date() + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(8)]
    openDays=[]

    for day in days:
        bookings = Bookings.query.filter_by(futsal_id=futsal,date=day).all()
        times=open_times.copy()
        for booking in bookings:
            times.remove(booking.time)
        if times:
            openDays.append(day)
    return openDays

def getOpenTimes(futsal,date):
    times = open_times.copy()
    bookings= Bookings.query.filter_by(futsal_id=futsal,date=date).all()
    
    for booking in bookings:
        times.remove(booking.time)
    
    return times


def canBook(id,futsal,date,time):
    for item in locked.copy():
        futsal_,date_,time_,c_=item
        if (date.now()-c_)>=timedelta(minutes=5):
            locked.remove(item)
            continue
        if (futsal,date,time) == (futsal_,date_,time_):
            return False
    return True

def book(futsal,user,date,time):
    for item in locked.copy():
        futsal_,date_,time_,c_=item
        if (futsal,date,time) == (futsal_,date_,time_):
            locked.remove(item)
    booking = Bookings(
        futsal_id=futsal,
        user_id = user,
        date=date,
        time=time
    )
    db.session.add(booking)
    db.commit()
