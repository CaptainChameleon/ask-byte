from django.db import models

# Create your models here.


class QuestionCategory(models.Model):
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey('self', related_name='subcategory',
                                        on_delete=models.CASCADE,
                                        null=True, blank=True)

    def __str__(self):
        return self.name


class UserQuestion(models.Model):
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text
