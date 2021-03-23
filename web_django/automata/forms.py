from django import forms


class InputAutomata(forms.Form):
    text = forms.CharField(label='Post:', max_length=2000,
                           widget=forms.Textarea(attrs={'rows': '10', 'cols': '50'}))
    file = forms.FileField()


class InputWord(forms.Form):
    word = forms.CharField()


class InputLogLevel(forms.Form):
    log_level = forms.ChoiceField(choices=[
        ("0", "just result"),
        ("1", "cycle"),
        ("2", "instruction")
    ])


class InputInt(forms.Form):
    number = forms.IntegerField(max_value=5, min_value=1)
