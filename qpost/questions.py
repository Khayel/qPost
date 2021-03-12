class Question(dict):
    """
    Extended dict for questions
    {   'q_id': '1',
        'user_id': '2',
        'question': 'What is a number between 1 and 3?',
        'answer': [(answer, a_id, is_answer)]
            answer - answer string
            a_id - answer unique id
            is_answer -  true if the answer is selected as an answer for a question false otherwise
        }
    """

    def __init__(self, q, answers=[], q_id=-1, user_id=-1):
        self['id'] = q_id
        self['question'] = q
        self['answers'] = answers
        self['user_id'] = user_id
