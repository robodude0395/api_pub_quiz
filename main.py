from requests import get
from html import unescape
from random import shuffle

BASE_URL = "https://opentdb.com/api.php"

class Question:
    def __init__(self, question: dict):
        self.difficulties = {"hard":"\x1b[1;41mHARD\x1b[0m",
                             "medium": "\x1b[1;43mMEDIUM\x1b[0m",
                             "easy": "\x1b[1;43mEASY\x1b[0m"}
        self.type = unescape(question["type"])
        self.difficulty = self.difficulties[unescape(question["difficulty"])]
        self.category = unescape(question["category"])
        self.question = unescape(question["question"])
        self.correct_answer = unescape(question["correct_answer"])
        self.incorrect_answers = [unescape(q) for q in question["incorrect_answers"]]

        self.possible_answers = self.incorrect_answers.copy()
        self.possible_answers.append(self.correct_answer)

        shuffle(self.possible_answers)

    def __str__(self):
        return self.question

    def __repr__(self):
        return self.__str__()

    def display(self):
        print(f"{self.question}")
        count = 0
        for a in self.possible_answers:
            print(f"    {count}-{a}")
            count += 1

    def answer(self, input_answer: str) -> bool:
        return input_answer == self.correct_answer

    def pose(self):
        self.display()

        user_answer = -1
        while user_answer not in range(0, len(self.possible_answers)):
            user_answer = int(input("Enter your answer: "))

        if self.answer(self.possible_answers[user_answer]):
            print("\x1b[1;43mCORRECT!\x1b[0m")
        else:
            print("\x1b[1;43mWRONG\x1b[0m")

def get_questions(number: int=5,
                  difficulty: str="medium") -> list[Question]:
    """Return a set of quiz questions from the API."""

    response = get(f"{BASE_URL}?amount={number}&difficulty={difficulty}&type=multiple", timeout=10)

    return [Question(question) for question in response.json()["results"]]

if __name__ == "__main__":
    #CLI arguments for settings
    questions = get_questions(10, difficulty="medium")
    print(questions[0].difficulty)
    for q in questions:
        print()
        q.pose()