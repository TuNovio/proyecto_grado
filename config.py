#null
class Config:
    DEBUG=True
    TESTING=True

    #CONFIGURACION BASE DATOS 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:5x5W12@localhost:3306/ronald"

class ProductionsConfig(Config):
    DEBUG= True

class DevelopmentConfig(Config):
    SECRET_KEY='dev'
    DEBUG=True
