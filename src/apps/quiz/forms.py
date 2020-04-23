from django import forms

from .models import Answer


class QuizForm(forms.Form):

    def __init__(self, quiz, *args, **kwargs):
        '''
            Construct a form for a quiz where each label is a related
            question text and each field is a ChoiceField where choices
            are related answers.
        '''
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        for question in quiz.question_set.all():
            field_name = f'question_{question.id}'
            choices = [(ans.id, ans.text) for ans in question.answer_set.all()]
            self.fields[field_name] = forms.ChoiceField(
                label=question.text, required=True,
                choices=choices, widget=forms.RadioSelect()
            )

    def clean(self):
        '''
            Calculate total percentage of correct answers and store it
            inside self.cleaned_data['result'].
        '''
        cleaned_data = super().clean()
        correct_answers = 0
        for question, answer_id in cleaned_data.items():
            if Answer.objects.get(id=answer_id).is_correct:
                correct_answers += 1
        cleaned_data['result'] = int((correct_answers / len(self.fields)) * 100)
        return cleaned_data
