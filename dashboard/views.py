import requests
from django.shortcuts import render, redirect
from .forms import *
from .models import Notes
from django.contrib import messages
from django.views.generic import DetailView
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth import logout


def home(request):
    return render(request, 'dashboard/home.html')


def notes(request):
    context = {}
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            new_note = Notes(user=request.user, title=request.POST['title'], description=request.POST['description'])
            new_note.save()
            messages.success(request, f"user {request.user.username} added a note successfully")
            return redirect('dashboard:notes')

    else:

        if request.user.is_authenticated:
            form = NotesForm()
            notes_list = Notes.objects.filter(user=request.user)
            context['notes'] = notes_list
            context['form'] = form
        else:
            context['login_required_msg'] = "you need to login first"
        return render(request, 'dashboard/notes.html', context)


def delete_note(request, pk=None):
    Notes.objects.get(pk=pk).delete()
    return redirect('dashboard:notes')


# DetailView automatically takes 'pk' from url and return the single model object associated with that 'pk'
# context data for DetailView stored in the variable which is lowercase of model (here it is 'notes')
class NotesDetailView(DetailView):
    model = Notes
    template_name = 'dashboard/notes_detail.html'


def homework(request):
    context = {}
    if request.method == 'POST':
        if request.POST.get('is_finished') == 'on':
            is_finished = True
        else:
            is_finished = False
        new_homework = Homework(user=request.user,
                                subject=request.POST['subject'],
                                title=request.POST['title'],
                                description=request.POST['description'],
                                due=request.POST['due'],
                                is_finished=is_finished)
        new_homework.save()
        messages.success(request, f"user {request.user.username} added a homework successfully")
        return redirect('dashboard:homework')

    else:
        if request.user.is_authenticated:
            form = HomeworkForm()
            finished_homeworks = Homework.objects.filter(user=request.user, is_finished=True)
            unfinished_homeworks = Homework.objects.filter(user=request.user, is_finished=False)
            context['unfinished_homeworks'] = unfinished_homeworks
            context['finished_homeworks'] = finished_homeworks
            context['forms'] = form
            if len(unfinished_homeworks) == 0:
                context["homeworks_done"] = True
            else:
                context["homeworks_done"] = False

        else:
            context['login_required_msg'] = "you need to login first"
        return render(request, 'dashboard/homework.html', context)


def update_homework(request, pk=None):
    homework = Homework.objects.get(pk=pk)
    homework.is_finished = not homework.is_finished
    homework.save()
    return redirect('dashboard:homework')


def delete_homework(request, pk):
    Homework.objects.get(id=pk).delete()
    return redirect('dashboard:homework')


def youtube(request):
    context = {}
    form = DashboardForm()
    if request.POST:
        # form = DashboardForm(request.POST)
        print("post method")
        text = request.POST['text']
        video = VideosSearch(text, limit=5)
        result_list = []
        # print(video.result()['result'])
        for i in video.result()['result']:
            try:
                result_dict = {
                    'input': text,
                    'title': i['title'],
                    'duration': i['duration'],
                    'thumbnail': i['thumbnails'][0]['url'],
                    'channel': i['channel']['name'],
                    'link': i['link'],
                    'views': i['viewCount']['short'],
                    'published': i['publishedTime']
                }
                desc = ''
                if i['descriptionSnippet']:
                    for j in i['descriptionSnippet']:
                        print(j['text'])
                        desc += j['text']
                    result_dict['description'] = desc
                result_list.append(result_dict)
                context = {"forms": form, "search_results": result_list}
                print(context["search_results"])
            except:
                context = {
                    'form': form,
                    'input': text,
                    'api_error': True
                }
                break

        return render(request, 'dashboard/youtube.html', context)

    else:
        if request.user.is_authenticated:
            print("get method")
            context["forms"] = form

        else:
            context['login_required_msg'] = "you need to login first"
        return render(request, 'dashboard/youtube.html', context)


def todo(request):
    context = {}
    if request.POST:
        todo = TodoForm(request.POST)
        if todo.is_valid():
            if request.POST.get('is_finished') == 'on':
                is_finished = True
            else:
                is_finished = False
            new_todo = Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=is_finished
            )
            new_todo.save()
            messages.success(request, f"user {request.user.username} added a todo successfully")
        return redirect('dashboard:todo')
    else:
        if request.user.is_authenticated:
            todos = Todo.objects.filter(user=request.user)
            pending_todos = Todo.objects.filter(user=request.user, is_finished=False)
            form = TodoForm()
            context = {
                'todos': todos,
                'form': form
            }
            if len(pending_todos) > 0:
                context["todos_completed"] = False
            else:
                context["todos_completed"] = True

        else:
            context['login_required_msg'] = "you need to login first"
        return render(request, "dashboard/todo.html", context)


