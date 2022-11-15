#null
class Config:
    DEBUG=True
    TESTING=True

    #CONFIGURACION BASE DATOS 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:5x5W12@localhost:3306/flask"

class ProductionsConfig(Config):
    DEBUG= False

class DevelopmentConfig(Config):
    SECRET_KEY='dev'
    DEBUG=True
