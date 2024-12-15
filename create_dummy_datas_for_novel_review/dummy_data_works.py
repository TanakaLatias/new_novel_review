import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()

from new_novel_review.models import Work

def add_works():
    
    for x in range(100):
        work_name = "work_" + str(x)
        creator_name = "creator_" + str(x)
        work = Work.objects.get_or_create(title=work_name, creator=creator_name,)[0]
        print(work_name, creator_name)
        work.save()

if __name__ == "__main__":
    print('adding_works')
    add_works()
    print('all_added')