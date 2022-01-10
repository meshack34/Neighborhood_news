from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from .forms import SignUpForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.core.mail import EmailMessage
from .models import Profile,NeighborHood,Post,Business
from .forms import *


# Create your views here.
@login_required
def index(request):
  current_user = request.user
  neighborhoods = NeighborHood.objects.all().order_by('-created_at')
  return render(request, 'index.html',{'current_user':current_user, 'neighborhoods':neighborhoods})

def signup_view(request):
  if request.method  == 'POST':
    form = SignUpForm(request.POST)
    if form.is_valid():
      user = form.save()
      user.refresh_from_db()
      user.profile.first_name = form.cleaned_data.get('first_name')
      user.profile.last_name = form.cleaned_data.get('last_name')
      user.profile.email = form.cleaned_data.get('email')
      return redirect('login')
      
   
  else:
    form = SignUpForm()
  return render(request, 'registration/signup.html', {'form': form})

def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        auth_login(request, user)
        messages.info(request, f"You are now logged in as {username}")
        return redirect('home')
      else:
        messages.error(request, "wrong password.")
    else:
      messages.error(request, "wrong password.")
  form = AuthenticationForm()
  return render(request = request,template_name = "registration/login.html",context={"form":form})

def activation_sent_view(request):
  return render(request, 'registration/activation_sent.html')



@login_required
def search(request):
  if 'name' in request.GET and request.GET["name"]:
    search_term = request.GET.get("name")
    searched_businesses = Business.search_businesses(search_term)
    message = f"{search_term}"

    return render(request,'search.html', {"message":message,"businesses":searched_businesses})

  else:
    message = "You haven't searched for any term"
    return render(request,'search.html',{"message":message})

@login_required
def create_neighborhood(request):
  if request.method == 'POST':
    add_neighborhood_form = CreateNeighborHoodForm(request.POST, request.FILES)
    if add_neighborhood_form.is_valid():
      neighborhood = add_neighborhood_form.save(commit=False)
      neighborhood.admin = request.user.profile
      neighborhood.save()
      return redirect('home')
  else:
    add_neighborhood_form = CreateNeighborHoodForm()
  return render(request, 'create_neighborhood.html', {'add_neighborhood_form': add_neighborhood_form})

@login_required
def choose_neighborhood(request, neighborhood_id):
  neighborhood = get_object_or_404(NeighborHood, id=neighborhood_id)
  request.user.profile.neighborhood = neighborhood
  request.user.profile.save()
  return redirect('home')

def get_neighborhood_users(request, neighborhood_id):
  neighborhood = NeighborHood.objects.get(id=neighborhood_id)
  users = Profile.objects.filter(neighborhood=neighborhood)
  return render(request, 'neighborhood_users.html', {'users': users})

@login_required
def leave_neighborhood(request, neighborhood_id):
  neighborhood = get_object_or_404(NeighborHood, id=neighborhood_id)
  request.user.profile.neighborhood = None
  request.user.profile.save()
  return redirect('home')

@login_required
def create_business(request,neighborhood_id):
  neighborhood = NeighborHood.objects.get(id=neighborhood_id)
  if request.method == 'POST':
    add_business_form = CreateBusinessForm(request.POST, request.FILES)
    if add_business_form.is_valid():
      business = add_business_form.save(commit=False)
      business.neighborhood =neighborhood
      business.user = request.user
      business.save()
      return redirect('neighborhood', neighborhood.id)
  else:
    add_business_form = CreateBusinessForm()
  return render(request, 'create_business.html', {'add_business_form': add_business_form,'neighborhood':neighborhood})

@login_required
def create_post(request, neighborhood_id):
  neighborhood = NeighborHood.objects.get(id=neighborhood_id)
  if request.method == 'POST':
    add_post_form = CreatePostForm(request.POST,request.FILES)
    if add_post_form.is_valid():
      post = add_post_form.save(commit=False)
      post.neighborhood = neighborhood
      post.user = request.user
      post.save()
      return redirect('neighborhood', neighborhood.id)
  else:
    add_post_form = CreatePostForm()
  return render(request, 'create_post.html', {'add_post_form': add_post_form,'neighborhood':neighborhood})

