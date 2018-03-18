from __future__ import print_function
import json
from flask import Flask,request,make_response,session
import logging
from logging import Formatter, FileHandler
from time import gmtime, strftime

app = Flask(__name__)
@app.route('/webhook', methods=['POST'])
def Image():
        app.logger.debug("Inside function Form2")
        req = request.get_json(silent=True, force=True)
        app.logger.debug("Request json:"+str(req))
        print (json.dumps(req, indent=4, sort_keys=True))
        res = processRequest(req)
        res = json.dumps(res, indent=4)
        app.logger.debug("Response json:"+res)
        r = make_response(res)
        r.headers['Content-Type'] = 'application/json'
        app.logger.debug("Response json:"+ str(r))
        return r


def processRequest(req):
    if(req.has_key("result")):
        if(req["result"].has_key("resolvedQuery")):
            if(req.get("result").get("resolvedQuery").startswith("FACEBOOK_MEDIA")):
                attach=req["originalRequest"]["data"]["data"]["message"]["attachments"]
                print(attach)
                imageData=attach[0]
                if(imageData["type"]=="image"):
                    return imageData["payload"]["url"] 
    
    if(req.has_key("queryResult")):
        intentName=req.get("queryResult").get("intent").get("displayName")
    else:
        intentName=req.get("result").get("metadata").get("intentName")
    print(intentName)


    if ( intentName == 'Facebook'):
        return facebookResult()

    res=intent(intentName,req)
    if(req.has_key("queryResult")):
        res = makeWebhookResultV2(res)
    else:
        res = makeWebhookResultV1(res)
    return res
    

def intent(x,req):
    if (x=='Default Welcome Intent'):
        return DefaultResponse(req)
    if (x == 'Default Fallback Intent'):
        return DefaultResponse(req)

    else:
        return DefaultResponse(req)

def DefaultResponse(req):
        return 'Sorry I do not understand that but I am learning new stuff.'




def facebookResult():
    return{
    "messages": 
    [
              {
                "buttons": 
                [
                    {
                        "postback": "https://www.macys.com/shop/product/jessica-howard-lasercut-bell-sleeve-dress-regular-petite-sizes?ID=5730174&CategoryID=170144",
                        "text": "Planet Gold Juniors Dress, Short Sleeve Space-Dye A-Line"
                    }
                ],
                "imageUrl": "http://slimages.macys.com/is/image/MCY/products/0/optimized/1564570_fpx.tif?bgc=255,255,255&amp;wid=100&amp;qlt=90&amp;layer=comp&amp;op_sharpen=0&amp;resMode=bicub&amp;op_usm=0.7,1.0,0.5,0&amp;fmt=jpeg",
                "platform": "facebook",
                "subtitle": "",
                 "title": "Recommendation 1",
                 "type": 1
              }
    ]
    }

def makeWebhookResultV2(speech,fullfillment="",flag=1):
    return {
  "fulfillmentText": speech,
  "source": speech,
  "followupEventInput": ""
}

def makeWebhookResultV1(speech,fullfillment="",flag=1):
      return {
        "followupEvent": {
            "name": fullfillment
        },
        "speech": speech,
        "displayText": speech,
        "source": "apiai-webhook-rebecca"
    }





if __name__ == '__main__':
    file_handler = FileHandler('output.log')
    handler = logging.StreamHandler()
    file_handler.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    handler.setFormatter(Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(handler)
    app.logger.addHandler(file_handler)
    app.logger.warning('Server started at '+strftime("%Y-%m-%d %H:%M:%S", gmtime()) )
    app.run(host='0.0.0.0', port=80,debug=False)
    app.logger.debug('Server stoped at '+strftime("%Y-%m-%d %H:%M:%S", gmtime()) )