#!/usr/bin/env python3
"""
Direct Ticker Lookup

Use company numbers to directly lookup tickers from official sources
"""

import csv
import requests
import time
import re

def extract_companies_with_numbers():
    """Extract companies with their numbers"""
    companies = []
    
    try:
        with open('/dropbox/01. Asset Ownership/02. general_information/general_information_20260219.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company_name = row['company_name']
                document_type = row['document_type']
                
                # Extract company number
                company_number = None
                number_match = re.search(r'\(([0-9]+)\)', company_name)
                if number_match:
                    company_number = number_match.group(1)
                
                # Clean company name
                clean_name = company_name.split('/')[0].strip()
                clean_name = clean_name.split('(')[0].strip()
                clean_name = clean_name.replace('"', '').strip()
                
                if clean_name and len(clean_name) > 3:
                    companies.append({
                        'clean_name': clean_name,
                        'original_name': company_name,
                        'document_type': document_type,
                        'company_number': company_number
                    })
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
    
    return companies

def lookup_tsx_ticker(company_number):
    """Lookup TSX/TSX-V ticker using SEDAR number"""
    # This would query TMX Money API or SEDAR database
    # Placeholder - in practice would use TMX Money API
    return None

def lookup_asx_ticker(company_number):
    """Lookup ASX ticker"""
    # This would query ASX API
    # Placeholder - in practice would use ASX API
    return None

def lookup_sec_ticker(company_number):
    """Lookup SEC ticker using CIK number"""
    # This would query SEC EDGAR API
    # Placeholder - in practice would use SEC API
    return None

def lookup_ticker(company_info):
    """Lookup ticker based on document type"""
    if "NI 43-101" in company_info['document_type']:
        return lookup_tsx_ticker(company_info['company_number'])
    elif "JORC" in company_info['document_type']:
        return lookup_asx_ticker(company_info['company_number'])
    elif "SK-1300" in company_info['document_type']:
        return lookup_sec_ticker(company_info['company_number'])
    return None

def main():
    """Main function"""
    print("Extracting companies with numbers...")
    companies = extract_companies_with_numbers()
    
    print(f"Found {len(companies)} companies")
    
    results = []
    
    # Sample lookup for demonstration
    for company in companies[:50]:  # First 50 for demo
        ticker = lookup_ticker(company)
        
        result = {
            'company_name': company['clean_name'],
            'original_name': company['original_name'],
            'document_type': company['document_type'],
            'company_number': company['company_number'],
            'ticker': ticker if ticker else 'NEEDS_LOOKUP',
            'status': 'Found' if ticker else 'Needs API lookup'
        }
        
        results.append(result)
    
    # Save results
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/direct_ticker_lookup_sample.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'original_name', 'document_type', 'company_number', 'ticker', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Saved sample results to: {csv_file}")
    print(f"Companies with numbers: {len([c for c in companies if c['company_number']])}")
    
    # Show companies with numbers
    print("\nCompanies with identifiable numbers:")
    companies_with_numbers = [c for c in companies if c['company_number']]
    for company in companies_with_numbers[:10]:
        print(f"{company['clean_name']} -> {company['company_number']} ({company['document_type']})")

if __name__ == "__main__":
    main()