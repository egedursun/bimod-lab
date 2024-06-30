from django.urls import path

from .views import CreateSubscriptionView, ListSubscriptionView, UpdateSubscriptionView, DeleteSubscriptionView


app_name = "subscription"

urlpatterns = [
    path('create/', CreateSubscriptionView.as_view(template_name="subscription/create_subscription.html"),
         name="create"),
    path('list/', ListSubscriptionView.as_view(template_name="subscription/list_subscriptions.html"),
         name="list"),
    path('update/<int:pk>/', UpdateSubscriptionView.as_view(template_name="subscription/update_subscription.html"),
         name="update"),
    path('delete/<int:pk>/', DeleteSubscriptionView.as_view(template_name="subscription/confirm_delete_subscription.html"),
         name="delete"),
]
