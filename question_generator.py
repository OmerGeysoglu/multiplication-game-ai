import random

class QuestionGenerator:
    def __init__(self, min_number=1, max_number=10):
        self.min_number = min_number
        self.max_number = max_number

    def generate_question(self):
        num1 = random.randint(self.min_number, self.max_number)
        num2 = random.randint(self.min_number, self.max_number)
        correct_answer = num1 * num2
        return num1, num2, correct_answer