from flask import *
import mysql.connector

api = Blueprint('api',__name__)

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

# def stringToList(string):
#     evalRes = eval(string)
#     return evalRes
    
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
        
        # 會在外層多出現[]
        # myresult = [''] * (len(num))
        # for i in range(0, len(num)):
        #     images = num[i][9].split(',')
        #     myresult[i] = {
        #         'id': num[i][0],
        #         'name': num[i][1],
        #         'category': num[i][2],
        #         'description': num[i][3],
        #         'address': num[i][4],
        #         'transport': num[i][5],
        #         'mrt': num[i][6],
        #         'latitude': num[i][7],
        #         'longitude': num[i][8],
        #         'images': [images]
        #     }
            
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
        
        # 會在外層多出現[]
        # num = mycursor.fetchall()
        # myresult = ['']
        # images = num[0][9].split(',')
        # myresult[0] = {
        #     'id': num[0][0],
        #     'name': num[0][1],
        #     'category': num[0][2],
        #     'description': num[0][3],
        #     'address': num[0][4],
        #     'transport': num[0][5],
        #     'mrt': num[0][6],
        #     'latitude': num[0][7],
        #     'longitude': num[0][8],
        #     'images': [images]
        # }
        
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
