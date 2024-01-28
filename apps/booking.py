from flask import render_template,session,request,redirect
from flask_login import current_user, login_required
from datetime import date, timedelta, datetime, time
import json

from . import app,db,Futsal,Bookings,tools

from utils.closest_futsal import FutsalFinder
from utils.khalti import Khalti

@app.route('/book',methods=["GET"])
@login_required
def book():
    laltitude = float(request.args.get("x"))
    longitude = float(request.args.get("y"))
    futsals = Futsal.query.all()
    futsal_wdisance = []

    for f in futsals:
        f.distance = FutsalFinder.calc_dist(laltitude,longitude,float(f.laltitude),float(f.longitude))
        futsal_wdisance.append(f)
    futsal_wdisance.sort(key=lambda x: x.distance)
    futsal_wdisance = futsal_wdisance[:5]
    return render_template('book/book_futsal.html',futsals=futsal_wdisance,session=session)

@app.route('/register-futsal/',methods=["GET","POST"])
@login_required
def register_futsal():
    
    if request.method == "GET":
        return render_template('auth/register_futsal.html',session=session)
   

    data = request.form
    
    f = Futsal()
    f.name = data["name"]
    f.address = data["address"]
    f.laltitude = data["laltitude"]
    f.longitude = data["longitude"]
    f.contacts = data["contacts"]
    f.price = int(data["price"])
    f.weekend_price = int(data["weekend_price"])

    db.session.add(f)
    db.session.commit()

    return redirect("/admin")

@app.route('/book-futsal/<id>',methods=["GET"])
@login_required
def pick_date(id):
    futsal = Futsal.query.get(id)
    sdate = date.today()
    edate = sdate + timedelta(days=7)
    bookings = Bookings.query.filter_by(futsal_id=futsal.id).filter(Bookings.date.between(sdate,edate)).all()
    return render_template('book/pick_date.html',futsal=futsal, bookings=bookings)

@app.route('/pick-time/<id>/<year>/<month>/<day>/',methods=["GET"])
@login_required
def pick_time(id,year,month,day):
    futsal = Futsal.query.get(id)
    sdate = date(int(year),int(month),int(day))
    weekend= sdate.isoweekday() == 7
    edate = sdate + timedelta(days=1)
    bookings = Bookings.query.filter_by(futsal_id=futsal.id).filter(Bookings.date.between(sdate,edate)).all()
    final_bookings = []
    for b in bookings:
        final_bookings.append(b.time.strftime('%I%p'))
    futsal.date = date(int(year),int(month),int(day)).strftime("%A %B %d")
    return render_template('book/pick_time.html',futsal = futsal,weekend=weekend,bookings=json.dumps(dict(final_bookings=final_bookings)))

@app.route('/pick-time/<id>/<year>/<month>/<day>/pay/<time_str>',methods=["GET"])
@login_required
def pay(id,year,month,day,time_str):
    futsal = Futsal.query.get(id)
    year = int(year)
    month = int(month)
    day = int(day)
    weekend = date(year,month,day).isoweekday()
    
    booked_date = datetime(year,month,day)
    time_str = time_str.zfill(3) if len(time_str) == 3 else time_str
    parsed_time = datetime.strptime(time_str, '%I%p').time()
    combined_date = datetime.combine(booked_date,parsed_time)

    pid = f"{id}|{combined_date.isoformat()}"
    name = f"futsal{id}-{month}-{day}"
    pidx, url = Khalti.initiate_payment(futsal.get_price(weekend==7)*100,pid,name)
    return redirect(url)

@app.route('/payment-complete/',methods=["GET"])
@login_required
def payment_complete():
    pidx = request.args.get("pidx")
    pid = request.args.get("purchase_order_id")

    parse_pid = pid.split("|")
    futsal = Futsal.query.get(parse_pid[0])
    booked_date = datetime.fromisoformat(parse_pid[1])

    booking_instance = Bookings(
        futsal_id=futsal.id,
        user_id=current_user.id,
        date=booked_date.date(),
        time=time(booked_date.time().hour),
        cost=futsal.get_price(booked_date.isoweekday()==7),
        status='Confirmed'
    )
    db.session.add(booking_instance)
    db.session.commit()
    
    resp = Khalti.verify_payment(pidx)
    if resp.get("success"):
        return render_template('book/success.html',futsal=futsal,booked_date=booked_date.strftime('%A %B %d, %I:%M %p'))
    else:
        return redirect("/")

@app.route('/admin/',methods=["GET"])
@login_required
def admin():
    sdate = datetime.utcnow()
    end_date =  sdate + timedelta(days=7)
    total_booking = Bookings.query.filter(Bookings.date.between(sdate,end_date))
    total_booking_count = total_booking.count()
    total_earned = 23000
    tot_fut = len(Futsal.query.all())

    recent_booking = Bookings.query.filter().all()
    upcoming_booking = Bookings.query.filter(Bookings.date > sdate).all()
    return render_template('admin/admin.html',total_booking_count=total_booking_count,total_earned=total_earned,tot_fut=tot_fut,recent_booking=recent_booking,upcoming_booking=upcoming_booking)
