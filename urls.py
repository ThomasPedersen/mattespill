from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'mattespill.main.views.index'),
	(r'^users/$', 'mattespill.main.views.users'),
	(r'^users/(?P<user_id>\d+)/$', 'mattespill.main.views.userid'),
	(r'^questions/(?P<question_id>\d+)/$', 'mattespill.main.views.questions'),
	(r'^login/$', 'mattespill.main.views.login'),
	# Example:
	# (r'^mattespill/', include('mattespill.foo.urls')),

	# Uncomment the admin/doc line below to enable admin documentation:
	# (r'^admin/doc/', include('django.contrib.admindocs.urls')),

	# Uncomment the next line to enable the admin:
	(r'^admin/', include(admin.site.urls)),

	# Hack to server static files
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
)
