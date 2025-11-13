from django.contrib import admin

from .models import (
    AuditoriaRegistro,
    AvaliacaoCandidato,
    Candidatura,
    Departamento,
    Disciplina,
    VagaMonitoria,
    VagaMonitoriaStatus,
)


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ("sigla", "nome", "ativo", "created_at")
    list_filter = ("ativo",)
    search_fields = ("sigla", "nome")
    ordering = ("sigla",)


@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ("codigo", "nome", "departamento", "coordenador", "semestre", "carga_horaria", "ativo")
    list_filter = ("departamento", "semestre", "coordenador", "ativo")
    search_fields = ("nome", "codigo")
    list_select_related = ("departamento", "coordenador")
    actions = ["ativar_disciplinas", "desativar_disciplinas"]

    @admin.action(description="Ativar disciplinas selecionadas")
    def ativar_disciplinas(self, request, queryset):
        queryset.update(ativo=True)

    @admin.action(description="Desativar disciplinas selecionadas")
    def desativar_disciplinas(self, request, queryset):
        queryset.update(ativo=False)


@admin.register(VagaMonitoria)
class VagaMonitoriaAdmin(admin.ModelAdmin):
    list_display = (
        "titulo",
        "disciplina",
        "status",
        "quantidade_vagas",
        "inscricoes_inicio",
        "inscricoes_fim",
        "inscricoes_abertas",
        "criado_por",
    )
    list_filter = (
        "status",
        "disciplina__departamento",
        "disciplina__semestre",
        "criado_por",
    )
    search_fields = ("titulo", "disciplina__nome", "disciplina__codigo")
    ordering = ("-created_at",)
    list_select_related = ("disciplina", "disciplina__departamento", "criado_por")
    actions = ["marcar_rascunho", "publicar_vagas", "finalizar_vagas"]

    @admin.action(description="Mover para rascunho")
    def marcar_rascunho(self, request, queryset):
        queryset.update(status=VagaMonitoriaStatus.RASCUNHO)

    @admin.action(description="Publicar vagas selecionadas")
    def publicar_vagas(self, request, queryset):
        queryset.update(status=VagaMonitoriaStatus.PUBLICADA)

    @admin.action(description="Finalizar vagas selecionadas")
    def finalizar_vagas(self, request, queryset):
        queryset.update(status=VagaMonitoriaStatus.FINALIZADA)


@admin.register(Candidatura)
class CandidaturaAdmin(admin.ModelAdmin):
    list_display = (
        "candidato_nome",
        "candidato_email",
        "vaga",
        "status",
        "created_at",
        "ultima_atualizacao_status",
    )
    list_filter = ("status", "vaga__disciplina__departamento", "vaga__disciplina__semestre")
    search_fields = ("candidato_nome", "candidato_email", "vaga__titulo")
    list_select_related = ("vaga", "vaga__disciplina")


@admin.register(AuditoriaRegistro)
class AuditoriaRegistroAdmin(admin.ModelAdmin):
    list_display = ("acao", "modelo", "objeto_id", "usuario", "criado_em")
    list_filter = ("acao", "modelo")
    search_fields = ("acao", "modelo", "objeto_id", "descricao")
    readonly_fields = ("acao", "modelo", "objeto_id", "descricao", "usuario", "criado_em")
    ordering = ("-criado_em",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AvaliacaoCandidato)
class AvaliacaoCandidatoAdmin(admin.ModelAdmin):
    list_display = (
        "candidatura",
        "avaliador",
        "nota",
        "resultado",
        "resultado_comunicado",
        "created_at",
    )
    list_filter = ("resultado", "resultado_comunicado", "avaliador")
    search_fields = (
        "candidatura__candidato_nome",
        "candidatura__candidato_email",
        "avaliador__username",
        "avaliador__first_name",
        "avaliador__last_name",
    )
    list_select_related = ("candidatura", "candidatura__vaga", "avaliador")
    readonly_fields = ("created_at", "updated_at", "data_comunicacao")
    
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("candidatura", "avaliador", "nota")
        }),
        ("Avaliação", {
            "fields": ("criterios_avaliacao", "comentarios")
        }),
        ("Resultado", {
            "fields": ("resultado", "mensagem_resultado", "resultado_comunicado", "data_comunicacao")
        }),
        ("Datas", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
