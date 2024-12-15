import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
from django.contrib.auth.models import User
from new_novel_review.models import Work, Read
from collections import defaultdict

def add_reads():
    sets = defaultdict(list)
    other_sets = defaultdict(list)
    for i in range(50):
        random_user = User.objects.get(pk=random.randint(1,13))
        random_work = Work.objects.get(pk=random.randint(1,99))
        if random_work.title not in sets[random_user.username]:
            sets[random_user.username].append(random_work.title)
            read = Read.objects.get_or_create(work=random_work, user=random_user)[0]
            print(random_user.username, random_work.title)
            read.save()
        else:
            other_sets[random_user.username].append(random_work.title)
    print("--")
    for k, v in other_sets.items():
        print(k, v)
    print("--")

if __name__ == "__main__":
    print('adding_reads')
    add_reads()
    print('all_added')