set -o errexit

pip install -r requirements.txt

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
import os

User = get_user_model()
username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

try:
    User.objects.get(username=username)
except ObjectDoesNotExist:
    User.objects.create_superuser(username, email, password)
EOF

python manage.py collectstatic --no-input
python manage.py migrate
