from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver

from quiz_system.models import Question, Answer

# Using m2m_changed because ManyToMany relationships (like Question.attributes)
# are not saved at the same time as the model instance.
# When creating a new Question in the Django admin, the Question object is saved first,
# but the selected attributes are added only afterward through a separate step.
# Therefore, if I use post_save, instance.attributes will still be empty at that point as it was before the changes.

@receiver(m2m_changed, sender=Question.attributes.through)
def create_default_answers(sender: Question, instance: Question, action, **kwargs):
    if action == "post_add":
        if instance.answer_set.exists():
            # question is already related to an answer
            return

        attribute = instance.attributes.first()
        if not attribute:
            # if not attribute is selected
            return


        default_answers = {
            "Strongly agree": 4,
            "Agree": 3,
            "Neutral": 2,
            "Disagree": 1,
            "Strongly disagree": 0,
        }

        for text, score in default_answers.items():
            Answer.objects.create(
                question=instance,
                text=text,
                score=score,
                attribute=attribute
            )