@login_required
def neighborhood(request, neighborhood_id):
  current_user = request.user
  neighborhood = NeighborHood.objects.get(id=neighborhood_id)
  business = Business.objects.filter(neighborhood=neighborhood)
  users = Profile.objects.filter(neighborhood=neighborhood)
  posts = Post.objects.filter(neighborhood=neighborhood)

  return render(request, 'neighborhood.html', {'users':users,'current_user':current_user, 'neighborhood':neighborhood,'business':business,'posts':posts})

@login_required
def delete_business(request,business_id):
  current_user = request.user
  business = Business.objects.get(pk=business_id)
  if business:
    business.delete_business()
  return redirect('home')

@login_required
def update_business(request, business_id):
  business = Business.objects.get(pk=business_id)
  if request.method == 'POST':
    update_business_form = UpdateBusinessForm(request.POST,request.FILES, instance=business)
    if update_business_form.is_valid():
      update_business_form.save()
      messages.success(request, f'Business updated!')
      return redirect('home')
  else:
    update_business_form = UpdateBusinessForm(instance=business)

  return render(request, 'update_business.html', {"update_business_form":update_business_form})

@login_required
def delete_post(request,post_id):
  current_user = request.user
  post = Post.objects.get(pk=post_id)
  if post:
    post.delete_post()
  return redirect('home')

@login_required
def update_post(request, post_id):
  post = Post.objects.get(pk=post_id)
  if request.method == 'POST':
    update_post_form = UpdatePostForm(request.POST,request.FILES, instance=post)
    if update_post_form.is_valid():
      update_post_form.save()
      messages.success(request, f'Post updated!')
      return redirect('home')
  else:
    update_post_form = UpdatePostForm(instance=post)

  return render(request, 'update_post.html', {"update_post_form":update_post_form})

@login_required
def profile(request):
  current_user = request.user
  user_posts = Post.objects.filter(user_id = current_user.id).all()
  
  return render(request,'profile/profile.html',{'user_posts':user_posts,"current_user":current_user})

@login_required
def update_profile(request):
  if request.method == 'POST':
    user_form = UpdateUser(request.POST,instance=request.user)
    profile_form = UpdateProfile(request.POST,request.FILES,instance=request.user.profile)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('profile')
  else:
    user_form = UpdateUser(instance=request.user)
    profile_form = UpdateProfile(instance=request.user.profile) 
  params = {
    'user_form':user_form,
    'profile_form':profile_form
  }
  return render(request,'profile/update.html',params)

@login_required
def update_neighborhood(request, neighborhood_id):
  neighborhood = NeighborHood.objects.get(pk=neighborhood_id)
  if request.method == 'POST':
    update_neighborhood_form = UpdateNeighborhoodForm(request.POST,request.FILES, instance=neighborhood)
    if update_neighborhood_form.is_valid():
      update_neighborhood_form.save()
      messages.success(request, f'Post updated!')
      return redirect('home')
  else:
    update_neighborhood_form = UpdateNeighborhoodForm(instance=neighborhood)

  return render(request, 'update_neighborhood.html', {"update_neighborhood_form":update_neighborhood_form})

@login_required
def delete_neighborhood(request,neighborhood_id):
  current_user = request.user
  neighborhood = NeighborHood.objects.get(pk=neighborhood_id)
  if neighborhood:
    neighborhood.delete_neighborhood()
  return redirect('home')

@login_required
def users_profile(request,pk):
  user = User.objects.get(pk = pk)
  user_posts = Post.objects.filter(user_id = user.id).all()
  current_user = request.user
  
  return render(request,'profile/users_profile.html',{'user_posts':user_posts,"user":user,"current_user":current_user})
