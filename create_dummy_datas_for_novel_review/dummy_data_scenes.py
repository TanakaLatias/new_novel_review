import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

import random
from django.contrib.auth.models import User
from new_novel_review.models import Scene, Work

def add_scenes():
    for i in range(50):
        random_work = Work.objects.get(pk=random.randint(1, 99))
        random_user = User.objects.get(pk=random.randint(1,10))
        scene_name = "scene_" + str(i) + " : " + str(random_work.title)
        scene = Scene.objects.get_or_create(title=scene_name, work=random_work, user=random_user)[0]
        print(scene_name, random_user.username, random_work.title)
        scene.save()

if __name__ == "__main__":
    print('adding_scenes')
    add_scenes()
    print('all_added')