# 🔒 Pre-commit Hooks - Configuração

## 📋 O Que Foi Configurado

O projeto agora possui **pre-commit hooks** que executam automaticamente antes de cada commit, garantindo:

✅ **Testes unitários** executados  
✅ **Cobertura mínima de 70%** verificada  
✅ **Código formatado** com Black  
✅ **Imports ordenados** com isort  
✅ **Linting** com flake8  
✅ **Validação de arquivos** (YAML, JSON)  
✅ **Sem arquivos grandes**  
✅ **Sem conflitos de merge**  

## 🚀 Instalação

### 1. Instalar Dependências

```bash
# Instalar pacotes necessários
pip install -r requirements.txt

# OU instalar individualmente
pip install coverage pre-commit black isort flake8
```

### 2. Instalar Pre-commit Hooks

```bash
# Instalar os hooks do git
pre-commit install

# Verificar instalação
pre-commit --version
```

### 3. Executar Manualmente (Opcional)

```bash
# Executar em todos os arquivos
pre-commit run --all-files

# Executar apenas nos arquivos staged
pre-commit run
```

## 🎯 O Que Acontece em Cada Commit

Quando você faz `git commit`, automaticamente:

### 1️⃣ **Verificações de Código**
- ✅ Remove espaços em branco no final
- ✅ Adiciona nova linha no final dos arquivos
- ✅ Valida YAML e JSON
- ✅ Detecta arquivos grandes (>1MB)
- ✅ Detecta conflitos de merge
- ✅ Valida sintaxe Python
- ✅ Detecta statements de debug (pdb, ipdb)

### 2️⃣ **Formatação Automática**
- 🎨 **Black**: Formata código Python
- 📦 **isort**: Ordena imports
- ⚠️ Se houver mudanças, o commit é interrompido para você revisar

### 3️⃣ **Linting**
- 🔍 **flake8**: Verifica estilo e erros
- ⚠️ Falha se houver problemas

### 4️⃣ **Testes**
- 🧪 Executa todos os testes unitários
- ⚠️ Falha se algum teste falhar

### 5️⃣ **Cobertura de Testes**
- 📊 Mede cobertura de código
- ✅ **Mínimo obrigatório: 70%**
- ⚠️ Falha se cobertura < 70%

## 📊 Verificar Cobertura Manualmente

### Executar Testes com Coverage

```bash
# Executar testes e medir cobertura
coverage run --source='.' manage.py test problems.tests

# Ver relatório no terminal
coverage report

# Gerar relatório HTML
coverage html

# Abrir no navegador
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Usar Script Incluído

```bash
# Dar permissão de execução
chmod +x run_tests_with_coverage.sh

# Executar
./run_tests_with_coverage.sh
```

## 🎨 Formatar Código Manualmente

```bash
# Formatar com Black
black . --line-length=100

# Ordenar imports
isort . --profile black

# Verificar com flake8
flake8 .
```

## ⚙️ Configuração dos Hooks

### Arquivos de Configuração

- **`.pre-commit-config.yaml`** - Configuração dos hooks
- **`.coveragerc`** - Configuração do coverage
- **`setup.cfg`** - Configuração de flake8, isort
- **`run_tests_with_coverage.sh`** - Script auxiliar

### Modificar Cobertura Mínima

Edite `.pre-commit-config.yaml`:

```yaml
- id: coverage-check
  entry: bash -c 'coverage run --source=. manage.py test && coverage report --fail-under=80'
  #                                                                                    ^^
  #                                                                     Altere aqui (70, 80, 90)
```

## 🔧 Pular Pre-commit (Não Recomendado)

```bash
# Pular TODOS os hooks (use com cautela!)
git commit --no-verify -m "mensagem"

# OU
git commit -n -m "mensagem"
```

⚠️ **Atenção**: Isso ignora todas as verificações de qualidade!

## 📈 Exemplo de Output

### ✅ Commit Bem-Sucedido

```bash
$ git commit -m "Add new feature"

Remove espaços em branco no final das linhas.........................Passed
Garante nova linha no final dos arquivos............................Passed
Valida sintaxe de arquivos YAML.....................................Passed
Valida sintaxe de arquivos JSON.....................................Passed
Previne commit de arquivos grandes..................................Passed
Verifica marcadores de conflito de merge............................Passed
Valida sintaxe Python (AST).........................................Passed
Detecta statements de debug.........................................Passed
Formatação de código com Black......................................Passed
Ordenação de imports com isort......................................Passed
Linting de código com flake8........................................Passed
Executar testes Django..............................................Passed
Verificar cobertura de testes (mínimo 70%).........................Passed

[main abc1234] Add new feature
 2 files changed, 50 insertions(+), 10 deletions(-)
```

### ❌ Commit com Cobertura Insuficiente

```bash
$ git commit -m "Add feature without tests"

[... outros hooks passam ...]

Verificar cobertura de testes (mínimo 70%)..........................Failed
- hook id: coverage-check
- exit code: 2

❌ Cobertura insuficiente: 65% (mínimo: 70%)

💡 Dicas para aumentar a cobertura:
  1. Adicione testes para código não coberto
  2. Execute 'coverage html' para ver relatório detalhado
  3. Abra htmlcov/index.html no navegador
```

## 💡 Boas Práticas

### ✅ DO (Faça)

1. ✅ Execute testes localmente antes de commitar
2. ✅ Mantenha cobertura > 70%
3. ✅ Deixe Black formatar seu código
4. ✅ Resolva warnings do flake8
5. ✅ Revise mudanças automáticas antes de commitar novamente

### ❌ DON'T (Não Faça)

1. ❌ Não use `--no-verify` sem necessidade
2. ❌ Não commite código não testado
3. ❌ Não ignore warnings de linting
4. ❌ Não commite arquivos grandes
5. ❌ Não deixe imports desorganizados

## 🐛 Solução de Problemas

### Erro: "pre-commit: command not found"

```bash
pip install pre-commit
pre-commit install
```

### Erro: "coverage: command not found"

```bash
pip install coverage
```

### Hooks Muito Lentos

```bash
# Desabilitar hook específico temporariamente
SKIP=coverage-check git commit -m "mensagem"

# OU remover do .pre-commit-config.yaml
```

### Atualizar Hooks

```bash
# Atualizar para últimas versões
pre-commit autoupdate

# Limpar cache
pre-commit clean
```

## 📊 Status Atual do Projeto

**Cobertura Atual:** ~85%  
**Testes:** 64  
**Mínimo Exigido:** 70%  
**Status:** ✅ Atende aos requisitos

## 🔄 Integração CI/CD

O pre-commit também pode ser usado em pipelines:

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run pre-commit
        run: |
          pip install pre-commit
          pre-commit run --all-files
```

## 📚 Documentação

- **Pre-commit**: https://pre-commit.com
- **Coverage.py**: https://coverage.readthedocs.io
- **Black**: https://black.readthedocs.io
- **isort**: https://pycqa.github.io/isort
- **flake8**: https://flake8.pycqa.org

## 🎯 Próximos Passos

1. ✅ Configuração instalada
2. ✅ Hooks configurados
3. ✅ Cobertura > 70%
4. 🔄 Fazer primeiro commit com hooks ativos
5. 🔄 Monitorar cobertura ao adicionar código novo

---

**✅ Pre-commit hooks configurados com sucesso!**

**Qualidade de código garantida em cada commit! 🚀**

