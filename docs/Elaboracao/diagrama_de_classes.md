---
id: diagrama_de_classes
title: Diagrama de Classes
---


<img width="3001" height="1212" alt="diagrama-de-classes" src="https://github.com/Projetos-de-Extensao/PBE_25.2_8001_I/blob/main/docs/assets/Diagrama_de_Classes/diagrama-de-classes.png
" />


@startuml

' Classes principais
class Usuario {
  - id: UUID
  - nome: String
  - email: String
  - senha: String
  - tipo: TipoUsuario
  - status: StatusConta
  + autenticar()
  + recuperarSenha()
  + editarPerfil()
}

enum TipoUsuario {
  Aluno
  Monitor
  Professor
  Admin
}

enum StatusConta {
  Pendente
  Ativa
  Bloqueada
}

class Perfil {
  - bio: String
  - fotoPerfil: String
  - departamentos: List<String>
  + editar()
  + visualizar()
}

class Disciplina {
  - id: UUID
  - nome: String
  - codigo: String
  - semestre: String
  - modalidade: String
  - campus: String
}

class VagaMonitoria {
  - id: UUID
  - disciplina: Disciplina
  - professorResponsavel: Usuario
  - requisitos: String
  - numeroVagas: int
  - status: StatusVaga
  + publicar()
  + editar()
  + salvarRascunho()
}

enum StatusVaga {
  Rascunho
  Publicada
  Encerrada
}

class Candidatura {
  - id: UUID
  - aluno: Usuario
  - vaga: VagaMonitoria
  - status: StatusCandidatura
  - historicoEscolar: String
  - cartaMotivacao: String
  + anexarDocumentos()
  + retirar()
}

enum StatusCandidatura {
  Pendente
  Aprovada
  Negada
}

class Selecao {
  - id: UUID
  - candidatura: Candidatura
  - avaliador: Usuario
  - nota: Float
  - comentario: String
  + avaliar()
}

class VinculoMonitoria {
  - id: UUID
  - monitor: Usuario
  - disciplina: Disciplina
  - dataInicio: Date
  - dataFim: Date
  - cargaHoraria: int
  + ativar()
  + desativar()
}

class Atendimento {
  - id: UUID
  - monitor: Usuario
  - aluno: Usuario
  - dataHora: DateTime
  - status: StatusAtendimento
  + agendar()
  + cancelar()
}

enum StatusAtendimento {
  Agendado
  Cancelado
  NoShow
}

class Mensagem {
  - id: UUID
  - remetente: Usuario
  - destinatario: Usuario
  - conteudo: String
  - dataEnvio: DateTime
  + enviar()
  + visualizar()
}

class Feedback {
  - id: UUID
  - avaliador: Usuario
  - monitor: Usuario
  - nota: Float
  - comentario: String
  - anonimo: Boolean
  + registrar()
}

class Notificacao {
  - id: UUID
  - destinatario: Usuario
  - tipo: String
  - mensagem: String
  - lida: Boolean
  + enviar()
  + marcarComoLida()
}

class Relatorio {
  + gerarPorDisciplina(disciplina: Disciplina)
  + exportarCSV()
}

class Admin {
  + aprovarProfessor(usuario: Usuario)
  + ocultarConteudo()
  + gerenciarTermosPoliticas()
  + verLogs()
}

' Relações
Usuario "1" -- "1" Perfil : possui >
Usuario "1" -- "*" Candidatura : faz >
Usuario "1" -- "*" Mensagem : envia/recebe >
Usuario "1" -- "*" Feedback : registra >
Usuario "1" -- "*" Atendimento : agenda/atende >
Usuario "1" -- "*" VinculoMonitoria : vinculado a >
Usuario "1" -- "*" Selecao : realiza >
Usuario "1" <|-- Admin
Usuario "1" <|-- Professor
Usuario "1" <|-- Aluno
Usuario "1" <|-- Monitor

VagaMonitoria "1" -- "1" Disciplina : relacionada a >
VagaMonitoria "1" -- "1" Usuario : criada por >
Candidatura "1" -- "1" VagaMonitoria : aplicada a >
Candidatura "1" -- "1" Usuario : realizada por >
Selecao "1" -- "1" Candidatura : avalia >
VinculoMonitoria "1" -- "1" Usuario : monitor >
VinculoMonitoria "1" -- "1" Disciplina : disciplina >
Atendimento "1" -- "1" Usuario : monitor >
Atendimento "1" -- "1" Usuario : aluno >
Mensagem "1" -- "1" Usuario : remetente >
Mensagem "1" -- "1" Usuario : destinatario >
Feedback "1" -- "1" Usuario : avaliador >
Feedback "1" -- "1" Usuario : monitor >

@enduml
