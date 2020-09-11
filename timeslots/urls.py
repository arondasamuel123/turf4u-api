from django.urls import path


from . import views

urlpatterns = [
    path(
        'timeslots/<str:pk>',
        views.ListCreateTimeslots.as_view(),
        name='create-timeslots'
    ),
    path(
        'timeslot/<str:pk>',
        views.RetrieveUpdateTimeslot.as_view(),
        name='update-timeslot'
    ),
    path(
        'timeslot/turf/<str:pk>',
        views.RetrieveTimeslotByTurf.as_view(),
        name='get-timeslots-turf'
    )
]
