---
id: Brainstorm
title: Brainstorm
hide:
  - toc
---

<p align = "justify">
O brainstorm é uma técnica de elicitação de requisitos que consiste em reunir a equipe e discutir tópicos gerais do projeto apresentados no documento de problema de negócio. No brainstorm o diálogo é incentivado e críticas são evitadas para permitir que todos colaborem com suas próprias ideias.
</p>

---

## Metodologia
<p align = "justify">
A equipe se reuniu para debater ideias gerais sobre o projeto . O integrante <b>Davi</b> foi o moderador responsável por conduzir e registrar o brainstorming, direcionando a equipe, organizando as contribuições em um quadro colaborativo no <b>Miro</b> e transcrevendo as respostas para este documento.
</p>

---

## Qual o objetivo principal da aplicação?

<p align="justify">
Deve ser uma plataforma onde qualquer aluno possa <i>encontrar</i> monitorias e informações de disciplinas, horários e vagas abertas.
</p>

<p align="justify">
A plataforma deve fornecer <i>transparência</i> no processo de seleção de monitores e facilitar a comunicação entre alunos, monitores e professores.
</p>

<p align="justify">
O objetivo da aplicação é <i>centralizar</i> processos hoje dispersos (divulgação de vagas, candidaturas, atendimentos e feedback).
</p>

<p align="justify">
O principal objetivo da aplicação é <i>organizar e acompanhar</i> o ciclo completo da monitoria (abertura de vaga → seleção → atendimentos → avaliação).
</p>

<p align="justify">
A plataforma deve <i>gerenciar</i> notificações e lembretes (novas vagas, alterações de status, horários de atendimento e prazos de feedback).
</p>

---

## Como será o processo para cadastrar um novo cliente?  <!-- (aluno/monitor/professor) -->

<p align="justify">
O usuário acessa “Cadastre-se”, escolhe o perfil (Aluno, Candidato a Monitor, Professor) e informa nome, e-mail, curso e semestre.
</p>

<p align="justify">
Confirma o e-mail e, ao entrar, tem acesso ao <i>perfil</i> com edição de dados e preferências (modalidade presencial/online, campus, áreas de interesse).
</p>

<p align="justify">
Para Professor, o cadastro pode exigir <i>validação</i> do administrador antes de abrir vagas.
</p>

<p align="justify">
Após o cadastro, o usuário visualiza disciplinas, vagas de monitoria e pode acompanhar candidaturas/atendimentos.
</p>

<p align="justify">
O sistema envia confirmação e ativa <i>notificações</i> (in-app e/ou e-mail) conforme preferências do usuário.
</p>

---

## Como poderá cadastrar uma nova disciplina ou abrir uma vaga de monitoria?

<p align="justify">
Professor (ou Admin) acessa o painel e cadastra a disciplina (nome, código, descrição, semestre, modalidade).
</p>

<p align="justify">
Para abrir vaga: define requisitos (CR mínimo, conhecimentos), período de candidatura, nº de vagas e vínculo com a disciplina.
</p>

<p align="justify">
A vaga pode ser <i>editada</i> posteriormente (requisitos, período, quantidade).
</p>

<p align="justify">
A vaga é publicada após validação (quando aplicável) e fica visível para os alunos interessados.
</p>

---

## Como seria a forma de o professor adicionar um novo monitor?

<p align="justify">
 No painel da disciplina, o professor avalia candidaturas recebidas, aprova/recusa e <i>vincula</i> o monitor selecionado, registrando datas de início/fim e carga horária.
</p>

---

## Como será o sistema de feedback entre alunos e monitores?

<p align="justify">
Ao final de atendimentos (ou do período), o aluno avalia o monitor (disponibilidade, clareza, domínio, ajuda prestada) e pode deixar comentários.
</p>

<p align="justify">
O professor também pode avaliar o desempenho do monitor na disciplina.
</p>

<p align="justify">
O sistema calcula a <i>média</i> das avaliações e exibe no perfil do monitor; histórico de feedbacks fica disponível para consulta.
</p>

---

## Quais informações seriam interessantes para os usuários?

<p align="justify">
Para alunos: lista e filtros de disciplinas/monitorias, vagas abertas, avaliações de monitores e agenda de atendimentos.
</p>

<p align="justify">
Para professores: monitores vinculados, status das vagas, relatórios simples (atendimentos, médias de avaliação).
</p>

<p align="justify">
Para monitores: agenda, fila de solicitações de atendimento, feedback recebido e orientações/regulamentos do curso.
</p>

---

## Outras perguntas pertinentes ao contexto

<p align="justify">
Haverá níveis de acesso (Admin, Professor, Monitor, Aluno) e permissões específicas?
</p>

<p align="justify">
Como tratar monitorias <i>remotas</i> e <i>híbridas</i> (links de reunião, presença)?
</p>

<p align="justify">
Quais critérios mínimos para candidatura (CR, pré-requisitos) e como lidar com desistências?
</p>

---

## Requisitos Elicitados

| ID   | Descrição |
|------|-----------|
| BS01 | O usuário poderá visualizar disciplinas e monitorias disponíveis. |
| BS02 | Professores poderão cadastrar novas disciplinas. |
| BS03 | Professores poderão editar disciplinas cadastradas. |
| BS04 | Usuários poderão configurar filtros personalizados (semestre, professor, modalidade, campus). |
| BS05 | O usuário poderá acessar informações sobre vagas de monitoria. |
| BS06 | O usuário poderá visualizar regulamentos e orientações do programa. |
| BS07 | O usuário poderá se cadastrar e autenticar na plataforma. |
| BS08 | O usuário poderá acessar ajuda/suporte básico. |
| BS09 | O usuário receberá notificações personalizadas (novas vagas, status, lembretes). |
| BS10 | A disciplina terá atributos como nome, código, descrição e semestre. |
| BS11 | Vagas serão vinculadas a disciplinas específicas. |
| BS12 | Disciplinas/vagas poderão exigir validação antes da publicação. |
| BS13 | Monitores poderão ser avaliados por alunos e professores. |
| BS14 | Relatórios simples para professores (monitores, atendimentos, médias). |
| BS15 | Conteúdo poderá ser filtrado por modalidade (presencial/online) e localização. |

---

## Conclusão

<p align="justify">
A aplicação da técnica de elicitação via brainstorming (moderada por Davi e organizada no Miro) permitiu identificar requisitos funcionais e não funcionais adequados ao contexto acadêmico. O escopo prioriza simplicidade, transparência e eficiência na gestão do ciclo de monitorias (vagas, seleção, atendimentos e feedback), oferecendo valor direto para alunos, monitores e professores.
</p>

---

## Autor(es)

| Data       | Versão | Descrição              | Autor(es)        |
|------------|--------|------------------------|------------------|
| 10/09/2025 | 1.0    | Criação do documento   | Davi (moderador) |
