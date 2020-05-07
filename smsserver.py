from quart import Quart, websocket, request  
import requests 
import logging, json, os, telethon.sync, time, difflib, re, traceback, Levenshtein, asyncio
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
from quart_cors import cors

app = Quart(__name__) # create an app instance
app = cors(app)

@app.route("/file") 
def getFile(self):
    self.conversations = request.json
    print(self.conversations)
    return "Ok", 200
 
class SMSInterface():
    @app.route("/") 
    #Send to the bot's endpoint
    def __init__(self, url = 'http://51.144.49.229:8080'):
        self.url=url+"/webhook"

        self.conversationReset = True
        self.test_counter = 0
        self.question_counter = 0

    

    def string_compare(self, first, second):
            ratio = difflib.SequenceMatcher(None, first, second).ratio()
            isFirstInSecond = second.find(first)
            result = ratio < 0.25 and isFirstInSecond < 0
            return result
     #load json files
    def load_json(self, file):
        json_file = open(file, "rb")
        return json.load(json_file)

    #Dig into content/intent files to get the expected responses 
    def getExpectedtext(self, expected_response):
        filtered = {}
        jsonfile = self.load_json(expected_response["file"])  # load the file in the conversations eg intents.json
        match = [i for i in jsonfile if i["id"] == expected_response["id"]][
            -1]  # if id in json file(eg intents) matches with the id in the expected conversation (conversation.json)

        # where there are filters
        if "filters" in expected_response:
            key = expected_response["filters"]["property"]
            match = match[key]  # match with the key using the id

            for item in match:  # for key(filter, property), fields in intents
                for i in list(expected_response["filters"])[1:]:  # for any item in list of filters
                    if item[i] == expected_response["filters"][
                        i]:  # if items in the filters match with the expected response
                        filtered = item
        else:
            filtered = match

        keys = expected_response["property"].split(".")  # split where there's . eg prompts.promptWithHints

        if len(keys) > 1:
            filtered = filtered[keys[0]]
            if isinstance(filtered, dict):
                filtered = filtered[keys[1]]

        # call the find keys function
        key_results = self.findkeys(filtered, keys[-1])
        return self.remove_placeholders(list(key_results))

        # recursive function

    def findkeys(self, node, kv):
        if isinstance(node, list):
            for i in node:
                for x in self.findkeys(i, kv):
                    yield x
        elif isinstance(node, dict):
            if kv in node:
                yield node[kv]
            for j in node.values():
                for x in self.findkeys(j, kv):
                    yield x

    def remove_placeholders(self, items):
        formated_string = []
        for i in items:
            if isinstance(i, list):
                # be used to replace substrings---( re.sub(pattern,repl,string). w+ matches one or more words / characters
                [formated_string.append(re.sub("\$\w+", '', j)) for j in i]
            else:
                formated_string.append(re.sub("\$\w+", '', i))
        return formated_string

        # save results after running a test

    #Saving the test results
    def save_result(self, results, result, status, message):
        result['status'] = status
        self.start = time.time()
        result['message'] = message
        results['results'].append(result)
        resultlog = 'results ' + time.strftime("%d-%m-%Y %H - %M", time.localtime(self.start)) + '.json'
        if os.path.exists(resultlog):
            res = open(resultlog, 'w')
        else:
            res = open(resultlog, 'w+')

        json.dump(results, res, indent=4)
        res.close

        #Function to post the message
        def post(self, text):
            data = {
                "from": "+254710535946",
                "to": "21393",
                "text": text
            }
            res = requests.post(self.url, json=data)
            print(res.status_code)

        def run_test(self):
            # conversations from TelegramInterface.selectfile
            testNumbers = self.load_json("testers.json")
            self.question_counter = 0
            self.test_counter = 0
            self.conversations = self.load_json("_conversations.json")

            # reset conversation if not conversation reset is true
            if self.conversationReset is False:
                self.post(self.conversations['tests'][self.test_counter]['questions'][self.question_counter])
            else:
                self.post("reset")
                self.conversationReset = False

#receive from the webhook // run ngrok first https:ngrok.io/tshdjsau7/receive (Put smthing like that in webhook app)
@app.route('/receive', methods=["POST"])
def fetchText(self):
    body = request.form.get("text")
    print(body)
    return "200"

if __name__ == "__main__":        # on running python app.py
    app.run()            