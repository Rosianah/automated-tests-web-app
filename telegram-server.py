from flask import Flask, request           # import flask
import logging, json, os, telethon.sync, time, difflib, re, traceback, Levenshtein, asyncio
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
from telethon.sync import TelegramClient, events
from flask_cors import CORS

app = Flask(__name__) # create an app instance
CORS(app)

class TelegramInterface():
    # @app.route('/file', methods=['GET', 'POST'])
    # def getFile(self):
    #     self.conversations = request.form.get("text")
    #     print(self.conversations)

    @app.route("/", methods = ['GET', 'POST'])
    def __init__(self):
        self.conversationReset = True
        self.test_counter = 0
        self.question_counter = 0

    def getFile(self):
        # if request.method == 'POST':
        self.conversations = request.form.get("text")
        print(self.conversations)

     #Load list of bots in bots.json file
    def loadBots(self, file):
        self.bots = self.load_json(file)

    #load json files
    def load_json(self, file):
        json_file = open(file, "rb")
        return json.load(json_file)

    #Compare expected response and bot's response
    def string_compare(self, first, second):
        ratio = difflib.SequenceMatcher(None, first, second).ratio()
        isFirstInSecond = second.find(first)
        result = ratio < 0.25 and isFirstInSecond < 0
        return result

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
        result['message'] = message
        results['results'].append(result)
        resultlog = 'results ' + time.strftime("%d-%m-%Y %H - %M", time.localtime(self.start)) + '.json'
        if os.path.exists(resultlog):
            res = open(resultlog, 'w')
        else:
            res = open(resultlog, 'w+')

        json.dump(results, res, indent=4)
        res.close

    def run_test(self):
        self.start = time.time()
        api_id = 1051818
        api_hash = 'c12711744c64b21019251856f1bd4acd'

        with TelegramClient('anon', api_id, api_hash) as client:

            results = {'results': [], 'start': time.asctime(time.localtime(self.start)),
                       'conversations': len(self.conversations['tests'])}

            # reset conversation if not conversation reset is true
            if self.conversationReset is False:
                client.send_message(id, self.conversations['tests'][self.test_counter]['questions'][self.question_counter])
            else:
                client.send_message(id, 'Reset')
                self.conversationReset = False

            # wait for a response from telegram
            @client.on(events.NewMessage)
            async def my_event_handler(event):
                try:
                    done = False
                    testPassed = True
                    expectedResponses = []

                    if self.conversationReset:
                        await client.send_message(id, 'Reset')
                        self.conversationReset = False
                    else:
                        result = {}
                        testtitle = 'Test ' + self.conversations['tests'][self.test_counter][
                            'title'] + ': '  # displayed at the status bar
                        title = str(self.test_counter + 1) + '. ' + self.conversations['tests'][self.test_counter][
                            'title']  # will be dispalyed in the results file
                        question = self.conversations['tests'][self.test_counter]['questions'][
                            self.question_counter]  # question from conversation files
                        if event.raw_text.find('you can now start afresh') < 0:
                            expectedResponses = self.conversations['tests'][self.test_counter]['expectedResponses'][
                                self.question_counter]

                        result['name'] = title
                        test_message = ''
                        test_status = ''
                        # if any errors occur
                        if event.sender_id == id:
                            if event.raw_text.find('experiencing difficulty') >= 0:
                                # bot has crashed
                                test_message = 'Bot crashed at ' + question + '(' + str(self.question_counter) + ')'
                                test_status = 'Failed'
                                done = True
                                
                            elif event.raw_text.find('404') >= 0:
                                # bot has crashed
                                test_message = 'Bot unreacheable, crashed at ' + question + '(' + str(
                                    self.question_counter) + ')'
                                test_status = 'Failed'
                                done = True
                            elif event.raw_text.find('403') >= 0:
                                # bot has crashed
                                test_message = 'Bot\'s endpoint failed with HTTP status 403, crashed at ' + question + '(' + str(
                                    self.question_counter) + ')'
                                test_status = 'Failed'
                                done = True
                            elif event.raw_text.find('502') >= 0:
                                # bot has crashed
                                test_message = 'Bot connection strings wrong, Bot crashed at ' + question + '(' + str(
                                    self.question_counter) + ')'
                                test_status = 'Failed'
                                done = True
                            elif event.raw_text.find('500') >= 0:
                                # bot has crashed
                                test_message = 'Bot code has a problem, Bot crashed at ' + question + '(' + str(
                                    self.question_counter) + ')'
                                test_status = 'Failed'
                                done = True
                            else:
                                if event.raw_text.find('timed out') < 0 and event.raw_text.find(
                                        'endpoint failed') and event.raw_text.find('.jpg') < 0 and event.raw_text.find(
                                        '.png') < 0:
                                    if event.raw_text.find('you can now start afresh') < 0:
                                        responses = self.getExpectedtext(expectedResponses)
                                        # calll the string-comapre method. Compare's string in expected response and the rawText from the bot
                                        if isinstance(responses, list):
                                            for expectedResponse in responses:
                                                comparisson = self.string_compare(expectedResponse,
                                                                                  re.sub('<.*>', '', event.raw_text))
                                                if comparisson == True:
                                                    testPassed = True

                                    # if test passed, go to the next test or end the tests if the all the tests in the conversation file have been run
                                    if testPassed:
                                        if self.question_counter < len(
                                                self.conversations['tests'][self.test_counter]['questions']) - 1:
                                            if event.raw_text.find('you can now start afresh') < 0:
                                                self.question_counter += 1
                                        else:
                                            self.question_counter = 0
                                            test_status = 'Test Passed'
                                            test_message = 'Test Result: ' + 'Passed'
                                            result['input'] = question
                                            result['status'] = test_status
                                            if self.test_counter < len(self.conversations['tests']) - 1:
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
                                        result['bot response'] = event.raw_text

                                        result['message'] = test_message
                                        if self.test_counter < len(self.conversations['tests']) - 1:
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
                                await client.disconnect()

                            # if tests are not done, continue with the next tests
                            else:
                                if self.conversationReset is False:
                                    if event.raw_text.find('is likely') < 0 and event.raw_text.find(
                                            'timed out') < 0 and event.raw_text.find(
                                            'endpoint failed') and event.raw_text.find(
                                            '.jpg') < 0 and event.raw_text.find('.png') < 0:
                                        question = self.conversations['tests'][self.test_counter]['questions'][
                                            self.question_counter]
                                        if question:
                                            await event.reply(question)
                                else:
                                    if event.raw_text.find('is likely') < 0:
                                        await client.send_message(id, 'Reset')
                                        self.conversationReset = False
                except Exception as e:
                    tb = traceback.format_exc()
                    print(e)
                    await client.disconnect()
                else:
                    tb = "No error"
                finally:
                    print(tb)

            client.start()
            client.run_until_disconnected()

if __name__ == "__main__":        # on running python app.py
    app.run(port=5001, debug=True)   