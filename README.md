# Sistema de Gerenciamento de Notas Escolares

Um sistema web desenvolvido em Django para gerenciamento de notas escolares, permitindo que professores organizem suas turmas, alunos e notas de forma eficiente.

## Funcionalidades

### Gestão de Turmas
- Criação de turmas
- Visualização de todas as turmas do professor
- Organização de alunos por turma

### Gestão de Alunos
- Adição de alunos a turmas específicas
- Registro de notas por semestre
- Visualização de médias dos alunos
- Exclusão de alunos (com confirmação de senha do professor)

### Sistema de Notas
- Registro de 3 notas por semestre
- Cálculo automático de médias
- Visualização detalhada das notas por aluno
- Estatísticas de aprovação e reprovação

### Segurança
- Sistema de login para professores
- Proteção de rotas
- Confirmação de senha para exclusão de alunos
- Cada professor só acessa suas próprias turmas e alunos

## Tecnologias Utilizadas

- Python 3.x
- Django
- HTML5
- CSS3
- JavaScript
- SQLite (banco de dados)

## Requisitos

- Python 3.x
- pip (gerenciador de pacotes Python)
- virtualenv (recomendado)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Thauangg/Site-Escolar.git
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
```

3. Ative o ambiente virtual:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. Instale as dependências:
```bash
pip install -r requirements.txt
```

5. Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

6. Crie um superusuário (opcional):
```bash
python manage.py createsuperuser
```

7. Inicie o servidor:
```bash
python manage.py runserver
```

## Estrutura do Projeto

```
Site-Escolar/
├── notas/
│   ├── migrations/
│   ├── templates/
│   │   └── notas/
│   │       ├── adicionar_notas.html
│   │       ├── adicionar_turma.html
│   │       ├── home.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── visualizar_notas.html
│   │       └── visualizar_turmas.html
│   ├── models.py
│   ├── views.py
│   └── urls.py
├── manage.py
└── README.md
```

## Como Usar

1. Acesse o sistema através do navegador:
```
http://localhost:8000
```

2. Faça login ou registre-se como professor

3. Após o login, você terá acesso a:
   - Adicionar turmas
   - Visualizar turmas
   - Adicionar alunos
   - Gerenciar notas
   - Visualizar estatísticas

## Fluxo de Uso

1. Primeiro, crie uma turma
2. Adicione alunos à turma
3. Registre as notas dos alunos
4. Visualize as notas e estatísticas
5. Gerencie os alunos conforme necessário

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas alterações (`git commit -m 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## Contato

Para sugestões, dúvidas ou problemas, abra uma issue no repositório. 