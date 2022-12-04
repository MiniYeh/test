from flask import *
import mysql.connector
from view.api import api

app=Flask(
    __name__,
    static_folder = "static", # 靜態檔案的資料夾名稱
    static_url_path = "/" # 靜態檔案對應的網址路徑
    )
app.config["JSON_AS_ASCII"]=False
app.config["TEMPLATES_AUTO_RELOAD"]=True

def db_connection():
    mydb = None
    try:
        mydb = mysql.connector.connect(
        host = "localhost",
        port = 3306,
        user = "root",
        database = "travel",
        password = "",
        charset = "utf8"
        )
    except mysql.connector.Error as e:
        print(e)
    return mydb

# Pages
@app.route("/")
def index():
    return render_template('index.html')
@app.route("/attraction/<id>")
def attraction(id):
	return render_template("attraction.html")
@app.route("/booking")
def booking():
	return render_template("booking.html")
@app.route("/thankyou")
def thankyou():
	return render_template("thankyou.html")


if __name__ == "__main__":
    app.register_blueprint(api)
    app.run(host='0.0.0.0',port=3000)


@api.route("/api/attractions", methods=['GET'])
def attractions():
    try:
        page = int(request.args.get('page', 0))
        nextPage = page + 1
        keyword = request.args.get('keyword', '')
        keyword2 = '%' + keyword + '%'
        datafrom = int(page) * 12
        dataNumPage = 12
        sql = """
            SELECT * 
            FROM (SELECT id, name, category, description, address, transport, mrt, latitude, longitude, images
            FROM attractions 
            WHERE name like %s order by id)
            as a LIMIT %s,%s;
        """
        val = (keyword2, datafrom, dataNumPage)
        mydb = db_connection()
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        num = mycursor.fetchall()
        myresult = []
        for i in range(len(num)):
            id = num[i][0]
            name = num[i][1]
            category = num[i][2]
            description  = num[i][3]
            address = num[i][4]
            transport = num[i][5]
            mrt = num[i][6]
            latitude = num[i][7]
            longitude = num[i][8]
            images = num[i][9]
            myresults = {
                "id": id,
                "name": name,
                "category": category,
                "description": description,
                "address": address,
                "transport": transport,
                "mrt": mrt,
                "latitude": latitude,
                "longitude": longitude,
                "images": eval(images)
            }
            myresult.append(myresults)
        
        # 查下一頁
        sql = """
            SELECT * 
            FROM (SELECT name 
            FROM attractions 
            WHERE name like %s ORDER BY id)
            as a LIMIT %s,%s;
        """
        val = (keyword2, datafrom+12, 1)
        mycursor.execute(sql, val)
        num = mycursor.fetchall()
        if num == []:
            nextPage = None
            
        mydb.close()
        return Response(json.dumps({
            "nextPage": nextPage,
            "data": myresult
        }, sort_keys = False), mimetype="application/json")
    except:
        return Response(json.dumps({
            "error": True,
            "message": "伺服器錯誤"
        }, sort_keys = False), mimetype="application/json"), 500
        
@api.route("/api/attraction/<int:attractionId>")
def attraction_id(attractionId):
    try:
        sql = """
            SELECT id, name, category, description, address, transport, mrt, latitude, longitude, images
            FROM attractions WHERE id = %s;
        """
        val = (attractionId, )
        mydb = db_connection()
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        num = mycursor.fetchone()
        id = num[0]
        name = num[1]
        category = num[2]
        description  = num[3]
        address = num[4]
        transport = num[5]
        mrt = num[6]
        latitude = num[7]
        longitude = num[8]
        images = num[9]
        myresults = {
                    "id": id,
                    "name": name,
                    "category": category,
                    "description": description,
                    "address": address,
                    "transport": transport,
                    "mrt": mrt,
                    "latitude": latitude,
                    "longitude": longitude,
                    "images": eval(images)
                }

        
        mydb.close()
        return Response(json.dumps({
            'data': myresults
        }, sort_keys = False), mimetype="application/json")
    except:
        return Response(json.dumps({
            "error": True,
            "message": "伺服器錯誤"
        }, sort_keys = False), mimetype="application/json"), 500
        
@api.route("/api/categories", methods=['GET'])
def categories():
    try:
        sql = """
            SELECT DISTINCT category FROM attractions
        """
        mydb = db_connection()
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        num = mycursor.fetchall()
        myresult=[]
        for i in num:
            category = i[0]
            myresult.append(category)
            result = {
                "data": myresult
            }
        return jsonify(result)
    except:
        return Response(json.dumps({
            "error": True,
            "message": "伺服器錯誤"
        }, sort_keys = False), mimetype="application/json"), 500
