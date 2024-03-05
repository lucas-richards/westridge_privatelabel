from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskCreateForm, TaskUpdateFormAssignee, TaskUpdateFormAuthor

@login_required
def home(request):
    tasks = Task.objects.filter(assignee=request.user)
    print('tasks', tasks)
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        try:
            task_instance = Task.objects.get(pk=task_id)
            
            # Create a form instance with the posted data
            form = TaskUpdateFormAssignee(request.POST, instance=task_instance)
            
            if form.is_valid():
                
                form.save()
                messages.success(request, f'{task_instance} task has been updated!')
            else:
                messages.error(request, 'Form is not valid. Please check the entered data.')

        except Task.DoesNotExist:
            messages.error(request, f'task with ID {task_id} does not exist.')

        return redirect('tasks-home')

    # Create forms for each task using the StatusUpdateForm
    forms = [TaskUpdateFormAssignee(instance=task) for task in tasks]
    formswithtasks = zip(tasks, forms)
    
    sidepanel = {
        'title': 'Tasks',
        'text1': '',
        'text2': 'Due dates',
    }
    
    context = {
        'title': 'Home',
        'sidepanel': sidepanel,
        'tasks': tasks,
        'forms': forms,
        'formswithtasks': formswithtasks
    }
    return render(request, 'tasks/home.html', context)




