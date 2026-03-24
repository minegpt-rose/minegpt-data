#!/usr/bin/env python3
"""
Refined Relationship Analyzer

Creates meaningful, logical relationships following Francisca's exact approach.
Focuses on quality over quantity.
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

def create_core_relationships():
    """Create core logical relationships following Francisca's examples"""
    relationships = []
    
    # 1. Project ownership relationships (from your examples)
    relationships.extend([
        create_relationship('general_information', 'project_name', 'general_information', 'company_name', 'owned_by', 'Owned By'),
        create_relationship('general_information', 'project_name', 'general_information', 'country', 'located_in', 'Located In'),
        create_relationship('general_information', 'project_name', 'general_information', 'province', 'located_in', 'Located In'),
        create_relationship('general_information', 'project_name', 'general_information', 'district', 'located_in', 'Located In'),
        create_relationship('general_information', 'project_name', 'general_information', 'state', 'located_in', 'Located In'),
        create_relationship('general_information', 'project_name', 'general_information', 'region', 'located_in', 'Located In'),
    ])
    
    # 2. Cost table relationships (logical contributions)
    relationships.extend([
        # Direct capex components contribute to total direct capex
        create_relationship('cost_table', 'mining_and_development_initial_direct_capex', 'cost_table', 'total_initial_direct_capex', 'contributes_to', 'Contributes To'),
        create_relationship('cost_table', 'process_plant_initial_direct_capex', 'cost_table', 'total_initial_direct_capex', 'contributes_to', 'Contributes To'),
        create_relationship('cost_table', 'tailings_initial_direct_capex', 'cost_table', 'total_initial_direct_capex', 'contributes_to', 'Contributes To'),
        create_relationship('cost_table', 'infrastructure_initial_direct_capex', 'cost_table', 'total_initial_direct_capex', 'contributes_to', 'Contributes To'),
        
        # Units belong to their values
        create_relationship('cost_table', 'total_initial_direct_capex', 'cost_table', 'total_initial_direct_capex_unit', 'has_unit', 'Has Unit'),
        create_relationship('cost_table', 'total_initial_indirect_capex', 'cost_table', 'total_initial_indirect_capex_unit', 'has_unit', 'Has Unit'),
        create_relationship('cost_table', 'total_sustaining_capex', 'cost_table', 'total_sustaining_capex_unit', 'has_unit', 'Has Unit'),
        create_relationship('cost_table', 'mining_and_development_initial_direct_capex', 'cost_table', 'mining_and_development_initial_direct_capex_unit', 'has_unit', 'Has Unit'),
        create_relationship('core_table', 'process_plant_initial_direct_capex', 'cost_table', 'process_plant_initial_direct_capex_unit', 'has_unit', 'Has Unit'),
    ])
    
    # 3. Process parameter relationships
    relationships.extend([
        create_relationship('process_parameters', 'throughput', 'process_parameters', 'throughput_unit', 'has_unit', 'Has Unit'),
        create_relationship('process_parameters', 'recovery_rate', 'process_parameters', 'recovery_rate_unit', 'has_unit', 'Has Unit'),
        create_relationship('process_parameters', 'grind_size', 'process_parameters', 'grind_size_unit', 'has_unit', 'Has Unit'),
    ])
    
    # 4. Resource table relationships
    relationships.extend([
        create_relationship('resource_table', 'total_tonnage', 'resource_table', 'total_tonnage_unit', 'has_unit', 'Has Unit'),
        create_relationship('resource_table', 'average_grade', 'resource_table', 'average_grade_unit', 'has_unit', 'Has Unit'),
    ])
    
    # 5. Financial relationships
    relationships.extend([
        create_relationship('financial_table', 'npv', 'financial_table', 'npv_unit', 'has_unit', 'Has Unit'),
        create_relationship('financial_table', 'irr', 'financial_table', 'irr_unit', 'has_unit', 'Has Unit'),
    ])
    
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
    print("Creating refined logical relationships...")
    
    relationships = create_core_relationships()
    
    print(f"Generated {len(relationships)} meaningful relationships")
    
    # Write to CSV
    csv_headers = [
        'node1_table', 'node1_column', 'node1_report_number', 'node1_display',
        'predicate', 'predicate_display', 'node2_table', 'node2_column',
        'node1_report_number_copy', 'node2_display', 'Example'
    ]
    
    output_path = '/dropbox/03. Knowledge Graph/refined_relationships.csv'
    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
        writer.writeheader()
        
        for rel in relationships:
            writer.writerow(rel)
    
    print(f"Saved refined relationships to: {output_path}")
    
    print("\nSample relationships:")
    for i, rel in enumerate(relationships[:15]):
        print(f"  {i+1}. {rel['node1_table']}.{rel['node1_column']} -> {rel['node2_table']}.{rel['node2_column']} ({rel['predicate']})")

if __name__ == "__main__":
    main()