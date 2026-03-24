#!/usr/bin/env python3
"""
Comprehensive Variable Analysis

Goes through EVERY variable in accurate_database_final_FL_corrected.csv
and creates meaningful relationships based on mining industry context.
"""

import csv
import re
from typing import List, Dict

def load_variable_database() -> List[Dict]:
    """Load the complete variable database"""
    variables = []
    
    try:
        with open('/dropbox/03. Knowledge Graph/accurate_database_final_FL_corrected.csv', 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                variables.append(row)
    except Exception as e:
        print(f"Error loading variable database: {e}")
        return []
    
    return variables

def analyze_variable_mining_context(variable: Dict, all_variables: List[Dict]) -> List[Dict]:
    """Analyze what a variable means in mining industry context and create relationships"""
    relationships = []
    
    table_name = variable['table_name']
    column_name = variable['column_name']
    column_type = variable['type']
    notes = variable['notes']
    column_lower = column_name.lower()
    
    # Skip report_number columns
    if 'report_number' in column_lower:
        return relationships
    
    print(f"Analyzing: {table_name}.{column_name}")
    
    # 1. Relationships to project_name (core relationship for most variables)
    if table_name != 'general_information':
        relationships.append(create_relationship(
            table_name, column_name,
            'general_information', 'project_name',
            'belongs_to_project', 'Belongs To Project'
        ))
    
    # 2. Analyze based on column name patterns (mining industry context)
    
    # Company/ownership relationships
    if any(keyword in column_lower for keyword in ['company', 'owner', 'operator', 'ticker']):
        relationships.append(create_relationship(
            table_name, column_name,
            'general_information', 'company_name',
            'owned_by', 'Owned By'
        ))
    
    # Geographic relationships
    location_mappings = {
        'country': 'country',
        'province': 'province', 
        'state': 'state',
        'region': 'region',
        'district': 'district',
        'location': 'location',
        'coordinate': 'coordinates',
        'latitude': 'coordinates',
        'longitude': 'coordinates',
        'utm': 'coordinates'
    }
    
    for keyword, target_field in location_mappings.items():
        if keyword in column_lower:
            relationships.append(create_relationship(
                table_name, column_name,
                'general_information', target_field,
                'located_in' if keyword != 'coordinate' else 'at_coordinates',
                'Located In' if keyword != 'coordinate' else 'At Coordinates'
            ))
    
    # Town relationships
    if 'town' in column_lower or 'city' in column_lower:
        relationships.append(create_relationship(
            table_name, column_name,
            'general_information', 'nearest_town',
            'near_town', 'Near Town'
        ))
    
    # Commodity relationships
    if any(keyword in column_lower for keyword in ['commodity', 'mineral', 'metal', 'ore']):
        relationships.append(create_relationship(
            table_name, column_name,
            'commodity_groups', 'commodity',
            'produces', 'Produces'
        ))
    
    # Project stage/phase
    if 'stage' in column_lower or 'phase' in column_lower:
        relationships.append(create_relationship(
            table_name, column_name,
            'project_entities', 'project_stage',
            'has_stage', 'Has Stage'
        ))
    
    # Mine type
    if any(keyword in column_lower for keyword in ['mine_type', 'mining_type', 'open_pit', 'underground']):
        relationships.append(create_relationship(
            table_name, column_name,
            'mine_entities', 'mine_type',
            'has_mine_type', 'Has Mine Type'
        ))
    
    # Deposit type
    if 'deposit_type' in column_lower:
        relationships.append(create_relationship(
            table_name, column_name,
            'deposit_types', 'deposit_type',
            'has_deposit_type', 'Has Deposit Type'
        ))
    
    # Time/year relationships
    if 'year' in column_lower:
        if 'start' in column_lower:
            relationships.append(create_relationship(
                table_name, column_name,
                'temporal_entities', 'start_year',
                'has_start_year', 'Has Start Year'
            ))
        elif 'end' in column_lower:
            relationships.append(create_relationship(
                table_name, column_name,
                'temporal_entities', 'end_year',
                'has_end_year', 'Has End Year'
            ))
    
    # Currency relationships
    if 'currency' in column_lower:
        relationships.append(create_relationship(
            table_name, column_name,
            'financial_metrics', 'currency',
            'uses_currency', 'Uses Currency'
        ))
    
    # Cost relationships
    if any(keyword in column_lower for keyword in ['cost', 'capex', 'opex', 'expenditure', 'investment']):
        relationships.append(create_relationship(
            table_name, column_name,
            'cost_metrics', 'cost_value',
            'has_cost', 'Has Cost'
        ))
    
    # Production relationships
    if any(keyword in column_lower for keyword in ['production', 'throughput', 'capacity', 'recovery']):
        relationships.append(create_relationship(
            table_name, column_name,
            'production_metrics', 'production_value',
            'has_production', 'Has Production'
        ))
    
    # Resource relationships
    if any(keyword in column_lower for keyword in ['resource', 'reserve', 'tonnage', 'grade']):
        relationships.append(create_relationship(
            table_name, column_name,
            'resource_metrics', 'resource_value',
            'has_resource', 'Has Resource'
        ))
    
    # Unit relationships
    if '_unit' in column_lower:
        base_var_name = column_name.replace('_unit', '')
        # Check if base variable exists in same table
        base_exists = any(v['table_name'] == table_name and v['column_name'] == base_var_name for v in all_variables)
        if base_exists:
            relationships.append(create_relationship(
                table_name, base_var_name,
                table_name, column_name,
                'has_unit', 'Has Unit'
            ))
    
    # Process relationships
    if any(keyword in column_lower for keyword in ['process', 'mill', 'plant', 'refinery']):
        relationships.append(create_relationship(
            table_name, column_name,
            'process_metrics', 'process_value',
            'has_process', 'Has Process'
        ))
    
    return relationships

def create_relationship(node1_table, node1_column, node2_table, node2_column, predicate, predicate_display):
    """Create a properly formatted relationship"""
    return {
        'node1_table': node1_table,
        'node1_column': node1_column,
        'node1_report_number': '',
        'node1_display': node1_column.replace('_', ' ').title(),
        'predicate': predicate,
        'predicate_display': predicate_display,
        'node2_table': node2_table,
        'node2_column': node2_column,
        'node1_report_number_copy': '',
        'node2_display': node2_column.replace('_', ' ').title(),
        'Example': f"{node1_column} — {predicate} → {node2_column}"
    }

def main():
    """Main function - analyze ALL variables"""
    print("Loading variable database...")
    variables = load_variable_database()
    
    if not variables:
        print("Failed to load variables")
        return
    
    print(f"Loaded {len(variables)} variables")
    print("\nAnalyzing mining industry context for each variable...")
    
    all_relationships = []
    
    # Process each variable
    for i, variable in enumerate(variables):
        relationships = analyze_variable_mining_context(variable, variables)
        all_relationships.extend(relationships)
        
        # Show progress
        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1} variables, {len(all_relationships)} relationships")
    
    print(f"\nTotal variables processed: {len(variables)}")
    print(f"Total relationships generated: {len(all_relationships)}")
    
    # Remove duplicates
    unique_relationships = []
    seen = set()
    
    for rel in all_relationships:
        rel_key = f"{rel['node1_table']}.{rel['node1_column']}.{rel['node2_table']}.{rel['node2_column']}.{rel['predicate']}"
        if rel_key not in seen:
            seen.add(rel_key)
            unique_relationships.append(rel)
    
    print(f"Unique relationships: {len(unique_relationships)}")
    
    # Write to CSV
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/comprehensive_edge_dictionary_complete.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in unique_relationships:
            writer.writerow(rel)
    
    print(f"Saved comprehensive edge dictionary to: {output_path}")
    
    # Show relationship type breakdown
    print("\nRelationship type breakdown:")
    rel_counts = {}
    for rel in unique_relationships:
        rel_type = rel['predicate']
        rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
    
    for rel_type, count in sorted(rel_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rel_type}: {count}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(unique_relationships[:10]):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()