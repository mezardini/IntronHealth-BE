import environ
env = environ.Env()
environ.Env.read_env()


class Config:
    SECRET_KEY = env('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///intronhealth.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = env('JWT_SECRET_KEY')
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ['access', 'refresh']


