from pathlib import Path

from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


from .forms import CandidaturaPublicForm, AvaliacaoCandidatoForm
from .models import (
    AvaliacaoCandidato,
    Candidatura,
    CandidaturaStatus,
    Disciplina,
    ResultadoSelecaoChoices,
    UserProfile,
    VagaMonitoria,
    VagaMonitoriaStatus,
)
from .permissions import (
    IsCoordinator,
    is_admin,
    is_coordinator,
    is_student,
)
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserProfileSerializer,
    UserRegistrationSerializer,
    AvaliacaoCandidatoSerializer,
    CandidaturaSerializer, 
    DisciplinaSerializer, 
    VagaMonitoriaSerializer
)
from .utils import registrar_auditoria


def login_view(request):
    """
    View customizada para login na raiz do servidor
    """
    # Se o usuário já está autenticado, redireciona para index
    if request.user.is_authenticated:
        return redirect('index')
    
    # Se for POST, processa o login
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        
        # Autentica o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login bem-sucedido
            login(request, user)
            
            # Verifica se há um 'next' parameter (para redirecionar para página solicitada)
            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Caso contrário, redireciona para index
            return redirect('index')
        else:
            # Credenciais inválidas
            messages.error(request, 'Usuário ou senha inválidos.')
            contexto = {
                'error': 'Credenciais inválidas',
                'next': request.POST.get('next') or request.GET.get('next') or '',
                'username': username,
            }
            return render(request, 'login.html', contexto)
    
    # Se for GET, apenas mostra o formulário de login
    return render(request, 'login.html', {
        'next': request.GET.get('next') or '',
        'username': '',
    })


def register_page(request):
    """Serve a lightweight React-powered registration page."""
    return render(request, "register.html")


@login_required
def user_profile_page(request):
    """Renderiza a área do usuário com SPA React simples."""
    return render(request, "user_area.html")


class ApiLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ApiRegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token_serializer = CustomTokenObtainPairSerializer(
            data={
                "username": user.username,
                "password": request.data.get("password", ""),
            },
            context=self.get_serializer_context(),
        )
        token_serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(token_serializer.validated_data, status=status.HTTP_201_CREATED, headers=headers)


class CurrentUserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        profile, _ = UserProfile.objects.get_or_create(user=self.request.user)
        return profile


def logout_view(request):
    """
    View customizada para logout
    """
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('login')


@login_required
def index(request):
    vagas_publicadas = (
        VagaMonitoria.objects.select_related("disciplina", "disciplina__departamento")
        .filter(status=VagaMonitoriaStatus.PUBLICADA, ativo=True)
        .order_by("inscricoes_fim")[:6]
    )
    return render(request, "index.html", {"vagas_publicadas": vagas_publicadas})


def area_candidato(request):
    contexto = {"email_form_submitted": False}
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip().lower()
        candidaturas = (
            Candidatura.objects.select_related("vaga", "vaga__disciplina")
            .filter(candidato_email__iexact=email)
            .order_by("-created_at")
        )
        if not candidaturas.exists():
            messages.error(request, "Nenhuma candidatura encontrada para este e-mail.")
        else:
            primeira = candidaturas.first()
            contexto.update(
                {
                    "candidato_nome": primeira.candidato_nome,
                    "candidato_email": primeira.candidato_email,
                    "candidaturas": list(candidaturas),
                    "email_form_submitted": True,
                }
            )
    return render(request, "area_candidato.html", contexto)


@login_required
def listar_vagas(request):
    hoje = timezone.now().date()
    vagas = (
        VagaMonitoria.objects.select_related("disciplina", "disciplina__departamento")
        .filter(
            status=VagaMonitoriaStatus.PUBLICADA,
            ativo=True,
            inscricoes_fim__gte=hoje,
        )
        .order_by("inscricoes_fim")
    )
    departamentos = Disciplina.objects.values_list("departamento__sigla", flat=True).distinct()
    return render(
        request,
        "listar_vagas.html",
        {
            "vagas": vagas,
            "departamentos": departamentos,
        },
    )


@login_required
@login_required
def prof_index(request):
    minhas_vagas = (
        VagaMonitoria.objects.select_related("disciplina")
        .filter(disciplina__coordenador=request.user)
        .annotate(total_candidaturas=Count("candidaturas"))
        .order_by("-created_at")
    )
    return render(request, "professor/prof_Index.html", {"minhas_vagas": minhas_vagas})


@login_required
def prof_gerenciar_vagas(request):
    """View para gerenciar vagas de monitoria"""
    minhas_vagas = (
        VagaMonitoria.objects.select_related("disciplina")
        .filter(disciplina__coordenador=request.user)
        .annotate(total_candidaturas=Count("candidaturas"))
        .order_by("-created_at")
    )
    return render(request, "professor/prof_gerenciarVagas.html", {"minhas_vagas": minhas_vagas})


