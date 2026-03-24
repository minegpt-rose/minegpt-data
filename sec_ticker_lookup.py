#!/usr/bin/env python3
"""
SEC Ticker Lookup

Lookup tickers for US companies (SK-1300 filings)
"""

import csv
import re

def extract_sec_companies():
    """Extract US companies with SK-1300 filings"""
    companies = []
    
    try:
        with open('/dropbox/01. Asset Ownership/02. general_information/general_information_20260219.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "SK-1300" in row['document_type']:
                    company_name = row['company_name']
                    
                    # Extract CIK number if available
                    cik_number = None
                    number_match = re.search(r'\(([0-9]+)\)', company_name)
                    if number_match:
                        cik_number = number_match.group(1)
                    
                    # Clean company name
                    clean_name = company_name.split('/')[0].strip()
                    clean_name = clean_name.split('(')[0].strip()
                    clean_name = clean_name.replace('"', '').strip()
                    
                    if clean_name:
                        companies.append({
                            'clean_name': clean_name,
                            'original_name': company_name,
                            'cik_number': cik_number
                        })
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
    
    return companies

def lookup_sec_ticker(company_name):
    """Lookup SEC ticker"""
    # Known SEC ticker mappings
    known_mappings = {
        "ALBEMARLE CORP": "ALB",
        "ARCH RESOURCES": "ARCH",
        "NEWMONT CORP": "NEM",
        "VALE SA": "VALE",
        "FREEPORT-MCMORAN INC": "FCX",
        "SOUTHERN COPPER CORP": "SCCO",
        "CLIMATE CHANGE CRITICAL MATERIALS": "CCCM",
        "COEUR MINING INC": "CDE",
        "HELENA GOLD MINING": "HL",
        "PAN AMERICAN SILVER CORP": "PAAS"
    }
    
    return known_mappings.get(company_name.upper(), "NEEDS_LOOKUP")

def main():
    """Main function"""
    print("Extracting SEC companies...")
    companies = extract_sec_companies()
    
    print(f"Found {len(companies)} US companies")
    
    # Lookup tickers
    results = []
    for company in companies:
        ticker = lookup_sec_ticker(company['clean_name'])
        
        results.append({
            'company_name': company['clean_name'],
            'cik_number': company['cik_number'],
            'ticker': ticker,
            'exchange': 'NYSE/NASDAQ',
            'source': 'SEC Known Mapping'
        })
    
    # Save results
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/sec_tickers.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'cik_number', 'ticker', 'exchange', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Saved SEC tickers to: {csv_file}")
    
    # Show results
    print("\nSample SEC Tickers:")
    for result in results[:10]:
        print(f"{result['company_name']} -> {result['ticker']}")

if __name__ == "__main__":
    main()