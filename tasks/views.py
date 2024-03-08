from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task
from .forms import TaskCreateForm, TaskUpdateFormAssignee, TaskUpdateFormAuthor

@login_required
def home(request):
    # count of all in progress tasks
    in_progress = Task.objects.filter(assignee=request.user, status='In Progress').count()
    # count of all completed tasks
    completed = Task.objects.filter(assignee=request.user, status='Completed').count()
    # count of all not started tasks
    not_started = Task.objects.filter(assignee=request.user, status='Not Started').count()
    # get all tasks assigned to the user and order by due date but leave the completed tasks at the bottom
    tasks = Task.objects.filter(assignee=request.user).order_by('due_date')
    # move all completed tasks to the bottom
    tasks = list(tasks)
    completed_tasks = [task for task in tasks if task.status == 'Completed']
    in_progress_tasks = [task for task in tasks if task.status == 'In Progress']
    not_started_tasks = [task for task in tasks if task.status == 'Not Started']
    tasks = in_progress_tasks + not_started_tasks + completed_tasks
    print('tasks', tasks)
    if request.method == 'POST':
        task_id = request.POST.get('task_id')
        print('task_id', task_id)
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
        'title': 'My Tasks',
        'text1': '',
        'text2': 'To do list',
    }
    
    context = {
        'title': 'Home',
        'sidepanel': sidepanel,
        'tasks': tasks,
        'in_progress': in_progress,
        'completed': completed,
        'not_started': not_started,
        'forms': forms,
        'formswithtasks': formswithtasks,
        'percentage': round(completed/(in_progress+completed+not_started)*100)
    }
    return render(request, 'tasks/home.html', context)

# assigned tasks
@login_required
def assigned(request):
    # count of all in progress tasks
    in_progress = Task.objects.filter(author=request.user,status='In Progress').count()
    # count of all completed tasks
    completed = Task.objects.filter(author=request.user,status='Completed').count()
    # count of all not started tasks
    not_started = Task.objects.filter(author=request.user,status='Not Started').count()
    # get all tasks assigned to the user and order by due date but leave the completed tasks at the bottom
    tasks = Task.objects.filter(author=request.user).order_by('due_date')
    # move all completed tasks to the bottom
    tasks = list(tasks)
    completed_tasks = [task for task in tasks if task.status == 'Completed']
    in_progress_tasks = [task for task in tasks if task.status == 'In Progress']
    not_started_tasks = [task for task in tasks if task.status == 'Not Started']
    tasks = in_progress_tasks + not_started_tasks + completed_tasks
    sidepanel = {
        'title': 'Assigned Tasks',
        'text1': '',
        'text2': 'To do list',
    }
    context = {
        'title': 'Assigned',
        'sidepanel': sidepanel,
        'tasks': tasks,
        'in_progress': in_progress,
        'completed': completed,
        'not_started': not_started,
        'percentage': round(completed/(in_progress+completed+not_started)*100),
    }
    return render(request, 'tasks/assigned.html', context)

# create task
@login_required
def create(request):
    if request.method == 'POST':
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            messages.success(request, f'Task has been created!')
            return redirect('tasks-home')
    else:
        form = TaskCreateForm()
    sidepanel = {
        'title': 'Create Task',
        'text1': 'Select an assignee for the task. Write a title and description. Click on the due date to select a date.',
        'text2': '',
    }
    context = {
        'title': 'Create Task',
        'sidepanel': sidepanel,
        'form': form
    }
    return render(request, 'tasks/create.html', context)

# update task
@login_required
def update(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskUpdateFormAuthor(instance=task)
    if request.method == 'POST':
        form = TaskUpdateFormAuthor(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task has been updated!')
            return redirect('tasks-home')
    sidepanel = {
        'title': 'Update Task',
        'text1': 'Click on any box to update the task.',
        'text2': '',
    }
    context = {
        'title': 'Update Task',
        'sidepanel': sidepanel,
        'form': form
    }
    return render(request, 'tasks/create.html', context)

# delete task
@login_required
def delete(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        messages.success(request, f'Task has been deleted!')
        return redirect('tasks-home')
    sidepanel = {
        'title': 'Delete Task',
        'text1': '',
        'text2': 'Due dates',
    }
    context = {
        'title': 'Delete Task',
        'sidepanel': sidepanel,
        'task': task
    }
    return render(request, 'tasks/delete.html', context)


