# Notório Saber

**Notório Saber** é uma plataforma de aulas particulares que facilita o agendamento de aulas, gestão financeira e acompanhamento dos alunos, proporcionando uma experiência eficiente para professores e estudantes.

## Funcionalidades

### 1. Agendamento de Aulas
- Professores podem disponibilizar seus horários.
- Alunos podem agendar aulas conforme disponibilidade.
- Notificações automáticas de confirmação e lembretes.

### 2. Gestão Financeira
- Controle de pagamentos e recebimentos.
- Histórico de transações.
- Geração de relatórios financeiros.

### 3. Área do Aluno
- Acompanhamento de atividades propostas pelos professores.
- Avaliações e feedbacks sobre as aulas.
- Histórico de aulas e progresso acadêmico.

## Tecnologias Utilizadas
- **Backend:** Django + Django REST Framework
- **Frontend:** React
- **Banco de Dados:** PostgreSQL
- **Servidor:** Gunicorn + Nginx

## Como Executar o Projeto

1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/notorio-saber.git
   ```
2. Entre no diretório do projeto:
   ```sh
   cd notorio-saber
   ```
3. Configure e ative o ambiente virtual:
   ```sh
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate  # Windows
   ```
4. Instale as dependências do backend:
   ```sh
   pip install -r requirements.txt
   ```
5. Configure o banco de dados e execute as migrações:
   ```sh
   python manage.py migrate
   ```
6. Inicie o servidor Django:
   ```sh
   python manage.py runserver
   ```


## Contribuição
Se você deseja contribuir com o Notório Saber, siga os passos:
1. Faça um fork do repositório.
2. Crie uma branch para sua funcionalidade/correção: `git checkout -b minha-feature`
3. Commit suas alterações: `git commit -m "Adiciona nova funcionalidade"`
4. Envie para o repositório remoto: `git push origin minha-feature`
5. Abra um Pull Request.

## Licença
Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

---
Desenvolvido por **Jullio Cesar** 🚀

