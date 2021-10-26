from os import name
from django.urls import path
# from . import views
from .views import EditSpecialSiteContentView, MemberDeleteConnectionView, MembersAddCategoryView, MembersAddClassView, MembersAddMasterCategoryView, MembersAddPostView, DashboardView, MembersCategoriesView, MembersClassesView, MembersConnectPostWikiFileView, MembersDeleteCategoryView, MembersDeleteClassView, MembersDeleteMasterCategoryView, MembersDeletePostView, MembersDeletePostViewOld, HomeView, MasterCategoryView, MembersDeleteWikiFileView, MembersDisconnectPostWikiFileView, MembersEditCategoryView, MembersEditClassView, MembersEditMasterCategoryView, MembersMasterCategoriesView, MembersPostsView, MembersUploadWikiFileView, MembersWikiFilesView, PostView, ClassView, CategoryView, SearchView, MembersUpdatePostView, SettingsView

# TODO: all - to _
urlpatterns = [
    path('', HomeView, name="home"),

    # Wiki
    path('wiki/<int:pk>', PostView.as_view(), name="post-detail"),
    path('wiki/<int:pk>/<str:searchText>', PostView.as_view(), name="post-detail-from-search"),
    path('wiki/<int:pk>/in_master_category/<int:from_master_category>', PostView.as_view(), name="post-detail-from-master-category"),
    
    # Classes
    path('classes/<int:class_id>', ClassView.as_view(), name="class-detail"),

    # Categories
    path('categories/<int:category_id>', CategoryView, name="category-detail"),

    # Master-Categories
    path('sites/<int:master_category_id>', MasterCategoryView, name="master-category-detail"),

    # Search
    path('search/', SearchView.as_view(), name="search"),

    # admin sections
    # path('wikip_admin/posts/add_new', AddPostView.as_view(), name="add-post"),    
    # path('wikip_admin/posts/edit/<int:pk>', UpdatePostView.as_view(), name="update-post"),
    # path('wikip_admin/posts/delete/<int:pk>', DeletePostView.as_view(), name="delete-post"),

    ###################
    # Members section #
    ###################

    # Members - dashboard
    path('wikip-members/', DashboardView, name="dashboard"),

    # Members - Posts
    path('wikip-members/posts/show', MembersPostsView.as_view(), name="members-posts"),
    path('wikip-members/posts/add', MembersAddPostView.as_view(), name="members-add-post"),
    path('wikip-members/posts/edit/<int:pk>', MembersUpdatePostView.as_view(), name="members-edit-post"),
    path('wikip-members/posts/delete_old/<int:pk>', MembersDeletePostViewOld.as_view(), name="members-delete-post-old"),
    path('wikip-members/posts/delete/<int:pk>', MembersDeletePostView, name="members-delete-post"),

    # Members - Files
    path('wikip-members/files/show', MembersWikiFilesView.as_view(), name="members-files"),
    path('wikip-members/files/upload', MembersUploadWikiFileView ,name="members-upload-file"),
    path('wikip-members/files/connect/<int:selected_file>', MembersConnectPostWikiFileView, name="members-connect-file"),
    path('wikip-members/files/disconnect/<int:selected_file>', MembersDisconnectPostWikiFileView.as_view(), name="members-disconnect-file"),
    path('wikip-members/files/delete/<int:pk>', MembersDeleteWikiFileView, name="members-delete-file"),
    path('wikip-members/files/delete_connection/<int:pk>', MemberDeleteConnectionView, name="members-delete-wikipostfile"),

    # Members - Classes
    path('wikip-members/classes/show', MembersClassesView.as_view(), name="members-classes"),
    path('wikip-members/classes/add', MembersAddClassView.as_view(), name="members-add-class"),
    path('wikip-members/classes/edit/<int:pk>', MembersEditClassView.as_view(), name="members-edit-class"),
    path('wikip-members/classes/delete/<int:pk>', MembersDeleteClassView, name="members-delete-class"),

    # Members - Categories
    path('wikip-members/categories/show', MembersCategoriesView.as_view(), name="members-categories"),
    path('wikip-members/categories/add', MembersAddCategoryView.as_view(), name="members-add-category"),
    path('wikip-members/categories/edit/<int:pk>', MembersEditCategoryView.as_view(), name="members-edit-category"),
    path('wikip-members/categories/delete/<int:pk>', MembersDeleteCategoryView, name="members-delete-category"),

    # Members - Master-Categories
    path('wikip-members/master-categories/show', MembersMasterCategoriesView.as_view(), name="members-master-categories"),
    path('wikip-members/master-categories/add', MembersAddMasterCategoryView.as_view(), name="members-add-master-category"),
    path('wikip-members/master-categories/edit/<int:pk>', MembersEditMasterCategoryView.as_view(), name="members-edit-master-category"),
    path('wikip-members/master-categories/delete/<int:pk>', MembersDeleteMasterCategoryView, name="members-delete-master-category"),

    path('wikip-members/settings', SettingsView, name="members-settings"),
    path('wikip-members/settings/special-sites/edit/<str:pk>', EditSpecialSiteContentView.as_view(), name="members-settings-edit-special-sites"),
]