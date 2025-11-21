"""
Demonstration script showing various analyses using pandas, numpy, scipy, and seaborn.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path
from data_loader import PeriodicTableDataLoader


def create_analysis_report(json_file_path):
    """
    Create comprehensive analysis report of periodic table data.
    
    Args:
        json_file_path (str): Path to PeriodicTableJSON.json
    """
    loader = PeriodicTableDataLoader(json_file_path)
    df = loader.get_dataframe()
    
    print("\n" + "="*70)
    print("PERIODIC TABLE ANALYSIS REPORT")
    print("="*70)
    
    # Basic Statistics
    print("\n1. BASIC STATISTICS")
    print("-" * 70)
    print(f"Total Elements: {len(df)}")
    print(f"Atomic Numbers Range: {df['number'].min()} - {df['number'].max()}")
    print(f"Atomic Mass Range: {df['atomic_mass'].min():.3f} - {df['atomic_mass'].max():.3f}")
    
    # Categories
    print("\n2. ELEMENT CATEGORIES")
    print("-" * 70)
    categories = df['category'].value_counts()
    for cat, count in categories.items():
        print(f"  {cat:.<40s} {count:>3d} elements")
    
    # Phases
    print("\n3. ELEMENT PHASES AT ROOM TEMPERATURE")
    print("-" * 70)
    phases = df['phase'].value_counts()
    for phase, count in phases.items():
        percentage = (count / len(df)) * 100
        print(f"  {phase:.<40s} {count:>3d} elements ({percentage:>5.1f}%)")
    
    # Thermal Properties Statistics
    print("\n4. THERMAL PROPERTIES STATISTICS")
    print("-" * 70)
    
    melt_valid = df['melt'].dropna()
    boil_valid = df['boil'].dropna()
    density_valid = df['density'].dropna()
    
    if len(melt_valid) > 0:
        print(f"\nMelting Points (K):")
        print(f"  Mean: {melt_valid.mean():.2f}")
        print(f"  Median: {melt_valid.median():.2f}")
        print(f"  Std Dev: {melt_valid.std():.2f}")
        print(f"  Range: {melt_valid.min():.2f} - {melt_valid.max():.2f}")
    
    if len(boil_valid) > 0:
        print(f"\nBoiling Points (K):")
        print(f"  Mean: {boil_valid.mean():.2f}")
        print(f"  Median: {boil_valid.median():.2f}")
        print(f"  Std Dev: {boil_valid.std():.2f}")
        print(f"  Range: {boil_valid.min():.2f} - {boil_valid.max():.2f}")
    
    if len(density_valid) > 0:
        print(f"\nDensity (g/cm³ or g/L):")
        print(f"  Mean: {density_valid.mean():.4f}")
        print(f"  Median: {density_valid.median():.4f}")
        print(f"  Std Dev: {density_valid.std():.4f}")
        print(f"  Range: {density_valid.min():.4f} - {density_valid.max():.4f}")
    
    # Electronegativity
    print("\n5. ELECTRONEGATIVITY (PAULING)")
    print("-" * 70)
    en_valid = df['electronegativity_pauling'].dropna()
    if len(en_valid) > 0:
        print(f"  Mean: {en_valid.mean():.2f}")
        print(f"  Median: {en_valid.median():.2f}")
        print(f"  Range: {en_valid.min():.2f} - {en_valid.max():.2f}")
        print(f"  Most Electronegative: {df[df['electronegativity_pauling'] == en_valid.max()]['name'].values[0]}")
        print(f"  Least Electronegative: {df[df['electronegativity_pauling'] == en_valid.min()]['name'].values[0]}")
    
    # Extreme Values
    print("\n6. EXTREME VALUES")
    print("-" * 70)
    heaviest = df.loc[df['atomic_mass'].idxmax()]
    lightest = df.loc[df['atomic_mass'].idxmin()]
    densest = df.loc[df['density'].idxmax()]
    least_dense = df.loc[df['density'].idxmin()]
    
    print(f"\nHeaviest Element:")
    print(f"  {heaviest['name']} ({heaviest['symbol']}) - {heaviest['atomic_mass']} amu")
    
    print(f"\nLightest Element:")
    print(f"  {lightest['name']} ({lightest['symbol']}) - {lightest['atomic_mass']} amu")
    
    if not pd.isna(densest['density']):
        print(f"\nDensest Element:")
        print(f"  {densest['name']} ({densest['symbol']}) - {densest['density']} g/cm³")
    
    if not pd.isna(least_dense['density']):
        print(f"\nLeast Dense Element:")
        print(f"  {least_dense['name']} ({least_dense['symbol']}) - {least_dense['density']} g/cm³")
    
    print("\n" + "="*70 + "\n")


def create_visualizations(json_file_path, output_dir="./periodic_table_analysis"):
    """
    Create various analytical visualizations.
    
    Args:
        json_file_path (str): Path to PeriodicTableJSON.json
        output_dir (str): Directory to save visualizations
    """
    loader = PeriodicTableDataLoader(json_file_path)
    df = loader.get_dataframe()
    
    Path(output_dir).mkdir(exist_ok=True)
    
    # Set style
    sns.set_style("whitegrid")
    plt.rcParams['figure.figsize'] = (12, 6)
    
    # 1. Atomic Mass Distribution
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.histplot(data=df, x='atomic_mass', bins=30, kde=True, ax=ax, color='steelblue')
    ax.set_title('Distribution of Atomic Masses', fontsize=14, fontweight='bold')
    ax.set_xlabel('Atomic Mass (amu)')
    ax.set_ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_atomic_mass_distribution.png', dpi=300)
    plt.close()
    print("✓ Saved: 01_atomic_mass_distribution.png")
    
    # 2. Elements by Category
    fig, ax = plt.subplots(figsize=(14, 8))
    category_counts = df['category'].value_counts()
    sns.barplot(x=category_counts.values, y=category_counts.index, palette='Set2', ax=ax)
    ax.set_title('Number of Elements by Category', fontsize=14, fontweight='bold')
    ax.set_xlabel('Count')
    ax.set_ylabel('Category')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_elements_by_category.png', dpi=300)
    plt.close()
    print("✓ Saved: 02_elements_by_category.png")
    
    # 3. Phase Distribution (Pie Chart)
    fig, ax = plt.subplots(figsize=(10, 8))
    phase_counts = df['phase'].value_counts()
    colors = sns.color_palette('husl', len(phase_counts))
    ax.pie(phase_counts.values, labels=phase_counts.index, autopct='%1.1f%%', 
           colors=colors, startangle=90)
    ax.set_title('Element Phases at Room Temperature', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_phase_distribution.png', dpi=300)
    plt.close()
    print("✓ Saved: 03_phase_distribution.png")
    
    # 4. Atomic Mass vs Electronegativity
    fig, ax = plt.subplots(figsize=(12, 8))
    df_valid = df[df['electronegativity_pauling'].notna()]
    scatter = ax.scatter(df_valid['atomic_mass'], df_valid['electronegativity_pauling'], 
                        s=100, c=df_valid['number'], cmap='viridis', alpha=0.6, edgecolors='black')
    ax.set_xlabel('Atomic Mass (amu)')
    ax.set_ylabel('Electronegativity (Pauling)')
    ax.set_title('Atomic Mass vs Electronegativity', fontsize=14, fontweight='bold')
    plt.colorbar(scatter, ax=ax, label='Atomic Number')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_mass_vs_electronegativity.png', dpi=300)
    plt.close()
    print("✓ Saved: 04_mass_vs_electronegativity.png")
    
    # 5. Melting vs Boiling Points
    fig, ax = plt.subplots(figsize=(12, 8))
    df_temp = df[(df['melt'].notna()) & (df['boil'].notna())]
    ax.scatter(df_temp['melt'], df_temp['boil'], s=100, alpha=0.6, 
              c=df_temp['density'], cmap='plasma', edgecolors='black')
    ax.set_xlabel('Melting Point (K)')
    ax.set_ylabel('Boiling Point (K)')
    ax.set_title('Melting Point vs Boiling Point', fontsize=14, fontweight='bold')
    plt.colorbar(ax.collections[0], ax=ax, label='Density')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_melt_vs_boil.png', dpi=300)
    plt.close()
    print("✓ Saved: 05_melt_vs_boil.png")
    
    # 6. Density by Category (Violin Plot)
    fig, ax = plt.subplots(figsize=(14, 8))
    df_density = df[df['density'].notna()].sort_values('density', ascending=False).head(20)
    sns.barplot(data=df_density, y='name', x='density', palette='coolwarm', ax=ax)
    ax.set_title('Top 20 Densest Elements', fontsize=14, fontweight='bold')
    ax.set_xlabel('Density (g/cm³ or g/L)')
    ax.set_ylabel('Element')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/06_densest_elements.png', dpi=300)
    plt.close()
    print("✓ Saved: 06_densest_elements.png")
    
    # 7. Electron Shells Distribution
    fig, ax = plt.subplots(figsize=(12, 6))
    shell_counts = df['period'].value_counts().sort_index()
    sns.barplot(x=shell_counts.index, y=shell_counts.values, palette='Set1', ax=ax)
    ax.set_title('Number of Elements in Each Period', fontsize=14, fontweight='bold')
    ax.set_xlabel('Period')
    ax.set_ylabel('Number of Elements')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/07_elements_per_period.png', dpi=300)
    plt.close()
    print("✓ Saved: 07_elements_per_period.png")
    
    # 8. Periodic Table Heatmap (Atomic Mass)
    fig, ax = plt.subplots(figsize=(18, 10))
    max_period = int(df['period'].max())
    max_group = int(df['group'].max())
    heatmap_data = np.full((max_period, max_group), np.nan)
    
    for _, row in df.iterrows():
        period = int(row['period']) - 1
        group = int(row['group']) - 1
        heatmap_data[period, group] = row['atomic_mass']
    
    sns.heatmap(heatmap_data, cmap='YlOrRd', ax=ax, cbar_kws={'label': 'Atomic Mass'}, 
               linewidths=0.5)
    ax.set_title('Periodic Table - Atomic Mass Heatmap', fontsize=14, fontweight='bold')
    ax.set_xlabel('Group')
    ax.set_ylabel('Period')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/08_periodic_table_heatmap.png', dpi=300)
    plt.close()
    print("✓ Saved: 08_periodic_table_heatmap.png")
    
    # 9. Correlation Matrix for Numerical Properties
    fig, ax = plt.subplots(figsize=(12, 10))
    numeric_cols = ['atomic_mass', 'density', 'melt', 'boil', 'electronegativity_pauling']
    df_numeric = df[numeric_cols].dropna()
    correlation = df_numeric.corr()
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', center=0, ax=ax)
    ax.set_title('Correlation Matrix of Element Properties', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig(f'{output_dir}/09_correlation_matrix.png', dpi=300)
    plt.close()
    print("✓ Saved: 09_correlation_matrix.png")
    
    print(f"\n✓ All visualizations saved to '{output_dir}/'")


def main():
    """Main entry point for analysis demo."""
    json_path = Path(__file__).parent / "Periodic-Table-JSON" / "PeriodicTableJSON.json"
    
    if not json_path.exists():
        print(f"Error: Could not find PeriodicTableJSON.json at {json_path}")
        return
    
    print("\nGenerating Analysis Report...")
    create_analysis_report(str(json_path))
    
    print("Generating Visualizations...")
    create_visualizations(str(json_path))


if __name__ == "__main__":
    main()
