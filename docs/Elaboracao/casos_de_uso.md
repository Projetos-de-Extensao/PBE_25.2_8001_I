<img width="1360" height="1416" alt="sequencia_1" src="https://github.com/Projetos-de-Extensao/PBE_25.2_8001_I/blob/main/docs/assets/Casos_de_Uso/ChatGPT%20Image%2026%20de%20set.%20de%202025,%2000_58_14%20(1).png?raw=true" />

UC01 – Registrar-se na plataforma

Atores: Aluno, Monitor, Professor

Pré-condição: Nenhuma.

Fluxo: O usuário acessa o cadastro, preenche seus dados, confirma o e-mail e, se for um professor, aguarda a validação do administrador.

UC02 – Autenticar-se (login/recuperar senha)

Atores: Todos.

Pré-condição: Conta existente.

Fluxo: O usuário fornece e-mail e senha, e o sistema inicia a sessão.

Fluxo Alternativo: Se o usuário esquecer a senha, ele pode recuperá-la via e-mail.

UC03 – Editar perfil

Atores: Todos.

Pré-condição: Usuário logado.

Fluxo: O usuário altera seus dados pessoais.

Fluxo Alternativo: Um professor pode vincular departamentos e disciplinas ao seu perfil.

UC04 – Navegar e filtrar disciplinas/monitorias

Atores: Aluno, Monitor, Professor (ou visitante com visão restrita).

Pré-condição: Logado ou visitante.

Fluxo: O usuário navega pelas opções de disciplinas ou monitorias e pode filtrar a lista por semestre, modalidade ou campus.

UC05 – Abrir vaga de monitoria

Atores: Professor.

Pré-condição: Professor validado pelo sistema.

Fluxo: O professor publica uma vaga, definindo requisitos, período e o número de vagas disponíveis.

Fluxo Alternativo: O professor pode salvar a vaga como rascunho ou editá-la posteriormente.

UC06 – Candidatar-se à vaga

Atores: Aluno (candidato).

Pré-condição: Usuário logado e que atende aos requisitos da vaga.

Fluxo: O aluno registra sua candidatura na vaga.

Fluxo Alternativo: O aluno pode anexar seu histórico acadêmico ou retirar a candidatura.

UC07 – Selecionar monitores

Atores: Professor.

Pré-condição: Candidaturas recebidas.

Fluxo: O professor analisa as candidaturas e altera o status para “aprovado”, “negado” ou “aguardando”, e o sistema envia convites.

UC08 – Vincular monitor à disciplina

Atores: Professor, Admin.

Pré-condição: Monitor aprovado.

Fluxo: O vínculo entre o monitor e a disciplina é ativado, registrando datas e a carga horária.

UC09 – Publicar agenda e agendar atendimentos

Atores: Monitor (publica agenda), Aluno (agenda atendimento).

Pré-condição: Vínculo de monitoria ativo.

Fluxo: Um aluno agenda um horário disponível na agenda do monitor.

Fluxo Alternativo: É possível cancelar o agendamento com justificativa.

UC10 – Trocar mensagens/comentários

Atores: Aluno, Monitor, Professor.

Pré-condição: Usuário logado e relacionado à disciplina ou vaga.

Fluxo: Os usuários trocam mensagens em um histórico associado ao contexto.

UC11 – Avaliar monitoria (feedback 360)

Atores: Aluno, Professor.

Pré-condição: Atendimento realizado ou período de monitoria encerrado.

Fluxo: O aluno e o professor registram suas avaliações sobre a monitoria.

Fluxo Alternativo: A avaliação pode ser anônima, dependendo da configuração.

UC12 – Receber notificações

Atores: Todos.

Fluxo: O sistema envia notificações para eventos importantes (nova vaga, mudança de status, lembretes de atendimento ou feedback).

UC13 – Consultar regulamentos

Atores: Todos.

Fluxo: O usuário acessa e visualiza os documentos ou links com os regulamentos da plataforma.

UC14 – Relatórios simples por disciplina

Atores: Professor.

Fluxo: O professor pode gerar relatórios que mostram dados como o número de monitores ativos, o total de atendimentos e a média das avaliações por disciplina.

UC15 – Moderação/Admin

Atores: Admin.

Fluxo: O administrador pode aprovar novos professores, moderar ou ocultar conteúdo e gerenciar as políticas e termos de uso do sistema.

