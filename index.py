import firebase_admin
from firebase_admin import credentials, firestore
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()



from flask import Flask, render_template,request    

from datetime import datetime, timezone, timedelta

app = Flask(__name__)

@app.route("/")
def index():
    homepage = "<h1>廖彥維Python網頁</h1>"
    homepage += "<a href=/mis>MIS</a><br>"
    homepage += "<a href=/today>顯示日期時間</a><br>"
    homepage += "<a href=/welcome?nick=廖彥維>傳送使用者暱稱</a><br>"
    homepage += "<a href=/about>彥維簡介網頁</a><br>"
    homepage += "<a href=/account>帳號密碼</a><br>"
    homepage += "<br><a href=/wave>人選之人演員名單</a><br>"
    homepage += "<br><a href=/addbooks>圖書精選</a><br>"
    homepage += "<br><a href=/query>書名查詢</a><br>"
    return homepage


@app.route("/mis")
def course():
    return "<h1>資訊管理導論</h1>"

@app.route("/today")
def today():
    tz = timezone(timedelta(hours=+8))
    now = datetime.now(tz)
    return render_template("today.html",datetime = str(now))

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/welcome", methods=["GET", "POST"])
def welcome():
    user = request.values.get("nick")
    return render_template("welcome.html", name=user)
@app.route("/account", methods=["GET", "POST"])
def account():
    if request.method == "POST":
        user = request.form["user"]
        pwd = request.form["pwd"]
        result = "您輸入的帳號是：" + user + "; 密碼為：" + pwd 
        return result
    else:
        return render_template("account.html")

@app.route("/wave")
def read():
    Result = ""     
    collection_ref = db.collection("人選之人─造浪者")    
    docs = collection_ref.order_by("name", direction=firestore.Query.DESCENDING).get()    
    for doc in docs:         
        Result += "文件內容：{}".format(doc.to_dict()) + "<br>"    
    return Result

@app.route("/addbooks")
def addbooks():
    Result = ""     
    collection_ref = db.collection("圖書精選")    
    docs = collection_ref.order_by("anniversary", direction=firestore.Query.DESCENDING).get()    
    for doc in docs:         
        bk = doc.to_dict()
        Result += "書名：<a href=" +bk["url"] +">"+ bk["title"]+ "</a><br>"
        Result += "作者："+bk["author"] + "<br>"
        Result += str(bk["title"]) +"週年紀念版" "<br>"
        Result += "<img src="+bk["cover"]+ "> </img><br>"  
    return Result

@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "POST":
        keyword = request.form["keyword"]
        result = "您輸入的關鍵字是："+ keyword 
        
        Result = ""     
        collection_ref = db.collection("圖書精選")    
        docs = collection_ref.order_by("anniversary", direction=firestore.Query.DESCENDING).get()    
        for doc in docs: 
            bk = doc.to_dict() 
            if keyword in bk["title"]:       
        
                Result += "書名：<a href=" +bk["url"] +">"+ bk["title"]+ "</a><br>"
                Result += "作者："+bk["author"] + "<br>"
                Result += str(bk["anniversary"]) +"週年紀念版" "<br>"
                Result += "<img src="+bk["cover"]+ "> </img><br>"  


        return Result
    else:
        return render_template("searchbk.html")

if __name__ == "__main__":
    app.run(debug=True)
    

