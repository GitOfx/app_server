from app.main import alchemy_db


class Movie_model(alchemy_db.Model):
    id = alchemy_db.Column(alchemy_db.Integer, primary_key=True)
    director = alchemy_db.Column(alchemy_db.String(1024))
    title = alchemy_db.Column(alchemy_db.String(1024))
    actors = alchemy_db.Column(alchemy_db.String(1024))
    movie_id = alchemy_db.Column(alchemy_db.String(1024), unique=True)
    introduce = alchemy_db.Column(alchemy_db.Text())
    length = alchemy_db.Column(alchemy_db.Text(1024))
    score = alchemy_db.Column(alchemy_db.Text(1024))
    category = alchemy_db.Column(alchemy_db.String(1024))
    pic_url = alchemy_db.Column(alchemy_db.String(1024))
    more_pic_url = alchemy_db.Column(alchemy_db.String(1024))

    def __init__(self, director=None, title=None, actors=None, movie_id=None,
                 introduce=None, length=None, score=None, category=None, pic_url=None, more_pic_url=None):
        self.director = director
        self.title = title
        self.actors = actors
        self.movie_id = movie_id
        self.introduce = introduce
        self.length = length
        self.score = score
        self.category = category
        self.pic_url = pic_url
        self.more_pic_url = more_pic_url
        pass


class Movie_Comment(alchemy_db.Model):
    id = alchemy_db.Column(alchemy_db.Integer, primary_key=True)
    comment = alchemy_db.Column(alchemy_db.Text())

    movie_id = alchemy_db.Column(alchemy_db.String(1024))

    def __init__(self, comment, movie_id):
        self.comment = comment;
        self.movie_id = movie_id

    def add_movie_comment(content, movie_id):
        comment = Movie_Comment(content, movie_id)

        from app.main import log
        log.info("add_comment comment %s" % content)

        try:
            alchemy_db.session.add(comment)
            alchemy_db.session.commit()
            pass
        except BaseException as e:
            log.error(" add_movie_comment error %s" % e)
            alchemy_db.session.rollback()
            # alchemy_db.session.close()
            pass


if __name__ == '__main__':
    alchemy_db.create_all()
