from django.contrib import admin
from VHStore.models import Cassette, Movie, User, MembershipStatus, Equipment

admin.site.register(Cassette)
admin.site.register(Movie)
admin.site.register(User)
admin.site.register(MembershipStatus)
admin.site.register(Equipment)
