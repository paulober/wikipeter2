import os
from typing import Any, Dict, List

from django.contrib.auth.models import User
from django.contrib.sessions.backends.base import SessionBase
from django.core.files import uploadedfile
from django.core.files.uploadedfile import UploadedFile
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseBase, HttpResponseRedirect, HttpResponseServerError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Class, MasterCategory, Post, ClassCategory, SpecialSiteContent, WikiFile, WikiPostFile
from .forms import CategoryForm, ClassForm, ConnectPostWikiFileForm, EditCategoryForm, EditClassForm, EditMasterCategoryForm, EditPostForm, EditSpecialSiteContentForm, MasterCategoryForm, PostForm, WikiFileForm
from .static_session_keys import CREATION_SUCCEED, POST_ALLREADY_CONNECTED, POST_CONNECTION_SUCCEED, SAVE_SUCCEED, UPDATE_SUCCEED, UPLOAD_SUCCEED

from markdown import Markdown

UPLOADS_ROOT = 'wikipeter2/wiki/static/uploads/'

# Create your views here.

#def home(request):
#    return render(request, 'home.html', {})

def HomeView(request: HttpRequest):
    special_site_content = SpecialSiteContent.objects.all().filter(site_name="home").values_list('content')

    if special_site_content.count() == 0:
        return render(request, 'home.html', {'home_content': None})

    return render(request, 'home.html', {'home_content': Markdown().convert(str(special_site_content[0][0]))})


class ClassView(ListView):
    template_name = 'class_details.html'

    def get_queryset(self) -> QuerySet[ClassCategory]:
        class_id = self.kwargs['class_id']

        # no super call to avoid get all query and than filtering the result
        # queryset = super(ClassView, self).get_queryset()
        if class_id == None or class_id == '':
            return None

        queryset = ClassCategory.objects.all().filter(target_class_id=class_id)
        return queryset


def CategoryView(request, category_id):
    posts = Post.objects.all().filter(category_id=category_id).values_list('id', 'title', 'short_description')
    if len(posts) == 1:
        return redirect('post-detail', posts[0][0])
    return render(request, 'category_details.html', {'posts': posts})


def MasterCategoryView(request, master_category_id):
    posts = Post.objects.all().filter(master_category_id=master_category_id).values_list('id', 'title', 'short_description')
    if len(posts) == 1:
        return redirect('post-detail-from-master-category', posts[0][0], 1)

    return render(request, 'master_category.html', {'posts': posts})


class PostView(DetailView):
    model = Post
    template_name = 'post_details.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        # Call the base implementation first to get the context
        context = super(__class__, self).get_context_data(**kwargs)
        
        downloads = WikiPostFile.objects.filter(post = context['post'].pk).values_list('pk', 'wiki_file_id')
        alert: str = None
        downloads_data = []

        for i in downloads:
            downloads_data.append((i[0], WikiFile.objects.filter(id = i[1]).values_list('name')[0][0]))

        # from_master_category is used to force page to show the master category optimized view
        # and self.model.category != None is used for post which are master category only but opened with normal view
        # they the have the default view mode 'Master Category View Mode' and not the standard one
        # but if a post have both a master category and a normal category record i will be show via the standard view mode
        if 'from_master_category' not in self.kwargs and context['post'].category != None:
            # TODO: maybe pk instead of id
            if self.model.objects.all().filter(category_id = context['post'].category.id).values_list('id').count() == 1:
                alert = """<div class="alert alert-info" role="alert">Du wurdest automatisch weiter geleitet, da es in dieser Kategorie nur einen Beitrag gibt.</div>"""
        else:
            context['from_master_category'] = True

        # Create any data and add it to the context
        if len(downloads_data) == 0:
            context['downloads'] = None
        else:
            context['downloads'] = downloads_data
        context['alert_tag'] = alert

        # translate markdown
        # IMPORTANT: ensure on each update that this also will work with html and without text
        context['rendered_content'] = Markdown().convert(context['post'].content)

        if 'searchText' in self.kwargs:
            context['search_text'] = self.kwargs['searchText']

        return context


class SearchView(ListView):
    model = Post
    template_name = 'search.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super(__class__, self).get_context_data(**kwargs)
        # data['search_text'] = kwargs.get('search', '')
        data['search_text'] = self.request.GET.get('search')
        return data

    def get_queryset(self) -> QuerySet:
        # search = self.kwargs.get('search', '')
        search = self.request.GET.get('search')
        object_list = self.model.objects.all()
        if search:
            object_list = object_list.filter(title__icontains=search).values_list('pk', 'title')

            """object_list = search.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=q) for q in object_list)) |
                reduce(operator.and_,
                       (Q(content__icontains=q) for q in object_list))
            )"""

        return object_list

