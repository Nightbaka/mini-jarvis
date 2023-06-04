import asyncio
from EdgeGPT import Chatbot, ConversationStyle
from EdgeUtils import Query
import json

class QuestionHandler:

    def __init__(self):
        self.prompt = None

    def ask(self, request):
        self.prompt = Query(request)
        return self.prompt.output
        