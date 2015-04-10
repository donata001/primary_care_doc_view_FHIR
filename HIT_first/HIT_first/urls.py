from django.conf.urls import patterns, include, url
from django.contrib import admin

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from my_app.views import PCPViewPage, lookup

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    
    #url(r'^api/', include('api.urls')),
    url(r'^api/v1/publishers/$', 'my_app.views.publisher_collection'),
    url(r'^api/v1/publishers/(?P<pk>[0-9]+)$', 'my_app.views.publisher_element'),
                          
    # Examples:
    # url(r'^$', 'My_Django.views.home', name='home'),
    # url(r'^My_Django/', include('My_Django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^demo/(\d{1,2})/(\d{1,2})$', 'my_app.views.my_view'),
    url(r'^search/$', 'my_app.views.search'),
    
    url(r'^dummy_1/$', 'my_app.views.dummy_my_view'),
    
    
    url(r'^pcpview/$', 'my_app.views.PCPView'),
    url(r'^patientview/$', 'my_app.views.PCPViewPage'),
    url(r'^lookup$', lookup,
        name='lookup'),

)

'''

# REST API
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'is_staff')

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

'''