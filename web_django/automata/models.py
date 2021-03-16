from django.db import models

# Create your models here.


class Automata(models.Model):
    types_of_automata = [('rrww', 'restarting with writing'),
                         ('rww', 'restarting with dd')]
    deterministic_choices = [
        ("0", "False"), ("1", "True"),  ("2", "Don't know")]
    name = models.CharField(max_length=30)
    json_specification = models.JSONField()
    published_date = models.DateField('date published')
    # deterministic = models.Choices(deterministic_choices)
    # type_of_automata = models.Choices(types_of_automata)

    def __str__(self):
        return self.name
