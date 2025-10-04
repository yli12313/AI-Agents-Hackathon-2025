import yaml
import os
import random
from pathlib import Path
from typing import List, Dict, Any, Optional
import glob

class AttackLoader:
    """Load and manage jailbreak and seed prompt attack methods."""
    
    def __init__(self, jailbreak_dir: str = "jailbreak", seed_prompts_dir: str = "seed_prompts"):
        self.jailbreak_dir = Path(jailbreak_dir)
        self.seed_prompts_dir = Path(seed_prompts_dir)
        self.jailbreak_attacks = {}
        self.seed_attacks = {}
        self._load_attacks()
    
    def _load_attacks(self):
        """Load all attack methods from YAML files."""
        # Load jailbreak attacks
        self._load_jailbreak_attacks()
        # Load seed prompt attacks
        self._load_seed_attacks()
    
    def _load_jailbreak_attacks(self):
        """Load jailbreak attacks from YAML files."""
        for yaml_file in self.jailbreak_dir.rglob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data and 'name' in data:
                        attack_name = data['name']
                        attack_category = self._extract_category_from_path(yaml_file)
                        
                        self.jailbreak_attacks[attack_name] = {
                            'name': attack_name,
                            'description':data.get('description', ''),
                            'authors': data.get('authors', []),
                            'source': data.get('source', ''),
                            'parameters': data.get('parameters', []),
                            'template': data.get('value', ''),
                            'category': attack_category,
                            'file_path': str(yaml_file),
                            'data_type': data.get('data_type', 'text')
                        }
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")
    
    def _load_seed_attacks(self):
        """Load seed prompt attacks from YAML and prompt files."""
        # Load YAML files
        for yaml_file in self.seed_prompts_dir.rglob("*.yaml"):
            try:
                with open(yaml_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    if data:
                        attack_name = data.get('name', data.get('dataset_name', yaml_file.stem))
                        harm_categories = data.get('harm_categories', [])
                        
                        # Extract prompts
                        prompts = []
                        if 'prompts' in data:
                            for prompt_item in data['prompts']:
                                if isinstance(prompt_item, dict) and 'value' in prompt_item:
                                    prompts.append(prompt_item['value'])
                                elif isinstance(prompt_item, str):
                                    prompts.append(prompt_item)
                        
                        category = self._extract_category_from_path(yaml_file)
                        
                        self.seed_attacks[attack_name] = {
                            'name': attack_name,
                            'description': data.get('description', ''),
                            'authors': data.get('authors', []),
                            'source': data.get('source', ''),
                            'harm_categories': harm_categories,
                            'prompts': prompts,
                            'category': category,
                            'file_path': str(yaml_file),
                            'groups': data.get('groups', [])
                        }
            except Exception as e:
                print(f"Error loading {yaml_file}: {e}")
        
        # Load prompt files
        for prompt_file in self.seed_prompts_dir.rglob("*.prompt"):
            try:
                with open(prompt_file, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    attack_name = prompt_file.stem
                    category = self._extract_category_from_path(prompt_file)
                    
                    self.seed_attacks[attack_name] = {
                        'name': attack_name,
                        'description': f"Direct prompt from {prompt_file.name}",
                        'prompts': [content],
                        'category': category,
                        'file_path': str(prompt_file),
                        'harm_categories': ['custom'],
                        'authors': [],
                        'source': str(prompt_file)
                    }
            except Exception as e:
                print(f"Error loading {prompt_file}: {e}")
    
    def _extract_category_from_path(self, file_path: Path) -> str:
        """Extract category from file path."""
        parts = file_path.parts
        # Skip the root directories
        if len(parts) > 2:
            if 'pliny' in parts:
                # Extract provider/model from pliny path
                provider_path = '/'.join(parts[parts.index('pliny')+1:])
                return f"pliny/{provider_path}"
            else:
                return '/'.join(parts[-2:]) if len(parts) > 1 else parts[-1]
        return 'general'
    
    def get_all_jailbreak_attacks(self) -> Dict[str, Dict]:
        """Get all jailbreak attacks."""
        return self.jailbreak_attacks
    
    def get_all_seed_attacks(self) -> Dict[str, Dict]:
        """Get all seed prompt attacks."""
        return self.seed_attacks
    
    def get_jailbreak_attack(self, name: str) -> Optional[Dict]:
        """Get a specific jailbreak attack by name."""
        return self.jailbreak_attacks.get(name)
    
    def get_seed_attack(self, name: str) -> Optional[Dict]:
        """Get a specific seed attack by name."""
        return self.seed_attacks.get(name)
    
    def apply_jailbreak(self, attack_name: str, original_prompt: str) -> str:
        """Apply a jailbreak attack to a prompt."""
        attack = self.get_jailbreak_attack(attack_name)
        if not attack:
            return original_prompt
        
        template = attack['template']
        # Replace {{ prompt }} placeholder with original prompt
        if '{{ prompt }}' in template:
            return template.replace('{{ prompt }}', original_prompt)
        else:
            # For attacks without placeholder, append original prompt
            return f"{template}\n\nUser: {original_prompt}"
    
    def get_random_seed_prompt(self, attack_name: str) -> Optional[str]:
        """Get a random prompt from a seed attack."""
        attack = self.get_seed_attack(attack_name)
        if not attack or not attack['prompts']:
            return None
        
        return random.choice(attack['prompts'])
    
    def get_attacks_by_category(self, category: str) -> Dict[str, List[str]]:
        """Get attacks grouped by category."""
        jailbreak_categories = {}
        seed_categories = {}
        
        # Group jailbreak attacks
        for name, attack in self.jailbreak_attacks.items():
            cat = attack['category']
            if cat not in jailbreak_categories:
                jailbreak_categories[cat] = []
            jailbreak_categories[cat].append(name)
        
        # Group seed attacks
        for name, attack in self.seed_attacks.items():
            cat = attack['category']
            if cat not in seed_categories:
                seed_categories[cat] = []
            seed_categories[cat].append(name)
        
        result = {
            'jailbreak': jailbreak_categories.get(category, []),
            'seed_prompts': seed_categories.get(category, [])
        }
        
        return result
    
    def get_all_categories(self) -> Dict[str, Dict[str, List[str]]]:
        """Get all available categories."""
        result = {'jailbreak': {}, 'seed_prompts': {}}
        
        # Collect jailbreak categories
        for name, attack in self.jailbreak_attacks.items():
            cat = attack['category']
            if cat not in result['jailbreak']:
                result['jailbreak'][cat] = []
            result['jailbreak'][cat].append(name)
        
        # Collect seed prompt categories
        for name, attack in self.seed_attacks.items():
            cat = attack['category']
            if cat not in result['seed_prompts']:
                result['seed_prompts'][cat] = []
            result['seed_prompts'][cat].append(name)
        
        return result
    
    def search_attacks(self, query: str) -> Dict[str, List[str]]:
        """Search for attacks by name, description, or content."""
        query_lower = query.lower()
        jailbreak_matches = []
        seed_matches = []
        
        # Search jailbreak attacks
        for name, attack in self.jailbreak_attacks.items():
            if (query_lower in name.lower() or 
                query_lower in attack['description'].lower() or
                query_lower in attack.get('template', '').lower()):
                jailbreak_matches.append(name)
        
        # Search seed attacks
        for name, attack in self.seed_attacks.items():
            if (query_lower in name.lower() or 
                query_lower in attack['description'].lower()):
                # Also search in prompts
                for prompt in attack.get('prompts', []):
                    if query_lower in prompt.lower():
                        seed_matches.append(name)
                        break
        
        return {
            'jailbreak': jailbreak_matches,
            'seed_prompts': seed_matches
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded attacks."""
        total_jailbreaks = len(self.jailbreak_attacks)
        total_seeds = len(self.seed_attacks)
        
        jailbreak_categories = set(attack['category'] for attack in self.jailbreak_attacks.values())
        seed_categories = set(attack['category'] for attack in self.seed_attacks.values())
        
        return {
            'total_jailbreak_attacks': total_jailbreaks,
            'total_seed_attacks': total_seeds,
            'total_attacks': total_jailbreaks + total_seeds,
            'jailbreak_categories': len(jailbreak_categories),
            'seed_categories': len(seed_categories),
            'unique_categories': len(jailbreak_categories | seed_categories)
        }
