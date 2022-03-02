#Carseller.com
from flask import Flask, render_template, request, redirect, url_for
import pymysql

app=Flask(__name__)

def connectdb():
    global con,cursor
    con=pymysql.connect(host='localhost', user='root', password='', database='project')
    cursor = con.cursor()
def closedb():
    con.close()
    cursor.close()

@app.route('/')
def index():
    return render_template("base.html")

def insertcar(Id,Model,Detail,Price,Image): # add new item
    connectdb()
    try:
        q="insert into cars values({},'{}','{}',{},'{}')".format(Id,Model,Detail,Price,Image)
        cursor.execute(q)
        con.commit()
        return True
    except pymysql.DatabaseError:
        con.rollback()
        closedb()
        return False

@app.route('/addcar/',methods=['GET','POST'])
def addcar():
    if request.method=='POST':
        data=request.form
        id=data['Id']
        model=data['Model']
        detail=data['Detail']
        price=data['Price']
        image=data['Image']
        status=insertcar(id,model,detail,price,image) # these values will pass through insercar().
        if status:
            return redirect ('/')
        else:
            print("Some Error")
    return render_template('addcars.html')


@app.route('/')
@app.route('/home')
def getcarsrecord():
    #data=getrecord()
    connectdb()
    q="select * from cars;"
    cursor.execute(q)
    data=cursor.fetchall()
    #print(data)
    return render_template('base.html',cars=data)


def updatecar(Id,Model,Detail,Price,Image): # update existing item
    connectdb()
    try:
        q="update cars set Model='{}',Detail='{}',Price={},Image='{}' where Id={}".format(Model,Detail,Price,Image,Id)
        cursor.execute(q)
        con.commit()  # it is final submission.
        return True
    except pymysql.DatabaseError:
        con.rollback()
        closedb()
        return False

@app.route("/updatecarsrecord/<int:Id>",methods=['GET','POST']) #connect to html with url
def updatecarsrecord(Id):
    print(Id)
    connectdb()
    q="select * from cars where Id={}".format(Id)
    cursor.execute(q)
    data=cursor.fetchone()
    if request.method == 'POST':
        data = request.form
        id = data['Id']
        model = data['Model']
        detail = data['Detail']
        price = data['price']
        image=data['Image']
        status=updatecar(id,model,detail,price,image) #these values will pass through updatecar()
        if status:
            return redirect('/home')
            print("inserted...")
        else:
            print("some error...")
    return render_template('updatecars.html',data=data)

def deletecar(cid):
    connectdb()
    try:
        q="delete from cars where Id={}".format(cid)
        cursor.execute(q)
        con.commit()
        return True
    except pymysql.DatabaseError:
        con.rollback()
        closedb()
        return False

@app.route('/deleterecord/<int:cid>')
def deleterecord(cid):
    status=deletecar(cid)
    print(status)
    if status:
        msg="record has been deleted..."
        return redirect('/home')
    else:
        msg="some error.."
    return render_template('base.html',msg=msg)


if __name__=="__main__":
    app.run(debug=True)

 