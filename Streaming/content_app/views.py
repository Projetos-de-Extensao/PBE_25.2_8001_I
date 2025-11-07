from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Avg, Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout


from .forms import CandidaturaPublicForm
from .models import (
    Candidatura,
    CandidaturaStatus,
    Disciplina,
    VagaMonitoria,
    VagaMonitoriaStatus,
)
from .permissions import (
    IsCoordinator,
    is_admin,
    is_coordinator,
    is_student,
)
from .serializers import CandidaturaSerializer, DisciplinaSerializer, VagaMonitoriaSerializer
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
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Autentica o usuário
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Login bem-sucedido
            login(request, user)
            
            # Verifica se há um 'next' parameter (para redirecionar para página solicitada)
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            
            # Caso contrário, redireciona para index
            return redirect('index')
        else:
            # Credenciais inválidas
            messages.error(request, 'Usuário ou senha inválidos.')
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})
    
    # Se for GET, apenas mostra o formulário de login
    return render(request, 'login.html')


def logout_view(request):
    """
    View customizada para logout
    """
    logout(request)
    messages.success(request, 'Você saiu com sucesso.')
    return redirect('login')


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
    """View para exibir relatórios"""
    # Estatísticas básicas
    total_vagas = VagaMonitoria.objects.filter(disciplina__coordenador=request.user).count()
    total_candidaturas = Candidatura.objects.filter(vaga__disciplina__coordenador=request.user).count()
    candidaturas_aprovadas = Candidatura.objects.filter(
        vaga__disciplina__coordenador=request.user,
        status=CandidaturaStatus.APROVADA
    ).count()
    
    context = {
        'total_vagas': total_vagas,
        'total_candidaturas': total_candidaturas,
        'candidaturas_aprovadas': candidaturas_aprovadas,
    }
    return render(request, "professor/prof_relatorio.html", context)


def cadastrar_candidato(request, vaga_id=None):
    vaga = None
    form_kwargs = {}
    if vaga_id is not None:
        vaga = get_object_or_404(
            VagaMonitoria.objects.select_related("disciplina"), pk=vaga_id, ativo=True
        )
        form_kwargs["vaga_queryset"] = VagaMonitoria.objects.filter(pk=vaga.pk)

    if request.method == "POST":
        form = CandidaturaPublicForm(request.POST, request.FILES, **form_kwargs)
        if vaga:
            form.fields["vaga"].widget = forms.HiddenInput()
            form.fields["vaga"].initial = vaga
        if form.is_valid():
            with transaction.atomic():
                candidatura_vaga = form.cleaned_data.get("vaga")
                if vaga:
                    candidatura_vaga = vaga
                if not candidatura_vaga:
                    form.add_error("vaga", "Selecione uma vaga válida.")
                else:
                    if not candidatura_vaga.inscricoes_abertas:
                        form.add_error("vaga", "As inscrições para esta vaga estão encerradas.")
                    candidato_cr = form.cleaned_data.get("candidato_cr")
                    if (
                        candidatura_vaga.cr_minimo
                        and candidato_cr is not None
                        and candidato_cr < candidatura_vaga.cr_minimo
                    ):
                        form.add_error("candidato_cr", "CR insuficiente para esta vaga.")

                if form.errors:
                    return render(request, "cadastrar_candidato.html", {"form": form, "vaga": vaga})

                candidatura, criada = Candidatura.objects.get_or_create(
                    vaga=candidatura_vaga,
                    candidato_email=form.cleaned_data["candidato_email"],
                    defaults={
                        "candidato_nome": form.cleaned_data["candidato_nome"],
                        "candidato_curso": form.cleaned_data.get("candidato_curso", ""),
                        "candidato_periodo": form.cleaned_data.get("candidato_periodo", ""),
                        "candidato_cr": form.cleaned_data.get("candidato_cr"),
                        "historico_escolar": form.cleaned_data.get("historico_escolar"),
                        "curriculo": form.cleaned_data.get("curriculo"),
                        "carta_motivacao": form.cleaned_data.get("carta_motivacao", ""),
                        "status": CandidaturaStatus.SUBMETIDA,
                    },
                )

                if not criada:
                    campos_atualizaveis = (
                        "candidato_nome",
                        "candidato_curso",
                        "candidato_periodo",
                        "candidato_cr",
                        "historico_escolar",
                        "curriculo",
                        "carta_motivacao",
                    )
                    for campo in campos_atualizaveis:
                        valor = form.cleaned_data.get(campo)
                        if campo in {"historico_escolar", "curriculo"}:
                            if valor:
                                setattr(candidatura, campo, valor)
                        elif valor not in (None, ""):
                            setattr(candidatura, campo, valor)
                    candidatura.status = CandidaturaStatus.SUBMETIDA
                    candidatura.save()
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

    return render(request, "cadastrar_candidato.html", {"form": form, "vaga": vaga})


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

    @action(detail=True, methods=["get"], permission_classes=[IsCoordinator])
    def candidaturas(self, request, pk=None):
        vaga = self.get_object()
        serializer = CandidaturaSerializer(
            vaga.candidaturas.all(),
            many=True,
            context=self.get_serializer_context(),
        )
        return Response(serializer.data)

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