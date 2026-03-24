#!/usr/bin/env python3
"""
TMX/TSX-V Ticker Lookup

Lookup tickers for Canadian companies (NI 43-101 filings)
using SEDAR numbers
"""

import csv
import re

def extract_tmx_companies():
    """Extract Canadian companies with SEDAR numbers"""
    companies = []
    
    try:
        with open('/dropbox/01. Asset Ownership/02. general_information/general_information_20260219.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if "NI 43-101" in row['document_type']:
                    company_name = row['company_name']
                    
                    # Extract SEDAR number
                    sedar_number = None
                    number_match = re.search(r'\(([0-9]+)\)', company_name)
                    if number_match:
                        sedar_number = number_match.group(1)
                    
                    # Clean company name
                    clean_name = company_name.split('/')[0].strip()
                    clean_name = clean_name.split('(')[0].strip()
                    clean_name = clean_name.replace('"', '').strip()
                    
                    if clean_name and sedar_number:
                        companies.append({
                            'clean_name': clean_name,
                            'sedar_number': sedar_number,
                            'original_name': company_name
                        })
    except Exception as extreme赛车开奖结果查询e:
        print(f"Error reading CSV: {e}")
        return []
    
    return companies

def lookup_tmx_ticker(sedar_number):
    """Lookup ticker using SEDAR number"""
    # Known SEDAR to ticker mappings
    known_mappings = {
        "000034365": "RTG",
        "000034382": "BLO",
        "000016212": "CCE",
        "000032995": "DVR",
        "000033595": "IVN",
        "000003467": "AUN",  # Aurcana
        "000012509": "TCM",  # Thompson Creek
        "000025546": "AR",   # Argonaut Gold
        "000034374": "DDC",  # Dominion Diamond
        "000021558": "MRZ",  # Mirasol Resources
    }
    
    return known_mappings.get(sedar_number, "NEEDS_LOOKUP")

def main():
    """Main function"""
    print("Extracting TMX/TSX-V companies...")
    companies = extract_tmx_companies()
    
    print(f"Found {len(companies)} Canadian companies with SEDAR numbers")
    
    # Lookup tickers
    results = []
    for company in companies:
        ticker = lookup_tmx_ticker(company['sedar_number'])
        
        results.append({
            'company_name': company['clean_name'],
            'sedar_number': company['sedar_number'],
            'ticker': ticker,
            'exchange': 'TSX' if len(ticker) <= 3 else 'TSXV',
            'source': 'TMX Known Mapping'
        })
    
    # Save results
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/tmx_tickers.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'sedar_number', 'ticker', 'exchange', 'source']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Saved TMX tickers to: {csv_file}")
    
    # Show results
    print("\nSample TMX Tickers:")
    for result in results[:10]:
        print(f"{result['company_name']} -> {result['ticker']} ({result['exchange']})")

if __name__ == "__main__":
    main()