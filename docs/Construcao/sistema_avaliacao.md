# Sistema de Seleção e Comunicação de Resultados

## Visão Geral

Este sistema permite que professores avaliem candidatos a vagas de monitoria, registrem suas avaliações e comuniquem resultados (aprovação, lista de espera, reprovação) de forma padronizada.

## Funcionalidades Implementadas

### 1. Modelo de Avaliação (`AvaliacaoCandidato`)

O modelo armazena todas as informações da avaliação:

- **Nota**: Avaliação numérica de 0 a 10 (opcional)
- **Critérios de Avaliação**: Campo JSON para registrar critérios específicos
- **Comentários**: Observações internas sobre o candidato
- **Resultado**: Aprovado, Lista de Espera ou Reprovado
- **Mensagem Padronizada**: Mensagem que será comunicada ao candidato
- **Status de Comunicação**: Indica se o resultado já foi comunicado
- **Data de Comunicação**: Timestamp de quando foi comunicado

### 2. Status de Candidatura Atualizado

Foi adicionado o novo status `LISTA_ESPERA` ao modelo `Candidatura`, permitindo:
- Submetida
- Em Análise
- Aprovada
- **Lista de Espera** (novo)
- Rejeitada
- Cancelada

### 3. Interface Web para Professores

#### 3.1 Listar Candidatos para Avaliação
**URL**: `/professor/avaliar/<vaga_id>/`

Exibe todos os candidatos de uma vaga específica com:
- Dados básicos do candidato (nome, email, curso, CR)
- Status da candidatura
- Indicador se já foi avaliado pelo professor
- Links para documentos (histórico, currículo)
- Botão para avaliar/editar avaliação

#### 3.2 Formulário de Avaliação
**URL**: `/professor/avaliar/candidato/<candidatura_id>/`

Permite registrar/atualizar uma avaliação com:
- Nota de 0 a 10
- Comentários internos
- Resultado da seleção (obrigatório)
- Mensagem padronizada para o candidato (obrigatório)

**Validações**:
- Se um resultado for definido, a mensagem é obrigatória
- A nota deve estar entre 0 e 10
- Apenas um professor pode avaliar cada candidato (unique constraint)

#### 3.3 Comunicar Resultado
**URL**: `/professor/comunicar/<avaliacao_id>/`

Permite marcar o resultado como comunicado ao candidato:
- Exibe resumo da avaliação
- Confirma que o candidato será notificado
- Registra data e hora da comunicação

### 4. API REST Endpoints

#### 4.1 CRUD de Avaliações
```
GET    /api/avaliacoes/              - Lista todas as avaliações
POST   /api/avaliacoes/              - Cria nova avaliação
GET    /api/avaliacoes/{id}/         - Detalhe de uma avaliação
PUT    /api/avaliacoes/{id}/         - Atualiza avaliação
PATCH  /api/avaliacoes/{id}/         - Atualiza parcialmente
DELETE /api/avaliacoes/{id}/         - Remove avaliação
```

#### 4.2 Actions Especiais

**Comunicar Resultado**
```
POST /api/avaliacoes/{id}/comunicar_resultado/
```
Marca o resultado como comunicado.

**Avaliações Pendentes**
```
GET /api/avaliacoes/pendentes/
```
Lista candidaturas que ainda não foram avaliadas pelo professor logado.

**Avaliação em Lote**
```
POST /api/avaliacoes/avaliar_lote/
Body: {
  "avaliacoes": [
    {
      "candidatura_id": 1,
      "nota": 8.5,
      "resultado": "approved",
      "mensagem_resultado": "Parabéns! Você foi aprovado..."
    },
    ...
  ]
}
```
Permite criar múltiplas avaliações de uma vez.

### 5. Integração com Candidaturas

Quando uma avaliação é criada/atualizada com um resultado:
- O status da candidatura é automaticamente atualizado
- **Aprovado** → `CandidaturaStatus.APROVADA`
- **Lista de Espera** → `CandidaturaStatus.LISTA_ESPERA`
- **Reprovado** → `CandidaturaStatus.REJEITADA`

### 6. Auditoria