@login_required  
def prof_gerenciar_candidaturas(request):
    """View para gerenciar candidaturas"""
    candidaturas = (
        Candidatura.objects.select_related("vaga", "vaga__disciplina")
        .filter(vaga__disciplina__coordenador=request.user)
        .order_by("-created_at")
    )
    return render(request, "professor/prof_gerenciarCandidatura.html", {"candidaturas": candidaturas})


@login_required
def prof_relatorios(request):
    """View para exibir relatórios com estatísticas dinâmicas"""
    from django.db.models import Count, Q
    from django.db.models.functions import TruncMonth
    import json
    
    # Filtrar apenas vagas e candidaturas do professor logado
    vagas_professor = VagaMonitoria.objects.filter(disciplina__coordenador=request.user)
    candidaturas_professor = Candidatura.objects.filter(vaga__disciplina__coordenador=request.user)
    
    # Estatísticas básicas
    total_vagas = vagas_professor.count()
    total_candidaturas = candidaturas_professor.count()
    candidaturas_aprovadas = candidaturas_professor.filter(status=CandidaturaStatus.APROVADA).count()
    
    # Calcular média de candidatos por vaga
    media_candidatos = round(total_candidaturas / total_vagas, 1) if total_vagas > 0 else 0
    
    # Calcular taxa de aprovação
    taxa_aprovacao = round((candidaturas_aprovadas / total_candidaturas * 100), 1) if total_candidaturas > 0 else 0
    
    # Candidaturas por mês (últimos 4 meses)
    candidaturas_por_mes = candidaturas_professor.annotate(
        mes=TruncMonth('created_at')
    ).values('mes').annotate(
        total=Count('id')
    ).order_by('mes')[:4]
    
    meses_labels = [c['mes'].strftime('%b') for c in candidaturas_por_mes]
    meses_dados = [c['total'] for c in candidaturas_por_mes]
    
    # Status das candidaturas
    status_counts = candidaturas_professor.values('status').annotate(
        total=Count('id')
    )
    
    status_labels = []
    status_dados = []
    for s in status_counts:
        status_display = dict(CandidaturaStatus.choices).get(s['status'], s['status'])
        status_labels.append(status_display)
        status_dados.append(s['total'])
    
    # Vagas por disciplina (top 5)
    vagas_por_disciplina = vagas_professor.values(
        'disciplina__nome'
    ).annotate(
        total=Count('id')
    ).order_by('-total')[:5]
    
    disciplinas_labels = [v['disciplina__nome'] for v in vagas_por_disciplina]
    disciplinas_dados = [v['total'] for v in vagas_por_disciplina]
    
    # Distribuição de CR dos candidatos
    cr_ranges = [
        {'label': '7.0-8.0', 'min': 7.0, 'max': 8.0},
        {'label': '8.0-9.0', 'min': 8.0, 'max': 9.0},
        {'label': '9.0-10.0', 'min': 9.0, 'max': 10.0},
    ]
    
    cr_labels = []
    cr_dados = []
    for r in cr_ranges:
        count = candidaturas_professor.filter(
            candidato_cr__gte=r['min'],
            candidato_cr__lt=r['max']
        ).count()
        cr_labels.append(r['label'])
        cr_dados.append(count)
    
    context = {
        'total_vagas': total_vagas,
        'total_candidaturas': total_candidaturas,
        'candidaturas_aprovadas': candidaturas_aprovadas,
        'media_candidatos': media_candidatos,
        'taxa_aprovacao': taxa_aprovacao,
        # Dados para gráficos (convertidos para JSON)
        'meses_labels': json.dumps(meses_labels),
        'meses_dados': json.dumps(meses_dados),
        'status_labels': json.dumps(status_labels),
        'status_dados': json.dumps(status_dados),
        'disciplinas_labels': json.dumps(disciplinas_labels),
        'disciplinas_dados': json.dumps(disciplinas_dados),
        'cr_labels': json.dumps(cr_labels),
        'cr_dados': json.dumps(cr_dados),
    }
    return render(request, "professor/prof_relatorio.html", context)


@login_required
def prof_avaliar_candidatos(request, vaga_id=None):
    """
    View para professores listarem e avaliarem candidatos de uma vaga específica
    """
    if not is_coordinator(request.user):
        messages.error(request, "Acesso restrito a coordenadores.")
        return redirect("index")
    
    # Se vaga_id foi fornecido, busca a vaga
    vaga = None
    if vaga_id:
        vaga = get_object_or_404(
            VagaMonitoria,
            pk=vaga_id,
            disciplina__coordenador=request.user
        )
    
    # Busca candidaturas da vaga (ou todas do professor)
    candidaturas = Candidatura.objects.select_related(
        "vaga", "vaga__disciplina"
    ).prefetch_related("avaliacoes", "avaliacoes__avaliador")
    
    if vaga:
        candidaturas = candidaturas.filter(vaga=vaga)
    else:
        candidaturas = candidaturas.filter(vaga__disciplina__coordenador=request.user)
    
    candidaturas = candidaturas.order_by("-created_at")
    
    # Adiciona informação se já foi avaliado pelo professor atual
    for candidatura in candidaturas:
        candidatura.avaliado_por_mim = candidatura.avaliacoes.filter(
            avaliador=request.user
        ).exists()
    
    context = {
        "candidaturas": candidaturas,
        "vaga": vaga,
        "total": candidaturas.count(),
    }
    
    return render(request, "professor/prof_avaliarCandidatos.html", context)


