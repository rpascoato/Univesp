from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CadastroForm, EscolaForm, QuestionarioForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Questionario, Resposta, Resultado, Escola, Perquest, Usuario
from django import forms

def home(request):
    return render(request, 'home.html')

def cadastro(request):
    form = CadastroForm()
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')

    return render(request, 'cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('questionario')
            else:
                error_message = "Usuário ou senha incorretos. Por favor, tente novamente."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
        else:
            error_message = "Formulário inválido. Por favor, tente novamente."
            return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login_view')

@login_required
def perquest(request):
    if request.method == 'POST':
        respostas = {}
        for key, value in request.POST.items():
            if key.startswith('perquest_'):
                pergunta_id = int(key.split('_')[1])
                resposta_id = int(value)
                respostas[pergunta_id] = resposta_id

        # Obtém o usuário logado
        usuario = Usuario.objects.get(user=request.user)
        
        # Cria um novo questionário para o usuário
        questionario = Questionario.objects.create(nome="Questionario")

        # Processa as respostas e determina o nível do espectro
        espectro = processar_respostas(respostas)

        # Cria um novo resultado associado ao questionário e usuário
        resultado = Resultado.objects.create(cod_ques=questionario, cod_usu=usuario, nivel=espectro)

        return redirect('resultado')

    perquests = Perquest.objects.all()
    contexto = {'perquests': perquests}
    return render(request, 'perquest.html', contexto)

def processar_respostas(respostas):
    total_pontos = sum(Resposta.objects.get(id=resposta_id).valor for resposta_id in respostas.values())
    if total_pontos <= 2:
        return 'Baixo'
    elif total_pontos <= 7:
        return 'Médio'
    else:
        return 'Alto'

@login_required
def resultado(request):
    resultados = Resultado.objects.filter(cod_usu=request.user)
    return render(request, 'resultado.html', {'resultados': resultados})

@login_required
def questionario(request):
    if request.method == 'POST':
        form = QuestionarioForm(request.POST)
        if form.is_valid():
            questionario = form.save()
            return redirect('perquest')
    else:
        form = QuestionarioForm()
    return render(request, 'questionario.html', {'form': form})

def administracao(request):
    if request.method == 'POST':
        form = EscolaForm(request.POST)
        if form.is_valid():
            escola = form.saveEscola()
            return redirect('administracao')
    else:
        form = EscolaForm()
    return render(request, 'administracao.html', {'form': form})

class EscolaExistenteForm(forms.Form):
    escola = forms.ModelChoiceField(queryset=Escola.objects.all(), label='Escola')