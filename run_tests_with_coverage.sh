#!/bin/bash

# Script para executar testes com verificação de cobertura
# Usado pelo pre-commit hook

set -e  # Sai se houver erro

echo "═══════════════════════════════════════════════════════════════"
echo "  🧪 Executando Testes com Verificação de Cobertura"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Executar testes com coverage
echo "📊 Executando testes e medindo cobertura..."
coverage run --source='.' manage.py test problems.tests --verbosity=1

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}❌ Testes falharam!${NC}"
    echo ""
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "  📈 Relatório de Cobertura"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Gerar relatório
coverage report

# Verificar se atingiu o mínimo de 70%
COVERAGE=$(coverage report | grep TOTAL | awk '{print $4}' | sed 's/%//')

echo ""
echo "═══════════════════════════════════════════════════════════════"

if (( $(echo "$COVERAGE < 70" | bc -l) )); then
    echo -e "${RED}❌ Cobertura insuficiente: ${COVERAGE}% (mínimo: 70%)${NC}"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
    echo "💡 Dicas para aumentar a cobertura:"
    echo "  1. Adicione testes para código não coberto"
    echo "  2. Execute 'coverage html' para ver relatório detalhado"
    echo "  3. Abra htmlcov/index.html no navegador"
    echo ""
    exit 1
else
    echo -e "${GREEN}✅ Cobertura adequada: ${COVERAGE}% (mínimo: 70%)${NC}"
    echo "═══════════════════════════════════════════════════════════════"
    echo ""
fi

# Gerar relatório HTML
echo "📊 Gerando relatório HTML..."
coverage html

echo ""
echo -e "${GREEN}✅ Todos os testes passaram com cobertura adequada!${NC}"
echo ""
echo "💡 Para ver relatório detalhado: open htmlcov/index.html"
echo ""

