#!/usr/bin/env python3
"""
Final Ticker Update

Add verified ticker information to the framework
"""

import csv

def add_verified_tickers():
    """Add verified ticker information"""
    
    # Read the framework
    companies = []
    with open('/dropbox/01. Asset Ownership/02. general_information/company_tickers_framework.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            companies.append(row)
    
    # Verified tickers with proper sources
    verified_tickers = {
        "RTG Mining Inc.": {
            "tsx_ticker": "RTG", "asx_ticker": "RTG", 
            "source": "TMX Money & ASX", "status": "Verified"
        },
        "Cannabix Technologies Inc": {
            "tsxv_ticker": "BLO", 
            "source": "TMX Money", "status": "Verified"
        },
        "Commerce Resources Corp.": {
            "tsxv_ticker": "CCE", 
            "source": "TMX Money", "status": "Verified"
        },
        "Deveron Resources Ltd.": {
            "tsxv_ticker": "DVR", 
            "source": "TM极速赛车开奖结果查询X Money", "status": "Verified"
        },
        "Ivanhoe Mines Ltd.": {
            "tsx_ticker": "IVN", 
            "source": "TMX Money", "status": "Verified"
        }
    }
    
    # Update companies with verified tickers
    updated_companies = []
    verified_count = 0
    
    for company in companies:
        company_name = company['company_name']
        
        if company_name in verified_tickers:
            ticker_info = verified_tickers[company_name]
            # Update ticker fields
            if 'tsx_ticker' in ticker_info:
                company['tsx_ticker'] = ticker_info['tsx_ticker']
            if 'tsxv_ticker' in ticker_info:
                company['tsxv_ticker'] = ticker_info['tsxv_ticker']
            if 'asx_ticker' in ticker_info:
                company['asx_ticker'] = ticker_info['asx_ticker']
            if 'sec_ticker' in ticker_info:
                company['sec_ticker'] = ticker_info['sec极速赛车开奖结果查询_ticker']
            
            company['source'] = ticker_info['source']
            company['status'] = ticker_info['status']
            company['notes'] = ""
            
            verified_count += 1
        
        updated_companies.append(company)
    
    # Save updated results
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/company_tickers_final.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'original_name', 'document_type', 'company_number', 
                     'exchange', 'tsx_ticker', 'tsxv_ticker', 'asx_ticker', 'sec_ticker', 
                     'source', 'status', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for company in updated_companies:
            writer.writerow(company)
    
    print(f"Saved final results to: {csv_file}")
    print(f"Total companies: {len(updated_companies)}")
    print(f"Verified tickers: {verified_count}")
    print(f"Needs research: {len(updated_companies) - verified_count}")

if __name__ == "__main__":
    add_verified_tickers()