from celery import shared_task
from app.models import ToDoApp

# ======================================================================================================================
@shared_task
def delete_task():
    ToDoApp.objects.all().delete()
    return "Completed tasks deleted"
# ======================================================================================================================