from flask import Flask,render_template,session,request,redirect
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import os
current_dir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///"+os.path.join(current_dir,"datab.sqlite3")
db=SQLAlchemy()
app.secret_key=os.urandom(24)

from model import *
db.init_app(app)
app.app_context().push()


@app.route('/')
def navbar():
    return render_template('navbar.html')


@app.route('/sign-in')
def signin():
    return render_template('sign-in.html')


@app.route('/admins',methods=['GET','POST'])
def admins():
    email=request.form.get('email')
    password=request.form.get('password')
    user_data = {
        'sachan@gmail.com': 'sachan@123',
        'Himanshu@gmail.com': 'Himanshu@123',
        'Shree@gmail.com': 'Shree@123',
        'Hamdan@gmail.com': 'Hamdan@123',
        'qw@gmail.com':'12'
    }
    if email in user_data and user_data[email] == password:
        return render_template('goahead.html')
    else:
        return render_template('admins.html')

@app.route('/TECG',methods=['POST','GET'])
def TECG():
    Username=request.form.get('Username')
    user=Creator.query.filter_by(name=Username)
    if user:
        conn = sqlite3.connect('datab.sqlite3')
        cursor = conn.cursor()
        cursor.execute('SELECT count(*) FROM upload where Username=?',(Username,))
        data1 = cursor.fetchall()
        cursor.execute('SELECT id,title FROM upload where Username=?',(Username,))
        data2=cursor.fetchall()
        cursor.execute('SELECT avg(rate) FROM rating where Username=?',(Username,))
        data3=cursor.fetchall()
        cursor.execute('SELECT count(distinct name) FROM album where Username=?',(Username,))
        data4=cursor.fetchall()
        cursor.execute('SELECT distinct name FROM album where Username=?',(Username,))
        data5=cursor.fetchall()
        conn.close()
        return render_template('creatdash.html',data1=data1,data2=data2,data3=data3,data4=data4,data5=data5)
    else:
        return redirect('/creator')
@app.route('/register')
def register():
    return render_template('register.html')
@app.route('/cra')
def cra():
    return render_template('cra.html')

@app.route('/index')
def Hello_world():
    return render_template('index.html')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login-action',methods=['GET','POST'])
def login_action():
    email=request.form.get('email')
    password=request.form.get('password')
    users=User.query.filter_by(email=email,password=password)
    check=[user for user in users]
    if check:
        session['user_id']=check[0].id
        return redirect('/harshu')
    else:
        return redirect('/sign-in')
    

@app.route('/conquer',methods=['POST'])
def conquer():
    try:
        email=request.form.get('email')
        phoneno=request.form.get('phoneno')
        name=request.form.get('name')
        password=request.form.get('password')
        update_user=User(email=email, phoneno=phoneno, name=name, password=password)
        db.session.add(update_user)
        db.session.flush()
    except Exception as e:
        return "{}".format(e),"not registered"
    
    else:
        db.session.commit()
        users=User.query.filter_by(email=email,password=password)
        check=[user for user in users]
        if check:
            session['user_id']=check[0].id
            return redirect('/harshu')
    
@app.route('/songstore',methods=['GET','POST'])
def songstore():
    try:
        Creator=request.form.get('Creator')
        Genre=request.form.get('Genre')
        title=request.form.get('title')
        Date=request.form.get('Date')
        Username=request.form.get('Username')
        Lyrics=request.form.get('Lyrics')
        update_user=Upload(Creator=Creator,Genre=Genre,title=title,Date=Date,Username=Username,Lyrics=Lyrics)
        db.session.add(update_user)
        db.session.flush()
        db.session.commit()
    except Exception as e:
        return "{}".format(e),"not uploaded"
    return redirect('/upload')
    

@app.route('/logout')
def logout():
    return redirect('/')     
@app.route('/creator')
def creator():
    if 'visited' in session and session['visited']:
        return redirect('/user')
    else:
        return render_template('creator.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')
