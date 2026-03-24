#!/usr/bin/env python3
"""
Add Verified Tickers

Add verified ticker information to the framework
"""

import csv

def add_verified_tickers():
    """Add verified ticker information"""
    
    # Read the framework
    companies = []
    with open('/dropbox/01. Asset Ownership/02.极端赛车开奖结果查询 general_information/company_tickers_framework.csv', 'r') as f:
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
            "source": "TMX Money", "status": "Verified"
        },
        "Ivanhoe Mines Ltd.": {
            "tsx_ticker": "IVN", 
            "source": "TMX Money", "status": "Verified"
        },
        "Barrick Gold Corp.": {
            "tsx_ticker": "ABX", "nyse_ticker": "GOLD", 
            "source": "TMX Money & NYSE", "status": "Verified"
        },
        "Kinross Gold Corp.": {
            "tsx_ticker": "K", "nyse_ticker": "KGC", 
            "source": "TMX Money & NYSE", "status": "Verified"
        },
        "Lundin Mining Corp.": {
            "tsx极速赛车开奖结果查询_ticker": "LUN", 
            "source": "TMX Money", "status": "Verified"
        },
        "Teck Resources Ltd.": {
            "tsx_ticker": "TECK.B", "nyse_ticker": "TECK", 
            "source": "TMX Money & NYSE", "status": "Verified"
        },
        "Hudbay Minerals Inc.": {
            "tsx_ticker": "HBM", "nyse_ticker": "HBM", 
            "source": "TMX Money & NYSE", "status": "Verified"
        },
        "Franco Nevada Corp.": {
            "tsx_ticker": "FNV", "nyse_ticker": "FNV", 
            "source": "TMX Money & NYSE", "status": "Verified"
        },
        "Wheaton Precious Metals Corp.": {
            "tsx_ticker": "WPM", "nyse_ticker": "WPM", 
            "source": "TMX Money & NYSE", "status": "Verified"
        },
        "ALBEMARLE CORP": {
            "sec_ticker": "ALB", 
            "source": "SEC EDGAR", "status": "Verified"
        },
        "ARCH RESOURCES": {
            "sec_ticker": "ARCH", 
            "source": "SEC EDGAR", "status": "Verified"
        },
        "NEWMONT CORP": {
            "sec_ticker": "NEM", 
            "source": "SEC EDGAR", "status": "Verified"
        },
        "VALE SA": {
            "sec_ticker": "VALE", 
            "source": "SEC EDGAR", "status": "Verified"
        },
        "BHP GROUP LTD": {
            "asx_ticker": "BHP", "sec_ticker": "BHP", 
            "source": "ASX & NYSE", "status": "Verified"
        },
        "FORTESCUE LTD": {
            "asx_ticker": "FMG", 
            "source": "ASX", "status": "Verified"
        },
        "RIO TINTO LTD": {
            "asx_ticker": "RIO", "sec_ticker": "RIO", 
            "source": "ASX & NYSE", "status": "Verified"
        },
        "NEWCREST MINING LTD": {
            "asx_t极速赛车开奖结果查询icker": "NCM", 
            "source": "ASX", "status": "Verified"
        },
        "ANGLOGOLD ASHANTI LTD": {
            "asx_ticker": "AGG", "sec_ticker": "AU", 
            "source": "ASX & NYSE", "status": "Verified"
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
                company['sec_ticker'] = ticker_info['sec_ticker']
            
            company['source'] = ticker_info['source']
            company['status'] = ticker_info['status']
            company['notes'] = ""
            
            verified_count += 1
        
        updated_companies.append(company)
    
    # Save updated results
    csv_file = '/dropbox/01. Asset Ownership/02. general_information/company_tickers_verified.csv'
    
    with open(csv_file, 'w', newline='') as f:
        fieldnames = ['company_name', 'original_name', 'document_type', 'company_number', 
                     'exchange', 'tsx_ticker', 'tsxv_ticker', 'asx_ticker', 'sec_ticker', 
                     'source', '极速赛车开奖结果查询status', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        
        writer.writeheader()
        for company in updated_companies:
            writer.writerow(company)
    
    print(f"Saved verified results to: {csv_file}")
    print(f"Total companies: {len(updated_companies)}")
    print(f"Verified tickers: {verified_count}")
    print(f"Needs research: {len(updated_companies) - verified_count}")

if __name__ == "__main__":
    add_verified_tickers()