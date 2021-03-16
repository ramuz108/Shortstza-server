import requests
import pymysql
usr = "o_612l4crd6l"
pwd = "Thunder.899"
from flasgger import Swagger
from flask import Flask,request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from cachetools import cached, TTLCache 

cache = TTLCache(maxsize=100, ttl=5) #limits caching to 5 seconds
app = Flask(__name__)
swagger = Swagger(app) #swagger plugin
db = pymysql.connect("localhost","shortstza","Sunnykuttan@108..","shortstza")
cursor = db.cursor()
limiter = Limiter(
    app,
    key_func=get_remote_address,
    
) #rate limiter
cors = CORS(app) #CORS

@limiter.limit("5 per minute")
@app.route('/api/test',methods = ['GET'])
@cached(cache)
def test():
   """Used to run unit tests to the endpoint
    ---
    responses:
      200:
        description: The server is alive and connected.
        
    """
   return {"status": "OK"}

@limiter.limit("10 per minute")
@app.route('/api/v1/shorten',methods = ['POST'])
@cached(cache)
def shorten():
    """Shortens the url entered using muliple integrations
    ---
    parameters:
      - name: url
        in: query
        type: string
        required: true
    definitions:
      url:
        type: string
    responses:
      200:
        description: Returns the shortened url.
      429:
        description: Request limit exceeded. Try again after sometime.
        
    """
    params = request.args
    url = params.get('url')
    query = "INSERT INTO urls(long_url,short_url) VALUES(%s,%s)" 
    if url == "": #if the input is empty
        return {"error":"No URL Found!"}
    else:
        if url.find("http://") != -1 or url.find("https://") != -1 : #if url is valid
            cursor.execute("SELECT short_url FROM urls WHERE long_url=%s", url)
            data = cursor.fetchone() #search if the url is already shortened to maintain high availability
            if data:
                return {"url":data}
            else:
                print("No data")
                x = bitly(url) #external api integration
                if x == "error" or x == "!GUID" or x == "!TOKEN": #in case of any load/downtime
                    y = cutly(url)   #second api integration
                    if y == "!ERROR":
                        return {"error":"01"}
                    else:
                        cursor.execute(query,(url,y)) #insert into the shortened database
                        db.commit()
                        return {"url":y}
                else:
                    cursor.execute(query,(url,x))
                    db.commit()
                    return {"url":x}
        else:
            return {"error":"URL doesnt seem to be valid!"}
    

def bitly(url):
    auth_resp = requests.post("https://api-ssl.bitly.com/oauth/access_token",auth=(usr,pwd))
    if auth_resp.status_code == 200:
        token = auth_resp.content.decode()
        print("Token:",token)
        headers = {"Authorization": f"Bearer {token}"}
        groups = requests.get("https://api-ssl.bitly.com/v4/groups",headers = headers)
        if groups.status_code == 200:
            gdata = groups.json()['groups'][0]
            guid = gdata['guid']
            shorten = requests.post("https://api-ssl.bitly.com/v4/shorten",json ={"group_guid": guid,"long_url": url}, headers = headers)
            if shorten.status_code ==200:
                link = shorten.json()['link']
                return(link)
            else:
                return("error")
        else:
            return("!GUID")
    else:
        return("!TOKEN")

def cutly(url):
    key = "a76e6e8cbe8c260736a8d1cf9811f7f76b0bd"
    req = f"https://cutt.ly/api/api.php?key={key}&short={url}"
    data = requests.get(req).json()["url"]
    if data["status"] == 7:
        shortened = data["shortLink"]
        return(shortened)
    else:
        return("!ERROR")

if __name__ == '__main__':
   app.run(host='0.0.0.0')
