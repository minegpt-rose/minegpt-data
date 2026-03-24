#!/usr/bin/env python3
"""
Create Comprehensive Edge Dictionary

Creates edge relationships following the exact format from comprehensive_edge_dictionary_curated.xlsx
"""

import csv
import re

def load_variable_database():
    """Load the accurate_database_final_FL_corrected.csv"""
    variables_by_table = {}
    
    try:
        with open('/dropbox/03. Knowledge Graph/accurate_database_final_FL_corrected.csv', 'r') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                table = row['table_name']
                column = row['column_name']
                notes = row['notes']
                
                if table not in variables_by_table:
                    variables_by_table[table] = []
                
                variables_by_table[table].append({
                    'column': column,
                    'type': row.get('type', ''),
                    'notes': notes
                })
    except Exception as e:
        print(f"Error loading variable database: {e}")
        return {}
    
    return variables_by_table

def generate_relationships(variables_by_table):
    """Generate relationships following the exact format"""
    relationships = []
    
    # Get variables from general_information
    general_info_vars = variables_by_table.get('general_information', [])
    
    # Relationship patterns based on mining industry
    relationship_patterns = [
        # Company relationships
        (r'(company|owner|operator)', 'owned_by', 'company_entities', 'company_name'),
        (r'(project|property|mine|deposit)', 'names', 'project_entities', 'project_name'),
        
        # Location relationships  
        (r'(country|nation|state|province|region|district)', 'located_in', 'geographic_regions', 'region'),
        (r'(location|coordinate|utm|latitude|longitude)', 'geolocated_at', 'geographic_regions', 'coordinates'),
        
        # Commodity relationships
        (r'(commodity|mineral|metal|element)', 'contains', 'commodity_groups', 'commodity'),
        (r'(deposit|mineralization|geology)', 'classified_as', 'deposit_types', 'deposit'),
        
        # Financial relationships
        (r'(cost|capex|opex|expenditure|budget)', 'has_cost', 'cost_metrics', 'cost_value'),
        (r'(price|value|revenue|cashflow|npv|irr)', 'has_value', 'financial_metrics', 'financial_value'),
        
        # Temporal relationships
        (r'(date|time|period|year|month|day)', 'occurs_at', 'temporal_entities', 'time_period'),
        (r'(schedule|timeline|duration)', 'has_duration', 'temporal_entities', 'duration'),
        
        # Mining relationships
        (r'(mine|mining|operation|production)', 'operates', 'mine_entities', 'mine_name'),
        (r'(drill|hole|intercept|exploration)', 'intersects', 'drill_entities', 'hole_id'),
        (r'(resource|reserve|tonnage|grade)', 'quantifies', 'resource_metrics', 'resource_value'),
        (r'(process|recovery|metallurgy|extraction)', 'processes', 'process_metrics', 'process_value'),
    ]
    
    # Create relationships for each general_information variable
    for source_var in general_info_vars:
        source_column = source_var['column']
        
        # Skip report_number (handled separately)
        if source_column.lower() == 'report_number':
            continue
            
        # Analyze source variable name
        source_var_lower = source_column.lower()
        
        # Find matching patterns for this source variable
        for pattern, rel_type, target_table, target_column in relationship_patterns:
            if re.search(pattern, source_var_lower):
                # Create relationship with proper display names
                relationships.append({
                    'node1_table': 'general_information',
                    'node1_column': source_column,
                    'node1_report_number': '',
                    'node1_display': source_column.replace('_', ' ').title(),
                    'predicate': rel_type,
                    'predicate_display': rel_type.replace('_', ' ').title(),
                    'node2_table': target_table,
                    'node2_column': target_column,
                    'node1_report_number_copy': '',
                    'node2_display': target_column.replace('_', ' ').title(),
                    'Example': f"{source_column} — {rel_type} → {target_column}"
                })
    
    # Add table-level relationships
    for table_name in variables_by_table.keys():
        if table_name != 'general_information':
            relationships.append({
                'node1_table': 'general_information',
                'node1_column': 'report_number',
                'node1_report_number': '',
                'node1_display': 'Report Number',
                'predicate': f'has_{table_name.lower()}',
                'predicate_display': f'Has {table_name.replace("_", " ").title()}',
                'node2_table': table_name,
                'node2_column': 'report_number',
                'node1_report_number_copy': '',
                'node2_display': f'{table_name.replace("_", " ").title()} Report Number',
                'Example': f"report_number — has_{table_name.lower()} → {table_name}.report_number"
            })
    
    return relationships

def main():
    """Main function"""
    print("Loading variable database...")
    variables_by_table = load_variable_database()
    
    if not variables_by_table:
        print("Failed to load variable database")
        return
    
    print(f"Loaded {len(variables_by_table)} tables")
    total_vars = sum(len(vars) for vars in variables_by_table.values())
    print(f"Total variables: {total_vars}")
    
    print("\nGenerating relationships...")
    relationships = generate_relationships(variables_by_table)
    
    print(f"Generated {len(relationships)} relationships")
    
    # Write to CSV with exact format
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/comprehensive_edge_dictionary_curated.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in relationships:
            writer.writerow(rel)
    
    print(f"Saved to {output_path}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(relationships[:5]):
        print(f"  {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()