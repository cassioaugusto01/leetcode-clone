from django.test import TestCase
from problems.code_executor import execute_code
import json


class CodeExecutorTest(TestCase):
    """Testes para o executor de código"""
    
    def test_execute_code_success(self):
        """Testa execução bem-sucedida"""
        code = "def solution(a, b):\n    return a + b"
        test_cases = [
            {
                'input_data': json.dumps([2, 3]),
                'expected_output': json.dumps(5)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(len(result['test_results']), 1)
        self.assertTrue(result['test_results'][0]['passed'])
    
    def test_execute_code_wrong_answer(self):
        """Testa código com resposta errada"""
        code = "def solution(a, b):\n    return a - b"  # Errado, deveria somar
        test_cases = [
            {
                'input_data': json.dumps([2, 3]),
                'expected_output': json.dumps(5)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'wrong_answer')
        self.assertFalse(result['test_results'][0]['passed'])
    
    def test_execute_code_function_not_found(self):
        """Testa quando a função não existe"""
        code = "def wrong_name(a, b):\n    return a + b"
        test_cases = [
            {
                'input_data': json.dumps([2, 3]),
                'expected_output': json.dumps(5)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'runtime_error')
        self.assertIn('não encontrada', result['message'])
    
    def test_execute_code_syntax_error(self):
        """Testa código com erro de sintaxe"""
        code = "def solution(a, b)\n    return a + b"  # Falta :
        test_cases = [
            {
                'input_data': json.dumps([2, 3]),
                'expected_output': json.dumps(5)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'runtime_error')
        self.assertIn('sintaxe', result['message'].lower())
    
    def test_execute_code_runtime_error(self):
        """Testa código com erro em tempo de execução"""
        code = "def solution(a, b):\n    return a / 0"  # Divisão por zero
        test_cases = [
            {
                'input_data': json.dumps([2, 3]),
                'expected_output': json.dumps(5)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'runtime_error')
    
    def test_execute_code_multiple_tests(self):
        """Testa múltiplos casos de teste"""
        code = "def solution(a, b):\n    return a + b"
        test_cases = [
            {
                'input_data': json.dumps([2, 3]),
                'expected_output': json.dumps(5)
            },
            {
                'input_data': json.dumps([10, 20]),
                'expected_output': json.dumps(30)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(len(result['test_results']), 2)
        self.assertTrue(all(t['passed'] for t in result['test_results']))
    
    def test_execute_code_stops_on_first_failure(self):
        """Testa se para no primeiro teste que falha"""
        code = "def solution(a, b):\n    return a - b"  # Errado
        test_cases = [
            {
                'input_data': json.dumps([2, 3]),
                'expected_output': json.dumps(5)
            },
            {
                'input_data': json.dumps([10, 20]),
                'expected_output': json.dumps(30)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'wrong_answer')
        self.assertEqual(len(result['test_results']), 1)  # Para no primeiro
    
    def test_execute_code_with_list_input(self):
        """Testa com entrada tipo lista"""
        code = "def solution(nums):\n    return max(nums)"
        test_cases = [
            {
                'input_data': json.dumps([[1, 5, 3, 9, 2]]),
                'expected_output': json.dumps(9)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'accepted')
        self.assertTrue(result['test_results'][0]['passed'])
    
    def test_execute_code_with_string_input(self):
        """Testa com entrada tipo string"""
        code = "def solution(s):\n    return s[::-1]"
        test_cases = [
            {
                'input_data': json.dumps(["hello"]),
                'expected_output': json.dumps("olleh")
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'accepted')
        self.assertTrue(result['test_results'][0]['passed'])
    
    def test_execute_code_with_dict_input(self):
        """Testa com entrada tipo dicionário (kwargs)"""
        code = "def solution(a, b):\n    return a * b"
        test_cases = [
            {
                'input_data': json.dumps({"a": 3, "b": 4}),
                'expected_output': json.dumps(12)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'accepted')
        self.assertTrue(result['test_results'][0]['passed'])
    
    def test_execute_code_measures_execution_time(self):
        """Testa se mede tempo de execução"""
        code = "def solution(a, b):\n    return a + b"
        test_cases = [
            {
                'input_data': json.dumps([2, 3]),
                'expected_output': json.dumps(5)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertIn('execution_time', result)
        self.assertIsInstance(result['execution_time'], float)
        self.assertGreaterEqual(result['execution_time'], 0)
    
    def test_execute_code_json_decode_error(self):
        """Testa erro ao decodificar JSON inválido"""
        code = "def solution(a, b):\n    return a + b"
        test_cases = [
            {
                'input_data': 'invalid json',
                'expected_output': json.dumps(5)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'runtime_error')
        self.assertIn('formato dos dados', result['message'].lower())
    
    def test_execute_code_with_complex_logic(self):
        """Testa código com lógica mais complexa"""
        code = """
def solution(n):
    if n <= 1:
        return n
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b
"""
        test_cases = [
            {
                'input_data': json.dumps([5]),
                'expected_output': json.dumps(5)
            },
            {
                'input_data': json.dumps([10]),
                'expected_output': json.dumps(55)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        self.assertEqual(result['status'], 'accepted')
        self.assertEqual(len(result['test_results']), 2)
    
    def test_execute_code_test_result_structure(self):
        """Testa estrutura do resultado de cada teste"""
        code = "def solution(a, b):\n    return a + b"
        test_cases = [
            {
                'input_data': json.dumps([2, 3]),
                'expected_output': json.dumps(5)
            }
        ]
        result = execute_code(code, test_cases, 'solution')
        
        test_result = result['test_results'][0]
        self.assertIn('test_number', test_result)
        self.assertIn('passed', test_result)
        self.assertIn('input', test_result)
        self.assertIn('expected', test_result)
        self.assertIn('actual', test_result)
        self.assertIn('error', test_result)

