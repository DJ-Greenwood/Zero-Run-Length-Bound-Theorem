import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
from typing import List, Dict
import os
from pathlib import Path

# Define base directory and ensure it exists
BASE_DIR = Path("number-analysis/Code/number-analysis")
os.makedirs(BASE_DIR, exist_ok=True)

def replace_special_chars(text: str) -> str:
    """Replace special Unicode characters with ASCII alternatives."""
    replacements = {
        '√': 'sqrt',
        'φ': 'phi',
        '∛': 'cbrt',
        'π': 'pi'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def load_data(json_path: Path) -> List[Dict]:
    """Load and process data from JSON report."""
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        # Process data to match required format
        processed_data = []
        for item in data:
            processed_item = {
                "name": replace_special_chars(item["name"]),
                "type": item["type"],
                "meanRatio": item["stats"]["mean_ratio"],
                "medianRatio": item["stats"]["median_ratio"],
                "stdDev": item["stats"]["std_ratio"],
                "totalRuns": item["total_runs"],
                "distribution": {
                    "low": item["stats"]["ratio_distribution"]["0-33%"],
                    "medium": item["stats"]["ratio_distribution"]["33-66%"],
                    "high": item["stats"]["ratio_distribution"]["66-100%"]
                }
            }
            
            if item["type"] == "algebraic":
                processed_item["degree"] = item["factor"]
            else:
                processed_item["measure"] = item["factor"]
                
            processed_data.append(processed_item)
        
        return processed_data
    except FileNotFoundError:
        print(f"Error: Could not find file at {json_path}")
        raise
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {json_path}")
        raise
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        raise

def create_ratio_comparison_plot(data: List[Dict]):
    """Create a bar plot comparing mean ratios, median ratios, and standard deviations."""
    df_ratios = pd.DataFrame([{
        'name': d['name'],
        'Mean Ratio': d['meanRatio'],
        'Median Ratio': d['medianRatio'],
        'Standard Deviation': d['stdDev'],
        'Type': d['type']
    } for d in data])
    
    plt.figure(figsize=(15, 8))
    x = np.arange(len(df_ratios['name']))
    width = 0.25
    
    plt.bar(x - width, df_ratios['Mean Ratio'], width, label='Mean Ratio', color='#8884d8')
    plt.bar(x, df_ratios['Median Ratio'], width, label='Median Ratio', color='#82ca9d')
    plt.bar(x + width, df_ratios['Standard Deviation'], width, label='Standard Deviation', color='#ffc658')
    
    plt.xlabel('Numbers')
    plt.ylabel('Ratio')
    plt.title('Ratio Comparison Analysis (4000 digits)')
    plt.xticks(x, df_ratios['name'], rotation=45, ha='right')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    return plt.gcf()

def create_distribution_plot(data: List[Dict]):
    """Create a stacked bar plot showing the distribution of run lengths."""
    df_dist = pd.DataFrame([{
        'name': d['name'],
        '0-33% of bound': d['distribution']['low'],
        '33-66% of bound': d['distribution']['medium'],
        '66-100% of bound': d['distribution']['high'],
        'Type': d['type']
    } for d in data])
    
    plt.figure(figsize=(15, 8))
    
    bottom = np.zeros(len(data))
    for column, color in zip(['0-33% of bound', '33-66% of bound', '66-100% of bound'],
                           ['#82ca9d', '#8884d8', '#ffc658']):
        plt.bar(df_dist['name'], df_dist[column], bottom=bottom, label=column, color=color)
        bottom += df_dist[column]
    
    plt.xlabel('Numbers')
    plt.ylabel('Number of Runs')
    plt.title('Distribution of Run Lengths (4000 digits)')
    plt.xticks(rotation=45, ha='right')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.tight_layout()
    
    return plt.gcf()

def analyze_data(data: List[Dict]) -> str:
    """Generate key findings based on the data."""
    algebraic_deg2 = [d for d in data if d['type'] == 'algebraic' and d.get('degree') == 2]
    deg2_means = [d['meanRatio'] for d in algebraic_deg2]
    deg3_data = next((d for d in data if d['type'] == 'algebraic' and d.get('degree') == 3), None)
    transcendental = [d for d in data if d['type'] == 'transcendental']
    
    findings = f"""Key Findings from High Precision Analysis:

1. Consistency in Algebraic Degree 2:
   - Mean ratios for degree 2 numbers: {min(deg2_means):.3f}-{max(deg2_means):.3f}

2. Higher Degree Impact:
   - cbrt(2) - 1 (degree 3) mean ratio: {deg3_data['meanRatio']:.3f}

3. Transcendental Hierarchy:
   - {' -> '.join(f"{d['name']} ({d['meanRatio']:.3f})" for d in sorted(transcendental, key=lambda x: -x['meanRatio']))}

4. Distribution Stability:
   - Average percentage in 0-33% range: {100 * np.mean([d['distribution']['low']/d['totalRuns'] for d in data]):.1f}%

5. Total Runs:
   - Range: {min(d['totalRuns'] for d in data)}-{max(d['totalRuns'] for d in data)} runs in 4000 digits

6. Standard Deviations:
   - Generally decrease with higher degree/measure"""
    
    return findings

def main():
    """Main function to generate all visualizations and analysis."""
    # Set up file paths
    json_path = BASE_DIR / "report.json"
    
    try:
        # Load and process data
        data = load_data(json_path)
        
        # Set style for better-looking plots
        plt.style.use('seaborn-v0_8')
        
        # Create and save ratio comparison plot
        ratio_fig = create_ratio_comparison_plot(data)
        ratio_fig.savefig(BASE_DIR / 'ratio_comparison.png', dpi=300, bbox_inches='tight')
        
        # Create and save distribution plot
        dist_fig = create_distribution_plot(data)
        dist_fig.savefig(BASE_DIR / 'distribution_analysis.png', dpi=300, bbox_inches='tight')
        
        # Generate, print, and save findings
        findings = analyze_data(data)
        print(findings)
        
        with open(BASE_DIR / 'findings.txt', 'w', encoding='utf-8') as f:
            f.write(findings)
        
        plt.show()
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())