import os
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import click


class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


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

    return app