from django.urls import path

from . import views


urlpatterns = [
    # Turf endpoints
    path('turfs/', views.ListTurfs.as_view(), name='turf-list'),
    path('turfs/create', views.CreateTurf.as_view(), name='turf-create'),
    path('turfs/org/<str:pk>', views.RetrieveTurfByOrg.as_view(), name='turf-get-org'),

    # Organization endpoints
    path('organizations/create', views.CreateOrg.as_view(), name='org-create'),
    path('organizations/<str:pk>', views.RetrieveUpdateOrg.as_view(), name='org-retrieve-update'),
    path('organizations/user/<str:pk>', views.RetrieveOrgByUser.as_view(), name='user-get-org')

]
