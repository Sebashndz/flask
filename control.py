from flask import Flask, render_template, send_file, redirect, url_for, request, g, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy
from flask_user import roles_required, UserManager, UserMixin
from flask_babelex import Babel
from flask_login import (
    LoginManager,
    login_required,
    current_user,
    login_user,
    logout_user,
)
import forms
import datetime

# from zeep import Client
# import os
# import codecs

from Divisa_Functions import (
    webservice_request,
    connectionDB,
    save_dataframe,
    Descarga_Excel,
    connectionDB_DM_Comercial,
)

def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config.from_pyfile('config.py')
    app.config["BABEL_DEFAULT_LOCALE"] = "es"
    login_manager = LoginManager(app)
    login_manager.login_view = "login"
    babel = Babel(app)
    db = SQLAlchemy(app)

    # # Use the browser's language preferences to select an available translation
    # @babel.localeselector
    # def get_locale():
    #     translations = [str(translation) for translation in babel.list_translations()]
    #     return request.accept_languages.best_match(translations)

    class User(db.Model, UserMixin):
        __tablename__ = "users"
        id = db.Column(db.Integer, primary_key=True)
        first_name = db.Column(db.String(80), nullable=False)
        last_name = db.Column(db.String(80), nullable=False)
        email = db.Column(db.String(256), unique=True, nullable=False)
        email_confirmed_at = db.Column(db.DateTime())
        password = db.Column(db.String(128), nullable=False)
        active = db.Column(
            "is_active", db.Boolean(), nullable=False, server_default="1"
        )
        roles = db.relationship("Role", cascade="all,delete", secondary="user_roles")

        def __repr__(self):
            return f"<User {self.email}>"

        def set_password(self, password):
            self.password = user_manager.hash_password(password)

        def check_password(self, password):
            return check_password_hash(self.password, password)

        def save(self):
            if not self.id:
                db.session.add(self)
            db.session.commit()

        def has_role(self, role):
            for r in self.roles:
                if r.name == role:
                    return True
            return False

        @staticmethod
        def get_by_id(id):
            return User.query.get(id)

        @staticmethod
        def get_by_email(email):
            return User.query.filter_by(email=email).first()

    # Define the Role data-model
    class Role(db.Model):
        __tablename__ = "roles"
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

    # Define the UserRoles association table
    class UserRoles(db.Model):
        __tablename__ = "user_roles"
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey("users.id", ondelete="CASCADE"))
        role_id = db.Column(db.Integer(), db.ForeignKey("roles.id", ondelete="CASCADE"))

    user_manager = UserManager(app, db, User)

    # Create all database tables
    db.create_all()

    @app.route("/user-register", methods=["GET", "POST"])
    @roles_required(["A", "B"])
    def show_signup_form():
        form = forms.SignupForm()
        error = None
        if form.validate_on_submit():
            first_name = form.first_name.data
            last_name = form.last_name.data
            email = form.email.data
            password = form.password.data
            role_name = form.roles.data
            # Comprobamos que no hay ya un usuario con ese email
            user = User.get_by_email(email)
            if user is not None:
                error = f"El email {email} ya está siendo utilizado por otro usuario"
            else:
                # Creamos el usuario y lo guardamos
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    email_confirmed_at=datetime.datetime.now(),
                    password=user_manager.hash_password(password),
                )
                role = Role.query.filter_by(name=role_name).first()
                if role:
                    user.roles.append(role)
                else:
                    user.roles.append(Role(name=role_name))
                user.save()
                return redirect("/users")
        return render_template("signup_form.html", form=form, error=error)

    @app.route("/user-update/<id>", methods=["GET", "POST"])
    @roles_required(["A", "B"])
    def update_user(id):
        user = User.get_by_id(id)
        if request.method == "GET":
            form = forms.UpdateForm(obj=user)
            form.roles.data = user.roles[0].name
            error = None
        else:
            form = forms.UpdateForm(request.form)
            if form.validate_on_submit():
                user.first_name = form.first_name.data
                user.last_name = form.last_name.data
                user.email = form.email.data

                r = UserRoles.query.filter_by(user_id=id).first()
                db.session.delete(r)
                db.session.commit()

                role_name = form.roles.data
                role = Role.query.filter_by(name=role_name).first()
                if role:
                    user.roles.append(role)
                else:
                    user.roles.append(Role(name=role_name))
                db.session.commit()
                return redirect("/users")
        return render_template("update_form.html", form=form, error=error)

    @app.route("/user-delete/<id>", methods=["GET", "POST"])
    @roles_required(["A", "B"])
    def delete_user(id):
        if request.method == "POST":
            user = User.get_by_id(id)
            db.session.delete(user)
            db.session.commit()
            return redirect("/users")

    @app.route("/consulta", methods=["GET", "POST"])
    @roles_required(["A", "B"])
    def index():

        nit_form = forms.ConsultaNit(request.form)  # Captura los datos del formuario
        if (
            request.method == "POST" and nit_form.validate()
        ):  # Validate() ejecuta las reglas de validacion que se establecieron en forms.py
            nit = nit_form.nit.data
            webservice_request(nit)
            # conn = connectionDB()
            # cursor = conn.cursor()
            save_dataframe(nit)
            flash("Consulta realizada exitosamente", "success")
            return redirect("/consulta")
        return render_template("index.html", form=nit_form)

    @app.route("/users")
    @roles_required(["A", "B"])
    def getusers():
        users = User.query.filter(User.id != current_user.id).all()
        return render_template("list_users.html", users=users)

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("user.login"))

    @app.route("/")
    @app.route("/reporte")
    @login_required
    def reporte():
        return render_template("reporte.html")

    @app.route("/download")
    @login_required
    def download_file():
        Descarga_Excel()
        path = "/var/www/html/flask/Resultados/Reporte.xls"
        flash("Descarga realizada exitosamente", "success")
        send_file(path, as_attachment=True)
        return redirect("/reporte")

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(int(user_id))

    return app

app = create_app()

if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0')

