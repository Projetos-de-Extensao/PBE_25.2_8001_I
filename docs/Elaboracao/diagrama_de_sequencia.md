---
id: diagrama_de_casos de uso
title: Diagrama de Casos de Uso
---

``` mermaid
graph LR
  A[Start] --> B{Error?};
  B -->|Yes| C[Hmm...];
  C --> D[Debug];
  D --> B;
  B ---->|No| E[Yay!];
```
### Caso de Uso: Fluxo completo de Monitoria

(Publicar vaga → Candidatura → Seleção → Vínculo → Atendimento → Feedback)

Atores

Professor – publica vaga, avalia candidatura.

Aluno – candidata-se, recebe aprovação/negação, agenda/participa de atendimento, registra feedback.

Monitor – após aprovação, agenda atendimentos e recebe feedbacks.

Sistema – valida, persiste dados, orquestra fluxos.

Notificação – componente que envia mensagens (e-mail, in-app, push).

### Pré-condições

Professor e Aluno possuem conta cadastrada.

Professor está autenticado para publicar/avaliar.

Aluno está autenticado para se candidatar/registrar feedback.

Disciplina existe e está ativa.

### Fluxo Básico

Professor autentica-se no Sistema.

Professor publica vaga de monitoria.

Sistema cria a VagaMonitoria com status Publicada.

Sistema → Notificação: informa o Professor que a vaga foi publicada.

Aluno autentica-se no Sistema.

Aluno envia candidatura (histórico escolar, carta de motivação, anexos).

Sistema cria a Candidatura com status Pendente.

Sistema → Notificação: informa o Professor sobre a nova candidatura.

Professor avalia candidatura.

Sistema processa avaliação: Aprovada → cria VinculoMonitoria ativo.

Sistema → Notificação: informa Aluno da aprovação e Professor da criação do vínculo.

Monitor agenda atendimento.

Sistema cria Atendimento com status Agendado.

Sistema → Notificação: informa Aluno sobre o agendamento.

Após o atendimento, Aluno registra feedback.

Sistema salva Feedback.

Sistema → Notificação: informa Monitor sobre novo feedback.

### Fluxos Alternativos

Falha de autenticação: Sistema rejeita login e pede novas credenciais.

Publicação inválida (disciplina inexistente, número de vagas ≤ 0, requisitos faltando): Sistema exibe erro ao Professor.

Candidatura inválida (duplicada, documentos ausentes, vaga encerrada): Sistema exibe erro ao Aluno.

Avaliação Negada: Sistema → Notificação: informa Aluno da negação. Nenhum vínculo é criado.

Conflito de agenda ao criar atendimento: Sistema rejeita e pede novo horário.

Cancelamento de atendimento: Atendimento muda status para Cancelado e Sistema notifica partes.

No-show: Sistema marca status NoShow e pode notificar coordenação.

Feedback inválido: Sistema rejeita e pede correção.

Falha em notificações: fluxo principal segue, notificações podem ser reenviadas em background.

### Pós-condições

Se candidatura Aprovada:

VinculoMonitoria criado e ativo.

Atendimentos podem existir nos estados Agendado, Cancelado ou NoShow.

Feedback registrado (se aluno enviou).

Se candidatura Negada:

VinculoMonitoria não criado.

Candidatura marcada como Negada e notificações enviadas.

Todas as ações relevantes registradas em log/auditoria.
