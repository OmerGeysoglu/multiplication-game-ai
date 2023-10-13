import random

class QuestionGenerator:
    def __init__(self, min_number=1, max_number=10):
        self.min_number = min_number
        self.max_number = max_number
        self.num1 = 0
        self.num2 = 0

    def generate_question(self):
        self.num1 = random.randint(self.min_number, self.max_number)
        self.num2 = random.randint(self.min_number, self.max_number)
        correct_answer = self.num1 * self.num2
        return "What should be in the missing number _ x {} = {}?".format(self.num2,correct_answer)
    
    def checkAnswer(self,numRaised):
        if(numRaised == self.num1):
            return True
        else:
            return False