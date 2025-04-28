from django.views.generic import ListView,CreateView,DeleteView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ToDoApp
# ======================================================================================================================
class TaskListView(ListView):
    template_name = "main/todo.html"
    context_object_name = "posts"
    def get_queryset(self):
        task=ToDoApp.objects.all()
        return task
# ======================================================================================================================
class CreateTaskView(LoginRequiredMixin,CreateView):
    model = ToDoApp
    fields = ('author','content',)
    template_name = "main/todolist_form.html"
    success_url = "/"
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
# ======================================================================================================================
class DeleteTaskView(LoginRequiredMixin,DeleteView):
    model=ToDoApp
    template_name = "main/todolist_confirm_delete.html"
    success_url = "/"
# ======================================================================================================================
class UpdateTaskView(LoginRequiredMixin,UpdateView):
    model=ToDoApp
    fields = ('author','content',)
    template_name = "main/todolist_form.html"
    success_url = "/"
# ======================================================================================================================