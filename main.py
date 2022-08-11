from flask import Flask, jsonify, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import CKEditor, CKEditorField
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class NewTask(FlaskForm):
    name = StringField("Name", validators=[DataRequired()], render_kw={"placeholder": "Task Name"})
    task_description = CKEditorField("Description", validators=[DataRequired()])
    submit = SubmitField("Add Task")


app = Flask(__name__)
Bootstrap(app)
ckeditor = CKEditor(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Task.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Task TABLE Configuration
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), unique=True, nullable=False)


# def to_dict(self):
#     return {column.name: getattr(self, column.name) for column in self.__table__.columns}
# db.create_all()

@app.route("/")
def home():
    # todos = Cafe.query.filter_by(location=query_location).all()
    all_tasks = Task.query.all()
    db.session.commit()
    return render_template("index.html", all_tasks=all_tasks)


@app.route("/new-task", methods=["POST", "GET"])
def new_task():
    form = NewTask(meta={'csrf': False})
    if form.validate_on_submit():
        add_task = Task(
            name=request.form.get("name"),
            description=request.form.get("task_description")
           )
        db.session.add(add_task)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("new_task.html", form=form)


# @app.route("/search")
# def get_cafe_at_location():
#     query_location = request.args.get("loc")
#     cafes = Cafe.query.filter_by(location=query_location).all()
#     if len(cafes) == 0:
#         return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})
#     else:
#         return jsonify(cafe=[cafe.to_dict() for cafe in cafes])


# @app.route("/add", methods=["POST", "GET"])
# def post_new_cafe():
#     api_key = "TopSecretApiKey"
#     if api_key == request.args.get("api_key"):
#         new_cafe = Cafe(
#             name=request.form.get("name"),
#             map_url=request.form.get("map_url"),
#             img_url=request.form.get("img_url"),
#             location=request.form.get("location"),
#             has_sockets=bool(request.form.get("sockets")),
#             has_toilet=bool(request.form.get("toilet")),
#             has_wifi=bool(request.form.get("wifi")),
#             can_take_calls=bool(request.form.get("calls")),
#             seats=request.form.get("seats"),
#             coffee_price=request.form.get("coffee_price"),
#         )
#         db.session.add(new_cafe)
#         db.session.commit()
#         return jsonify(response={"Success": "Successfully added the new cafe."}), 200
#     else:
#         return jsonify(
#             response={"Not Found": "Sorry, that's not allowed. Make sure you have the corretct api_key."}), 404


# @app.route("/update-price/<int:cafe_id>", methods=["PATCH"])
# def patch_new_price(cafe_id):
#     new_price = request.args.get("new_price")
#     cafe = db.session.query(Cafe).get(cafe_id)
#     if cafe:
#         cafe.coffee_price = new_price
#         db.session.commit()
#         ## Just add the code after the jsonify method. 200 = Ok
#         return jsonify(response={"success": "Successfully updated the price."}), 200
#     else:
#         # 404 = Resource not found
#         return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404


# @app.route("/report-closed/<int:cafe_id>", methods=["DELETE"])
# def delete_caffe(cafe_id):
#     cafe = db.session.query(Cafe).get(cafe_id)
#     api_key = "TopSecretAPIKey"
#
#     if api_key == request.args.get("api_key"):
#         if cafe:
#             db.session.delete(cafe)
#             db.session.commit()
#             return jsonify(response={"Success": "Successfully deleted cafe from database."}), 200
#         else:
#             return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database"}), 404
#
#     else:
#         return jsonify(error={"Not Found": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 404



if __name__ == '__main__':
    app.run(debug=True)
