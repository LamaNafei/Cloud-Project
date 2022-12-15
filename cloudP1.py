from PIL import Image
import os
from flask import Flask, render_template, request
import mysql.connector
import os.path
import mysql.connector
from flask_mysqldb import MySQL
import boto3,botocore



# con = mysql.connector.connect(host='database-2.ce56zqclzkbk.us-east-1.rds.amazonaws.com',username='admin',password='lamamaialaa',database='c_db')
con = mysql.connector.connect(host = 'localhost', user = 'root', password = '1955', database = 'db')            
cur = con.cursor()

app = Flask(__name__)
app.config['UPLOAD_FOLDER']="static/" #the path for images folder
path = './static/'

app.config['S3_BUCKET']="proj2bucket"
app.config['S3_LOCATION']='http://proj2bucket.s3.amazonaws.com/'
s3 = boto3.client(
   "s3",
   aws_access_key_id = app.config['S3_KEY'],
   aws_secret_access_key = app.config['S3_SECRET']
)

@app.route('/')
def main() :
    return render_template("index.html")

@app.route('/manager')
def manager():
    return render_template ("manager.html")

@app.route('/request', methods = ['GET','POST'])
def req():  
    if request.method == 'POST' :
        try:
            # con=mysql.connector.connect(host='database-2.ce56zqclzkbk.us-east-1.rds.amazonaws.com',username='admin',password='lamamaialaa',database='c_db')
            con = mysql.connector.connect(host = 'localhost', user = 'root', password = '1955', database = 'db')            
            cur = con.cursor()    
            key = request.form['keyy']
            cur.execute("SELECT keyy FROM images WHERE keyy = ?", [key])
            isNewKey = len(cur.fetchall()) == 0
            if not isNewKey :
                 name = cur.execute("SELECT image FROM images WHERE keyy = ?", [key]).fetchall()[0][0]
            else :
                    return render_template('request.html', keyCheck = "key not found !")

            return render_template('request.html', user_image = ('..\\static\\' + name))
        except:
            return("error occur")
        finally:
            con.close()
    return render_template('request.html')

@app.route('/upload', methods = ['POST','GET']) 
def upload():
    if request.method=='POST':
        key= request.form['key']
        image=request.files['image']
        if image.filename!='':
            filepath=os.path.join(app.config['UPLOAD_FOLDER'],image.filename)
            image.save(filepath)
            print(filepath) #in static folder path
            
            cur.execute("SELECT keyy FROM images WHERE keyy = %s", [key])
            isNewKey = len(cur.fetchall()) == 0
            # saveFile(path + image.filename, image.filename, imagePath)
            if(isNewKey) :
                cur.execute("INSERT INTO images (keyy,image) VALUES(%s,%s)",(key,image.filename))    
                #s3.upload_file(Filename=f"{imagePath}/{image.filename}",Bucket=app.config["S3_BUCKET"],Key=key)
                done = "Upload Successfully"
            else :
                cur.execute("UPDATE images SET image = %s WHERE keyy = %s", (image.filename,key))
                done = "Update Successfully"                    
                    
            con.commit()
            con.close()

        
            return render_template('upload.html', done = done)
    return render_template('upload.html')

@app.route('/list', methods = ['POST','GET'])
def keyList():
    if request.method == 'GET' :
        try:
            # con=mysql.connector.connect(host='database-2.ce56zqclzkbk.us-east-1.rds.amazonaws.com',username='admin',password='lamamaialaa',database='c_db')            
            con = mysql.connector.connect(host = 'localhost', user = 'root', password = '1955', database = 'db')            
            cur = con.cursor()    
            cur.execute("SELECT keyy FROM images")
            con.commit()
        except:
            return 'error'
        finally:
            return render_template('KeyList.html', keys=[str(val[0]) for val in cur.fetchall()])
    return render_template('KeyList.html')
if __name__ == '__main__':
    app.run('0.0.0.0',debug=True)

