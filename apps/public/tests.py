from django.test import Client
from django.urls import reverse

client = Client()
response = client.get(reverse("root_url"))
assert(response.status_code == 200)
