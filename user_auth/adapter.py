from allauth.account.adapter import DefaultAccountAdapter
from .models import User

class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.username = data['username']
        user.email = data['email']
        if 'first_name' in data.keys():
            user.first_name = data['first_name']
        if 'last_name' in data.keys():
            user.last_name = data['last_name']
        if 'phone_number' in data.keys():
            user.phone_number = data['phone_number']
        if 'city' in data.keys():
            user.city = data['city']
        if 'address' in data.keys():
            user.address = data['address']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        print(1)
        user.save()
        return user