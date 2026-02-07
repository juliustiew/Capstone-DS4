#!/usr/bin/env python3
"""
Data Cleaning & Quality Assurance Report
Shows before/after comparison of data cleaning operations
"""

import pandas as pd
import json
import numpy as np
from datetime import datetime

def extract_primary_category(cat_str):
    """Extract primary category from JSON."""
    try:
        if pd.isna(cat_str) or cat_str == '':
            return 'Other'
        categories = json.loads(cat_str.replace('""', '"'))
        if isinstance(categories, list) and len(categories) > 0:
            return categories[0].get('category', 'Other')
    except:
        pass
    return 'Other'


def clean_data_quality(df):
    """Advanced data quality cleaning."""
    df = df.copy()
    
    # Remove entirely empty columns
    if 'occupationId' in df.columns:
        df = df.drop('occupationId', axis=1)
    
    # Convert salary columns to numeric
    for col in ['salary_minimum', 'salary_maximum', 'average_salary']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Define reasonable salary bounds
    SALARY_MIN_THRESHOLD = 500
    SALARY_MAX_THRESHOLD = 50000
    
    # Remove zero/null salaries
    df = df[df['average_salary'].notna() & (df['average_salary'] > 0)]
    
    # Remove extreme outliers
    salary_q001 = df['average_salary'].quantile(0.001)
    salary_q999 = df['average_salary'].quantile(0.999)
    salary_q999 = min(salary_q999, SALARY_MAX_THRESHOLD)
    df = df[(df['average_salary'] >= salary_q001) & (df['average_salary'] <= salary_q999)]
    
    # Clean salary range
    for col in ['salary_minimum', 'salary_maximum']:
        if col in df.columns:
            df.loc[df[col] > SALARY_MAX_THRESHOLD, col] = df[col].median()
            df[col] = df[col].fillna(df[col].median())
    
    # Clean experience
    df['minimumYearsExperience'] = pd.to_numeric(df['minimumYearsExperience'], errors='coerce').fillna(0)
    MAX_EXP = 40
    df.loc[df['minimumYearsExperience'] > MAX_EXP, 'minimumYearsExperience'] = MAX_EXP
    df = df[df['minimumYearsExperience'] >= 0]
    
    # Clean dates
    date_cols = ['metadata_newPostingDate', 'metadata_originalPostingDate', 'metadata_expiryDate']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    df = df[df['metadata_newPostingDate'].notna()]
    
    # Normalize titles
    if 'title' in df.columns:
        df['title'] = df['title'].str.strip()
        df['title'] = df['title'].str.title()
        df = df[df['title'].notna() & (df['title'] != '')]
    
    # Standardize categoricals
    if 'employmentTypes' in df.columns:
        df['employmentTypes'] = df['employmentTypes'].fillna('Unknown')
        df['employmentTypes'] = df['employmentTypes'].str.strip().str.title()
    
    if 'positionLevels' in df.columns:
        df['positionLevels'] = df['positionLevels'].fillna('Unknown')
        df['positionLevels'] = df['positionLevels'].str.strip().str.title()
    
    # Clean engagement metrics
    df['metadata_totalNumberOfView'] = pd.to_numeric(df['metadata_totalNumberOfView'], errors='coerce').fillna(0)
    df['metadata_totalNumberJobApplication'] = pd.to_numeric(df['metadata_totalNumberJobApplication'], errors='coerce').fillna(0)
    df = df[df['metadata_totalNumberOfView'] >= 0]
    df = df[df['metadata_totalNumberJobApplication'] >= 0]
    
    # Clean company names
    if 'postedCompany_name' in df.columns:
        df['postedCompany_name'] = df['postedCompany_name'].fillna('Unknown Company')
        df['postedCompany_name'] = df['postedCompany_name'].str.strip()
    
    # Remove duplicates
    df = df.drop_duplicates()
    
    return df.reset_index(drop=True)


