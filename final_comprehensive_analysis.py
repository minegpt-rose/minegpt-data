#!/usr/bin/env python3
"""
Final Comprehensive Analysis

Creates meaningful relationships while avoiding self-references and duplicates.
"""

import csv

def load_variable_database():
    """Load the variable database"""
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

def analyze_variable_mining_context(variable, all_variables):
    """Analyze variable with mining context, avoiding self-references"""
    relationships = []
    
    table_name = variable['table_name']
    column_name = variable['column_name']
    column_lower = column_name.lower()
    
    # Skip report_number columns
    if 'report_number' in column_lower:
        return relationships
    
    # 1. Relationships to project_name (avoid self-reference)
    if table_name != 'general_information' and column_name != 'project_name':
        relationships.append(create_relationship(
            table_name, column_name,
            'general_information', 'project_name',
            'belongs_to_project', 'Belongs To Project'
        ))
    
    # 2. Company relationships (avoid self-reference)
    if any(keyword in column_lower for keyword in ['company', 'owner', 'operator', 'ticker']) and column_name != 'company_name':
        relationships.append(create_relationship(
            table_name, column_name,
            'general_information', 'company_name',
            'owned_by', 'Owned By'
        ))
    
    # 3. Geographic relationships (avoid self-reference)
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
        if keyword in column_lower and column_name != target_field:
            relationships.append(create_relationship(
                table_name, column_name,
                'general_information', target_field,
                'located_in' if keyword != 'coordinate' else 'at_coordinates',
                'Located In' if keyword != 'coordinate' else 'At Coordinates'
            ))
    
    # 4. Other relationships (avoid self-reference)
    relationship_patterns = [
        # Town relationships
        (['town', 'city'], 'nearest_town', 'near_town', 'Near Town'),
        # Commodity relationships
        (['commodity', 'mineral', 'metal', 'ore'], 'commodity', 'produces', 'Produces'),
        # Project stage
        (['stage', 'phase'], 'project_stage', 'has_stage', 'Has Stage'),
        # Mine type
        (['mine_type', 'mining_type', 'open_pit', 'underground'], 'mine_type', 'has_mine_type', 'Has Mine Type'),
        # Deposit type
        (['deposit_type'], 'deposit_type', 'has_deposit_type', 'Has Deposit Type'),
        # Currency
        (['currency'], 'currency', 'uses_currency', 'Uses Currency'),
        # Cost
        (['cost', 'capex', 'opex', 'expenditure', 'investment'], 'cost_value', 'has_cost', 'Has Cost'),
        # Production
        (['production', 'throughput', 'capacity', 'recovery'], 'production_value', 'has_production', 'Has Production'),
        # Resource
        (['resource', 'reserve', 'tonnage', 'grade'], 'resource_value', 'has_resource', 'Has Resource'),
        # Process
        (['process', 'mill', 'plant', 'refinery'], 'process_value', 'has_process', 'Has Process')
    ]
    
    for keywords, target_field, predicate, predicate_display in relationship_patterns:
        if any(keyword in column_lower for keyword in keywords) and column_name != target_field:
            relationships.append(create_relationship(
                table_name, column_name,
                f"{target_field.split('_')[0]}_metrics" if '_value' in target_field else f"{target_field.split('_')[0]}_entities",
                target_field,
                predicate, predicate_display
            ))
    
    # 5. Unit relationships (special case)
    if '_unit' in column_lower:
        base_var_name = column_name.replace('_unit', '')
        base_exists = any(v['table_name'] == table_name and v['column_name'] == base_var_name for v in all_variables)
        if base_exists and column_name != base_var_name:
            relationships.append(create_relationship(
                table_name, base_var_name,
                table_name, column_name,
                'has_unit', 'Has Unit'
            ))
    
    # 6. Year relationships
    if 'year' in column_lower and column_name not in ['start_year', 'end_year']:
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
    """Main function"""
    print("Loading variable database...")
    variables = load_variable_database()
    
    if not variables:
        print("Failed to load variables")
        return
    
    print(f"Loaded {len(variables)} variables")
    print("\nAnalyzing mining industry context...")
    
    all_relationships = []
    
    # Process each variable
    for i, variable in enumerate(variables):
        relationships = analyze_variable_mining_context(variable, variables)
        all_relationships.extend(relationships)
        
        if (i + 1) % 50 == 0:
            print(f"Processed {i + 1} variables, {len(all_relationships)} relationships")
    
    print(f"\nTotal relationships before deduplication: {len(all_relationships)}")
    
    # Remove duplicates and self-references
    unique_relationships = []
    seen = set()
    
    for rel in all_relationships:
        # Skip relationships where node1 == node2
        if rel['node1_table'] == rel['node2_table'] and rel['node1_column'] == rel['node2_column']:
            continue
        
        rel_key = f"{rel['node1_table']}.{rel['node1_column']}.{rel['node2_table']}.{rel['node2_column']}.{rel['predicate']}"
        if rel_key not in seen:
            seen.add(rel_key)
            unique_relationships.append(rel)
    
    print(f"Final unique relationships: {len(unique_relationships)}")
    
    # Write to CSV
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/final_comprehensive_edge_dictionary.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in unique_relationships:
            writer.writerow(rel)
    
    print(f"Saved final comprehensive edge dictionary to: {output_path}")
    
    # Show relationship type breakdown
    print("\nRelationship type breakdown:")
    rel_counts = {}
    for rel in unique_relationships:
        rel_type = rel['predicate']
        rel_counts[rel_type] = rel_counts.get(rel_type, 0) + 1
    
    for rel_type, count in sorted(rel_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"  {rel_type}: {count}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(unique_relationships[:15]):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()