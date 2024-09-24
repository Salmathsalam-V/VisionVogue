from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

def create_superuser():
    username = 'dj-admin'    # Replace with desired username
    email = 'salma1020@gmail.com'  # Replace with desired email
    password = '1234'  # Replace with the desired password
    first_name = 'salmath'
    last_name = 'v'
    User = get_user_model()  # Get the custom user model
    
    try:
        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username=username, email=email, password=password,first_name=first_name,last_name=last_name)
            print(f"Superuser '{username}' created successfully.")
        else:
            print(f"Superuser '{username}' already exists.")
    except IntegrityError:
        print("Superuser creation failed due to IntegrityError.")

# Call the function
create_superuser()

  