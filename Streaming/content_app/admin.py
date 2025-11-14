from django.contrib import admin

from .models import (
    AuditoriaRegistro,
    AvaliacaoCandidato,
    Candidatura,
    Departamento,
    Disciplina,
    Monitor,
    RegistroFrequencia,
    RelatorioMensal,
    UserProfile,
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


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "nome_exibicao", "curriculo_pdf", "updated_at")
    search_fields = ("user__username", "user__email", "nome_exibicao")
    list_select_related = ("user",)
    readonly_fields = ("created_at", "updated_at")


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


# ==================== Admin de Controle de Frequência ====================

@admin.register(Monitor)
class MonitorAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "vaga",
        "status",
        "data_inicio",
        "data_fim",
        "carga_horaria_semanal",
        "horas_mes_atual",
        "percentual_cumprido",
    )
    list_filter = ("status", "vaga__disciplina__departamento", "data_inicio")
    search_fields = ("nome", "email", "vaga__titulo", "vaga__disciplina__nome")
    list_select_related = ("vaga", "vaga__disciplina", "candidatura", "usuario")
    readonly_fields = ("created_at", "updated_at", "horas_mes_atual", "percentual_cumprido")
    
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("candidatura", "vaga", "usuario", "nome", "email")
        }),
        ("Período e Carga Horária", {
            "fields": ("data_inicio", "data_fim", "carga_horaria_semanal", "status")
        }),
        ("Estatísticas", {
            "fields": ("horas_mes_atual", "percentual_cumprido"),
            "classes": ("collapse",)
        }),
        ("Observações", {
            "fields": ("observacoes",)
        }),
        ("Datas", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def horas_mes_atual(self, obj):
        return f"{obj.horas_trabalhadas_mes_atual:.2f}h"
    horas_mes_atual.short_description = "Horas Mês Atual"
    
    def percentual_cumprido(self, obj):
        return f"{obj.percentual_cumprido_mes:.1f}%"
    percentual_cumprido.short_description = "% Cumprido"


@admin.register(RegistroFrequencia)
class RegistroFrequenciaAdmin(admin.ModelAdmin):
    list_display = (
        "monitor",
        "data",
        "entrada",
        "saida",
        "horas",
        "tipo",
        "validado",
        "validado_por",
    )
    list_filter = ("tipo", "data", "validado_por", "monitor__vaga__disciplina")
    search_fields = ("monitor__nome", "atividades", "local")
    list_select_related = ("monitor", "monitor__vaga", "validado_por")
    readonly_fields = ("created_at", "updated_at", "horas", "validado_em")
    date_hierarchy = "data"
    
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("monitor", "data", "entrada", "saida", "tipo")
        }),
        ("Detalhes", {
            "fields": ("atividades", "local", "observacoes")
        }),
        ("Validação", {
            "fields": ("validado_por", "validado_em")
        }),
        ("Datas", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def horas(self, obj):
        return f"{obj.horas_trabalhadas:.2f}h"
    horas.short_description = "Horas Trabalhadas"
    
    def validado(self, obj):
        return "✓" if obj.validado_por else "✗"
    validado.short_description = "Validado"
    validado.boolean = True


@admin.register(RelatorioMensal)
class RelatorioMensalAdmin(admin.ModelAdmin):
    list_display = (
        "monitor",
        "mes_ano",
        "total_horas",
        "dias_trabalhados",
        "percentual_cumprido",
        "aprovado",
    )
    list_filter = ("ano", "mes", "aprovado_por", "monitor__vaga__disciplina")
    search_fields = ("monitor__nome", "resumo_atividades")
    list_select_related = ("monitor", "monitor__vaga", "aprovado_por")
    readonly_fields = ("created_at", "updated_at", "aprovado_em")
    
    fieldsets = (
        ("Informações Básicas", {
            "fields": ("monitor", "mes", "ano")
        }),
        ("Totalizadores", {
            "fields": (
                "total_horas",
                "dias_trabalhados",
                "carga_horaria_prevista",
                "percentual_cumprido"
            )
        }),
        ("Resumo", {
            "fields": ("resumo_atividades", "observacoes_professor")
        }),
        ("Aprovação", {
            "fields": ("aprovado_por", "aprovado_em")
        }),
        ("Datas", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    actions = ["recalcular_totais"]
    
    def mes_ano(self, obj):
        return f"{obj.mes:02d}/{obj.ano}"
    mes_ano.short_description = "Mês/Ano"
    
    def aprovado(self, obj):
        return "✓" if obj.aprovado_por else "✗"
    aprovado.short_description = "Aprovado"
    aprovado.boolean = True
    
    @admin.action(description="Recalcular totais dos relatórios selecionados")
    def recalcular_totais(self, request, queryset):
        for relatorio in queryset:
            relatorio.calcular_totais()
            relatorio.save()
        self.message_user(request, f"{queryset.count()} relatório(s) recalculado(s) com sucesso.")
