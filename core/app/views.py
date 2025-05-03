from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ToDoApp

# ======================================================================================================================
# TaskListView: A class-based view for displaying a list of tasks
class TaskListView(ListView):
    """
    This view retrieves and displays a list of all tasks.
    """
    template_name = "main/todo.html"  # Specifies the template used to render the task list
    context_object_name = "posts"  # Sets the name used to reference the tasks in the template

    def get_queryset(self):
        """
        Returns the queryset containing all tasks from the database.
        """
        task = ToDoApp.objects.all()  # Retrieves all tasks
        return task

# ======================================================================================================================
# CreateTaskView: A class-based view for creating new tasks
class CreateTaskView(LoginRequiredMixin, CreateView):
    """
    This view allows authenticated users to create new tasks.
    """
    model = ToDoApp  # Specifies the model that this view interacts with
    fields = ('author', 'content',)  # Defines the fields available in the task creation form
    template_name = "main/todolist_form.html"  # Specifies the template used for task creation
    success_url = "/"  # Redirects the user to the task list page upon successful task creation

    def form_valid(self, form):
        """
        Saves the form data and calls the parent method to finalize validation.
        """
        form.save()  # Saves the new task to the database
        return super().form_valid(form)

# ======================================================================================================================
# DeleteTaskView: A class-based view for deleting tasks
class DeleteTaskView(LoginRequiredMixin, DeleteView):
    """
    This view enables authenticated users to delete tasks.
    """
    model = ToDoApp  # Specifies the model from which objects can be deleted
    template_name = "main/todolist_confirm_delete.html"  # Specifies the template used for delete confirmation
    success_url = "/"  # Redirects the user to the task list page upon successful deletion

# ======================================================================================================================
# UpdateTaskView: A class-based view for updating existing tasks
class UpdateTaskView(LoginRequiredMixin, UpdateView):
    """
    This view allows authenticated users to modify existing tasks.
    """
    model = ToDoApp  # Specifies the model to be updated
    fields = ('author', 'content',)  # Defines the fields available for editing
    template_name = "main/todolist_form.html"  # Specifies the template used for task updates
    success_url = "/"  # Redirects the user to the task list page upon successful update

# ======================================================================================================================