import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PIMD.settings')
django.setup()

from Core.feed import manzoom

# manzoom.scrapp()
manzoom.scrap_movie_thread()
# manzoom.actor_thumbnail()
# manzoom.scrap_cast_list()
# manzoom.test()
