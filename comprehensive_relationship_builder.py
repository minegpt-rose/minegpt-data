#!/usr/bin/env python3
"""
Comprehensive Relationship Builder

Processes EVERY variable in accurate_database_final_FL_corrected.csv row by row
and creates relationships following the exact format from comprehensive_edge_dictionary_curated
"""

import csv
import re
from typing import List, Dict

def load_variable_database() -> Dict:
    """Load the complete variable database"""
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
                    'notes': notes,
                    'full_row': row  # Keep the full row for reference
                })
    except Exception as e:
        print(f"Error loading variable database: {e}")
        return {}
    
    return variables_by_table

def analyze_variable_for_relationships(variable_info: Dict, all_tables: Dict) -> List[Dict]:
    """Analyze a single variable and generate all possible relationships"""
    relationships = []
    
    table_name = variable_info['table']
    column_name = variable_info['column']
    column_type = variable_info['type']
    notes = variable_info['notes']
    
    # Skip report_number columns (handled separately)
    if column_name.lower() == 'report_number':
        return relationships
    
    column_lower = column_name.lower()
    
    # 1. Foreign key relationships
    if 'report_number' in column_lower and table_name != 'general_information':
        relationships.append(create_relationship(
            table_name, column_name, 'general_information', 'report_number',
            f'belongs_to_{table_name}', f'Belongs To {table_name.replace("_", " ").title()}'
        ))
    
    # 2. Semantic relationships based on column name patterns
    semantic_patterns = [
        # Company/Project relationships
        (r'(company|owner|operator|ticker)', 'company_entities', 'company_name', 'related_to_company', 'Related To Company'),
        (r'(project|property|mine|deposit|site)', 'project_entities', 'project_name', 'names', 'Names'),
        
        # Location relationships
        (r'(country|nation|state|province|region|district|location)', 'geographic_regions', 'region', 'located_in', 'Located In'),
        (r'(coordinate|utm|latitude|longitude|elevation)', 'geographic_regions', 'coordinates', 'geolocated_at', 'Geolocated At'),
        
        # Commodity relationships
        (r'(commodity|mineral|metal|element|ore)', 'commodity_groups', 'commodity', 'contains', 'Contains'),
        (r'(deposit|mineralization|geology|lithology)', 'deposit_types', 'deposit', 'classified_as', 'Classified As'),
        
        # Financial relationships
        (r'(cost|capex|opex|expenditure|budget|investment)', 'cost_metrics', 'cost_value', 'has_cost', 'Has Cost'),
        (r'(price|value|revenue|income|cashflow|npv|irr|profit)', 'financial_metrics', 'financial_value', 'has_value', 'Has Value'),
        
        # Temporal relationships
        (r'(date|time|period|year|month|day|schedule)', 'temporal_entities', 'time_period', 'occurs_at', 'Occurs At'),
        (r'(duration|period|timeline)', 'temporal_entities', 'duration', 'has_duration', 'Has Duration'),
        
        # Mining operations
        (r'(mine|mining|operation|production)', 'mine_entities', 'mine_name', 'operates', 'Operates'),
        (r'(drill|hole|intercept|exploration)', 'drill_entities', 'hole_id', 'intersects', 'Intersects'),
        (r'(resource|reserve|tonnage|grade)', 'resource_metrics', 'resource_value', 'quantifies', 'Quantifies'),
        (r'(process|recovery|metallurgy|extraction)', 'process_metrics', 'process_value', 'processes', 'Processes'),
        
        # Infrastructure
        (r'(infrastructure|facility|plant|mill|refinery)', 'infrastructure_entities', 'facility_name', 'has_facility', 'Has Facility'),
        (r'(equipment|machine|vehicle)', 'equipment_entities', 'equipment_name', 'uses_equipment', 'Uses Equipment'),
    ]
    
    for pattern, target_table, target_column, predicate, predicate_display in semantic_patterns:
        if re.search(pattern, column_lower):
            relationships.append(create_relationship(
                table_name, column_name, target_table, target_column,
                predicate, predicate_display
            ))
    
    # 3. Relationships based on notes/type
    if 'general_information' in notes.lower():
        relationships.append(create_relationship(
            table_name, column_name, 'general_information', 'report_number',
            'references_general_info', 'References General Info'
        ))
    
    if 'project_list' in notes.lower():
        relationships.append(create_relationship(
            table_name, column_name, 'project_entities', 'project_name',
            'references_project', 'References Project'
        ))
    
    # 4. Type-based relationships
    if 'date' in column_type.lower():
        relationships.append(create_relationship(
            table_name, column_name, 'temporal_entities', 'time_period',
            'occurs_at', 'Occurs At'
        ))
    
    if any(geo in column_type.lower() for geo in ['location', 'coordinate', 'address']):
        relationships.append(create_relationship(
            table_name, column_name, 'geographic_regions', 'coordinates',
            'located_at', 'Located At'
        ))
    
    return relationships

def create_relationship(source_table, source_column, target_table, target_column, predicate, predicate_display):
    """Create a relationship dictionary with proper formatting"""
    return {
        'node1_table': source_table,
        'node1_column': source_column,
        'node1_report_number': '',
        'node1_display': source_column.replace('_', ' ').title(),
        'predicate': predicate,
        'predicate_display': predicate_display,
        'node2_table': target_table,
        'node2_column': target_column,
        'node1_report_number_copy': '',
        'node2_display': target_column.replace('_', ' ').title(),
        'Example': f"{source_column} — {predicate} → {target_column}"
    }

def main():
    """Main function - process every variable"""
    print("Loading complete variable database...")
    variables_by_table = load_variable_database()
    
    if not variables_by_table:
        print("Failed to load variable database")
        return
    
    print(f"Loaded {len(variables_by_table)} tables")
    
    total_variables = 0
    all_relationships = []
    
    # Process every variable in every table
    for table_name, variables in variables_by_table.items():
        print(f"\nProcessing {table_name}: {len(variables)} variables")
        
        for variable in variables:
            total_variables += 1
            
            # Add table context to variable info
            variable_info = {
                'table': table_name,
                'column': variable['column'],
                'type': variable['type'],
                'notes': variable['notes']
            }
            
            # Generate relationships for this variable
            relationships = analyze_variable_for_relationships(variable_info, variables_by_table)
            all_relationships.extend(relationships)
            
            # Show progress
            if total_variables % 50 == 0:
                print(f"  Processed {total_variables} variables, {len(all_relationships)} relationships")
    
    print(f"\nTotal variables processed: {total_variables}")
    print(f"Total relationships generated: {len(all_relationships)}")
    
    # Write to CSV with exact format
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/comprehensive_edge_dictionary_complete.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in all_relationships:
            writer.writerow(rel)
    
    print(f"Saved complete edge dictionary to: {output_path}")
    
    # Show relationship type breakdown
    print("\nRelationship type breakdown:")
    rel_counts = {}
    for rel in all_relationships:
        rel_type = rel['predicate']
        rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
    
    for rel_type, count in sorted(rel_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rel_type}: {count}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(all_relationships[:10]):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()