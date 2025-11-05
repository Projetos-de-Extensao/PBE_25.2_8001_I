from rest_framework import viewsets, generics, permissions
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import VagaMonitoria, Candidatura, Candidato
from .forms import CandidatoForm
from .serializers import VagaMonitoriaSerializer

def index(request):
    return render(request, 'index.html')

def area_candidato(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        candidato = get_object_or_404(Candidato, email=email)
        candidaturas = Candidatura.objects.filter(candidato=candidato)
        return render(request, 'area_candidato.html', {
            'candidato': candidato,
            'candidaturas': candidaturas,
            'email_form_submitted': True
        })
    return render(request, 'area_candidato.html', {'email_form_submitted': False})

def listar_vagas(request):
     vagas = VagaMonitoria.objects.all()
     return render(request, 'listar_vagas.html', {'vagas': vagas})


@login_required
def prof_index(request):
    # Simple dashboard for professors — later can check request.user permissions
    minhas_vagas = VagaMonitoria.objects.filter(professor=request.user)
    return render(request, 'profIndex.html', {'minhas_vagas': minhas_vagas})

@login_required
@login_required
def cadastrar_candidato(request, vaga_id=None):
    vaga = None
    if vaga_id is not None:
        vaga = get_object_or_404(VagaMonitoria, pk=vaga_id)

    if request.method == 'POST':
        form = CandidatoForm(request.POST, request.FILES)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            existing = Candidato.objects.filter(email__iexact=email).first()
            if existing:
                # update existing candidate fields
                existing.nome = form.cleaned_data.get('nome')
                existing.curso = form.cleaned_data.get('curso')
                # update files only if provided
                hist = form.cleaned_data.get('historico_escolar')
                if hist:
                    existing.historico_escolar = hist
                curr = form.cleaned_data.get('curriculo')
                if curr:
                    existing.curriculo = curr
                existing.carta_motivacao = form.cleaned_data.get('carta_motivacao')
                existing.save()
                candidato = existing
                messages.info(request, 'Candidato existente atualizado e usado para a candidatura.')
            else:
                candidato = form.save()
                messages.success(request, 'Candidato cadastrado com sucesso.')

            # If this registration came from a specific vaga, create a Candidatura (avoid duplicates)
            if vaga is not None:
                if not Candidatura.objects.filter(candidato=candidato, vaga=vaga).exists():
                    Candidatura.objects.create(candidato=candidato, vaga=vaga)
                    messages.success(request, 'Candidatura criada para a vaga.')
                else:
                    messages.info(request, 'Você já se candidatou para esta vaga.')

            return redirect('listar_vagas')
    else:
        form = CandidatoForm()
    return render(request, 'cadastrar_candidato.html', {'form': form, 'vaga': vaga})




class VagaMonitoriaViewSet(viewsets.ModelViewSet):
    queryset = VagaMonitoria.objects.all()
    serializer_class = VagaMonitoriaSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(professor=self.request.user)

class VagaMonitoriaAPIView(generics.ListAPIView):
    serializer_class = VagaMonitoriaSerializer

    def get_queryset(self):
        return VagaMonitoria.objects.filter(numero_vagas__gte=1)