Todas as ações são registradas no sistema de auditoria:
- `criar_avaliacao` - Quando uma nova avaliação é criada
- `atualizar_avaliacao` - Quando uma avaliação é editada
- `comunicar_resultado` - Quando o resultado é comunicado
- `criar_avaliacao_lote` - Para avaliações em lote

## Fluxo de Uso

1. **Professor acessa a lista de vagas**
   - Menu: Professor → Gerenciar Vagas
   - Visualiza suas vagas com contadores de candidaturas

2. **Seleciona uma vaga para avaliar candidatos**
   - Clica em "Avaliar Candidatos" na vaga desejada
   - Vê lista completa de candidaturas

3. **Avalia cada candidato**
   - Clica no botão de avaliar
   - Visualiza informações completas do candidato
   - Preenche formulário de avaliação:
     - Nota (opcional)
     - Comentários internos
     - Resultado (obrigatório)
     - Mensagem para o candidato (obrigatório)
   - Salva a avaliação

4. **Comunica os resultados**
   - Na lista de candidatos, identifica avaliações completas
   - Clica em "Comunicar Resultado"
   - Confirma a comunicação
   - Sistema registra data/hora da notificação

## Permissões

- **Coordenadores/Professores**: Podem avaliar candidatos de suas disciplinas
- **Administradores**: Acesso total a todas as avaliações
- **Estudantes**: Não têm acesso às avaliações

## Estrutura de Dados

### AvaliacaoCandidato
```python
{
    "id": 1,
    "candidatura": {...},
    "avaliador": {...},
    "nota": 8.50,
    "criterios_avaliacao": {
        "conhecimento_tecnico": 9,
        "motivacao": 8,
        "experiencia": 7
    },
    "comentarios": "Candidato demonstrou...",
    "resultado": "approved",
    "mensagem_resultado": "Parabéns! Você foi aprovado...",
    "resultado_comunicado": true,
    "data_comunicacao": "2025-11-12T15:30:00Z",
    "created_at": "2025-11-12T10:00:00Z",
    "updated_at": "2025-11-12T15:30:00Z"
}
```

## Exemplos de Uso da API

### Criar Avaliação
```bash
curl -X POST http://localhost:8000/api/avaliacoes/ \
  -H "Authorization: Token <seu-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "candidatura_id": 1,
    "nota": 8.5,
    "comentarios": "Excelente candidato",
    "resultado": "approved",
    "mensagem_resultado": "Parabéns! Você foi aprovado para a vaga de monitoria."
  }'
```

### Listar Avaliações Pendentes
```bash
curl -X GET http://localhost:8000/api/avaliacoes/pendentes/ \
  -H "Authorization: Token <seu-token>"
```

### Comunicar Resultado
```bash
curl -X POST http://localhost:8000/api/avaliacoes/1/comunicar_resultado/ \
  -H "Authorization: Token <seu-token>"
```

## Validações Implementadas

1. **Avaliação única por professor/candidato**: Um professor não pode criar múltiplas avaliações para o mesmo candidato
2. **Resultado requer mensagem**: Se o resultado for definido, a mensagem é obrigatória
3. **Nota entre 0-10**: Se fornecida, a nota deve estar no intervalo válido
4. **Comunicação única**: Um resultado não pode ser comunicado mais de uma vez
5. **Resultado definido**: Só é possível comunicar se o resultado estiver definido

## Admin Django

O modelo `AvaliacaoCandidato` está registrado no Django Admin com:
- Listagem com filtros por resultado e status de comunicação
- Busca por nome/email do candidato e avaliador
- Campos somente leitura para timestamps
- Organização em fieldsets para melhor UX

## Próximos Passos (Sugestões)

1. **Notificações por Email**: Integrar envio automático de emails ao comunicar resultados
2. **Dashboard de Avaliações**: Criar relatório com estatísticas de avaliações
3. **Exportação de Dados**: Permitir exportar avaliações em CSV/PDF
4. **Comentários Múltiplos**: Sistema de comentários/anotações adicionais
5. **Histórico de Alterações**: Rastrear mudanças nas avaliações
