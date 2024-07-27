from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
     path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('', include('acessos.urls')),
    path('home/', include('pagina_inicial.urls')),
    path('relatorios/', include('relatorios.urls')),
    path('registros/', include('registros.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('plano_de_aula/', include('plano_de_aula.urls')),
    path('calendario/', include('calendario.urls')),
    path('contratos/', include('contratos.urls')),
    path('perfil/', include('perfil.urls')),
    path('aulas/', include('aulas_avulsas.urls')),
    path('avisos/', include('avisos.urls')),
    path('chat/', include('chat.urls')),
    path('desempenho_aluno/', include('desempenho_aluno.urls')),
    path('feedback/', include('feedback.urls')),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)