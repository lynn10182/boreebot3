import asyncio
import random
import re
import os

class Equiz:

    def __init__(self, client, win_limit=10, hint_time=30):
        self.__running = False
        self.current_question = None
        self._win_limit = win_limit
        self._hint_time = hint_time
        self._questions = []
        self._asked = []
        self.scores = {}
        self._client = client
        self._quiz_channel = None
        self._cancel_callback = True

    datafiles = os.listdir('Equizdata')
    for df in datafiles:
        filepath = 'Equizdata' + os.path.sep + df
        self._load_questions(filepath)
        print('Loaded: ' + filepath)
    print('Equiz data loading complete.\n')



    def _load_questions(self, question_file):
        with open(question_file, encoding='utf-8', errors='replace') as qfile:
            lines = qfile.readlines()

        question = None
        category = None
        answer = None
        regex = None
        position = 0

        while position < len(lines):
            if lines[position].strip().startswith('#'):
                position += 1
                continue
            if lines[position].strip() == '':
                if question is not None and answer is not None:
                    q = Question(question=question, answer=answer, 
                                 category=category, regex=regex)
                    self._questions.append(q)

                question = None
                category = None
                answer = None
                regex = None
                position += 1
                continue

            if lines[position].strip().lower().startswith('category'):
                category = lines[position].strip()[lines[position].find(':') + 1:].strip()
            elif lines[position].strip().lower().startswith('question'):
                question = lines[position].strip()[lines[position].find(':') + 1:].strip()
            elif lines[position].strip().lower().startswith('answer'):
                answer = lines[position].strip()[lines[position].find(':') + 1:].strip()
            elif lines[position].strip().lower().startswith('regexp'):
                regex = lines[position].strip()[lines[position].find(':') + 1:].strip()
            position += 1


    def started(self):
        return self.__running

    def question_in_progress(self):
        return self.__current_question is not None


    async def _hint(self, hint_question, hint_number):
        if self.__running and self.current_question is not None:
            await asyncio.sleep(self._hint_time)
            if (self.current_question == hint_question 
                 and self._cancel_callback == False):
                if (hint_number >= 5):
                    await self.next_question(self._channel)
                
                hint = self.current_question.get_hint(hint_number)
                await self._client.send_message(self._channel, "힌트 {}: {}".format(hint_number, hint), tts=True)
                if hint_number < 5:
                    await self._hint(hint_question, hint_number + 1) 


    async def start(self, channel):
        if self.__running:
            await self._client.send_message(channel, 
             "퀴즈가 이미 {}에서 진행중입니다. !stop 또는 !halt 메시지로 퀴즈를 끝낼 수 있습니다.".format(self._channel.name), tts=True)
        else:
            await self.reset()
            self._channel = channel
            await self._client.send_message(self._channel, "퀴즈가 10초 후에 시작합니다.", tts=True)
            await asyncio.sleep(10)
            self.__running = True
            await self.ask_question()


    async def reset(self):
        if self.__running:
            await self.stop()

        self.current_question = None
        self._cancel_callback = True
        self.__running = False
        self._questions.append(self._asked)
        self._asked = []
        self.scores = {}


    async def stop(self):
        if self.__running:
            await self._client.send_message(self._channel, "퀴즈가 끝났습니다.", tts=True)
            if(self.current_question is not None):
                await self._client.send_message(self._channel, 
                     "이 문제의 정답은: {}".format(self.current_question.get_answer()), tts=True)
            await self.print_scores()
            self.current_question = None
            self._cancel_callback = True
            self.__running = False
        else:
            await self._client.send_message(self._channel, "퀴즈가 진행중이질 않습니다. 시작하세요. !ask 또는 !quiz", tts=True)


    async def ask_question(self):
        if self.__running:
            qpos = random.randint(0,len(self._questions) - 1)
            self.current_question = self._questions[qpos]
            self._questions.remove(self.current_question)
            self._asked.append(self.current_question)
            await self._client.send_message(self._channel, 
             "문제 {}: {}".format(len(self._asked), self.current_question.ask_question()), tts=True)
            self._cancel_callback = False
            await self._hint(self.current_question, 1)


    async def next_question(self, channel):
        if self.__running:
            if channel == self._channel:
                await self._client.send_message(self._channel, 
                         "다음 질문으로 넘어갑니다. 이전 문제의 정답은 {}.".format(self.current_question.get_answer()), tts=True)
                self.current_question = None
                self._cancel_callback = True
                await self.ask_question()

            
    
    async def answer_question(self, message):
        if self.__running and self.current_question is not None:
            if message.channel != self._channel:
                pass

            if self.current_question.answer_correct(message.content):
                self._cancel_callback = True

                if message.author.name in self.scores:
                    self.scores[message.author.name] += 1
                else:
                    self.scores[message.author.name] = 1
                               
                await self._client.send_message(self._channel, 
                 "잘하셨습니다. {}님. 정답은: {}".format(message.author.name, self.current_question.get_answer()), tts=True)
                self.current_question = None

                if self.scores[message.author.name] == self._win_limit:
                    
                    await self.print_scores()
                    await self._client.send_message(self._channel, "{}님이 성공하셨습니다! 축하합니다.".format(message.author.name), tts=True)
                    self._questions.append(self._asked)
                    self._asked = []
                    self.__running = False            

                elif len(self._asked) % 5 == 0:
                    await self.print_scores()                    
                
                    
                await self.ask_question()        




    async def print_scores(self):
        if self.__running:
            await self._client.send_message(self._channel,"퀴즈 결과입니다.", tts=True)
        else:
            await self._client.send_message(self._channel,"가장 최근의 퀴즈 결과입니다.", tts=True)
            
        highest = 0
        for name in self.scores:
            await self._client.send_message(self._channel,'{}:\t{}'.format(name,self.scores[name]), tts=True)
            if self.scores[name] > highest:
                highest = self.scores[name]
                
        if len(self.scores) == 0:
            await self._client.send_message(self._channel,"결과가 없습니다.", tts=True)
                
        leaders = []
        for name in self.scores:
            if self.scores[name] == highest:
                leaders.append(name)
                
        if len(leaders) > 0:
            if len(leaders) == 1:
                await self._client.send_message(self._channel,"현재 1등: {}".format(leaders[0]), tts=True)
            else:
                await self._client.send_message(self._channel,"1등: {}".format(leaders), tts=True)





class Question:
    def __init__(self, question, answer, category=None, author=None, regex=None):
        self.question = question
        self.answer = answer
        self.author = author
        self.regex = regex
        self.category = category
        self._hints = 0


    def ask_question(self):
        question_text = ''
        if self.category is not None:
            question_text+='({}) '.format(self.category)
        else:
            question_text+="(일반) "
        if self.author is not None:
            question_text+="문제 냅니다. {}님. ".format(self.author)
        question_text += self.question
        return question_text


    def answer_correct(self, answer):
        if self.regex is not None:
            match = re.fullmatch(self.regex.strip(),answer.strip())
            return match is not None


        return  answer.lower().strip() == self.answer.lower().strip()


    def get_hint(self, hint_number):
        hint = []
        for i in range(len(self.answer)):
            if i % 5 < hint_number:
                hint = hint + list(self.answer[i])
            else:
                if self.answer[i] == ' ':
                    hint += ' '
                else:
                    hint += '-'
                    
        return ''.join(hint)


    def get_answer(self):
        return self.answer
