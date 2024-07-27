from rolepermissions.roles import AbstractUserRole

class Administrador(AbstractUserRole):
    available_permissions = {
        'ver_conteudo': True,
        'Cadastrar_usuario': True,
        'Adicionar_eventos': True,
        'visualizar_contrato':True,
        'Gerenciar_financas': True,
        'dashboard_professor': True,
        'dashboard_admin':True,
        'dashboard_aluno': True,
        'plano_de_aula':True,
        'Ver_planos_aula':True,
        'Registrar_chamada':True,
        'Ver_relatorios':True
        

    }
    
class Aluno(AbstractUserRole):
    available_permissions = {
            'ver_conteudo': True,
            'dashboard_aluno': True,
            'aluno_financeiro': True,
            'plano_de_aula':True,
            
            
        }
        
class Professor(AbstractUserRole):
    available_permissions = {
        'ver_conteudo': True,
        'dashboard_professor': True,
        'Ver_planos_aula':True,
        'Registrar_chamada': True
        }
    
    