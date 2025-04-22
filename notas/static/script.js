document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('alunoForm');
    
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const data = {
                nome: document.getElementById('nomeAluno').value,
                sem1_nota1: parseFloat(document.getElementById('sem1_nota1').value),
                sem1_nota2: parseFloat(document.getElementById('sem1_nota2').value),
                sem1_nota3: parseFloat(document.getElementById('sem1_nota3').value),
                sem2_nota1: parseFloat(document.getElementById('sem2_nota1').value),
                sem2_nota2: parseFloat(document.getElementById('sem2_nota2').value),
                sem2_nota3: parseFloat(document.getElementById('sem2_nota3').value),
                sem3_nota1: parseFloat(document.getElementById('sem3_nota1').value),
                sem3_nota2: parseFloat(document.getElementById('sem3_nota2').value),
                sem3_nota3: parseFloat(document.getElementById('sem3_nota3').value)
            };

            fetch('/salvar_dados/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    alert('Aluno adicionado com sucesso!');
                    form.reset();
                    location.reload(); // Recarrega a página para atualizar as estatísticas
                } else {
                    alert('Erro ao adicionar aluno: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Erro:', error);
                alert('Erro ao adicionar aluno. Por favor, tente novamente.');
            });
        });
    }
});

// Função auxiliar para obter o token CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 