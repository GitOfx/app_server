from app.main import alchemy_db

from app.data_model import base_model


class News_Category(alchemy_db.Model):
    id = alchemy_db.Column(alchemy_db.Integer, primary_key=True)
    type = alchemy_db.Column(alchemy_db.Text())
    category_id = alchemy_db.Column(alchemy_db.String(1024))  #一个类型对应多新闻
    category_name = alchemy_db.Column(alchemy_db.Text())
    artical_id = alchemy_db.Column(alchemy_db.String(1024), unique=True)
    #
    # artical = alchemy_db.relationship('News_Model', backref='artical', lazy='dynamic')

    def __init__(self, type, category_id, category_name, artical_id):
        self.type = type;
        self.category_id = category_id
        self.category_name = category_name
        self.artical_id = artical_id
        pass


    @staticmethod
    def add_news_cate(type, category_id, category_name, artical_id):
        cat = News_Category(type, category_id, category_name, artical_id)
        if len(cat.query.filter_by(artical_id=artical_id).all()) == 0:
            from app.main import log
            log.info("add News_Category %s artical_id %s"%(category_name,artical_id))

            try:
                alchemy_db.session.add(cat)
                alchemy_db.session.commit()
                pass
            except BaseException as e:
                log.error("add News_Category error %s" %e)
                alchemy_db.session.rollback()
                # alchemy_db.session.close()
                pass

    @staticmethod
    def get_all(limit = None):
        if limit == None:
            return News_Category.query.all()
        return News_Category.query.limit(limit).all()

    @staticmethod
    def commit_data():
        alchemy_db.session.commit()


class News_Model(alchemy_db.Model):
    # _tablename__ = 'news_detail'
    id = alchemy_db.Column(alchemy_db.Integer, primary_key=True)
    title = alchemy_db.Column(alchemy_db.Text())
    artical_id = alchemy_db.Column(alchemy_db.String(1024), unique=True)
    category = alchemy_db.Column(alchemy_db.Text())
    category_id = alchemy_db.Column(alchemy_db.String(1024))
    excerpt = alchemy_db.Column(alchemy_db.Text())
    # img = alchemy_db.Column(alchemy_db.Text())
    time = alchemy_db.Column(alchemy_db.Text())
    url = alchemy_db.Column(alchemy_db.Text())
    content = alchemy_db.Column(alchemy_db.Text())
    html = alchemy_db.Column(alchemy_db.Text())
    img = alchemy_db.relationship('News_Img', backref='artical', lazy='dynamic')

    def __init__(self,
                 title=None,
                 category=None,
                 img=None,
                 time=None,
                 url=None,
                 content=None,
                 artical_id=None,
                 html=None,
                 excerpt=None):
        self.title = title
        self.time = time
        self.category = category
        # self.img = img
        self.url = url
        self.content = content
        self.excerpt = excerpt
        self.artical_id = artical_id
        self.html = html


    @staticmethod
    def get_all(limit = 2):
        return  News_Model.query.limit(limit).all()

    @staticmethod
    def add_news_detail(title=None,
                        category=None,
                        img=None,
                        time=None,
                        url=None,
                        content=None,
                        artical_id=None,
                        html=None,
                        excerpt=None):

        news = News_Model(title=title,
                          category=category,
                          img=img,
                          time=time,
                          url=url,
                          artical_id=artical_id,
                          content=content,
                          html=html,
                          excerpt=excerpt)
        result = news.query.filter_by(artical_id=artical_id).all();
        if (result == None or len(result) == 0):
            from app.main import log
            log.info("add News_Model %s" %title)
            try:
                alchemy_db.session.add(news)
                alchemy_db.session.commit()
                pass
            except BaseException as e:
                log.error("add News_Model error %s" %e)
                alchemy_db.session.rollback()
                # alchemy_db.session.close()
                pass
            finally:
                pass



# alter table address convert to character set utf8

class News_Img(alchemy_db.Model):
    id = alchemy_db.Column(alchemy_db.Integer, primary_key=True)
    # ForeignKey 不能用字符串   外键表必须存在
    artical_id = alchemy_db.Column(alchemy_db.String(1024), alchemy_db.ForeignKey(News_Model.artical_id))
    url = alchemy_db.Column(alchemy_db.Text())
    save_path = alchemy_db.Column(alchemy_db.Text())
    desc = alchemy_db.Column(alchemy_db.Text())

    def __init__(self, artical_id, url, desc=None):
        self.artical_id = artical_id
        self.url = url
        self.desc = desc

        pass


    @staticmethod
    def get_all(limit=2):
        return News_Img.query.limit(limit).all()

    @staticmethod
    def add_news_img(artical_id, url, desc):
        img = News_Img(artical_id, url, desc)
        if len(img.query.filter_by(url=url).all()) == 0 or img.query.filter_by(url=url).all() == None:
            from app.main import log
            log.info("add add_news_img des %s"%desc)

            try:
                alchemy_db.session.add(img)
                alchemy_db.session.commit()
                pass
            except BaseException as e:
                log.error("add News_Img error %s" %e)
                alchemy_db.session.rollback()
                # alchemy_db.session.close()
                pass


@staticmethod
def selectAllNews():
    pass

def create_db():
    # alchemy_db.drop_all()
    alchemy_db.create_all()





if __name__ == '__main__':
    alchemy_db.drop_all()
    alchemy_db.create_all()
    # log.info("size %s " % len(News_Category.query.filter_by(artical_id="44955").all()))
    # from app.data_model import base_model
    # li = News_Model.get_all(2)
    # print(li)
    # json = base_model.toJson(li)
    # print(json)