@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/creatdash')
def creatdash():
    return render_template('creatdash.html')

@app.route('/craplaylist')
def craplaylist():
    return render_template('craplaylist.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')
@app.route('/goaheadh')
def goaheadh():
    return render_template('goahead.html')
@app.route('/admininf')
def admininf():
    return render_template('admininf.html')
@app.route('/user')
def user():
    return render_template('user.html')
@app.route('/song')
def song():
    return render_template('song.html')


@app.route('/Songs',methods=['GET','POST'])
def Songs():
    title=request.form.get('title')
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM upload where title=?',(title,))
    data = cursor.fetchall()
    conn.close()
    return render_template('song.html',data=data)

@app.route('/adminalbums',methods=['GET','POST'])
def adminalbums():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT  distinct(name) FROM album')
    data = cursor.fetchall()
    conn.close()
    return render_template('adminalbums.html',data=data)

@app.route('/TECGp',methods=['GET','POST'])
def tecgp():
    Username=request.form.get('Username')
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT distinct(name) FROM playlist where Username=?',(Username,))
    data = cursor.fetchall()
    conn.close()
    return render_template('playlist.html',data=data)
    
@app.route('/flexi',methods=['GET','POST'])
def flexi():
    if request.method=='POST':
        try:
            name=request.form.get('name')
            Gender=request.form.get('Gender')
            age=request.form.get('age')
            is_creator='True'
            update_user=Creator(name=name,Gender=Gender,age=age,is_creator=is_creator)
            db.session.add(update_user)
            db.session.flush()
            db.session.commit()
            return redirect('/user')
        except Exception as e:
            return "{}".format(e),"not uploaded"
        

@app.route('/seesong',methods=['GET','POST'])
def seesong():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT count(title) FROM upload where Creator')
    data = cursor.fetchall()
    conn.close()
    return render_template('/creatdash',data=data)

@app.route('/alls',methods=['GET','POST'])
def alls():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT title,Username FROM upload')
    data = cursor.fetchall()
    conn.close()
    return render_template('admininf.html',data=data)
@app.route('/createplaylist',methods=['GET','POST'])
def createplaylist():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT id,title FROM upload')
    data = cursor.fetchall()
    conn.close()
    return render_template('createplaylist.html',data=data)

@app.route('/acting',methods=['GET','POST'])
def acting():
    try:
        name=request.form.get('name')
        phoneno=request.form.get('phoneno')
        email=request.form.get('email')
        password=request.form.get('password')
        conn = sqlite3.connect('datab.sqlite3')
        cursor = conn.cursor()
        cursor.execute('update user set email=?,phoneno=?,password=? where name=?',(email,phoneno,password,name))
        conn.commit()
        return render_template('profile.html')
    except Exception as e:
            return "{}".format(e),"not uploaded"
    finally:
       conn.close()

@app.route('/editsong',methods=['GET','POST'])
def editsong():
    try:
        Creator=request.form.get('Creator')
        Genre=request.form.get('Genre')
        title=request.form.get('title')
        Date=request.form.get('Date')
        Lyrics=request.form.get('Lyrics')
        conn = sqlite3.connect('datab.sqlite3')
        cursor = conn.cursor()
        cursor.execute('update upload set Creator=?,Genre=?,Date=?,Lyrics=? where title=?',(Creator,Genre,Date,Lyrics,title))
        conn.commit()
        return render_template('edits.html')
    except Exception as e:
            return "{}".format(e),"not changed"
    finally:
       conn.close()

@app.route('/tert',methods=['GET','POST'])
def tert():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM upload')
    data = cursor.fetchall()
    conn.close()
    return render_template('allsongs.html',data=data)

@app.route('/text',methods=['GET','POST'])
def text():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT distinct(name) FROM album')
    data = cursor.fetchall()
    conn.close()
    return render_template('useralbum.html',data=data)

