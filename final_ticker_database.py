#!/usr/bin/env python3
"""
Final Ticker Database

Create complete database with all companies and their tickers
"""

import csv
import re

def create_complete_database():
    """Create complete database with all companies"""
    all_companies = []
    
    # Read original general_information
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
                
                if clean_name:
                    all_companies.append({
                        'company_name': clean_name,
                        'original_name': company_name,
                        'document_type': document_type,
                        'company_number': company_number
                    })
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return []
    
    # Read ticker mappings
    ticker_mappings = {}
    try:
        with open('/dropbox/01. Asset Ownership/02. general_information/all_tickers_combined.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                ticker_mappings[row['company_name']] = {
                    'ticker': row['ticker'],
                    'exchange': row['exchange'],
                    'source': row['source']
                }
    except FileNotFoundError:
        print("Tickers file not found")
    
    # Create final database
    final_database = []
    
    for company in all_companies:
        ticker_info = ticker_mappings.get(company['company_name'], {})
        
        final_database.append({
            'company_name': company['company_name'],
            'original_name': company['original_name'],
            'document_type': company['document_type'],
            'company_number': company['company_number'],
            'ticker': ticker_info.get('ticker', 'NEEDS_LOOKUP'),
            'exchange': ticker_info.get('exchange', ''),
            'source': ticker_info.get('source', 'Needs research'),
            'status': 'Found' if ticker_info.get('ticker') and ticker_info['ticker'] != 'NEEDS_LOOKUP' else 'Needs lookup'
        })
    
    # Save final database
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/complete_ticker_database.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'original_name', 'document_type', 'company_number', 
                     'ticker', 'exchange', 'source', 'status']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for company in final_database:
            writer.writerow(company)
    
    print(f"Saved complete database to: {csv_file}")
    print(f"Total companies: {len(final_database)}")
    
    # Show statistics
    found_count = len([c for c in final_database if c['status'] == 'Found'])
    needs_lookup = len(final_database) - found_count
    
    print(f"Tickers found: {found_count}")
    print(f"Tickers needing lookup: {needs_lookup}")
    print(f"Success rate: {found_count/len(final_database)*100:.1f}%")
    
    # Show sample
    print("\nSample Found Tickers:")
    found_companies = [c for c in final_database if c['status'] == 'Found']
    for company in found_companies[:10]:
        print(f"{company['company_name']} -> {company['ticker']} ({company['exchange']})")

def main():
    """Main function"""
    print("Creating complete ticker database...")
    create_complete_database()

if __name__ == "__main__":
    main()