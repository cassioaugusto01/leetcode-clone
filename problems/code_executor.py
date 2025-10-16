import json
import sys
import traceback
from io import StringIO
import time
import platform


class TimeoutException(Exception):
    """Exceção para timeout de execução"""
    pass


def execute_code(code, test_cases, function_name='solution'):
    """
    Executa o código do usuário com os casos de teste
    
    Args:
        code: String com o código Python do usuário
        test_cases: Lista de dicionários com 'input_data' e 'expected_output'
        function_name: Nome da função a ser chamada
    
    Returns:
        dict com status, mensagem e resultados dos testes
    """
    results = {
        'status': 'accepted',
        'message': 'Todos os testes passaram!',
        'test_results': [],
        'execution_time': 0
    }
    
    start_time = time.time()
    
    try:
        # Criar namespace isolado para execução
        namespace = {}
        
        # Redirecionar stdout para capturar prints
        old_stdout = sys.stdout
        sys.stdout = StringIO()
        
        try:
            # Executar o código do usuário
            exec(code, namespace)
            
            # Verificar se a função existe
            if function_name not in namespace:
                sys.stdout = old_stdout
                return {
                    'status': 'runtime_error',
                    'message': f'Função "{function_name}" não encontrada no código',
                    'test_results': [],
                    'execution_time': 0
                }
            
            user_function = namespace[function_name]
            
            # Executar cada caso de teste
            for i, test_case in enumerate(test_cases):
                test_result = {
                    'test_number': i + 1,
                    'passed': False,
                    'input': test_case['input_data'],
                    'expected': test_case['expected_output'],
                    'actual': None,
                    'error': None
                }
                
                try:
                    # Parse do input (JSON)
                    input_args = json.loads(test_case['input_data'])
                    expected_output = json.loads(test_case['expected_output'])
                    
                    # Executar a função
                    if isinstance(input_args, list):
                        actual_output = user_function(*input_args)
                    elif isinstance(input_args, dict):
                        actual_output = user_function(**input_args)
                    else:
                        actual_output = user_function(input_args)
                    
                    test_result['actual'] = actual_output
                    
                    # Comparar resultado
                    if actual_output == expected_output:
                        test_result['passed'] = True
                    else:
                        test_result['passed'] = False
                        results['status'] = 'wrong_answer'
                        results['message'] = f'Teste {i + 1} falhou'
                    
                except json.JSONDecodeError as e:
                    test_result['error'] = f'Erro ao parsear JSON: {str(e)}'
                    results['status'] = 'runtime_error'
                    results['message'] = 'Erro no formato dos dados de teste'
                except Exception as e:
                    test_result['error'] = str(e)
                    results['status'] = 'runtime_error'
                    results['message'] = f'Erro no teste {i + 1}: {str(e)}'
                
                results['test_results'].append(test_result)
                
                # Se um teste falhou, parar
                if not test_result['passed']:
                    break
        
        finally:
            # Restaurar stdout
            sys.stdout = old_stdout
    
    except SyntaxError as e:
        results['status'] = 'runtime_error'
        results['message'] = f'Erro de sintaxe: {str(e)}'
    
    except Exception as e:
        results['status'] = 'runtime_error'
        results['message'] = f'Erro durante execução: {str(e)}\n{traceback.format_exc()}'
    
    end_time = time.time()
    results['execution_time'] = round(end_time - start_time, 3)
    
    return results

