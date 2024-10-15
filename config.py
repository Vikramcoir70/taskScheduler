import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///tasks.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY',
                                    '5eb6a38d-12f3-4e0f-af8f-c17b51aa62e0')
