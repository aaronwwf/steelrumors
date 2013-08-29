from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse, reverse_lazy

from .models import Link, Vote, UserProfile
from .forms import UserProfileForm
from .forms import LinkForm



class LinkCreateView(CreateView):
	model = Link
	form_class = LinkForm
	
	def form_valid(self, form):
		f = form.save(commit=False)
		f.rank_score = 0.0
		f.submitter = self.request.user
		f.save()
		return super(LinkCreateView, self).form_valid(form)


class LinkListView(ListView):
	model = Link
	query = Link.with_votes.all()
	paginate_by = 5

class LinkDetailView(DetailView):
	model = Link

class LinkUpdateView(UpdateView):
	model = Link
	form_class = LinkForm

class LinkDeleteView(DeleteView):
	model = Link
	success_url = reverse_lazy('home');

class UserProfileDetailView(DetailView):
	model = get_user_model()
	slug_field = 'username'
	template_name = 'user_detail.html'

	def get_object(self, queryset=None):
		user = super(UserProfileDetailView, self).get_object(queryset)
		UserProfile.objects.get_or_create(user=user)
		return user

class UserProfileEditView(UpdateView):
	model = get_user_model()
	template_name = 'edit_profile.html'
	form_class = UserProfileForm

	def get_object(self, queryset=None):
		return UserProfile.objects.get_or_create(user=self.request.user)[0]

	def get_success_url(self):
		return reverse('profile', kwargs={'slug': self.request.user})