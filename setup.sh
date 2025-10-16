#!/bin/bash

echo "======================================"
echo "   CodePlatform - Setup Inicial"
echo "======================================"
echo ""

# Verificar se Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 não está instalado. Por favor, instale Python 3.8 ou superior."
    exit 1
fi

echo "✓ Python3 encontrado"

# Criar ambiente virtual
echo ""
echo "Criando ambiente virtual..."
python3 -m venv venv

# Ativar ambiente virtual
echo "Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo ""
echo "Instalando dependências..."
pip install --upgrade pip
pip install -r requirements.txt

# Aplicar migrações
echo ""
echo "Aplicando migrações do banco de dados..."
python manage.py makemigrations
python manage.py migrate

# Criar problemas de exemplo
echo ""
echo "Criando problemas de exemplo..."
python manage.py create_sample_problems

# Criar superusuário
echo ""
echo "======================================"
echo "Agora vamos criar um superusuário para acessar o admin."
echo "======================================"
python manage.py createsuperuser

echo ""
echo "======================================"
echo "   ✅ Setup concluído com sucesso!"
echo "======================================"
echo ""
echo "Para iniciar o servidor:"
echo "  1. Ative o ambiente virtual: source venv/bin/activate"
echo "  2. Execute: python manage.py runserver"
echo "  3. Acesse: http://localhost:8000"
echo ""
echo "Para acessar o admin:"
echo "  - URL: http://localhost:8000/admin"
echo "  - Use as credenciais do superusuário criado acima"
echo ""

