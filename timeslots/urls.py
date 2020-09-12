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
    ),
    path('book/<str:pk>', views.MakeBooking.as_view(), name="make-booking"),

    path(
        'bookings/<str:pk>',
        views.ReadUpdateDeleteBooking.as_view(),
        name='read-update-delete-bookings'
    ),
    path(
        'user/bookings/',
        views.ListBookingsByUser.as_view(),
        name='list-user-bookings'
    )
]
