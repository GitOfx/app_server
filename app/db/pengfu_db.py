import sqlite3
import sys
from app.main import alchemy_db as db
#sqlite3.connect(dbName) will create the db if not exists
# http://www.pythondoc.com/flask-sqlalchemy/index.html
import types
dbName = "app_service.db"

class PengfuJoke(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    detail_url = db.Column(db.Text())
    img_url = db.Column(db.Text())

    def __init__(self, id,content, detail_url,img_url):
        self.id = id
        self.content = content
        self.detail_url = detail_url
        self.img_url = img_url

    def __repr__(self):
        return 'content:%s ' % self.content

    @staticmethod
    def AddJoke(id,content, detail_url,img_url):
        joke = PengfuJoke(id,content, detail_url,img_url)
        print(joke.__repr__())
        db.session.add(joke)
        db.session.commit()

    @staticmethod
    def GetAll():
        return PengfuJoke.query.all()

    @staticmethod
    def GetPage(page_size,num):
        if page_size == 0:
            page_size = 10

        return PengfuJoke.query.offset(int(num)*int(page_size)).limit(int(page_size)).all()


if __name__ == '__main__':
     db.create_all()