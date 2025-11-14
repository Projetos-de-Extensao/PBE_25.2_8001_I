# Documentação Swagger/OpenAPI da API

## 📋 Visão Geral

A API do Sistema de Monitoria agora possui documentação interativa completa usando **Swagger/OpenAPI**, gerada automaticamente com o **drf-spectacular**.

## 🚀 Como Acessar

Após iniciar o servidor Django, você pode acessar a documentação através dos seguintes endereços:

### Swagger UI (Recomendado)
```
http://localhost:8000/api/docs/
```
Interface interativa e amigável para testar todos os endpoints da API.

### ReDoc
```
http://localhost:8000/api/redoc/
```
Documentação em formato de leitura limpo e organizado.

### Schema OpenAPI (JSON/YAML)
```
http://localhost:8000/api/schema/
```
Arquivo schema OpenAPI bruto para integração com outras ferramentas.

## 📚 Recursos Documentados

### Endpoints da API

#### 🎓 **Disciplinas** (`/api/disciplinas/`)
- **GET** - Listar todas as disciplinas
- **POST** - Criar nova disciplina (apenas coordenadores)
- **GET** /{id}/ - Detalhes de uma disciplina
- **PUT/PATCH** /{id}/ - Atualizar disciplina
- **DELETE** /{id}/ - Desativar disciplina

#### 📢 **Vagas de Monitoria** (`/api/vagas/`)
- **GET** - Listar vagas de monitoria
- **POST** - Criar nova vaga (apenas coordenadores)
- **GET** /{id}/ - Detalhes de uma vaga
- **PUT/PATCH** /{id}/ - Atualizar vaga
- **DELETE** /{id}/ - Arquivar vaga

**Actions Personalizadas:**
- **GET** `/api/vagas/dashboard/` - Estatísticas das vagas
- **GET** `/api/vagas/{id}/candidaturas/` - Candidaturas de uma vaga
- **POST** `/api/vagas/{id}/alterar_status/` - Alterar status da vaga
- **POST** `/api/vagas/{id}/duplicar/` - Duplicar vaga

#### 📝 **Candidaturas** (`/api/candidaturas/`)
- **GET** - Listar candidaturas
- **POST** - Submeter nova candidatura
- **GET** /{id}/ - Detalhes de uma candidatura
- **PUT/PATCH** /{id}/ - Atualizar candidatura
- **POST** /{id}/atualizar_status/ - Alterar status (coordenadores)

#### ⭐ **Avaliações** (`/api/avaliacoes/`)
- **GET** - Listar avaliações
- **POST** - Criar nova avaliação (apenas coordenadores)
- **GET** /{id}/ - Detalhes de uma avaliação
- **PUT/PATCH** /{id}/ - Atualizar avaliação
- **POST** /{id}/comunicar_resultado/ - Marcar resultado como comunicado

**Actions Personalizadas:**
- **GET** `/api/avaliacoes/pendentes/` - Candidaturas sem avaliação
- **POST** `/api/avaliacoes/avaliar_lote/` - Avaliar múltiplos candidatos

#### 🔐 **Autenticação**
- **POST** `/api/auth/login/` - Login com JWT
- **POST** `/api/auth/register/` - Registrar novo usuário
- **POST** `/api/jwt/` - Obter token JWT
- **POST** `/api/jwt/refresh/` - Atualizar token JWT
- **GET** `/api/me/profile/` - Perfil do usuário logado
- **PATCH** `/api/me/profile/` - Atualizar perfil

## 🔑 Autenticação na Documentação

### Usando JWT (Recomendado)

1. Obtenha o token JWT:
   - Vá para `/api/jwt/` ou `/api/auth/login/`
   - Forneça username e password
   - Copie o token `access` retornado

2. Autorize no Swagger UI:
   - Clique no botão **"Authorize"** no topo da página
   - Digite: `Bearer seu_token_aqui`
   - Clique em **"Authorize"**

3. Agora você pode testar todos os endpoints autenticados!

### Exemplo de Token
```
Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

## 🧪 Testando Endpoints

### Passo a Passo

1. **Expanda um endpoint** clicando nele
2. Clique em **"Try it out"**
3. Preencha os parâmetros necessários
4. Clique em **"Execute"**
5. Veja a resposta logo abaixo

### Exemplo: Listar Vagas

```http
GET /api/vagas/
```

**Filtros disponíveis:**
- `status` - Filtrar por status (draft, published, etc.)
- `disciplina__codigo` - Filtrar por código da disciplina
- `search` - Busca por título ou disciplina

### Exemplo: Criar Candidatura

```http
POST /api/candidaturas/
Content-Type: application/json

