from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice, PolUser, ChoisedQuestions
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.views.generic import UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import ChangeUserInfo, AvatarChangeForm, RegisterUserForm
from django.contrib import messages
from django.db.utils import IntegrityError

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        
        
        
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    user_ = get_object_or_404(PolUser, username=request.user)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
        chosed_question = ChoisedQuestions(user=user_, question=question)
        Choises = Choice.objects.filter(question=question)
        
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        selected_choice.votes += 1
        summ = 0
        for i in Choises:
            summ += i.votes
        persentage = []
        
        try:
            chosed_question.save()
        except IntegrityError:
            for i in Choises:
                persentage.append([i, (i.votes / (summ if summ != 0 else 1)) * 100])
            return render(request, 'polls/results.html', {
                'error_message': 'вы уже делали выбор по этому вопросу',
                "choise_sum": summ,
                "persentage": persentage,
            })
        else:
            summ += 1
            for i in Choises:
                persentage.append([i, (i.votes / (summ if summ != 0 else 1)) * 100])
            selected_choice.save()
            return render(request, 'polls/results.html', context={
                "choise_sum": summ,
                "persentage": persentage,
                }) 




class PollsLogin(LoginView):
    template_name = 'polls/login.html'


class RegisterUserView(SuccessMessageMixin, CreateView):
    model = PolUser
    template_name = 'polls/registration.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('polls:index')
    success_message = 'Пользователь зарегестрирован, можете войти'
    
    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.method in ('POST', 'PUT'):
            kwargs.update({
                'data': self.request.POST,
                'files': self.request.FILES
            })
        return kwargs
   
@login_required
def profile(request):
    return render(request, 'polls/profile.html')

def logout_view(request):
    logout(request)
    return redirect('/')

# Контроллер для изменения данных пользователя
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = PolUser
    template_name = 'polls/change_user_info.html'
    form_class = ChangeUserInfo
    success_url = reverse_lazy('polls:profile')
    success_message = 'Личные данные пользователя изменены'
    
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)

# Контроллер для изменения аватара
@login_required
def avatar_change(request):
    instance = request.user
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            avatar = form.save()
            return redirect('polls:profile')
    else:
        form = AvatarChangeForm(instance=instance)
    context = {'form': form}
    return render(request, 'polls/avatar_changing.html', context=context)

class PollsPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = 'polls/password_change.html'
    success_url = reverse_lazy('polls:profile')
    success_message = 'Пароль успешно изменен'

class DeleteUserView(LoginRequiredMixin, DeleteView):
    model = PolUser
    template_name = 'polls/delete_user.html'
    success_url = reverse_lazy('polls:index')
    
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS, 'Пользователь успешно удален')
        return super().post(request, *args, **kwargs)
        
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
    