@app.route('/useralbum',methods=['GET','POST'])
def useralbum():
    name=request.form.get('name')
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT title FROM album where name=?',(name,))
    data = cursor.fetchall()
    conn.close()
    return render_template('useralbums.html',data=data)


@app.route('/albumd',methods=['GET','POST'])
def albumd():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM upload')
    data = cursor.fetchall()
    conn.close()
    return render_template('albums.html',data=data)

@app.route('/albumedit',methods=['GET','POST'])
def albumedit():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    if 'view_butto' in request.form:
        name=request.form.get('name')
        cursor.execute('SELECT title FROM album where name=?',(name,))
        data = cursor.fetchall()
        conn.close()
        return render_template('crtalbum.html',data=data)
    if 'edit_butto' in request.form:
        cursor.execute('Select * from upload')
        data=cursor.fetchall()
        return render_template('editalbum.html',data=data)
    if 'delete_butto' in request.form:
        name=request.form.get('name')
        cursor.execute('DELETE FROM album where name=?',(name,))
        conn.commit()
        conn.close()
        return render_template('upload.html')
    
@app.route('/editaplay',methods=['GET','POST'])
def editaplayl():
    try:
        name=request.form.get('name')
        Username=request.form.get('Username')
        titles=request.form.getlist('title[]')
        isks=request.form.getlist('isk[]')
        for title, isk in zip(titles, isks):
            update_user=Playlist(name=name,Username=Username,title=title,isk=isk)
            db.session.add(update_user)
            db.session.flush()
            db.session.commit()
        return render_template('added.html')
    except Exception as e:
            return "{}".format(e),"not uploaded"
    
@app.route('/playlistedit',methods=['GET','POST'])
def playlistedit():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    if 'view_butto' in request.form:
        name=request.form.get('name')
        cursor.execute('SELECT title FROM playlist where name=?',(name,))
        data = cursor.fetchall()
        conn.close()
        return render_template('allsongs.html',data=data)
    if 'delete_butto' in request.form:
        name=request.form.get('name')
        cursor.execute('DELETE FROM playlist where name=?',(name,))
        conn.commit()
        conn.close()
        return render_template('deleted.html')
    
@app.route('/createplay',methods=['GET','POST'])
def createplay():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    if 'view_butto' in request.form:
        name=request.form.get('name')
        cursor.execute('SELECT title FROM playlist where name=?',(name,))
        data = cursor.fetchall()
        conn.close()
        return render_template('crtalbum.html',data=data)
    if 'edit_butto' in request.form:
        cursor.execute('Select * from upload')
        data=cursor.fetchall()
        return render_template('editalbum.html',data=data)
    if 'delete_butto' in request.form:
        name=request.form.get('name')
        cursor.execute('DELETE FROM album where name=?',(name,))
        conn.commit()
        conn.close()
        return render_template('upload.html')
    
@app.route('/albumeditadmin',methods=['GET','POST'])
def albumeditadmin():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    if 'view_butto' in request.form:
        name=request.form.get('name')
        cursor.execute('SELECT title FROM album where name=?',(name,))
        data = cursor.fetchall()
        conn.close()
        return render_template('crtalbum.html',data=data)
    if 'delete_butto' in request.form:
        name=request.form.get('name')
        cursor.execute('DELETE FROM album where name=?',(name,))
        conn.commit()
        conn.close()
        return render_template('/index')
    
@app.route('/creatorsee',methods=['GET','POST'])
def creatorsee():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    if 'view_butto' in request.form:
        craetorse=request.form.get('craetorse')
        cursor.execute('SELECT * FROM upload where title=?',(craetorse,))
        data1 = cursor.fetchall()
        conn.close()
        return render_template('song.html',data=data1)
    if 'edit_butto' in request.form:
        return render_template('edits.html')
    if 'delete_butto' in request.form:
        craetorse=request.form.get('craetorse')
        cursor.execute('DELETE FROM upload where title=?',(craetorse,))
        data1 = cursor.fetchall()
        conn.commit()
        conn.close()
        return render_template('creatdash.html')
    
