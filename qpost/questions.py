class Question(dict):
    """
    Extended dict for questions
    {'question': 'What is a number between 1 and 3?',
                                  'answer': ['1', '2', '3']}
    """

    def __init__(self, q, answers=[], q_id=-1):
        self['id'] = q_id
        self['question'] = q
        self['answers'] = answers

    def new_answer(self, n):
        self['answers'].append(n)
        return self['answers']