@login_required
def prof_avaliar_candidato_form(request, candidatura_id):
    """
    View para formulário de avaliação de um candidato específico
    """
    if not is_coordinator(request.user):
        messages.error(request, "Acesso restrito a coordenadores.")
        return redirect("index")
    
    candidatura = get_object_or_404(
        Candidatura.objects.select_related("vaga", "vaga__disciplina"),
        pk=candidatura_id,
        vaga__disciplina__coordenador=request.user
    )
    
    # Verifica se já existe avaliação deste professor para este candidato
    avaliacao_existente = AvaliacaoCandidato.objects.filter(
        candidatura=candidatura,
        avaliador=request.user
    ).first()
    
    if request.method == "POST":
        form = AvaliacaoCandidatoForm(request.POST, instance=avaliacao_existente)
        
        if form.is_valid():
            with transaction.atomic():
                avaliacao = form.save(commit=False)
                avaliacao.candidatura = candidatura
                avaliacao.avaliador = request.user
                avaliacao.save()
                
                # Atualiza status da candidatura se resultado foi definido
                if avaliacao.resultado:
                    if avaliacao.resultado == ResultadoSelecaoChoices.APROVADO:
                        candidatura.status = CandidaturaStatus.APROVADA
                    elif avaliacao.resultado == ResultadoSelecaoChoices.LISTA_ESPERA:
                        candidatura.status = CandidaturaStatus.LISTA_ESPERA
                    elif avaliacao.resultado == ResultadoSelecaoChoices.REPROVADO:
                        candidatura.status = CandidaturaStatus.REJEITADA
                    candidatura.save()
                
                registrar_auditoria(
                    request.user, 
                    "avaliar_candidato" if not avaliacao_existente else "atualizar_avaliacao",
                    avaliacao
                )
                
                messages.success(request, "Avaliação registrada com sucesso!")
                return redirect("prof_avaliar_candidatos", vaga_id=candidatura.vaga.pk)
    else:
        initial_data = {"candidatura": candidatura}
        form = AvaliacaoCandidatoForm(instance=avaliacao_existente, initial=initial_data)
    
    context = {
        "form": form,
        "candidatura": candidatura,
        "avaliacao_existente": avaliacao_existente,
    }
    
    return render(request, "professor/prof_avaliarForm.html", context)


@login_required
def prof_comunicar_resultado(request, avaliacao_id):
    """
    View para marcar resultado como comunicado
    """
    if not is_coordinator(request.user):
        messages.error(request, "Acesso restrito a coordenadores.")
        return redirect("index")
    
    avaliacao = get_object_or_404(
        AvaliacaoCandidato.objects.select_related("candidatura", "candidatura__vaga"),
        pk=avaliacao_id,
        avaliador=request.user
    )
    
    if not avaliacao.resultado:
        messages.error(request, "Defina um resultado antes de comunicar ao candidato.")
        return redirect("prof_avaliar_candidatos", vaga_id=avaliacao.candidatura.vaga.pk)
    
    if avaliacao.resultado_comunicado:
        messages.info(request, "Este resultado já foi comunicado.")
        return redirect("prof_avaliar_candidatos", vaga_id=avaliacao.candidatura.vaga.pk)
    
    if request.method == "POST":
        avaliacao.resultado_comunicado = True
        avaliacao.data_comunicacao = timezone.now()
        avaliacao.save(update_fields=["resultado_comunicado", "data_comunicacao", "updated_at"])
        
        registrar_auditoria(request.user, "comunicar_resultado", avaliacao)
        
        messages.success(request, f"Resultado comunicado para {avaliacao.candidatura.candidato_nome}!")
        return redirect("prof_avaliar_candidatos", vaga_id=avaliacao.candidatura.vaga.pk)
    
    context = {
        "avaliacao": avaliacao,
    }
    
    return render(request, "professor/prof_comunicarResultado.html", context)


