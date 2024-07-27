
from django.contrib import admin
from .models import Users, Administrador, Aluno, Professor, Modalidade
from django.contrib.auth import admin as admin_auth_django
from .forms import UserChangeForm, UserCreationForm

# Register your models here.
@admin.register(Users)
class UserAdmin(admin_auth_django.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = Users
    fieldsets = admin_auth_django.UserAdmin.fieldsets + (
        ('cargo', {'fields':('cargo',)}),
    )
    

admin.site.register(Administrador)
admin.site.register(Professor)

class AlunoAdmin(admin.ModelAdmin):
    list_display = ('user', 'modalidade', 'quantidade_aulas', 'aulas_restante', 'valor_total', 'total_ja_pago')
    actions = ['marcar_como_pago']

    def marcar_como_pago(self, request, queryset):
        for aluno in queryset:
            # Lógica para adicionar pagamento
            aluno.adicionar_pagamento(aluno.mensalidade)
            aluno.save()
        self.message_user(request, "Mensalidade marcada como paga.")
    
    marcar_como_pago.short_description = "Marcar mensalidade como paga"

admin.site.register(Aluno, AlunoAdmin)

admin.site.register(Modalidade)