##################################################
################## Members #######################
##################################################

def DashboardView(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('home')

    general_posts = Post.objects.count()
    general_files = WikiFile.objects.count()
    general_classes = Class.objects.count()
    general_categories = ClassCategory.objects.count()
    general_master_categories = MasterCategory.objects.count()

    return render(request, 'dashboard.html', {
        'general_posts': general_posts,
        'general_files': general_files,
        'general_classes': general_classes,
        'general_categories': general_categories,
        'general_master_categories': general_master_categories
    })

class MembersPostsView(ListView):
    http_method_names = ['get']
    model = Post
    template_name = 'members/posts.html'
    ordering = ['post_date']

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super(__class__, self).get_context_data(**kwargs)

        # TODO: implement filter
        if 'filter_by' in self.kwargs:
            pass

        if self.request.session.has_key(UPDATE_SUCCEED):
            context['update_succeed'] = True
            del self.request.session[UPDATE_SUCCEED]

        elif self.request.session.has_key(CREATION_SUCCEED):
            context['creation_succeed'] = True
            del self.request.session[CREATION_SUCCEED]

        return context


class MembersAddPostView(CreateView):
    http_method_names = ['get', 'post']
    model = Post
    form_class = PostForm
    template_name = 'members/add_post.html'
    success_url = reverse_lazy('members-posts')

    # Both not used because managed in .forms.PostForm
    # fields = '__all__'
    # maybe add post_date and let the outher select a day in the future and the post is visible until that day
    # fields = ('title', 'category', 'master_category', 'short_description', 'content')

    def get_success_url(self) -> str:
        self.request.session[CREATION_SUCCEED] = True
        return super().get_success_url()

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        form.instance.author = User.objects.get(id = self.request.user.id)
        return super(__class__, self).form_valid(form)

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().post(request, *args, **kwargs)


class MembersUpdatePostView(UpdateView):
    http_method_names = ['get', 'post']
    model = Post
    form_class = EditPostForm
    template_name = 'members/edit_post.html'
    # maybe change this attribute in get() if navigated from the edit button in post_detail
    success_url = reverse_lazy('members-posts')

    def get_success_url(self) -> str:
        self.request.session[UPDATE_SUCCEED] = True     
        return super().get_success_url()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        data = super(__class__, self).get_context_data(**kwargs)
        # data['search_text'] = kwargs.get('search', '')
        data['post_pk'] = data['post'].pk
        return data


class MembersDeletePostViewOld(DeleteView):
    http_method_names = ['get']
    model = Post
    template_name = 'members/delete_post.html'
    success_url = reverse_lazy('members-posts')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super(__class__, self).get(request, *args, **kwargs)


def MembersDeletePostView(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')

    if pk != None:
        p = Post.objects.get(pk=pk)

        if p != None:
            p.delete()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


class MembersWikiFilesView(ListView):
    http_method_names = ['get']
    model = WikiFile
    template_name = 'members/wiki_files.html'
    ordering = ['upload_date']

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')

        return super(__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        contex_data = super(__class__, self).get_context_data(**kwargs)

        if self.request.session.has_key(UPLOAD_SUCCEED):
            contex_data['upload_succeed'] = True
            # remove session key so the alert is only shown once
            del self.request.session[UPLOAD_SUCCEED]
        
        elif self.request.session.has_key(POST_ALLREADY_CONNECTED):
            contex_data['post_allready_connected'] = True
            del self.request.session[POST_ALLREADY_CONNECTED]

        elif self.request.session.has_key(POST_CONNECTION_SUCCEED):
            contex_data['post_connection_succeed'] = True
            del self.request.session[POST_CONNECTION_SUCCEED]

        return contex_data


def handle_uploaded_file(u_file: UploadedFile):
    # TODO: this could cause a potential problem !!!! (the path below)
    try:
        # insert into filesystem
        with open(UPLOADS_ROOT+str(u_file.name), 'wb+') as destination:
            for chunk in u_file.chunks():
                destination.write(chunk)

        # Insert into db
        WikiFile.objects.create(name=u_file.name)
    except:
        print("Error on writing new file to: " + os.getcwd() + "/wikipeter2/wiki/static/uploads/" + u_file.name)
    

def MembersUploadWikiFileView(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = WikiFileForm(request.POST, request.FILES)

        if form.is_valid():
            if WikiFile.objects.all().filter(name=request.FILES['upload_file']).count() != 0:
                form = WikiFileForm()
                return render(request, 'members/upload_wikifile.html', {'file_name_exists': True, 'form': form})
            handle_uploaded_file(request.FILES['upload_file'])

            # parse the succeed info via request session 
            request.session[UPLOAD_SUCCEED] = True
            return redirect('members-files')

        errors = form.errors.as_json()
        form = WikiFileForm()
        return render(request, 'members/upload_wikifile.html', {'server_error': True, 'form': form, 'errors': errors})

    form = WikiFileForm()
    return render(request, 'members/upload_wikifile.html', {'form': form})


def connection_requested(wikifile: WikiFile, post: Post):
    WikiPostFile.objects.create(wiki_file=wikifile, post=post)


def MembersConnectPostWikiFileView(request: HttpRequest, selected_file: int):
    if not request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = ConnectPostWikiFileForm(request.POST, request.FILES)

        if form.is_valid():
            post = Post.objects.get(pk=request.POST.get('post'))
            wikifile = WikiFile.objects.get(pk=selected_file)

            if WikiPostFile.objects.all().filter(post=post, wiki_file=wikifile).count() != 0:
                form = ConnectPostWikiFileForm()
                request.session[POST_ALLREADY_CONNECTED] = True
                return redirect('members-files')
            
            connection_requested(wikifile, post)
            # parse the succeed info via request session 
            request.session[POST_CONNECTION_SUCCEED] = True
            return redirect('members-files')

        form = ConnectPostWikiFileForm()
        return render(request, 'members/connect_post_wikifile.html', {'server_error': True, 'form': form})
    
    form = ConnectPostWikiFileForm()
    return render(request, 'members/connect_post_wikifile.html', {'form': form})


class MembersDisconnectPostWikiFileView(ListView):
    http_method_names = ['get']
    template_name = 'members/disconnect_wiki_file.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')

        return super().get(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet:
        selected_file_id = self.kwargs['selected_file']

        # no super call to avoid get all query and than filtering the result
        # queryset = super(ClassView, self).get_queryset()
        if selected_file_id == None or selected_file_id == '':
            return None

        queryset = WikiPostFile.objects.all().filter(wiki_file_id=selected_file_id).values_list('pk', 'post__title')

        return queryset


def MemberDeleteConnectionView(request: HttpRequest, pk: int):
    if not request.user.is_authenticated:
        return redirect('home')

    if pk != None:
        wpf = WikiPostFile.objects.get(pk=pk)

        if wpf != None:
            wpf.delete()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


"""
class MembersDeleteWikiFileView(DeleteView):
    model = WikiFile
    template_name = 'members/delete_wikifile.html'
    success_url = reverse_lazy('members-files')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super(__class__, self).get(request, *args, **kwargs)"""

def MembersDeleteWikiFileView(request: HttpRequest, pk):
    if not request.user.is_authenticated:
        return redirect('home')

    if pk != None:
        wf = WikiFile.objects.get(pk=pk)

        # fast response and to avoid errors with os.remove
        if not os.path.isfile(UPLOADS_ROOT+str(wf.name)):
            wf.delete()
            return HttpResponse()


        try:
            # remove from filesystem
            os.remove(UPLOADS_ROOT+str(wf.name))

            # Delete from db
            wf.delete()
            return HttpResponse()
        except:
            print("Error on deleting file from: " + os.getcwd() + "/" + UPLOADS_ROOT + wf.name)
            return HttpResponseServerError() 
    else:
        return HttpResponseBadRequest()


class MembersCategoriesView(ListView):
    http_method_names = ['get']
    model = ClassCategory
    template_name = 'members/categories.html'
    ordering = ['date_created']

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')

        return super(__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        contex_data = super(__class__, self).get_context_data(**kwargs)

        if self.request.session.has_key(CREATION_SUCCEED):
            contex_data['creation_succeed'] = True
            # remove session key so the alert is only shown once
            del self.request.session[CREATION_SUCCEED]

        return contex_data


class MembersAddCategoryView(CreateView):
    http_method_names = ['get', 'post']
    model = ClassCategory
    form_class = CategoryForm
    template_name = 'members/add_category.html'
    success_url = reverse_lazy('members-categories')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # if user ist not authenticated redirect back to home
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().post(request, *args, **kwargs)


class MembersEditCategoryView(UpdateView):
    http_method_names = ['get', 'post']
    model = ClassCategory
    form_class = EditCategoryForm
    template_name = 'members/edit_category.html'
    success_url = reverse_lazy('members-categories')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().post(request, *args, **kwargs)

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #    data = super(__class__, self).get_context_data(**kwargs)
    #    # data['search_text'] = kwargs.get('search', '')
    #    data['category_pk'] = data['classcategory'].pk
    #    return data


def MembersDeleteCategoryView(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')

    if pk != None:
        cat = ClassCategory.objects.get(pk=pk)

        if cat != None:
            cat.delete()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# Classes

class MembersClassesView(ListView):
    http_method_names = ['get']
    model = Class
    template_name = 'members/classes.html'
    ordering = ['date_created']

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')

        return super(__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        contex_data = super(__class__, self).get_context_data(**kwargs)

        if self.request.session.has_key(CREATION_SUCCEED):
            contex_data['creation_succeed'] = True
            # remove session key so the alert is only shown once
            del self.request.session[CREATION_SUCCEED]

        return contex_data


class MembersAddClassView(CreateView):
    http_method_names = ['get', 'post']
    model = Class
    form_class = ClassForm
    template_name = 'members/add_class.html'
    success_url = reverse_lazy('members-classes')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # if user ist not authenticated redirect back to home
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().post(request, *args, **kwargs)


class MembersEditClassView(UpdateView):
    http_method_names = ['get', 'post']
    model = Class
    form_class = EditClassForm
    template_name = 'members/edit_class.html'
    success_url = reverse_lazy('members-classes')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().post(request, *args, **kwargs)

    # def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
    #    data = super(__class__, self).get_context_data(**kwargs)
    #    # needed for delete btn inside edit view, but no edit page only
    #    # endpoint so this is not great ux, use the delete btn in classes
    #    # data['class_pk'] = data['class'].pk
    #    return data


def MembersDeleteClassView(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')

    if pk != None:
        c = Class.objects.get(pk=pk)

        if c != None:
            c.delete()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()

# Master category

class MembersMasterCategoriesView(ListView):
    http_method_names = ['get']
    model = MasterCategory
    template_name = 'members/master_categories.html'
    ordering = ['date_created']

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')

        return super(__class__, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        contex_data = super(__class__, self).get_context_data(**kwargs)

        if self.request.session.has_key(CREATION_SUCCEED):
            contex_data['creation_succeed'] = True
            # remove session key so the alert is only shown once
            del self.request.session[CREATION_SUCCEED]

        return contex_data


class MembersAddMasterCategoryView(CreateView):
    http_method_names = ['get', 'post']
    model = MasterCategory
    form_class = MasterCategoryForm
    template_name = 'members/add_master_category.html'
    success_url = reverse_lazy('members-master-categories')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # if user ist not authenticated redirect back to home
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().post(request, *args, **kwargs)


class MembersEditMasterCategoryView(UpdateView):
    http_method_names = ['get', 'post']
    model = MasterCategory
    form_class = EditMasterCategoryForm
    template_name = 'members/edit_master_category.html'
    success_url = reverse_lazy('members-master-categories')

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().post(request, *args, **kwargs)


def MembersDeleteMasterCategoryView(request, pk):
    if not request.user.is_authenticated:
        return redirect('home')

    if pk != None:
        cat = MasterCategory.objects.get(pk=pk)

        if cat != None:
            cat.delete()

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def SettingsView(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('home')

    custom_ctx = {}

    if request.session.has_key(SAVE_SUCCEED):
        custom_ctx['save_succeed'] = True
        del request.session[SAVE_SUCCEED]

    return render(request, 'members/settings.html', custom_ctx)


class EditSpecialSiteContentView(UpdateView):
    http_method_names = ['get', 'post']
    model = SpecialSiteContent
    form_class = EditSpecialSiteContentForm
    template_name = 'members/edit_special_site.html'
    success_url = reverse_lazy('members-settings')

    def get_success_url(self) -> str:
        self.request.session[SAVE_SUCCEED] = True
        return super().get_success_url()

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if not request.user.is_authenticated:
            return redirect('home')
        return super().post(request, *args, **kwargs)
