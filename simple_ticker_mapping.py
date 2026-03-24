#!/usr/bin/env python3
"""
Simple Ticker Mapping

Create a direct mapping from company numbers to tickers using known patterns
"""

import csv
import re

def extract_companies():
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

def get_ticker_from_number(company_number, document_type):
    """Get ticker from company number based on document type"""
    # Known mappings - these would be expanded with actual API calls
    known_mappings = {
        # SEDAR numbers (NI 43-101)
        "000034365": {"ticker": "RTG", "exchange": "TSX", "source": "TMX"},
        "000034382": {"ticker": "BLO", "exchange": "TSXV", "source": "TMX"},
        "000016212": {"ticker": "CCE", "exchange": "TSXV", "source": "TMX"},
        "000032995": {"ticker": "DVR", "exchange": "TSXV", "source": "TMX"},
        "000033595": {"ticker": "IVN", "exchange": "TSX", "source": "TMX"},
        
        # Add more known mappings here
    }
    
    if company_number in known_mappings:
        return known_mappings[company_number]
    
    return None

def main():
    """Main function"""
    print("Extracting companies...")
    companies = extract_companies()
    
    print(f"Found {len(companies)} companies")
    
    results = []
    found_count = 0
    
    for company in companies:
        ticker_info = None
        
        if company['company_number']:
            ticker_info = get_ticker_from_number(company['company_number'], company['document_type'])
        
        if ticker_info:
            result = {
                'company_name': company['clean_name'],
                'original_name': company['original_name'],
                'document_type': company['document_type'],
                'company_number': company['company_number'],
                'exchange': ticker_info['exchange'],
                'ticker': ticker_info['ticker'],
                'source': ticker_info['source'],
                'status': 'Found'
            }
            found_count += 1
        else:
            result = {
                'company_name': company['clean_name'],
                'original_name': company['original_name'],
                'document_type': company['document_type'],
                'company_number': company['company_number'],
                'exchange': '',
                'ticker': '',
                'source': 'Needs lookup',
                'status': 'Not found'
            }
        
        results.append(result)
    
    # Save results
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/simple_ticker_mapping.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'original_name', 'document_type', 'company_number', 
                     'exchange', 'ticker', 'source', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Saved results to: {csv_file}")
    print(f"Total companies: {len(results)}")
    print(f"Tickers found: {found_count}")
    print(f"Need lookup: {len(results) - found_count}")
    
    # Show companies with numbers
    companies_with_numbers = [c for c in companies if c['company_number']]
    print(f"\nCompanies with numbers: {len(companies_with_numbers)}")
    
    for company in companies_with_numbers[:10]:
        print(f"{company['clean_name']} -> {company['company_number']}")

if __name__ == "__main__":
    main()