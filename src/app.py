import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import click
import sqlalchemy as sa
from datetime import datetime


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)

    def __repr__(self) -> str:
        return f"User(id= {self.id!r}), username= {self.username!r}"


class Post(db.Model):

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    body: Mapped[str] = mapped_column(sa.String, nullable=False)
    created: Mapped[datetime] = mapped_column(sa.DateTime, server_default=sa.func.now())
    author_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"User(id= {self.id!r}, title= {self.title!r}, author_id= {self.author_id})"


# Define um comando de linha de comando chamado init-db.
# Defines a command line called init-db
@click.command('init-db')
def init_db_command():
    global db
    with current_app.app_context():
        
        #  Cria todas as tabelas definidas nos modelos.
        #  Creates all tables defined on models.
        db.create_all()
    click.echo('Initialized the database.')


def create_app(test_config=None):    
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(

        SECRETKEY = 'dev',

        # URI do banco de dados usado pelo SQLAlchemy.
        # Database URI used by SQLAlchemy
        SQLALCHEMY_DATABASE_URI = "sqlite:///dio_bank.sqlite"
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test coonfig if passed in
        app.config.from_mapping(test_config)

    #  Adiciona o comando init-db ao CLI da aplicação Flask.
    #  Add the command init-db to CLI of the Flak application
    app.cli.add_command(init_db_command)

    # Inicializa a extensão SQLAlchemy com a aplicação Flask.
    # Initializes the SQLAlchemy extension with the Flask application.
    db.init_app(app)


    # Register Blueprint
    from src.controllers import user, post

    app.register_blueprint(user.app)
    app.register_blueprint(post.bp)
    


    return app