@app.route('/techno',methods=['GET','POST'])
def techno():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    if 'view_butto' in request.form:
        craetorse=request.form.get('craetorse')
        cursor.execute('SELECT * FROM upload where title=?',(craetorse,))
        data1 = cursor.fetchall()
        conn.close()
        return render_template('song.html',data=data1)
    if 'delete_butto' in request.form:
        craetorse=request.form.get('craetorse')
        cursor.execute('DELETE FROM upload where title=?',(craetorse,))
        data1 = cursor.fetchall()
        conn.commit()
        conn.close()
        return render_template('admininf.html')

@app.route('/admincreat',methods=['GET','POST'])
def admincreat():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT count(distinct Genre) FROM upload')
        data1 = cursor.fetchall()
        cursor.execute('SELECT title FROM rating where rate=? LIMIT 3',(5,))
        data2 = cursor.fetchall()
        cursor.execute('SELECT count(*) FROM user')
        data3 = cursor.fetchall()
        cursor.execute('SELECT count(distinct Username) FROM upload')
        data4 = cursor.fetchall()
        cursor.execute('SELECT count(*) FROM upload')
        data5 = cursor.fetchall()
        cursor.execute('SELECT count(distinct name) FROM Album')
        data6 = cursor.fetchall()
        cursor.execute('SELECT count(distinct name) FROM playlist')
        data7 = cursor.fetchall()
        conn.close()
        return render_template('dashboard.html',data1=data1,data2=data2,data3=data3,data4=data4,data5=data5,data6=data6,data7=data7)
    except Exception as e:
        return "{}".format(e),"not uploaded"
    



@app.route('/harshu',methods=['GET','POST'])
def harshu():
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT title FROM upload LIMIT 6')
        data1 = cursor.fetchall()
        cursor.execute('SELECT distinct(name) FROM album LIMIT 6')
        data2 = cursor.fetchall()
        conn.close()
        return render_template('index.html',data1=data1,data2=data2)
    except Exception as e:
        return "{}".format(e),"not fetched"

@app.route('/userson',methods=['GET','POST'])
def userson():
    title=request.form.get('title')
    conn = sqlite3.connect('datab.sqlite3')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM upload where title=?',(title,))
    data = cursor.fetchall()
    conn.close()
    return render_template('usersong.html',data=data)

@app.route('/Ratingsofsong',methods=['GET','POST'])
def Ratingsofsong():
    Username=request.form.get('Username')
    title=request.form.get('title')
    rate=request.form.get('rate')
    update_user=Rating(title=title,rate=rate,Username=Username)
    db.session.add(update_user)
    db.session.flush()
    db.session.commit()
    return render_template('thanks.html')

@app.route('/albumcrt',methods=['GET','POST'])
def albumcrt():
    name=request.form.get('name')
    titles=request.form.getlist('title[]')
    isds=request.form.getlist('isd[]')
    Username=request.form.get('Username')
    for title, isd in zip(titles, isds):
        update_user=Album(title=title,isd=isd,name=name,Username=Username)
        db.session.add(update_user)
    db.session.flush()
    db.session.commit()
    return redirect('/albumd')

@app.route('/editalbum',methods=['GET','POST'])
def editalbum():
    name=request.form.get('name')
    titles=request.form.getlist('title[]')
    isds=request.form.getlist('isd[]')
    for title, isd in zip(titles, isds):
        conn = sqlite3.connect('datab.sqlite3')
        cursor = conn.cursor()
        cursor.execute('update album set title=?,isd=? where name=?',(title,isd,name))
        conn.commit()
        conn.close()
    return redirect('/albumd')



if __name__=='__main__':
    app.run(debug=True)