import math
import decimal
from decimal import Decimal
from typing import Tuple, List, Dict, Optional
from collections import defaultdict
import numpy as np
from mpmath import mp
from statistics import mean, median, stdev
import json

# Set precision for both decimal and mpmath
decimal.getcontext().prec = 1000
mp.dps = 1000  # digital precision for mpmath

class NumberValidator:
    def __init__(self, precision: int = 1000):
        """Initialize validator with given precision."""
        self.precision = precision
        decimal.getcontext().prec = precision
        mp.dps = precision

    def get_binary_expansion(self, num: float, length: int) -> List[int]:
        """
        Get binary expansion of the fractional part of a number.
        Uses mpmath for enhanced precision.
        """
        mp_num = mp.mpf(str(num))
        mp_frac = mp_num - mp.floor(mp_num)
        binary = []
        
        for _ in range(length):
            mp_frac *= 2
            bit = int(mp.floor(mp_frac))
            binary.append(bit)
            mp_frac -= bit
            
        return binary

    def find_zero_runs(self, binary: List[int]) -> List[Tuple[int, int]]:
        """
        Find all zero runs in a binary sequence.
        Returns: List of tuples (starting_position, length) for each zero run
        """
        runs = []
        current_run = 0
        start_position = None
        
        for i, bit in enumerate(binary):
            if bit == 0:
                if start_position is None:
                    start_position = i
                current_run += 1
            else:
                if current_run > 0:
                    runs.append((start_position, current_run))
                current_run = 0
                start_position = None
        
        if current_run > 0:
            runs.append((start_position, current_run))
            
        return runs

    def validate_number(self, number: float, factor: float, length: int, 
                       is_transcendental: bool = False, verbose: bool = True) -> Dict:
        """Enhanced validation with detailed statistical analysis."""
        binary = self.get_binary_expansion(number, length)
        zero_runs = self.find_zero_runs(binary)
        violations = []
        ratios = []
        
        number_type = "transcendental" if is_transcendental else "algebraic"
        factor_name = "μ (irrationality measure)" if is_transcendental else "d (degree)"
        
        # Store all run data for analysis
        run_data = []
        max_ratio = 0
        
        for position, run_length in zero_runs:
            if position < 1:
                continue
                
            bound = factor * math.log2(position + 1)
            ratio = run_length / bound if bound > 0 else float('inf')
            max_ratio = max(max_ratio, ratio)
            
            run_data.append({
                'position': position,
                'length': run_length,
                'bound': bound,
                'ratio': ratio
            })
            
            if ratio > 1:
                violations.append({
                    'position': position,
                    'run_length': run_length,
                    'bound': bound,
                    'ratio': ratio
                })
        
        # Calculate statistics
        if run_data:
            ratios = [d['ratio'] for d in run_data]
            stats = {
                'mean_ratio': mean(ratios),
                'median_ratio': median(ratios),
                'std_ratio': stdev(ratios),
                'ratio_distribution': {
                    '0-33%': len([r for r in ratios if r < 0.33]),
                    '33-66%': len([r for r in ratios if 0.33 <= r < 0.66]),
                    '66-100%': len([r for r in ratios if r >= 0.66])
                }
            }
        else:
            stats = {}
        
        result = {
            'valid': len(violations) == 0,
            'violations': violations,
            'max_ratio': max_ratio,
            'total_runs': len(zero_runs),
            'binary_prefix': binary[:50],
            'stats': stats,
            'number_type': number_type,
            'factor': factor,
            'factor_name': factor_name,
            'number': number,
            'run_data': run_data
        }
        
        if verbose:
            self._print_analysis(result)
        
        return result
    
    def _print_analysis(self, result: Dict):
        """Print detailed analysis of the validation results."""
        print(f"\nAnalyzing {result['number_type']} number: {result['number']}")
        print(f"Factor ({result['factor_name']}): {result['factor']}")
        print(f"First 50 bits: {''.join(map(str, result['binary_prefix']))}")
        print(f"Found {result['total_runs']} zero runs")
        
        if result['stats']:
            print("\nStatistical Analysis:")
            print(f"Mean ratio to bound: {result['stats']['mean_ratio']:.3f}")
            print(f"Median ratio to bound: {result['stats']['median_ratio']:.3f}")
            print(f"Standard deviation: {result['stats']['std_ratio']:.3f}")
            print("\nRatio Distribution:")
            print(f"0-33% of bound: {result['stats']['ratio_distribution']['0-33%']} runs")
            print(f"33-66% of bound: {result['stats']['ratio_distribution']['33-66%']} runs")
            print(f"66-100% of bound: {result['stats']['ratio_distribution']['66-100%']} runs")
            
        if result['violations']:
            print("\nViolations found:")
            for violation in result['violations']:
                print(f"Position: {violation['position']}, Run Length: {violation['run_length']}, "
                      f"Bound: {violation['bound']:.3f}, Ratio: {violation['ratio']:.3f}")

    @staticmethod
    def create_report(results: List[Tuple[Dict, Dict]], filename: str = "report.json"):
        """Create a JSON report from the analysis results."""
        def convert_to_serializable(obj):
            """Convert non-serializable objects to JSON-serializable types."""
            if isinstance(obj, (np.integer, np.floating)):
                return float(obj)
            if isinstance(obj, (mp.mpf, decimal.Decimal)):
                return float(obj)
            if isinstance(obj, (list, tuple)):
                return [convert_to_serializable(item) for item in obj]
            if isinstance(obj, dict):
                return {k: convert_to_serializable(v) for k, v in obj.items()}
            return obj

        report_data = []
        
        for case, result in results:
            report_entry = {
                'name': case['name'],
                'type': case['type'],
                'number': float(result['number']),  # Convert to standard float
                'factor': float(result['factor']),  # Convert to standard float
                'factor_name': result['factor_name'],
                'valid': result['valid'],
                'max_ratio': float(result['max_ratio']),  # Convert to standard float
                'total_runs': result['total_runs'],
                'violations': convert_to_serializable(result['violations']),
                'stats': convert_to_serializable(result['stats']),
                'binary_prefix': ''.join(map(str, result['binary_prefix'])),
                'run_data': convert_to_serializable(result['run_data'])
            }
            report_data.append(report_entry)
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=4)

        # Generate the report after running the analysis
        #results = run_analysis()
        #create_report(results)