def print_section(title):
    """Print formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def main():
    # Load raw data
    print("\n📊 LOADING RAW DATA...")
    df_raw = pd.read_csv('/home/julius/SGJobData.csv', on_bad_lines='skip', encoding='utf-8')
    
    print_section("BEFORE CLEANING")
    print(f"Total Records:           {len(df_raw):>15,}")
    print(f"Total Columns:           {len(df_raw.columns):>15}")
    
    # Salary stats
    salary_valid = df_raw[df_raw['average_salary'] > 0]['average_salary']
    print(f"\n💰 SALARY STATISTICS (Before)")
    print(f"  Records with valid salary: {len(salary_valid):,} / {len(df_raw):,}")
    print(f"  Min:                       SGD {df_raw['average_salary'].min():,.0f}")
    print(f"  Max:                       SGD {df_raw['average_salary'].max():,.0f}")
    print(f"  Mean:                      SGD {df_raw['average_salary'].mean():,.0f}")
    print(f"  Median:                    SGD {df_raw['average_salary'].median():,.0f}")
    print(f"  Std Dev:                   SGD {df_raw['average_salary'].std():,.0f}")
    
    # Experience stats
    print(f"\n📚 EXPERIENCE REQUIREMENTS (Before)")
    print(f"  Min:                       {df_raw['minimumYearsExperience'].min()} years")
    print(f"  Max:                       {df_raw['minimumYearsExperience'].max()} years")
    print(f"  Mean:                      {df_raw['minimumYearsExperience'].mean():.1f} years")
    
    # Data quality issues
    print(f"\n⚠️  DATA QUALITY ISSUES (Before)")
    print(f"  Zero/Null salaries:        {(df_raw['average_salary'] == 0).sum():,}")
    print(f"  Missing dates:             {df_raw['metadata_newPostingDate'].isna().sum():,}")
    print(f"  Missing titles:            {df_raw['title'].isna().sum():,}")
    print(f"  Duplicate records:         {df_raw.duplicated().sum():,}")
    print(f"  Salary > 50K:              {(df_raw['average_salary'] > 50000).sum():,}")
    print(f"  Experience > 40 years:     {(df_raw['minimumYearsExperience'] > 40).sum():,}")
    
    # Apply cleaning
    print("\n🧹 APPLYING DATA CLEANING...")
    df_clean = clean_data_quality(df_raw)
    
    print_section("AFTER CLEANING")
    print(f"Total Records:           {len(df_clean):>15,}")
    print(f"Records Removed:         {len(df_raw) - len(df_clean):>15,} ({(len(df_raw) - len(df_clean))/len(df_raw)*100:.2f}%)")
    
    # Salary stats after
    print(f"\n💰 SALARY STATISTICS (After)")
    print(f"  Min:                       SGD {df_clean['average_salary'].min():,.0f}")
    print(f"  Max:                       SGD {df_clean['average_salary'].max():,.0f}")
    print(f"  Mean:                      SGD {df_clean['average_salary'].mean():,.0f}")
    print(f"  Median:                    SGD {df_clean['average_salary'].median():,.0f}")
    print(f"  Std Dev:                   SGD {df_clean['average_salary'].std():,.0f}")
    
    # Experience stats after
    print(f"\n📚 EXPERIENCE REQUIREMENTS (After)")
    print(f"  Min:                       {df_clean['minimumYearsExperience'].min():.0f} years")
    print(f"  Max:                       {df_clean['minimumYearsExperience'].max():.0f} years")
    print(f"  Mean:                      {df_clean['minimumYearsExperience'].mean():.1f} years")
    
    # Engagement metrics
    print(f"\n📈 ENGAGEMENT METRICS (After)")
    print(f"  Avg views per posting:     {df_clean['metadata_totalNumberOfView'].mean():.1f}")
    print(f"  Avg applications:          {df_clean['metadata_totalNumberJobApplication'].mean():.1f}")
    
    # Data completeness
    print(f"\n✅ DATA COMPLETENESS (After)")
    print(f"  Records with valid salary: {(df_clean['average_salary'] > 0).sum():,} / {len(df_clean):,} (100%)")
    print(f"  Records with dates:        {df_clean['metadata_newPostingDate'].notna().sum():,} / {len(df_clean):,} (100%)")
    print(f"  Duplicate records:         {df_clean.duplicated().sum():,}")
    
    # Category distribution
    df_clean['primary_category'] = df_clean['categories'].apply(extract_primary_category)
    print(f"\n🏢 JOB CATEGORY DISTRIBUTION (Top 10)")
    cat_dist = df_clean['primary_category'].value_counts().head(10)
    for idx, (cat, count) in enumerate(cat_dist.items(), 1):
        pct = count / len(df_clean) * 100
        print(f"  {idx:2d}. {cat:<30s} {count:>8,} ({pct:>5.1f}%)")
    
    # Summary
    print_section("CLEANING SUMMARY")
    improved_pct = ((len(df_raw) - len(df_clean)) / len(df_raw) * 100)
    data_quality = max(0, 100 - improved_pct)
    
    print(f"✅ Cleaned Data Quality Score:  {data_quality:.1f}%")
    print(f"✅ Records Retained:             {len(df_clean):,} / {len(df_raw):,}")
    print(f"✅ Removed Outliers/Bad Data:    {len(df_raw) - len(df_clean):,}")
    print(f"\n🧹 Cleaning Operations Applied:")
    print(f"   • Removed 100% empty columns (occupationId)")
    print(f"   • Removed salary outliers (>99.9th percentile)")
    print(f"   • Removed zero/null salaries ({(df_raw['average_salary'] == 0).sum():,})")
    print(f"   • Capped experience at 40 years")
    print(f"   • Removed records with missing critical dates")
    print(f"   • Standardized job titles and categories")
    print(f"   • Removed duplicate records ({df_raw.duplicated().sum():,})")
    print(f"   • Normalized categorical fields")
    
    print("\n✅ Dashboard is ready to use with cleaned data!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
