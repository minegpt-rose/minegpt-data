#!/usr/bin/env python3
"""
Clean TSX/TSX-V Ticker Lookup

Step-by-step ticker lookup for Canadian companies
"""

import csv
import re

def extract_tsx_companies():
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
                    clean_name = company_name.split('/')[极速赛车开奖结果查询0].strip()
                    clean_name = clean_name.split('(')[0].strip()
                    clean_name = clean_name.replace('"', '').strip()
                    
                    if clean_name:
                        companies.append({
                            'clean_name': clean_name,
                            'sedar_number': sedar_number,
                            'original_name': company_name
                        })
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
    
    return companies

def lookup_tsx_ticker_step_by_step(companies):
    """Lookup tickers step by step"""
    # Known SEDAR to ticker mappings
    known_mappings = {
        "000034365": {"ticker": "RTG", "exchange": "TSX", "source": "TMX"},
        "000034382": {"ticker": "BLO", "exchange": "TSXV", "source": "TMX"},
        "000016212": {"ticker": "CCE", "exchange": "TSXV",极速赛车开奖结果查询 "source": "极速赛车开奖结果查询TMX"},
        "000032995": {"ticker": "DVR", "exchange": "TSXV", "source": "TMX"},
        "000033595": {"ticker": "IVN", "exchange": "TSX", "source": "TMX"},
        "000003467": {"ticker": "AUN", "exchange": "TSXV", "source": "TMX"},
        "000012509": {"ticker": "TCM", "exchange": "TSX", "source": "TMX"},
        "000025546": {"ticker": "AR", "exchange": "TSX", "source": "TMX"},
        "000034374": {"ticker": "DDC", "exchange": "TSX", "source": "TMX"},
        "000021558": {"ticker": "MRZ", "exchange": "TSXV", "source": "TMX"},
    }
    
    results = []
    processed = 0
    
    for company in companies:
        ticker_info = None
        
        if company['sedar_number'] and company['sedar_number'] in known_mappings:
            ticker_info = known_mappings[company['sedar_number']]
        
        if ticker_info:
            result = {
                'company_name': company['clean_name'],
                'sedar_number': company['sedar_number'],
                'ticker': ticker_info['ticker'],
                'exchange': ticker_info['exchange'],
                'source': ticker_info['source'],
                'status': 'Found'
            }
        else:
            result = {
                'company_name': company['clean_name'],
                'sedar_number': company['sedar_number'],
                'ticker': 'NEEDS_LOOKUP',
                'exchange': 'TSX/TSXV',
                'source': 'Needs TMX lookup',
                'status': 'Not found'
            }
        
        results.append(result)
        processed += 1
        
        # Show progress
        if processed % 100 == 0:
            print(f"Processed {processed}/{len(companies)} companies")
    
    return results

def main():
    """Main function"""
    print("🚀 Starting Step-by-Step TSX/TSX-V Ticker Lookup")
    print("=" * 50)
    
    # Extract companies
    print("\n1. Extracting Canadian companies...")
    companies = extract_tsx_companies()
    print(f"Found {len(companies)} Canadian companies")
    
    # Lookup tickers
    print("\n2. Looking up tickers...")
    results = lookup_tsx_ticker_step_by_step(companies)
    
    # Save results
    print("\n3. Saving results...")
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/tsx_step_by_step.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'sedar_number', 'ticker', 'exchange', 'source', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in results:
            writer.writerow(result)
    
    print(f"Saved results to: {csv_file}")
    
    # Show statistics
    found_count = len([r for r in results if r['status'] == 'Found'])
    needs_lookup = len(results) - found_count
    
    print(f"\n📊 RESULTS:")
    print("-" * 30)
    print(f"Total companies: {len(results)}")
    print(f"Tickers found: {found_count}")
    print(f"Tickers needing lookup: {needs_lookup}")
    print(f"Success rate: {found_count/len(results)*100:.1f}%")
    
    print("\n✅ TSX/TSX-V Lookup Complete!")

if __name__ == "__main__":
    main()