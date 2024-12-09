from django.contrib import admin
from .models import User, Doctor, Service, OpeningHour, Appointment, Blog, Statistic, Newsletter, FAQ, Testimonial

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Service)
admin.site.register(OpeningHour)
admin.site.register(Appointment)
admin.site.register(Blog)
admin.site.register(Statistic)
admin.site.register(Newsletter)
admin.site.register(FAQ)
admin.site.register(Testimonial)
