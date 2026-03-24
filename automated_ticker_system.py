#!/usr/bin/env python3
"""
Automated Ticker Lookup System

Complete system to lookup tickers for all companies
"""

import csv
import re
import os

def run_ticker_lookup_system():
    """Run the complete ticker lookup system"""
    print("🚀 Starting Automated Ticker Lookup System")
    print("=" * 50)
    
    # Step 1: Extract TMX/TSX-V tickers
    print("\n1. Extracting TMX/TSX-V tickers...")
    os.system("python3 tmx_ticker_lookup.py")
    
    # Step 2: Extract ASX tickers
    print("\n2. Extracting ASX tickers...")
    os.system("python3 asx_ticker_lookup.py")
    
    # Step 3: Extract SEC tickers
    print("\n3. Extracting SEC tickers...")
    os.system("python3 sec_ticker_lookup.py")
    
    # Step 4: Combine all results
    print("\n4. Combining all ticker results...")
    os.system("python3 combine_all_tickers.py")
    
    # Step 5: Create complete database
    print("\n5. Creating complete database...")
    os.system("python3 final_ticker_database.py")
    
    print("\n✅ Ticker Lookup System Complete!")
    print("=" * 50)
    
    # Show final results
    print("\n📊 FINAL RESULTS:")
    print("-" * 30)
    
    # Count companies
    with open('/dropbox/01. Asset Ownership/02. general_information/complete_ticker_database.csv', 'r') as f:
        reader = csv.DictReader(f)
        companies = list(reader)
        
    found = len([c for c in companies if c['status'] == 'Found'])
    total = len(companies)
    
    print(f"Total companies: {total}")
    print(f"Tickers found: {found}")
    print(f"Tickers needed: {total - found}")
    print(f"Success rate: {found/total*100:.1f}%")
    
    print("\n📁 FILES CREATED:")
    print("-" * 30)
    print("• tmx_tickers.csv - TMX/TSX-V tickers")
    print("• asx_tickers.csv - ASX tickers") 
    print("• sec_tickers.csv - SEC tickers")
    print("• all_tickers_combined.csv - Combined results")
    print("• complete_ticker_database.csv - Complete database")
    
    print("\n🚀 NEXT STEPS:")
    print("-" * 30)
    print("1. Review complete_ticker_database.csv")
    print("2. Use official APIs for remaining lookups:")
    print("   • TMX: https://www.tmxmoney.com")
    print("   • ASX: https://www.asx.com.au") 
    print("   • SEC: https://www.sec.gov/edgar")
    print("3. Update database with verified tickers")

def main():
    """Main function"""
    run_ticker_lookup_system()

if __name__ == "__main__":
    main()