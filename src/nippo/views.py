from typing import Any
from django.db.models.base import Model as Model
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, FormView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import NippoModel
from .forms import NippoModelForm, NippoFormClass
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from utils.access_restrictions import OwnerOnly


class NippoListView(ListView):
  template_name = "nippo/nippo-list.html"
  model = NippoModel
  
  # クエリセットをコンテキストで渡す
  def get_queryset(self):
      q = self.request.GET.get("search")
      qs = NippoModel.objects.search(query=q)
      if self.request.user.is_authenticated:
          qs = qs.filter(Q(public=True)|Q(user=self.request.user))
      else:
          qs = qs.filter(public=True)
      return qs
  
  # 好きなコンテキストが渡せる
  def get_context_data(self, *arg, **kwargs):
    ctx = super().get_context_data(*arg, **kwargs)
    return ctx


class NippoDetailView(DetailView):
    template_name = "nippo/nippo-detail.html"
    model = NippoModel

    def get_object(self):
       return super().get_object()
     
     
class NippoCreateModelFormView(LoginRequiredMixin, CreateView):
  template_name = "nippo/nippo-form.html"
  form_class = NippoModelForm
  success_url = reverse_lazy("nippo-list")
  
  def get_form_kwargs(self):
    kwgs = super().get_form_kwargs()
    kwgs["user"] = self.request.user
    return kwgs
  

class NippoUpdateModelFormView(OwnerOnly, UpdateView):
  template_name = "nippo/nippo-form.html"
  model = NippoModel
  form_class = NippoModelForm
  success_url = reverse_lazy("nippo-list")


class NippoDeleteView(OwnerOnly, DeleteView):
  template_name = "nippo/nippo-delete.html"
  model = NippoModel
  success_url = reverse_lazy("nippo-list")
  
  
class NippoCreateFormView(FormView):
    template_name = "nippo/nippo-form.html"
    form_class = NippoFormClass
    success_url = reverse_lazy("nippo-list")
    
    # validされたらこのメソッドが始まる？
    def form_valid(self, form):
        data = form.cleaned_data
        obj = NippoModel(**data)
        obj.save()
        return super().form_valid(form)
    
 # --------------以下未使用------------------------
    
     
# def nippoListView(request):
#     template_name = "nippo/nippo-list.html"
#     ctx = {}
#     qs = NippoModel.objects.all()
#     ctx["object_list"] = qs
#     return render(request, template_ntx) 
  

# def nippoDetailView(request, pk):
#     template_name = "nippo/nippo-detail.html"
#     ctx = {}
#     q = get_object_or_404(NippoModel ,pk=pk)
#     ctx["object"] = q
#     return render(request, template_name, ctx)
  
  
def nippoCreateView(request):
  template_name = "nippo/nippo-form.html"
  form = NippoFormClass(request.POST or None)
  ctx = {}
  ctx["form"] = form
  if form.is_valid():
      title = form.cleaned_data["title"]
      content = form.cleaned_data["content"]
      obj = NippoModel(title=title, content=content)
      obj.save()
      return redirect("nippo-list")
  return render(request, template_name, ctx)


def nippoUpdateFormView(request, pk):
    template_name = "nippo/nippo-form.html"
    obj = get_object_or_404(NippoModel, pk=pk)
    initial_values = {"title": obj.title, "content":obj.content}
    form = NippoFormClass(request.POST or initial_values) # request.POSTは編集用, initial_valuesは初期用
    ctx = {"form": form}
    ctx["object"] = obj
    if form.is_valid():
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]
        obj.title = title
        obj.content = content
        obj.save()
        if request.POST:
          return redirect("nippo-list")
    return render(request, template_name, ctx)
  
  
# 削除ページ
def nippoDeleteView(request, pk):
  template_name = "nippo/nippo-delete.html"
  obj = get_object_or_404(NippoModel, pk=pk)
  ctx = {"object" : obj}
  if request.POST:
    obj.delete()
    return redirect("nippo-list")
  return render(request, template_name, ctx)
  