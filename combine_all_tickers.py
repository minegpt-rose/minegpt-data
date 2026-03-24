#!/usr/bin/env python3
"""
Combine All Tickers

Combine results from TMX, ASX, and SEC lookups
"""

import csv

def combine_results():
    """Combine all ticker results"""
    all_results = []
    
    # Read TMX results
    try:
        with open('/dropbox/01. Asset Ownership/02. general_information/tmx_tickers.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_results.append({
                    'company_name': row['company_name'],
                    'exchange': row['exchange'],
                    'ticker': row['ticker'],
                    'source': row['source'],
                    'type': 'TMX'
                })
    except FileNotFoundError:
        print("TMX tickers file not found")
    
    # Read ASX results
    try:
        with open('/dropbox/01. Asset Ownership/02. general_information/asx_tickers.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_results.append({
                    'company_name': row['company_name'],
                    'exchange': row['exchange'],
                    'ticker': row['ticker'],
                    'source': row['source'],
                    'type': 'ASX'
                })
    except FileNotFoundError:
        print("ASX tickers file not found")
    
    # Read SEC results
    try:
        with open('/dropbox/01. Asset Ownership/02. general_information/sec_tickers.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                all_results.append({
                    'company_name': row['company_name'],
                    'exchange': row['exchange'],
                    'ticker': row['ticker'],
                    'source': row['source'],
                    'type': 'SEC'
                })
    except FileNotFoundError:
        print("SEC tickers file not found")
    
    # Save combined results
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/all_tickers_combined.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'exchange', 'ticker', 'source', 'type']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for result in all_results:
            writer.writerow(result)
    
    print(f"Saved combined results to: {csv_file}")
    print(f"Total tickers found: {len(all_results)}")
    
    # Show statistics
    found_tickers = [r for r in all_results if r['ticker'] != 'NEEDS_LOOKUP']
    print(f"Tickers successfully mapped: {len(found_tickers)}")
    print(f"Tickers needing lookup: {len(all_results) - len(found_tickers)}")
    
    # Show sample
    print("\nSample Found Tickers:")
    for result in found_tickers[:20]:
        print(f"{result['company_name']} -> {result['ticker']} ({result['exchange']})")

def main():
    """Main function"""
    print("Combining all ticker results...")
    combine_results()

if __name__ == "__main__":
    main()