from django.db import models
from django.contrib.auth import get_user_model

# Dynamically fetches the user model, ensuring flexibility in case of custom user models
User = get_user_model()


# ======================================================================================================================
# ToDoApp: A model representing tasks or notes created by users
class ToDoApp(models.Model):
    """
    This model stores individual to-do tasks associated with a specific user.
    """

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Links each task to a user (author) using a ForeignKey relationship.
    # If the user is deleted, all associated tasks will also be deleted (CASCADE).

    content = models.TextField()
    # Stores the actual task content or note.

    created_date = models.DateTimeField(auto_now_add=True)
    # Automatically sets the date and time when a task is created.

    updated_date = models.DateTimeField(auto_now=True)
    # Updates the timestamp whenever the task is modified.

    def __str__(self):
        """
        Returns the task content as the string representation of the object.
        """
        return self.content


# ======================================================================================================================
