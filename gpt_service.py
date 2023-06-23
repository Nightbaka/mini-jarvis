import asyncio
from EdgeGPT import Chatbot, ConversationStyle
from EdgeUtils import Query
import json
import time

class QuestionHandler:

    def __init__(self):
        self.prompt = None

    def ask(self, request):
        self.prompt = Query(request)
        try:
            text = self.prompt.output
        except KeyError:
            test = "Unfortunately there was an error with the request. Please try again."
        except Exception as e:
            test = "Unfortunate error: ```/n" + str(e) + "```"
        finally:
            return text


        