@login_required
def cadastrar_candidato(request, vaga_id=None):
    vaga = None
    form_kwargs = {}
    if vaga_id is not None:
        vaga = get_object_or_404(
            VagaMonitoria.objects.select_related("disciplina"), pk=vaga_id, ativo=True
        )
        form_kwargs["vaga_queryset"] = VagaMonitoria.objects.filter(pk=vaga.pk)

    usuario = request.user
    perfil, _ = UserProfile.objects.get_or_create(user=usuario)
    nome_automatico = perfil.nome_exibicao or usuario.get_full_name() or usuario.get_username()
    email_automatico = (usuario.email or "").strip().lower()
    curriculo_pdf = perfil.curriculo_pdf if perfil.curriculo_pdf else None

    if request.method == "POST":
        form = CandidaturaPublicForm(request.POST, **form_kwargs)
        if vaga:
            form.fields["vaga"].widget = forms.HiddenInput()
            form.fields["vaga"].initial = vaga
        if form.is_valid():
            erros_personalizados = False
            candidatura_vaga = vaga or form.cleaned_data.get("vaga")
            if not candidatura_vaga:
                form.add_error("vaga", "Selecione uma vaga válida.")
                erros_personalizados = True
            elif not candidatura_vaga.inscricoes_abertas:
                form.add_error("vaga", "As inscrições para esta vaga estão encerradas.")
                erros_personalizados = True

            if not email_automatico:
                form.add_error(
                    None,
                    "Atualize seu e-mail em 'Meu perfil' antes de enviar a candidatura.",
                )
                erros_personalizados = True

            if not curriculo_pdf:
                form.add_error(
                    None,
                    "Envie um currículo em PDF na sua área do usuário antes de se candidatar.",
                )
                erros_personalizados = True

            if erros_personalizados:
                contexto = {
                    "form": form,
                    "vaga": vaga,
                    "aluno_nome": nome_automatico,
                    "aluno_email": email_automatico,
                    "curriculo_url": curriculo_pdf.url if curriculo_pdf else "",
                    "curriculo_nome": Path(curriculo_pdf.name).name if curriculo_pdf else "",
                    "curriculo_disponivel": bool(curriculo_pdf),
                }
                return render(request, "cadastrar_candidato.html", contexto)

            with transaction.atomic():
                candidatura, criada = Candidatura.objects.get_or_create(
                    vaga=candidatura_vaga,
                    candidato_email=email_automatico,
                    defaults={
                        "candidato_nome": nome_automatico,
                        "candidato_periodo": form.cleaned_data.get("candidato_periodo", ""),
                        "curriculo": curriculo_pdf,
                        "status": CandidaturaStatus.SUBMETIDA,
                    },
                )

                if not criada:
                    candidatura.candidato_nome = nome_automatico
                    candidatura.candidato_periodo = form.cleaned_data.get("candidato_periodo", "")
                    if curriculo_pdf:
                        candidatura.curriculo = curriculo_pdf
                    candidatura.status = CandidaturaStatus.SUBMETIDA
                    candidatura.save(update_fields=[
                        "candidato_nome",
                        "candidato_periodo",
                        "curriculo",
                        "status",
                        "updated_at",
                    ])
                    messages.info(request, "Dados atualizados para a candidatura existente.")
                else:
                    messages.success(request, "Candidatura registrada com sucesso.")

                registrar_auditoria(request.user, "submeter_candidatura_portal", candidatura)
                return redirect("listar_vagas")
    else:
        form = CandidaturaPublicForm(**form_kwargs)
        if vaga:
            form.fields["vaga"].widget = forms.HiddenInput()
            form.fields["vaga"].initial = vaga

    contexto = {
        "form": form,
        "vaga": vaga,
        "aluno_nome": nome_automatico,
        "aluno_email": email_automatico,
        "curriculo_url": curriculo_pdf.url if curriculo_pdf else "",
        "curriculo_nome": Path(curriculo_pdf.name).name if curriculo_pdf else "",
        "curriculo_disponivel": bool(curriculo_pdf),
        "email_disponivel": bool(email_automatico),
    }

    return render(request, "cadastrar_candidato.html", contexto)


