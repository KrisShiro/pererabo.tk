import json

from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponseForbidden

from .models import Place, Proposal
from .forms import LoginForm, SignupForm, MyUserChangeForm, AddPlaceForm, AddProposalForm, AnswerProposalForm


# Create your views here.


def index(request):
    places = json.dumps(list(Place.objects.values()))
    return render(request, 'index.html', {'places_data': places})


def sign_in(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})
    form = LoginForm(request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Нет такого пользователя'})
    else:
        return render(request, 'login.html', {'form': form, 'error': 'Что-то пошло не так'})


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()

    context = {'place_form': AddPlaceForm()}
    if request.user.is_superuser:
        context['proposals'] = Proposal.objects.all()
        context['approve_form'] = AnswerProposalForm()
    else:
        context['proposals'] = Proposal.objects.filter(author=request.user)

    if request.method == 'GET':
        form = MyUserChangeForm(request.user, instance=request.user)
        context['form'] = form
    else:
        form = MyUserChangeForm(request.user, request.POST, instance=request.user)
        if form.is_valid():
            changed_user = form.save(commit=False)
            changed_user.save()
        context['form'] = form

    if request.user.is_superuser:
        context['places'] = Place.objects.all().values()
        for place in context['places']:
            place['type'] = []
            if place['type_mask'] & Place.PLAST != 0:
                place['type'].append('plastic')
            if place['type_mask'] & Place.PAPER != 0:
                place['type'].append('paper')
            if place['type_mask'] & Place.GLASS != 0:
                place['type'].append('glass')
            if place['type_mask'] & Place.ACCUM != 0:
                place['type'].append('accum')
            place['css_class'] = ' '.join(place['type'])
    return render(request, 'profile.html', context)


def signup(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})
    form = SignupForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return render(request, 'signup.html', {'form': form})


def sign_out(request):
    logout(request)
    return HttpResponseRedirect('/')


def delete_place(request, place_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    to_delete = Place.objects.get(id=place_id)
    to_delete.delete()
    return HttpResponseRedirect('/profile/')


def add_place(request):
    if not request.user.is_superuser or request.method != 'POST':
        return HttpResponseForbidden()
    form = AddPlaceForm(request.POST)
    if form.is_valid():
        place = form.save(commit=False)
        place.type_mask = 0
        if form.cleaned_data['plastic']:
            place.type_mask |= Place.PLAST
        if form.cleaned_data['paper']:
            place.type_mask |= Place.PAPER
        if form.cleaned_data['glass']:
            place.type_mask |= Place.GLASS
        if form.cleaned_data['accum']:
            place.type_mask |= Place.ACCUM
        place.save()
    return HttpResponseRedirect('/profile')


def edit_place(request, place_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    current_place = Place.objects.get(id=place_id)
    context = {}
    if request.method == 'POST':
        form = AddPlaceForm(request.POST, instance=current_place)
        if form.is_valid():
            place = form.save(commit=False)
            place.type_mask = 0
            if form.cleaned_data['plastic']:
                place.type_mask |= Place.PLAST
            if form.cleaned_data['paper']:
                place.type_mask |= Place.PAPER
            if form.cleaned_data['glass']:
                place.type_mask |= Place.GLASS
            if form.cleaned_data['accum']:
                place.type_mask |= Place.ACCUM
            place.save()
            return HttpResponseRedirect('/profile')
        context['form'] = form
    else:
        form = AddPlaceForm(instance=current_place)
        context['form'] = form
    return render(request, 'edit_place.html', context)


def add_proposal(request):
    if request.method == 'GET':
        place = request.GET.get('id', None)
        form = AddProposalForm()
        form.fields['place'].initial = place
    else:
        form = AddProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.author = request.user
            proposal.status = None
            proposal.status_explanation = ''
            proposal.save()
            return HttpResponseRedirect('/profile')
    return render(request, 'add_proposal.html', {'form': form})


def approve_proposal(request, proposal_id):
    if not request.user.is_superuser or request.method == 'GET':
        return HttpResponseForbidden()
    form = AnswerProposalForm(request.POST)
    proposal = Proposal.objects.get(id=proposal_id)
    if form.is_valid():
        proposal.status = True
        proposal.status_explanation = form.cleaned_data['explanation']
        proposal.save()
    return HttpResponseRedirect('/profile')


def disapprove_proposal(request, proposal_id):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    form = AnswerProposalForm(request.POST)
    proposal = Proposal.objects.get(id=proposal_id)
    if form.is_valid():
        proposal.status = False
        proposal.status_explanation = form.cleaned_data['explanation']
        proposal.save()
    return HttpResponseRedirect('/profile')