def update_todo(request, pk):
    todo = Todo.objects.get(id=pk)
    todo.is_finished = not todo.is_finished
    todo.save()
    return redirect('dashboard:todo')


def delete_todo(request, pk):
    Todo.objects.get(id=pk).delete()
    return redirect('dashboard:todo')


def books(request):
    context = {}
    form = DashboardForm()
    if request.POST:
        text = request.POST['text']
        url = "https://www.googleapis.com/books/v1/volumes?q=" + text
        result = requests.get(url).json()
        books_list = []
        for i in range(10):
            try:
                result_dict = {
                    'title': result['items'][i]['volumeInfo'].get('title'),
                    'subtitle': result['items'][i]['volumeInfo'].get('subtitle'),
                    'description': result['items'][i]['volumeInfo'].get('description'),
                    'count': result['items'][i]['volumeInfo'].get('pageCount'),
                    'categories': result['items'][i]['volumeInfo'].get('categories'),
                    'rating': result['items'][i]['volumeInfo'].get('averageRating'),
                    'thumbnail': result['items'][i]['volumeInfo']['imageLinks'].get('thumbnail'),
                    'preview': result['items'][i]['volumeInfo'].get('previewLink'),
                }
                books_list.append(result_dict)
                context = {
                    'form': form,
                    'books_list': books_list
                }
            except:
                context = {
                    'form': form,
                    'input': text,
                    'api_error': True
                }
                break

        return render(request, 'dashboard/books.html', context)

    else:
        if request.user.is_authenticated:
            print("get method")
            context["form"] = form

        else:
            context['login_required_msg'] = "you need to login first"
        return render(request, 'dashboard/books.html', context)


def dictionary(request):
    form = DashboardForm()
    context = {}
    if request.method == 'POST':
        text = request.POST['text']
        url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/" + text
        result = requests.get(url).json()
        try:
            context = {
                'form': form,
                'input': text,
                'phonetics': result[0]['phonetics'][0]['text'],
                'audio': result[0]['phonetics'][0]['audio'],
                'definition': result[0]['meanings'][0]['definitions'][0]['definition'],
                'example': result[0]['meanings'][0]['definitions'][0]['example'],
                'synonyms': result[0]['meanings'][0]['definitions'][0]['synonyms'],
            }
        except:
            context = {
                'form': form,
                'input': text,
                'api_error': True
            }
        print(context)
        return render(request, 'dashboard/dictionary.html', context)
    else:

        if request.user.is_authenticated:
            print("get method")
            context["form"] = form
            context['get_request'] = True
        else:
            context['login_required_msg'] = "you need to login first"

        return render(request, 'dashboard/dictionary.html', context)


def wiki(request):
    context = {}
    form = DashboardForm()

    if request.method == 'POST':
        context["form"] = form
        text = request.POST["text"]
        try:
            search_result = wikipedia.page(text)
            context['title'] = search_result.title
            context['link'] = search_result.url
            context['details'] = search_result.summary

        except:
            context["api_error"] = True
            context["input"] = text
        return render(request, 'dashboard/wiki.html', context)

    else:
        if request.user.is_authenticated:
            context["get_request"] = True
            context["form"] = form
        else:
            context["login_required_msg"] = "you need to login first"
        return render(request, 'dashboard/wiki.html', context)


def register(request):
    if request.method == 'POST':
        register_form = UserRegistrationForm(request.POST)
        print(request.POST)
        if register_form.is_valid():
            register_form.save()
            print("form is valid")
            username = register_form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}")
            return redirect("dashboard:home")
        else:
            print("form is not valid")
            print(f"form.errors:  {register_form.errors}")
            return render(request, 'dashboard/register.html', {'register_form': register_form})
    else:
        register_form = UserRegistrationForm
        return render(request, 'dashboard/register.html', {'register_form': register_form})


def profile(request):
    context = {}
    if request.user.is_authenticated:
        todos = Todo.objects.filter(user=request.user)
        if len(Todo.objects.filter(user=request.user, is_finished=False)) > 0:
            todos_left = True
        else:
            todos_left = False

        homeworks = Homework.objects.filter(user=request.user)
        if len(Homework.objects.filter(user=request.user, is_finished=False)) > 0:
            homeworks_left = True
        else:
            homeworks_left = False

        context = {'todos': todos, 'homeworks': homeworks, 'todos_left': todos_left, 'homeworks_left': homeworks_left}
        return render(request, 'dashboard/profile.html', context)

    else:
        context["login_required_msg"] = "you need to login first"
        return render(request, 'dashboard/profile.html', context)


def handle_logout(request):
    logout(request)
    messages.success(request, "logged out successfully")
    return redirect('dashboard:home')
