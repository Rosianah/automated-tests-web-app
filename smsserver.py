from quart import Quart, websocket, request, session 
import requests 
import logging, json, os, telethon.sync, time, difflib, re, traceback, Levenshtein, asyncio
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
from quart_cors import cors
from configparser import ConfigParser

app = Quart(__name__) # create an app instance
app = cors(app, allow_origin="*")
app.config['SESSION_TYPE'] = 'filesystem'
app.secret_key = 'super secret key'


 
class SMSInterface(): 
    #Send to the bot's endpoint
    def __init__(self, url = 'http://52.136.249.181:4000/webhook'):
        # self.url=url+"/webhook"
        self.url=url

        self.conversationReset = True
        self.test_counter = 0
        self.question_counter = 0

     #Function to post the message
    def post(self, text):

        config_object = ConfigParser()
        config_object.read("config.ini")
        SMSinfo = config_object['SMSINFO']
        _to = format(SMSinfo["code"])
        _from = format(SMSinfo["phone_number"])
        print(_to, _from)

        data = {
            "from": _from,
            "to": _to,
            "text": text
        }
        res = requests.post(self.url, json=data)
        print(res.status_code)

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
                # be used to replace substrings---( re.sub(pattern,repl,string). w+ matches one or more words characters
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

    async def run_test(self):
        self.start = time.time()
        self.question_counter = 0
        self.test_counter = 0
        # reset conversation if not conversation reset is true

        #print(session.get('conversations'))
        #results = {'results': [], 'start': time.asctime(time.localtime(self.start)), 'conversations': len(session.get('conversations')['tests'])}

        if self.conversationReset is False:
            self.post(session.get('conversations')['tests'][self.test_counter]['questions'][self.question_counter])
        else:
            self.post("reset")
            self.conversationReset = False

        done = False
        testPassed = True
        expectedResponses = []

        if self.conversationReset:
            await self.post("reset")
            self.conversationReset = False
        else:
            result = {}
            testtitle = 'Test ' + session.get('conversations')['tests'][self.test_counter][
                'title'] + ': '  # displayed at the status bar
            title = str(self.test_counter + 1) + '. ' + session.get('conversations')['tests'][self.test_counter][
                'title']  # will be dispalyed in the results file
            question = session.get('conversations')['tests'][self.test_counter]['questions'][
                self.question_counter]  # question from conversation files

            if session.get('body') == 'you can now start afresh':
                expectedResponses = session.get('conversations')['tests'][self.test_counter]['expectedResponses'][self.question_counter]

            result['name'] = title
            test_message = ''
            test_status = ''

            responses = self.getExpectedtext(expectedResponses)
            # calll the string-comapre method. Compare's string in expected response and the rawText from the bot
            if isinstance(responses, list):
                for expectedResponse in responses:
                    comparisson = self.string_compare(expectedResponse,
                                                    re.sub('<.*>', '', session.get('text')))
                    if comparisson == True:
                        testPassed = True

                                # if test passed, go to the next test or end the tests if the all the tests in the conversation file have been run
                    if testPassed:
                        if self.question_counter < len(
                                session.get('conversations')['tests'][self.test_counter]['questions']) - 1:
                            if session.get('body') == 'you can now start afresh':
                                self.question_counter += 1
                        else:
                            self.question_counter = 0
                            test_status = 'Test Passed'
                            test_message = 'Test Result: ' + 'Passed'
                            result['input'] = question
                            result['status'] = test_status
                            if self.test_counter < len(session.get('conversations')['tests']) - 1:
                                self.test_counter += 1
                                self.conversationReset = True
                                self.save_result(results, result, test_status, test_message)
                            else:
                                results['Final Test Result'] = 'Test Passed'
                                self.test_counter = 0
                                done = True
                    # if tests did not pass, set the test_status to failed and show where the test_failed using the test_message
                    else:
                        test_message = 'Test Failed at : ' + str(self.question_counter)
                        self.question_counter = 0
                        test_status = 'Failed'
                        result['input'] = question
                        result['status'] = test_status

                        result['expected response'] = responses
                        result['bot response'] = session.get('body')

                        result['message'] = test_message
                        if self.test_counter < len(session.get('conversations')['tests']) - 1:
                            self.test_counter += 1
                            self.conversationReset = True
                            self.save_result(results, result, test_status, test_message)
                        else:
                            results['Final Test Result'] = 'Test Failed'
                            self.test_counter = 0
                            done = True

            # if done == True, count the successful and i=unseccessful tests,save the results and disconnect from the telegram client
            if done:
                results["results"].append(result)
                end = time.time()
                results["end"] = time.asctime(time.localtime(end))
                results["duration"] = (end - self.start) / 100
                successful = 0
                unsuccessful = 0

                for item in results["results"]:
                    if item['test_status'] == 'Failed':
                        unsuccessful += 1
                    else:
                        successful += 1

                results["successful"] = successful
                results["unsuccessful"] = unsuccessful
                final_status = "Failed" if unsuccessful > 0 else "Passed"
                self.save_result(results, {}, final_status, test_message)

            # if tests are not done, continue with the next tests
            else:
                if self.conversationReset is False:
                    if session.get('body').find('is likely') < 0 and session.get('body').find(
                            'timed out') < 0 and session.get('body').find(
                            'endpoint failed') and session.get('body').find(
                            '.jpg') < 0 and session.get('body').find('.png') < 0:
                        question = session.get('conversations')['tests'][self.test_counter]['questions'][
                            self.question_counter]
                        if question:
                            await event.reply(question)
                else:
                    if session.get('body').find('is likely') < 0:
                        await self.post('Reset')
                        self.conversationReset = False


@app.route("/file", methods = ['POST']) 
async def getFile():
    session['conversations'] =  await request.json
    print(session.get('conversations'))
    return "Ok", 200

#receive from the webhook // run ngrok first https:ngrok.io/tshdjsau7/receive (Put smthing like that in webhook app)
@app.route('/receive', methods=["POST"])
async def fetchText():
    session['text'] = await request.json
    #body = request.form.get("text")
    print(await request)
    return "200"

@app.route('/send', methods=["POST"])
async def send():
    session['conversations'] = await request.json
    print(session.get('conversations'))
    server = SMSInterface()
    await server.run_test()
    server.post("Hi")
    await fetchText()
    return "Ok", 200

if __name__ == "__main__":        # on running python app.py
    app.run()            