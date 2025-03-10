from django.urls import path
from .views.views import *
#from .views.single_instituicao import *
#from .views.multi_instituicao import *
from django.conf.urls.static import static, settings

urlpatterns = [
    #path('', DummyDashboardView.as_view(), name='dummy_dashboardo'),
    path('', DashboardView.as_view(), name='dashboard'),
    # Single institution views
    #path('<path:institutions>/', app_dashboard_view.as_view(), name='initial_data'), # Da pagina inicial
    path('new_results', DashboardView.as_view(), name='new_results'), # Do forms apos aplicar botao filtrar
    #path('new_results', app_dashboard_view.as_view(), name='new_results'), # Do forms apos aplicar botao filtrar
    #path('new_results', app_dashboard_view.as_view(), name='new_results'), # Do forms apos aplicar botao filtrar
    path('graph_data', GraphicProducerDashboardView.as_view(), name='graph_data'), # Do grafico
    
] 
# During development, serve media files in DEBUG mode
if settings.DEBUG and settings.CURRENT_ENVIRONMENT == 'DEV':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
