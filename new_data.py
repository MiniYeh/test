import json
import mysql.connector
#from encodings import utf_8

#使用 try 測試內容是否正確
def db_connection():
    mydb = None
    try:
        mydb = mysql.connector.connect(
            host = "localhost",
            port = 3306,
            user = "root",
            database = "travel_1119",
            password = " ",
                # auth_plugin = "mysql_native_password",
            charset = "utf8"
        )
    except mysql.connector.Error as e:
        print(e)
    return mydb

mydb = db_connection()
mycursor = mydb.cursor()

def stringToList(string):
    listRes = list(string.split(" "))
    return listRes

#讀取檔案/讀取 json 格式

# with open('taipei-attractions.json', mode ='r', encoding='utf-8') as file:
#     data = file.read()
#     obj = json.loads(data)
#     info = obj['result']['results']

data = open('taipei-attractions.json', 'r', encoding='utf-8').read()
obj = json.loads(data)
information = obj["result"]["results"]

for i in information:
    id = i["_id"]
    name = i["name"]
    category = i["CAT"]
    description = i["description"]
    address = i["address"].replace(' ', '')
    transport = i["direction"]
    mrt = i["MRT"]
    lat = i["latitude"]
    lng = i["longitude"]
    imgs = i["file"].split("http")

    img_list =[]
    for j in imgs:
        #問這個
        suffixes =("JPG", "PNG", "jpg", "png")
        if j.endswith(suffixes) !=True or j == '':
            continue
        images = 'http'+j
        img_list.append(images)
    img_list = str(img_list)

    sql = """
        INSERT INTO attractions (id, name, category, description, address, transport, mrt, lat, lng, imgs)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    val = (id, name, category, description, address, transport, mrt, lat, lng, img_list, )
    mycursor.execute(sql, val)        
    mydb.commit()
mydb.close()
    