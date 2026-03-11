
# MineGPT Alias Resolver
# Comprehensive entity resolution system

import pandas as pd
import re
from typing import Dict, List, Optional

class AliasResolver:
    def __init__(self):
        self.alias_tables = {
            'company': self._load_company_aliases(),
            'commodity': self._load_commodity_aliases(),
            'location': self._load_location_aliases(),
            'project': self._load_project_aliases(),
            'mineral': self._load_mineral_aliases()
        }
    
    def _load_company_aliases(self) -> Dict[str, str]:
        # Top 200 mining companies + tickers/abbreviations
        return {
            'BHP': 'BHP Group',
            'RIO': 'Rio Tinto',
            'FCX': 'Freeport-McMoRan',
            'NEM': 'Newmont Corporation',
            'GOLD': 'Barrick Gold',
            'AEM': 'Agnico Eagle Mines',
            'FNV': 'Franco-Nevada',
            'WPM': 'Wheaton Precious Metals',
            'SCCO': 'Southern Copper',
            'VALE': 'Vale SA',
            'BHP Group': 'BHP',
            'Rio Tinto': 'RIO',
            'Freeport-McMoRan': 'FCX',
            'Newmont': 'NEM',
            'Barrick Gold': 'GOLD'
        }
    
    def _load_commodity_aliases(self) -> Dict[str, str]:
        # Commodity groupings from MineGPT SOW 6.3.4
        return {
            'Au': 'Gold',
            'gold': 'Gold',
            'Cu': 'Copper',
            'copper': 'Copper',
            'Ag': 'Silver',
            'silver': 'Silver',
            'Pb': 'Lead',
            'lead': 'Lead',
            'Zn': 'Zinc',
            'zinc': 'Zinc',
            'Ni': 'Nickel',
            'nickel': 'Nickel'
        }
    
    def _load_location_aliases(self) -> Dict[str, str]:
        # Geographic aliases from MineGPT SOW 6.3.2/6.3.3
        return {
            'USA': 'United States',
            'US': 'United States',
            'U.S.': 'United States',
            'UK': 'United Kingdom',
            'U.K.': 'United Kingdom',
            'CA': 'Canada',
            'AU': 'Australia',
            'NZ': 'New Zealand'
        }
    
    def _load_project_aliases(self) -> Dict[str, str]:
        # Project name normalization
        return {
            'cote gold': 'Côté Gold',
            'cote': 'Côté',
            'escondida': 'Minera Escondida'
        }
    
    def _load_mineral_aliases(self) -> Dict[str, str]:
        # Mineral name normalization
        return {
            'CuEq': 'Copper Equivalent',
            'AuEq': 'Gold Equivalent',
            'spodumene': 'Lithium'
        }
    
    def resolve(self, entity_type: str, value: str) -> Optional[str]:
        # Resolve entity to canonical form
        if entity_type not in self.alias_tables:
            return value
        
        # Check exact match first
        if value in self.alias_tables[entity_type]:
            return self.alias_tables[entity_type][value]
        
        # Case-insensitive match
        value_lower = value.lower()
        for alias, canonical in self.alias_tables[entity_type].items():
            if alias.lower() == value_lower:
                return canonical
        
        # Partial match (for company names)
        if entity_type == 'company':
            for alias, canonical in self.alias_tables[entity_type].items():
                if alias.lower() in value_lower or value_lower in alias.lower():
                    return canonical
        
        return value
    
    def batch_resolve(self, entity_type: str, values: List[str]) -> List[str]:
        # Resolve multiple values
        return [self.resolve(entity_type, value) for value in values]

# Usage example
if __name__ == '__main__':
    resolver = AliasResolver()
    
    # Test company resolution
    companies = ['BHP', 'Rio Tinto', 'FCX', 'Newmont']
    resolved = resolver.batch_resolve('company', companies)
    print(f'Companies: {resolved}')
    
    # Test commodity resolution  
    commodities = ['Au', 'gold', 'Cu', 'copper']
    resolved = resolver.batch_resolve('commodity', commodities)
    print(f'Commodities: {resolved}')
