from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, BoardForm, TaskForm
from .models import Board, Column, Task

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'boards/register.html', {'form': form})

@login_required
def dashboard_view(request):
    boards = request.user.boards.all()
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.owner = request.user
            board.save()
            Column.objects.create(board=board, title='To Do', slug='todo', order=1)
            Column.objects.create(board=board, title='In Progress', slug='in_progress', order=2)
            Column.objects.create(board=board, title='Done', slug='done', order=3)
            return redirect('dashboard')
    else:
        form = BoardForm()
    return render(request, 'boards/dashboard.html', {'boards': boards, 'form': form})

@login_required
def delete_board_view(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    if request.method == 'POST':
        board.delete()
        return redirect('dashboard')
    return render(request, 'boards/confirm_delete.html', {'object': board, 'type': 'доску'})

@login_required
def board_detail_view(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    columns = board.columns.all()

    query = request.GET.get('q', '')
    priority_filter = request.GET.get('priority', '')

    tasks = Task.objects.filter(column__board=board)
    if query:
        tasks = tasks.filter(title__icontains=query)
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    return render(request, 'boards/board_detail.html', {
        'board': board,
        'columns': columns,
        'tasks': tasks,
        'query': query,
        'priority_filter': priority_filter
    })

@login_required
def create_task_view(request, board_id):
    board = get_object_or_404(Board, id=board_id, owner=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, board=board)
        if form.is_valid():
            form.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = TaskForm(board=board)
        initial_column = request.GET.get('column')
        if initial_column:
            form.fields['column'].initial = initial_column
    return render(request, 'boards/task_form.html', {'form': form, 'board': board})

@login_required
def edit_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, column__board__owner=request.user)
    board = task.column.board
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task, board=board)
        if form.is_valid():
            form.save()
            return redirect('board_detail', board_id=board.id)
    else:
        form = TaskForm(instance=task, board=board)
    return render(request, 'boards/task_form.html', {'form': form, 'board': board})

@login_required
def delete_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id, column__board__owner=request.user)
    board_id = task.column.board.id
    if request.method == 'POST':
        task.delete()
        return redirect('board_detail', board_id=board_id)
    return render(request, 'boards/confirm_delete.html', {'object': task, 'type': 'задачу'})