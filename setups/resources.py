# any_app/resources.py
from import_export import resources
from django.contrib.auth.models import User

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
        export_order = ('id', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active')
    
    # def before_save_instance(self, instance, dry_run):
    #     # Hash the password if it is plain text
    #     if instance.password and not instance.password.startswith('pbkdf2_'):
    #         instance.set_password(instance.password)