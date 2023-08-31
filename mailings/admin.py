# from django.contrib import admin
#
# from mailings.models import MailingSettings, Mailing
#
#
# @admin.register(MailingSettings)
# class MailingListSettingsAdmin(admin.ModelAdmin):
#     list_display = ('creation_date', 'start_time', 'interval', 'status',)
#
#
# @admin.register(Mailing)
# class EmailAdmin(admin.ModelAdmin):
#     list_display = ('subject', 'body',)
#     filter_horizontal = ('customers',)
