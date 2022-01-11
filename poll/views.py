from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import CreatePollForm
from .models import Poll
from django.contrib import messages
from django.core.exceptions import PermissionDenied




def home(request):
    polls = Poll.objects.all()
    num_of_questions =  Poll.objects.all().count()
    context = {
        'num_of_questions' : num_of_questions,
        'polls' : polls
    }
    return render(request, 'home.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            polls = form.save(commit=False)
            if request.user.is_authenticated:
            	polls.author = request.user
            polls.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    num_of_questions =  Poll.objects.all().count()
    context = {
        'num_of_questions' : num_of_questions,
        'form' : form
    }
    return render(request, 'create.html', context)


@login_required
def update_view(request, poll_id): 
    # dictionary for initial data with  
    # field names as keys 
    context ={} 
  
    # fetch the object related to passed id 
    poll = Poll.objects.get(pk=poll_id)
  
    # pass the object as instance in form 
    form = CreatePollForm(request.POST or None, instance = poll) 
  
    # save the data from the form and 
    # redirect to detail_view 
    if form.is_valid(): 
        form.save()
        messages.success(request, ('poll has been edited')) 
        return redirect("home") 
  
    # add form dictionary to context 
    num_of_questions =  Poll.objects.all().count()
    context = {
        'num_of_questions' : num_of_questions,
        'form' : form
    }
    return render(request, 'edit.html', context)


@login_required
def vote(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)

    if request.method == 'POST':

        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
            return HttpResponse(400, 'Invalid form')

        poll.save()

        return redirect('results', poll.id)
    num_of_questions =  Poll.objects.all().count()

    context = {
        'num_of_questions' : num_of_questions,
        'poll' : poll
    }
    return render(request, 'vote.html', context)
    
@login_required
def results(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    num_of_questions =  Poll.objects.all().count()
    context = {
        'num_of_questions' : num_of_questions,
        'poll' : poll
    }
    return render(request, 'results.html', context)

@login_required
def delete(request, poll_id):
    poll = Poll.objects.get(pk=poll_id)
    poll.delete()
    messages.success(request, ('poll has been deleted'))
    return redirect('home')