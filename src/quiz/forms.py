from django import forms

from .models import Answer

class QuizForm(forms.Form):

    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.use_required_attribute = False
        for question in questions:
            field_name = f'question_{question.id}'
            choices = [(answer.id, answer.text) for answer in question.answer_set.all()]
            self.fields[field_name] = forms.ChoiceField(label=question.text, required=True, choices=choices, widget=forms.RadioSelect())

    def clean(self):
        cleaned_data = super().clean()
        correct = 0
        for question, answer_id in cleaned_data.items():
            if Answer.objects.get(id=answer_id).correct:
                correct += 1
        cleaned_data['result'] = correct / len(self.fields)
        return cleaned_data