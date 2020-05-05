from django import forms

from .models import Answer, Quiz


class QuizForm(forms.Form):

    def __init__(self, quiz, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False

        for question in quiz.get_questions():
            choices = [(answer.id, answer.text) for answer in question.get_answers()]
            self.fields[str(question.id)] = forms.ChoiceField(
                label=question.text, choices=choices, widget=forms.RadioSelect()
            )

    def clean(self):
        '''
            Calculate total percentage of correct answers and store it
            inside self.cleaned_data['result'].
        '''
        cleaned_data = super().clean()

        answers = {}
        correct_answers = 0

        for question_id, answer_id in cleaned_data.items():
            if Answer.objects.get(id=answer_id).is_correct:
                correct_answers += 1
            answers[question_id] = answer_id

        cleaned_data['answers'] = answers
        cleaned_data['result'] = int((correct_answers / len(self.fields)) * 100)

        return cleaned_data
