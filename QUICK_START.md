# 🚀 Quick Start - CodePlatform

Este guia rápido te ajudará a ter a plataforma rodando em menos de 5 minutos!

## ⚡ Início Rápido (3 comandos)

```bash
# 1. Execute o script de setup
chmod +x setup.sh && ./setup.sh

# 2. Ative o ambiente virtual
source venv/bin/activate

# 3. Inicie o servidor
python manage.py runserver
```

✅ Pronto! Acesse: **http://localhost:8000**

## 📸 O que você verá

### 1. Página Inicial
- Estatísticas da plataforma
- Problemas recentes
- Recursos disponíveis

### 2. Lista de Problemas (http://localhost:8000/problems/)
- 8 problemas de exemplo já cadastrados
- Filtros por dificuldade
- Busca por texto
- Indicador de problemas resolvidos

### 3. Resolver um Problema
- Descrição detalhada
- Casos de teste de exemplo
- Editor de código
- Botões para testar e submeter

### 4. Área Administrativa (http://localhost:8000/admin/)
- Gerenciar problemas
- Adicionar casos de teste
- Visualizar submissões
- Gerenciar usuários

## 🎯 Teste Rápido

### 1. Criar uma Conta
```
1. Clique em "Registrar" no menu
2. Preencha: username, email, senha
3. Login automático após registro
```

### 2. Resolver Primeiro Problema
```
1. Vá para "Problemas"
2. Clique em "Soma de Dois Números"
3. No editor, escreva:

def solution(a, b):
    return a + b

4. Clique em "Executar Testes" → Deve passar!
5. Clique em "Submeter" → Aceito! ✓
```

### 3. Ver Seu Perfil
```
1. Clique no seu nome de usuário
2. Veja: 1 problema resolvido
3. Veja seu histórico de submissões
```

## 👨‍💼 Acessar como Admin

```bash
# Após o setup, você criou um superusuário
# Use essas credenciais em:
http://localhost:8000/admin/
```

### No Admin, você pode:
- ➕ Criar novos problemas
- ✏️ Editar problemas existentes
- 🧪 Adicionar casos de teste
- 👥 Gerenciar usuários
- 📊 Ver todas as submissões

## 🔥 Criar Seu Primeiro Problema Personalizado

1. Acesse http://localhost:8000/admin/
2. Clique em "Problemas" → "Adicionar Problema"
3. Preencha:
   ```
   Título: Multiplicar Dois Números
   Slug: multiplicar-dois-numeros
   Descrição: Dado dois números, retorne a multiplicação deles
   Dificuldade: Fácil
   Código Inicial:
   def solution(a, b):
       # Seu código aqui
       pass
   Nome da Função: solution
   ```
4. Adicione Casos de Teste (inline):
   ```
   Entrada: [3, 4]
   Saída: 12
   É exemplo: ✓
   
   Entrada: [5, 5]
   Saída: 25
   É exemplo: ✓
   ```
5. Salve!
6. Acesse http://localhost:8000/problems/ e veja seu problema lá!

## 📚 Problemas Incluídos

### Fáceis (4)
1. ✅ Soma de Dois Números
2. ✅ Número Par ou Ímpar
3. ✅ Inverter String
4. ✅ Maior Elemento em uma Lista

### Médios (3)
5. ✅ Calcular Fatorial
6. ✅ Verificar Palíndromo
7. ✅ Número de Fibonacci

### Difíceis (1)
8. ✅ Ordenar Lista (sem usar sort)

## 🎓 Soluções dos Problemas de Exemplo

<details>
<summary>1. Soma de Dois Números</summary>

```python
def solution(a, b):
    return a + b
```
</details>

<details>
<summary>2. Número Par ou Ímpar</summary>

```python
def solution(n):
    return n % 2 == 0
```
</details>

<details>
<summary>3. Inverter String</summary>

```python
def solution(s):
    return s[::-1]
```
</details>

<details>
<summary>4. Maior Elemento</summary>

```python
def solution(nums):
    return max(nums)
```
</details>

<details>
<summary>5. Calcular Fatorial</summary>

```python
def solution(n):
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result
```
</details>

<details>
<summary>6. Verificar Palíndromo</summary>

```python
def solution(s):
    return s == s[::-1]
```
</details>

<details>
<summary>7. Número de Fibonacci</summary>

```python
def solution(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
```
</details>

<details>
<summary>8. Ordenar Lista (sem sort)</summary>

```python
def solution(nums):
    # Bubble Sort
    n = len(nums)
    for i in range(n):
        for j in range(0, n - i - 1):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums
```
</details>

## 🛠️ Comandos Úteis

```bash
# Parar o servidor
Ctrl + C

# Reiniciar o servidor
python manage.py runserver

# Criar novo superusuário
python manage.py createsuperuser

# Recriar problemas de exemplo
python manage.py create_sample_problems

# Abrir shell Django (para testes)
python manage.py shell
```

## 🐛 Problemas Comuns

### "Django não encontrado"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Porta 8000 em uso"
```bash
# Use outra porta
python manage.py runserver 8001
```

### "Erro ao fazer login"
```bash
# Verifique se criou o usuário
python manage.py createsuperuser
```

## 📖 Documentação Completa

Para mais detalhes, consulte:
- 📄 **GUIA_DE_USO.md** - Documentação completa
- 📄 **README.md** - Visão geral do projeto

## 🎉 Próximos Passos

Agora que você tem a plataforma rodando:

1. ✅ Resolva os 8 problemas incluídos
2. ✅ Crie seus próprios problemas
3. ✅ Personalize o design
4. ✅ Adicione mais funcionalidades

## 💡 Dicas

- 🔥 Use o admin para explorar os dados
- 🎨 Personalize cores em `templates/base.html`
- 🧪 Teste diferentes casos de teste
- 📊 Acompanhe seu progresso no perfil
- 🚀 Compartilhe com amigos para competir!

---

**Divirta-se codificando! 💻🚀**

