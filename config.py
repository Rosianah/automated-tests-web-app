from configparser import ConfigParser
from quart import Quart, websocket, request, session
from quart_session import Session 
from quart_cors import cors
from configparser import ConfigParser

app = Quart(__name__) # create an app instance
app = cors(app, allow_origin="*")
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'super secret key'

@app.route("/sms", methods = ['POST'])
async def getSMSCreds():
    # session['creds'] = await request.data
    # print(session.get('creds'))
    creds = await request.json
    print(creds)
    # print(creds[1])
    config_object = ConfigParser()

    config_object["SMSINFO"] = {
        "code": creds.get("code"),
        "Phone_number": creds.get("phone")
    }

    #Write the sections to config.ini file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    return "Ok", 200

@app.route("/telegram", methods = ['POST'])
async def getTelegramCreds():
    creds = await request.json
    print(creds)
    # print(creds[1])
    config_object = ConfigParser()

    config_object["TELEGRAMINFO"] = {
        "api_hash": creds.get("hash"),
        "api_id": creds.get("id")
    }
    #Write the sections to config.ini file
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
    return "Ok", 200

if __name__ == "__main__":   # on running python app.py
    app.run(port=5002, debug=True)   