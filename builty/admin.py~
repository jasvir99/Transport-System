'''
    This files is used to display various options in admin pannel.
'''

from django.contrib import admin
from BuiltyMaker.builty.models import *

#::::::::::::Defining admin classes:::::::::::::#

class fixed_valuesAdmin(admin.ModelAdmin):
    '''
        ** Admin option to display and edit values of title, owner
           and service tax **
    '''
    list_display = ('title','owner', 'serviceTax')
    search_fields = ('title',)
    list_filter = ['title']

class freight_modeAdmin(admin.ModelAdmin):
    '''
        ** Admin options to add freight modes. **
    '''
    list_display = ('mode',)
    search_feilds = ('mode',)
    list_filter = ['mode']

class transfer_modeAdmin(admin.ModelAdmin):
	'''
		** Admin options to add mode of transfer. **
	'''
	list_display = ('mode',)
	search_fields = ('mode',)
	list_filter = ['mode']

class accountAdmin(admin.ModelAdmin):
	'''
		** Admin options to add mode of transfer. **
	'''
	list_display = ('account',)
	search_fields = ('account',)
	list_filter = ['account']

admin.site.register(account, accountAdmin)
admin.site.register(transfer_mode, transfer_modeAdmin)
admin.site.register(fixed_values, fixed_valuesAdmin)
admin.site.register(freight, freight_modeAdmin)