{
  "vaga": 1,
  "candidato_nome": "João Silva",
  "candidato_email": "joao@example.com",
  "candidato_curso": "Ciência da Computação",
  "candidato_periodo": "5º período",
  "candidato_cr": 8.5,
  "carta_motivacao": "Tenho grande interesse em monitoria..."
}
```

## 📊 Schemas e Modelos

A documentação inclui todos os schemas dos modelos:

- **Disciplina** - Informações sobre disciplinas
- **VagaMonitoria** - Dados de vagas de monitoria
- **Candidatura** - Informações de candidaturas
- **AvaliacaoCandidato** - Dados de avaliações
- **UserProfile** - Perfil do usuário

Todos os campos, tipos, validações e exemplos estão documentados.

## 🔍 Filtros e Busca

### Filtros Disponíveis

A maioria dos endpoints suporta filtros via query params:

```
/api/vagas/?status=published&disciplina__semestre=2024.1
/api/candidaturas/?status=submitted&vaga_id=5
/api/avaliacoes/?resultado=approved
```

### Busca (Search)

Use o parâmetro `search` para buscar:

```
/api/vagas/?search=monitoria
/api/disciplinas/?search=programação
```

### Ordenação

Use o parâmetro `ordering`:

```
/api/vagas/?ordering=-created_at
/api/candidaturas/?ordering=candidato_nome
```

## 📦 Exportar Schema

Você pode exportar o schema OpenAPI para usar em outras ferramentas:

```bash
# Baixar schema JSON
curl http://localhost:8000/api/schema/ -o openapi.json

# Baixar schema YAML
curl http://localhost:8000/api/schema/?format=yaml -o openapi.yaml
```

## 🛠️ Ferramentas Compatíveis

O schema OpenAPI pode ser usado com:

- **Postman** - Importe o schema para criar coleções
- **Insomnia** - Importe para testar a API
- **OpenAPI Generator** - Gere clientes em várias linguagens
- **Swagger Editor** - Edite e visualize o schema

## 🎨 Personalização

A documentação pode ser personalizada em `settings.py`:

```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'API do Sistema de Monitoria',
    'DESCRIPTION': 'API REST para gerenciamento de vagas de monitoria',
    'VERSION': '1.0.0',
    # Adicione mais configurações conforme necessário
}
```

## 📝 Notas Importantes

1. **Permissões**: Alguns endpoints requerem permissões específicas:
   - 👨‍🎓 **Estudantes** - Podem ver vagas e suas próprias candidaturas
   - 👨‍🏫 **Coordenadores** - Podem gerenciar vagas e avaliar candidatos
   - 🔧 **Admins** - Acesso total

2. **Rate Limiting**: O endpoint de candidaturas tem limite de 5 requisições por minuto

3. **Upload de Arquivos**: Para endpoints que aceitam arquivos (ex: histórico, currículo):
   - Use `multipart/form-data`
   - Tamanho máximo: 5MB para PDFs

## 🐛 Problemas Comuns

### Erro 401 Unauthorized
- Verifique se você está autenticado
- Confirme se o token JWT não expirou
- Use o formato correto: `Bearer token`

### Erro 403 Forbidden
- Você não tem permissão para este recurso
- Verifique seu grupo de usuário (estudante/coordenador)

### Erro 400 Bad Request
- Verifique os dados enviados
- Consulte o schema do modelo na documentação
- Veja a mensagem de erro retornada

## 🚀 Iniciando o Servidor

```bash
# Ativar ambiente virtual
.venv\Scripts\activate

# Navegar para o diretório do projeto
cd Streaming

# Iniciar o servidor
python manage.py runserver

# Acessar documentação
# http://localhost:8000/api/docs/
```

## 📚 Recursos Adicionais

- [Documentação drf-spectacular](https://drf-spectacular.readthedocs.io/)
- [Especificação OpenAPI](https://swagger.io/specification/)
- [Django REST Framework](https://www.django-rest-framework.org/)

---

**Versão da API**: 1.0.0  
**Última Atualização**: Novembro 2025
