from main import db
class User(db.Model):
    __tablename__='user'
    id=db.Column('id',db.Integer,primary_key=True)
    email=db.Column(db.String(40))
    phoneno=db.Column(db.String(10))
    name=db.Column(db.String(30))
    password=db.Column(db.String(20))
class Upload(db.Model):
    __tablename__='upload'
    id=db.Column('id',db.Integer,primary_key=True)
    Username=db.Column(db.String(30))
    Creator=db.Column(db.String(30))
    Genre=db.Column(db.String(40))
    title=db.Column(db.String(10))
    Date=db.Column(db.String(30))
    Lyrics=db.Column(db.String(900))
class Creator(db.Model):
    __tablename__='creator'
    id=db.Column('id',db.Integer,primary_key=True)
    name=db.Column(db.String(30))
    Gender=db.Column(db.String(30))
    age=db.Column(db.String(30))
    is_creator = db.Column(db.String(20))
class Rating(db.Model):
    __tablename__='rating'
    id=db.Column('id',db.Integer,primary_key=True)
    Username=db.Column(db.String(30))
    title=db.Column(db.String(30))
    rate=db.Column(db.String(2))

class Album(db.Model):
    __tablename__='album'
    id=db.Column('id',db.Integer,primary_key=True)
    Username=db.Column(db.String(30))
    isd=db.Column(db.String(2))
    name=db.Column(db.String(30))
    title=db.Column(db.String(30))

class Playlist(db.Model):
    __tablename__='playlist'
    id=db.Column('id',db.Integer,primary_key=True)
    Username=db.Column(db.String(30))
    isk=db.Column(db.String(2))
    name=db.Column(db.String(30))
    title=db.Column(db.String(30))

