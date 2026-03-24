#!/usr/bin/env python3
"""
ASX Ticker Lookup

Lookup tickers for Australian companies (JORC filings)
"""

import csv
import re

def extract_asx_companies():
    """Extract Australian companies with JORC filings"""
    companies = []
    
    try:
        with open('/dropbox/01. Asset Ownership/02. general_information/general_information_20260219.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "JORC" in row['document_type']:
                    company_name = row['company_name']
                    
                    # Clean company name
                    clean_name = company_name.split('/')[0].strip()
                    clean_name = clean_name.split('(')[0].strip()
                    clean_name = clean_name.replace('"', '').strip()
                    
                    if clean_name:
                        companies.append({
                            'clean_name': clean_name,
                            'original_name': company_name
                        })
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
    
    return companies

def lookup_asx_ticker(company_name):
    """Lookup ASX ticker"""
    # Known ASX ticker mappings
    known_mappings = {
        "BHP GROUP LTD": "BHP",
        "RIO TINTO LTD": "RIO",
        "FORTESCUE LTD": "FMG",
        "NEWCREST MINING LTD": "NCM",
        "ANGLOGOLD ASHANTI LTD": "AGG",
        "SOUTH32 LTD": "S32",
        "ILUKA RESOURCES LTD": "ILU",
        "MINERAL RESOURCES LTD": "MIN",
        "NORTHERN STAR RESOURCES LTD": "NST",
        "EVOLUTION MINING LTD": "EVN"
    }
    
    return known_mappings.get(company_name.upper(), "NEEDS_LOOKUP")

def main():
    """Main function"""
    print("Extracting ASX companies...")
    companies = extract_asx_companies()
    
    print(f"Found {len(companies)} Australian companies")
    
    # Lookup tickers
    results = []
    for company in companies:
        ticker = lookup_asx_ticker(company['clean_name'])
        
        results.append({
            'company_name': company['clean_name'],
            'ticker': ticker,
            'exchange': 'ASX',
            'source': 'ASX Known Mapping'
        })
    
    # Save results
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/asx_tickers.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'ticker', 'exchange', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Saved ASX tickers to: {csv_file}")
    
    # Show results
    print("\nSample ASX Tickers:")
    for result in results[:10]:
        print(f"{result['company_name']} -> {result['ticker']}")

if __name__ == "__main__":
    main()