def run_analysis():
    """Run comprehensive analysis with statistical insights."""
    validator = NumberValidator(precision=4000)
    test_length = 4000
    
    # Test cases with their expected theoretical properties
    test_cases = [
        {'number': math.sqrt(2) - 1, 'factor': 2, 'name': '√2 - 1', 'type': 'algebraic'},
        {'number': math.sqrt(3) - 1, 'factor': 2, 'name': '√3 - 1', 'type': 'algebraic'},
        {'number': (1 + math.sqrt(5))/2 - 1, 'factor': 2, 'name': 'φ - 1', 'type': 'algebraic'},
        {'number': mp.root(2, 3) - 1, 'factor': 3, 'name': '∛2 - 1', 'type': 'algebraic'},
        {'number': math.pi - 3, 'factor': 7.625, 'name': 'π - 3', 'type': 'transcendental'},
        {'number': math.e - 2, 'factor': 2.445, 'name': 'e - 2', 'type': 'transcendental'},
        {'number': float(mp.log(2)), 'factor': 3.444, 'name': 'ln(2)', 'type': 'transcendental'},
        {'number': float(mp.log(3)), 'factor': 3.892, 'name': 'ln(3)', 'type': 'transcendental'}
    ]
    
    results = []
    for case in test_cases:
        print(f"\nTesting {case['name']} ({case['type']}):")
        result = validator.validate_number(
            case['number'], 
            case['factor'], 
            test_length, 
            is_transcendental=(case['type'] == 'transcendental')
        )
        results.append((case, result))

    
    return results

    

if __name__ == "__main__":
    results = run_analysis()
    NumberValidator.create_report(results, filename="number-analysis/Code/number-analysis/report.json")