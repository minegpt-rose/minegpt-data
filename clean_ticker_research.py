#!/usr/bin/env python3
"""
Clean Company Ticker Research

Extract company names and create framework for ticker research
"""

import csv
import re

def extract_company_data():
    """Extract company names, filing types, and identifiers"""
    companies = []
    
    try:
        with open('/dropbox/01. Asset Ownership/02. general_information/general_information_20260219.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                company_name = row['company_name']
                document_type = row['document_type']
                
                # Clean up company name
                clean_name = company_name.split('/')[0].strip()
                clean_name = clean_name.split('(')[0].strip()
                clean_name = clean_name.replace('"', '').strip()
                
                if clean_name and len(clean_name) > 3:
                    # Extract company number if available
                    company_number = None
                    number_match = re.search(r'\(([0-9]+)\)', company_name)
                    if number_match:
                        company_number = number_match.group(1)
                    
                    companies.append({
                        'original_name': company_name,
                        'clean_name': clean_name,
                        'document_type': document_type,
                        'company_number': company_number
                    })
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
    
    return companies

def determine_exchange(document_type):
    """Determine appropriate exchange based on filing type"""
    if "NI 43-101" in document_type:
        return "TSX/TSX-V"
    elif "JORC" in document_type:
        return "ASX"
    elif "SK-1300" in document_type:
        return "SEC"
    else:
        return "Unknown"

def main():
    """Main function"""
    print("Extracting company data...")
    companies = extract_company_data()
    
    print(f"Found {len(companies)} companies")
    
    results = []
    
    for company in companies:
        exchange = determine_exchange(company['document_type'])
        
        result = {
            'company_name': company['clean_name'],
            'original_name': company['original_name'],
            'document_type': company['document_type'],
            'company_number': company['company_number'],
            'exchange': exchange,
            'tsx_ticker': '',
            'tsxv_ticker': '',
            'asx_ticker': '',
            'sec_ticker': '',
            'source': 'Needs manual research',
            'status': 'Not found',
            'notes': f'Research needed for {exchange}'
        }
        
        results.append(result)
    
    # Save comprehensive results
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/company_tickers_framework.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'original_name', 'document_type', 'company_number', 
                     'exchange', 'tsx_ticker', 'tsxv_ticker', 'asx_ticker', 'sec_ticker', 
                     'source', 'status', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Saved framework to: {csv_file}")
    print(f"Total companies processed: {len(results)}")
    
    # Show breakdown by exchange
    print("\nExchange breakdown:")
    exchanges = {}
    for result in results:
        if result['exchange']:
            exchanges[result['exchange']] = exchanges.get(result['exchange'], 0) + 1
    
    for exchange, count in exchanges.items():
        print(f"{exchange}: {count} companies")

if __name__ == "__main__":
    main()