@extend_schema_view(
    list=extend_schema(
        summary="Listar disciplinas",
        description="Retorna lista de disciplinas. Coordenadores veem apenas suas disciplinas.",
        tags=["Disciplinas"]
    ),
    retrieve=extend_schema(
        summary="Detalhes da disciplina",
        description="Retorna informações detalhadas de uma disciplina específica.",
        tags=["Disciplinas"]
    ),
    create=extend_schema(
        summary="Criar disciplina",
        description="Cria uma nova disciplina. Apenas coordenadores podem criar disciplinas.",
        tags=["Disciplinas"]
    ),
    update=extend_schema(
        summary="Atualizar disciplina",
        description="Atualiza informações de uma disciplina existente.",
        tags=["Disciplinas"]
    ),
    partial_update=extend_schema(
        summary="Atualizar disciplina parcialmente",
        description="Atualiza parcialmente informações de uma disciplina.",
        tags=["Disciplinas"]
    ),
    destroy=extend_schema(
        summary="Desativar disciplina",
        description="Desativa uma disciplina (soft delete).",
        tags=["Disciplinas"]
    ),
)
class DisciplinaViewSet(viewsets.ModelViewSet):
    serializer_class = DisciplinaSerializer
    permission_classes = [IsCoordinator]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("nome", "codigo", "departamento__nome")
    ordering_fields = ("nome", "codigo", "semestre", "updated_at")
    filterset_fields = {
        "departamento__sigla": ["exact"],
        "semestre": ["exact"],
        "coordenador_id": ["exact"],
        "ativo": ["exact"],
    }

    def get_queryset(self):
        queryset = Disciplina.objects.select_related("departamento", "coordenador")
        user = self.request.user
        if is_admin(user):
            return queryset
        if is_coordinator(user):
            return queryset.filter(coordenador=user)
        if is_student(user):
            return queryset.filter(ativo=True)
        return queryset.none()

    def perform_create(self, serializer):
        disciplina = serializer.save()
        registrar_auditoria(self.request.user, "criar_disciplina", disciplina)

    def perform_update(self, serializer):
        disciplina = serializer.save()
        registrar_auditoria(self.request.user, "atualizar_disciplina", disciplina)

    def destroy(self, request, *args, **kwargs):
        instancia = self.get_object()
        instancia.ativo = False
        instancia.save(update_fields=["ativo", "updated_at"])
        registrar_auditoria(request.user, "desativar_disciplina", instancia)
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema_view(
    list=extend_schema(
        summary="Listar vagas de monitoria",
        description="Retorna lista de vagas. Estudantes veem apenas vagas publicadas e abertas.",
        tags=["Vagas de Monitoria"],
        parameters=[
            OpenApiParameter(name='status', description='Filtrar por status da vaga', type=str),
            OpenApiParameter(name='disciplina__codigo', description='Filtrar por código da disciplina', type=str),
        ]
    ),
    retrieve=extend_schema(
        summary="Detalhes da vaga",
        description="Retorna informações detalhadas de uma vaga de monitoria.",
        tags=["Vagas de Monitoria"]
    ),
    create=extend_schema(
        summary="Criar vaga de monitoria",
        description="Cria uma nova vaga de monitoria. Apenas coordenadores.",
        tags=["Vagas de Monitoria"]
    ),
    update=extend_schema(
        summary="Atualizar vaga",
        description="Atualiza informações de uma vaga de monitoria.",
        tags=["Vagas de Monitoria"]
    ),
    partial_update=extend_schema(
        summary="Atualizar vaga parcialmente",
        description="Atualiza parcialmente informações de uma vaga.",
        tags=["Vagas de Monitoria"]
    ),
    destroy=extend_schema(
        summary="Arquivar vaga",
        description="Arquiva uma vaga de monitoria (soft delete).",
        tags=["Vagas de Monitoria"]
    ),
)
class VagaMonitoriaViewSet(viewsets.ModelViewSet):
    serializer_class = VagaMonitoriaSerializer
    permission_classes = [IsCoordinator]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("titulo", "disciplina__nome", "disciplina__codigo")
    ordering_fields = (
        "created_at",
        "inscricoes_inicio",
        "inscricoes_fim",
        "status",
        "quantidade_vagas",
    )
    filterset_fields = {
        "status": ["exact"],
        "disciplina__departamento__sigla": ["exact"],
        "disciplina__semestre": ["exact"],
        "disciplina__coordenador_id": ["exact"],
        "inscricoes_inicio": ["gte", "lte"],
        "inscricoes_fim": ["gte", "lte"],
    }

    def get_queryset(self):
        queryset = VagaMonitoria.objects.select_related(
            "disciplina",
            "disciplina__departamento",
            "criado_por",
            "atualizado_por",
        ).prefetch_related("candidaturas")
        user = self.request.user
        if is_admin(user):
            return queryset
        if is_coordinator(user):
            return queryset.filter(disciplina__coordenador=user)
        if is_student(user):
            hoje = timezone.now().date()
            return queryset.filter(
                status=VagaMonitoriaStatus.PUBLICADA,
                ativo=True,
                inscricoes_fim__gte=hoje,
            )
        return queryset.none()

    def perform_create(self, serializer):
        vaga = serializer.save(criado_por=self.request.user, atualizado_por=self.request.user)
        registrar_auditoria(self.request.user, "criar_vaga", vaga)

    def perform_update(self, serializer):
        vaga = serializer.save(atualizado_por=self.request.user)
        registrar_auditoria(self.request.user, "atualizar_vaga", vaga)

    def destroy(self, request, *args, **kwargs):
        vaga = self.get_object()
        vaga.ativo = False
        vaga.status = VagaMonitoriaStatus.FINALIZADA
        vaga.save(update_fields=["ativo", "status", "updated_at"])
        registrar_auditoria(request.user, "arquivar_vaga", vaga)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        summary="Dashboard de vagas",
        description="Retorna estatísticas e métricas sobre vagas de monitoria.",
        tags=["Vagas de Monitoria"],
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(detail=False, methods=["get"], permission_classes=[IsCoordinator])
    def dashboard(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        contagens = queryset.aggregate(
            abertas=Count("id", filter=Q(status=VagaMonitoriaStatus.PUBLICADA)),
            em_avaliacao=Count("id", filter=Q(status=VagaMonitoriaStatus.EM_AVALIACAO)),
            fechadas=Count("id", filter=Q(status=VagaMonitoriaStatus.FINALIZADA)),
        )
        total_candidaturas = Candidatura.objects.filter(vaga__in=queryset).count()
        soma_posicoes = queryset.aggregate(total=Sum("quantidade_vagas"))
        total_posicoes = soma_posicoes.get("total") or 0
        media_candidatos = (
            queryset.annotate(total=Count("candidaturas")).aggregate(media=Avg("total")).get("media")
            or 0
        )
        vagas_sem_candidato = queryset.filter(candidaturas__isnull=True)

        dados = {
            "abertas": contagens.get("abertas", 0),
            "em_avaliacao": contagens.get("em_avaliacao", 0),
            "fechadas": contagens.get("fechadas", 0),
            "total_candidaturas": total_candidaturas,
            "taxa_candidaturas_por_vaga": round(
                total_candidaturas / total_posicoes, 2
            ) if total_posicoes else 0,
            "media_candidatos_por_vaga": round(media_candidatos, 2),
            "vagas_sem_candidatos": list(
                vagas_sem_candidato.values("id", "titulo", "disciplina__codigo")
            ),
        }
        return Response(dados)

    @extend_schema(
        summary="Listar candidaturas de uma vaga",
        description="Retorna todas as candidaturas de uma vaga específica.",
        tags=["Vagas de Monitoria"]
    )
    @action(detail=True, methods=["get"], permission_classes=[IsCoordinator])
    def candidaturas(self, request, pk=None):
        vaga = self.get_object()
        serializer = CandidaturaSerializer(
            vaga.candidaturas.all(),
            many=True,
            context=self.get_serializer_context(),
        )
        return Response(serializer.data)

    @extend_schema(
        summary="Alterar status da vaga",
        description="Altera o status de uma vaga de monitoria.",
        tags=["Vagas de Monitoria"]
    )
    @action(detail=True, methods=["post"], permission_classes=[IsCoordinator])
    def alterar_status(self, request, pk=None):
        vaga = self.get_object()
        novo_status = request.data.get("status")
        if novo_status not in dict(VagaMonitoriaStatus.choices):
            return Response({"status": "Status inválido."}, status=status.HTTP_400_BAD_REQUEST)
        vaga.status = novo_status
        vaga.atualizado_por = request.user
        vaga.save(update_fields=["status", "atualizado_por", "updated_at"])
        registrar_auditoria(request.user, f"alterar_status_{novo_status}", vaga)
        return Response(VagaMonitoriaSerializer(vaga, context=self.get_serializer_context()).data)

    @extend_schema(
        summary="Duplicar vaga",
        description="Cria uma cópia de uma vaga existente com status de rascunho.",
        tags=["Vagas de Monitoria"]
    )
    @action(detail=True, methods=["post"], permission_classes=[IsCoordinator])
    def duplicar(self, request, pk=None):
        vaga = self.get_object()
        with transaction.atomic():
            nova_vaga = VagaMonitoria.objects.create(
                titulo=f"{vaga.titulo} - Cópia",
                disciplina=vaga.disciplina,
                prerequisitos=vaga.prerequisitos,
                responsabilidades=vaga.responsabilidades,
                periodo_minimo=vaga.periodo_minimo,
                cr_minimo=vaga.cr_minimo,
                quantidade_vagas=vaga.quantidade_vagas,
                carga_horaria_semanal=vaga.carga_horaria_semanal,
                bolsa_valor=vaga.bolsa_valor,
                inscricoes_inicio=vaga.inscricoes_inicio,
                inscricoes_fim=vaga.inscricoes_fim,
                monitoria_inicio=vaga.monitoria_inicio,
                monitoria_fim=vaga.monitoria_fim,
                status=VagaMonitoriaStatus.RASCUNHO,
                criado_por=request.user,
                atualizado_por=request.user,
                permitir_edicao_submetida=vaga.permitir_edicao_submetida,
            )
            registrar_auditoria(request.user, "duplicar_vaga", nova_vaga, f"Origem: {vaga.pk}")
        serializer = VagaMonitoriaSerializer(nova_vaga, context=self.get_serializer_context())
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema_view(
    list=extend_schema(
        summary="Listar candidaturas",
        description="Retorna lista de candidaturas. Estudantes veem apenas suas próprias candidaturas.",
        tags=["Candidaturas"]
    ),
    retrieve=extend_schema(
        summary="Detalhes da candidatura",
        description="Retorna informações detalhadas de uma candidatura específica.",
        tags=["Candidaturas"]
    ),
    create=extend_schema(
        summary="Criar candidatura",
        description="Submete uma nova candidatura para uma vaga de monitoria.",
        tags=["Candidaturas"]
    ),
    update=extend_schema(
        summary="Atualizar candidatura",
        description="Atualiza informações de uma candidatura (se permitido).",
        tags=["Candidaturas"]
    ),
    partial_update=extend_schema(
        summary="Atualizar candidatura parcialmente",
        description="Atualiza parcialmente informações de uma candidatura.",
        tags=["Candidaturas"]
    ),
)
class CandidaturaViewSet(viewsets.ModelViewSet):
    serializer_class = CandidaturaSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_scope = "candidaturas"
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("candidato_nome", "candidato_email", "vaga__titulo", "vaga__disciplina__codigo")
    ordering_fields = ("created_at", "status", "ultima_atualizacao_status")
    filterset_fields = {
        "status": ["exact"],
        "vaga__disciplina__departamento__sigla": ["exact"],
        "vaga_id": ["exact"],
        "candidato_email": ["exact", "iexact"],
    }

    def get_queryset(self):
        queryset = Candidatura.objects.select_related("vaga", "vaga__disciplina")
        user = self.request.user
        if is_admin(user):
            return queryset
        if is_coordinator(user):
            return queryset.filter(vaga__disciplina__coordenador=user)
        if is_student(user):
            email = (user.email or "").strip()
            if not email:
                return queryset.none()
            return queryset.filter(candidato_email__iexact=email)
        return queryset.none()

    def perform_create(self, serializer):
        vaga = serializer.validated_data.get("vaga")
        if vaga and not vaga.inscricoes_abertas:
            raise ValidationError({"vaga_id": "Inscrições encerradas para esta vaga."})

        save_kwargs = {}
        usuario = self.request.user
        if is_student(usuario) and usuario.email and not serializer.validated_data.get("candidato_email"):
            save_kwargs["candidato_email"] = usuario.email.strip().lower()

        candidatura = serializer.save(**save_kwargs)
        registrar_auditoria(self.request.user, "submeter_candidatura_api", candidatura)

    def perform_update(self, serializer):
        candidatura = serializer.save()
        registrar_auditoria(self.request.user, "atualizar_candidatura", candidatura)

    @extend_schema(
        summary="Atualizar status da candidatura",
        description="Altera o status de uma candidatura e adiciona feedback (apenas coordenadores).",
        tags=["Candidaturas"]
    )
    @action(detail=True, methods=["post"], permission_classes=[IsCoordinator])
    def atualizar_status(self, request, pk=None):
        candidatura = self.get_object()
        novo_status = request.data.get("status")
        if novo_status not in dict(CandidaturaStatus.choices):
            return Response({"status": "Status inválido."}, status=status.HTTP_400_BAD_REQUEST)
        candidatura.status = novo_status
        candidatura.feedback = request.data.get("feedback", candidatura.feedback)
        candidatura.save(update_fields=["status", "feedback", "ultima_atualizacao_status", "updated_at"])
        registrar_auditoria(request.user, f"status_candidatura_{novo_status}", candidatura)
        return Response(CandidaturaSerializer(candidatura, context=self.get_serializer_context()).data)


@extend_schema_view(
    list=extend_schema(
        summary="Listar avaliações de candidatos",
        description="Retorna lista de avaliações. Coordenadores veem avaliações de suas disciplinas.",
        tags=["Avaliações"]
    ),
    retrieve=extend_schema(
        summary="Detalhes da avaliação",
        description="Retorna informações detalhadas de uma avaliação específica.",
        tags=["Avaliações"]
    ),
    create=extend_schema(
        summary="Criar avaliação",
        description="Cria uma nova avaliação para um candidato. Apenas coordenadores.",
        tags=["Avaliações"]
    ),
    update=extend_schema(
        summary="Atualizar avaliação",
        description="Atualiza informações de uma avaliação existente.",
        tags=["Avaliações"]
    ),
    partial_update=extend_schema(
        summary="Atualizar avaliação parcialmente",
        description="Atualiza parcialmente informações de uma avaliação.",
        tags=["Avaliações"]
    ),
)
class AvaliacaoCandidatoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para avaliações de candidatos
    Permite professores criar, visualizar e gerenciar avaliações
    """
    serializer_class = AvaliacaoCandidatoSerializer
    permission_classes = [IsCoordinator]
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("candidatura__candidato_nome", "candidatura__candidato_email")
    ordering_fields = ("created_at", "nota", "resultado")
    filterset_fields = {
        "resultado": ["exact"],
        "resultado_comunicado": ["exact"],
        "candidatura__vaga_id": ["exact"],
        "candidatura__status": ["exact"],
        "avaliador_id": ["exact"],
    }

    def get_queryset(self):
        queryset = AvaliacaoCandidato.objects.select_related(
            "candidatura",
            "candidatura__vaga",
            "candidatura__vaga__disciplina",
            "avaliador"
        )
        user = self.request.user
        if is_admin(user):
            return queryset
        if is_coordinator(user):
            # Professores veem apenas avaliações de suas disciplinas
            return queryset.filter(candidatura__vaga__disciplina__coordenador=user)
        return queryset.none()

    def perform_create(self, serializer):
        avaliacao = serializer.save(avaliador=self.request.user)
        registrar_auditoria(self.request.user, "criar_avaliacao", avaliacao)

    def perform_update(self, serializer):
        avaliacao = serializer.save()
        registrar_auditoria(self.request.user, "atualizar_avaliacao", avaliacao)

    @extend_schema(
        summary="Comunicar resultado ao candidato",
        description="Marca o resultado da avaliação como comunicado ao candidato.",
        tags=["Avaliações"]
    )
    @action(detail=True, methods=["post"], permission_classes=[IsCoordinator])
    def comunicar_resultado(self, request, pk=None):
        """
        Marca o resultado como comunicado ao candidato
        """
        avaliacao = self.get_object()
        
        if not avaliacao.resultado:
            return Response(
                {"detail": "Defina um resultado antes de comunicar ao candidato."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if avaliacao.resultado_comunicado:
            return Response(
                {"detail": "Este resultado já foi comunicado."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        avaliacao.resultado_comunicado = True
        avaliacao.data_comunicacao = timezone.now()
        avaliacao.save(update_fields=["resultado_comunicado", "data_comunicacao", "updated_at"])
        
        registrar_auditoria(request.user, "comunicar_resultado_avaliacao", avaliacao)
        
        return Response({
            "detail": "Resultado comunicado com sucesso.",
            "data_comunicacao": avaliacao.data_comunicacao
        })

    @extend_schema(
        summary="Candidaturas pendentes de avaliação",
        description="Lista candidaturas que ainda não foram avaliadas pelo coordenador atual.",
        tags=["Avaliações"]
    )
    @action(detail=False, methods=["get"], permission_classes=[IsCoordinator])
    def pendentes(self, request):
        """
        Lista candidaturas que ainda não têm avaliação do professor atual
        """
        user = request.user
        
        # Busca vagas do professor
        vagas_professor = VagaMonitoria.objects.filter(
            disciplina__coordenador=user,
            status__in=[VagaMonitoriaStatus.EM_AVALIACAO, VagaMonitoriaStatus.PUBLICADA]
        )
        
        # Busca candidaturas dessas vagas que não têm avaliação do professor
        candidaturas_pendentes = Candidatura.objects.filter(
            vaga__in=vagas_professor,
            status__in=[CandidaturaStatus.SUBMETIDA, CandidaturaStatus.EM_ANALISE]
        ).exclude(
            avaliacoes__avaliador=user
        ).select_related("vaga", "vaga__disciplina")
        
        serializer = CandidaturaSerializer(
            candidaturas_pendentes,
            many=True,
            context=self.get_serializer_context()
        )
        
        return Response({
            "total": candidaturas_pendentes.count(),
            "candidaturas": serializer.data
        })

    @extend_schema(
        summary="Avaliar múltiplos candidatos",
        description="Permite criar avaliações para múltiplos candidatos em uma única requisição.",
        tags=["Avaliações"]
    )
    @action(detail=False, methods=["post"], permission_classes=[IsCoordinator])
    def avaliar_lote(self, request):
        """
        Permite avaliar múltiplos candidatos de uma vez
        """
        avaliacoes_data = request.data.get("avaliacoes", [])
        
        if not avaliacoes_data:
            return Response(
                {"detail": "Nenhuma avaliação fornecida."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        avaliacoes_criadas = []
        erros = []
        
        with transaction.atomic():
            for idx, avaliacao_data in enumerate(avaliacoes_data):
                serializer = self.get_serializer(data=avaliacao_data)
                if serializer.is_valid():
                    avaliacao = serializer.save(avaliador=request.user)
                    avaliacoes_criadas.append(avaliacao)
                    registrar_auditoria(request.user, "criar_avaliacao_lote", avaliacao)
                else:
                    erros.append({
                        "index": idx,
                        "candidatura_id": avaliacao_data.get("candidatura_id"),
                        "erros": serializer.errors
                    })
        
        return Response({
            "sucesso": len(avaliacoes_criadas),
            "erros": len(erros),
            "detalhes_erros": erros
        }, status=status.HTTP_201_CREATED if avaliacoes_criadas else status.HTTP_400_BAD_REQUEST)