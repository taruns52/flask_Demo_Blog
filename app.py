from flask import Flask, redirect, render_template, request, url_for
from database import db
 
# Creating Flask App
app = Flask(__name__)
# Database Name
db_name = 'vehicle.db'
 
# Configuring SQLite Database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
 
# Suppresses warning while tracking modifications
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 
# Initialising SQLAlchemy with Flask App
db.init_app(app)


""" Creating Database with App Context"""
def create_db():
    with app.app_context():
        db.create_all()

@app.route("/")
def home():
    details = Vehicle.query.all()
    return render_template("home.html", details=details)

@app.route("/add-vehicle", methods=['GET', 'POST'])
def add_vehicle():
    if request.method == "POST":
        v_name = request.form.get('vehicle')
        price = request.form.get('price')

        add_detail = Vehicle(
            name=v_name,
            price=price
        ) 

        db.session.add(add_detail)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('vehicle.html')

@app.route("/update-vehicle-price/<id>", methods=['POST', 'GET'])
def update_vehicle_price(id):
    if request.method=='POST':
        vehicle = Vehicle.query.filter_by(id = id).first()

        new_price = request.form.get('new_price')

        vehicle.price = new_price

        db.session.commit()
        return redirect("/")
    print('id', id)
    vehicle = Vehicle.query.filter_by(id = id).first()
    print('Vehicle to be Updated', vehicle)
    return render_template('update_vehicle_price.html', vehicle=vehicle)
 
if __name__ == "__main__":
    from models import Vehicle
    create_db()
    app.run(debug=True)