from django.contrib import admin
from app.models import *




class UserProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserProfile, UserProfileAdmin)




class RecruiterProjectAdmin(admin.ModelAdmin):
    pass


admin.site.register(RecruiterProject, RecruiterProjectAdmin)






class LinkedinProfileAdmin(admin.ModelAdmin):
    pass


admin.site.register(LinkedinProfile, LinkedinProfileAdmin)

