from flask import Flask, flash, redirect, render_template, request, typing as ft, url_for
from flask.views import MethodView, View
from database import db
from models import Vehicle

# Creating Flask App
app = Flask(__name__)


# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

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



# class VehicleView(View):
#     def dispatch_request(self, id=None):
#         if request.method == "GET":
#             if id is None:
#                 # Read all vehicle
#                 vehicles = Vehicle.query.all()
#                 print("GET Request Without ID ", request.args.get('id'))
#                 return render_template("home.html", details=vehicles)
#             else:
#                 # Read one vehicle by id
#                 print("GET Request With ID ", request.args.get('id'))
#                 vehicle = Vehicle.query.get_or_404(id)
#                 return render_template("update_vehicle_price.html", vehicle=vehicle)
#         elif request.method == "POST":
#             if id is None:
#                 # Create a new vehicle
#                 name = request.form.get("name")
#                 price = request.form.get("price")
#                 vehicle = Vehicle(name=name, price=price)
#                 db.session.add(vehicle)
#                 db.session.commit()
#                 return redirect(url_for("home"))
#             else:
#                 # Update an existing user by id
#                 user = Vehicle.query.get_or_404(id)
#                 price = request.form.get("new_price")
#                 user.price = price
#                 db.session.commit()
#                 return redirect(url_for("home"))
#         elif request.method == "DELETE":
#             if id is not None:
#                 # Delete an existing user by id
#                 vehicle = Vehicle.query.get_or_404(id)
#                 db.session.delete(vehicle)
#                 db.session.commit()
#             return redirect(url_for("home"))
        
# app.add_url_rule("/",view_func=VehicleView.as_view('home'))
# app.add_url_rule("/add-vehicle",view_func=VehicleView.as_view('add_vehicle'))
# app.add_url_rule("/update-vehicle",view_func=VehicleView.as_view('update_vehicle_price'))
# app.add_url_rule("/delete-vehicle",view_func=VehicleView.as_view('delete_vehicle'))

class Home(MethodView):
    def get(self):
        details = Vehicle.query.all()
        return render_template("home.html", details=details)

app.add_url_rule('/', view_func=Home.as_view('home'))

class AddVehicle(MethodView):
    def get(self):
        return render_template('vehicle.html')
    
    def post(self):
        v_name = request.form.get('vehicle')
        price = request.form.get('price')

        add_detail = Vehicle(
            name=v_name,
            price=price
        ) 

        db.session.add(add_detail)
        db.session.commit()
        return redirect(url_for('home'))

app.add_url_rule("/add-vehicle",view_func=AddVehicle.as_view('add_vehicle'))

class UpdateVehiclePrice(MethodView):
    def get(self, id):
        vehicle = Vehicle.query.filter_by(id = id).first()
        return render_template('update_vehicle_price.html', vehicle=vehicle)
    
    def post(self, id):
        vehicle = Vehicle.query.filter_by(id = id).first()

        vehicle.price = request.form.get('new_price')
        db.session.commit()

        return redirect("/")
        
app.add_url_rule("/update-vehicle-price/<id>",view_func=UpdateVehiclePrice.as_view('update_vehicle_price'))

class DeleteVehicle(MethodView):
    def delete(self, id):
        vehicle = Vehicle.query.filter_by(id=id).first()
        db.session.delete(vehicle)
        db.session.commit()
        flash("Vehicle deleted successfully")
        return redirect("/")
app.add_url_rule("/delete-vehicle/<id>",view_func=DeleteVehicle.as_view('delete_vehicle'), methods=['delete'])


# @app.route("/delete-vehicle/<id>")
# def delete_vehicle(id):
#     vehicle = Vehicle.query.filter_by(id=id).first()
#     db.session.delete(vehicle)
#     db.session.commit()
#     flash("Vehicle deleted successfully")
#     return redirect("/")


if __name__ == "__main__":
    from models import Vehicle
    create_db()
    app.run(debug=True)