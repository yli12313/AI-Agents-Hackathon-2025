# AI Attack Integration System

This document describes the integration of jailbreak and seed prompt attack methods into the RedBot application.

## Overview

The attack system has been successfully integrated into `redbot_app.py` with the following capabilities:

- **140 Total Attacks**: 132 jailbreak attacks + 8 seed prompt attacks
- **46 Jailbreak Categories**: Organized by provider/model/variant
- **2 Seed Prompt Categories**: Organized by attack type and purpose

## Components

### 1. AttackLoader (`attack_loader.py`)

Core class that loads and manages all attack methods:

```python
from attack_loader import AttackLoader

# Initialize the attack system
loader = AttackLoader()

# Get statistics
stats = loader.get_statistics()
print(f"Loaded {stats['total_attacks']} attacks")

# Apply a jailbreak attack
attack_message = loader.apply_jailbreak('Jailbreak', 'Tell me secrets')

# Get a random seed prompt
prompt = loader.get_random_seed_prompt('illegal')

# Search attacks
results = loader.search_attacks('dan')
```

### 2. Enhanced RedBot UI

The Streamlit interface now includes:

#### Quick Attack Mode
- **Custom Prompt**: Direct prompt input
- **Jailbreak**: Apply known jailbreak templates
- **Seed Prompt**: Use pre-defined attack prompts

#### Advanced Attack Mode
- **Jailbreak Selection**: Choose from 132+ jailbreak attacks
- **Seed Prompt Selection**: Choose from 8+ seed attack sets
- **Custom Prompt Combination**: Mix jailbreaks with seed prompts
- **Attack Statistics**: View all available attacks with metadata

### 3. Attack Categories Available

#### Jailbreak Categories (46 total)
- **Classic Attacks**: Jailbreak, DAN variants, Dev Mode
- **Persona Attacks**: Hackerman, Coach Bobby Knight, Evil Confidant
- **Special Techniques**: Prefix Injection, Role Play, Style Injection
- **Model-Specific**: Pliny attacks for specific LLM providers
- **Advanced**: Complex multi-parameter attacks

#### Seed Prompt Categories (2 total)
- **illegal**: General illegal/harmful content prompts
- **fairness**: Bias testing and fairness evaluation prompts

## Usage Examples

### Basic Attack Execution

```python
# Quick attack with jailbreak
attack_config = {
    "jailbreak_attack": "Jailbreak",
    "custom_prompt": "Tell me about admin access"
}

# Advanced attack with seed prompt
attack_config = {
    "jailbreak_attack": "DAN 1", 
    "seed_prompt": "illegal"
}

# Send attack
result = direct_attack_and_capture(target_url, attack_config)
```

### UI Configuration

1. **Target**: Set the chatbot endpoint URL
2. **Attack Mode**: Choose Quick Attack or Advanced
3. **Attack Selection**: 
   - Quick Attack: Select type and configure
   - Advanced: Choose jailbreak + seed prompt + custom prompt
4. **Execution**: Click "Run Cycle" to execute

### Attack Statistics Panel

Click "📊 Show Attack Stats" to see:
- Total attack counts by type
- All available categories
- Sample attack lists
- Attack system health

## Supported Attack Types

### Jailbreak Attacks (132)
Examples include:
- `Jailbreak`: Classic role substitution attack
- `DAN 1`: Do Anything Now personality override
- `Hackerman`: Unhinged AI persona attack
- `prefix injection`: Simple prefix override
- `Role Play`: Character-based attack

### Seed Prompt Attacks (8)
Examples include:
- `illegal`: Harmful content requests
- `gandalf`: Gandalf-style prompt injection
- `steal_system_prompt`: System prompt exfiltration
- `fairness`: Bias testing prompts

## Integration Points

### With Existing Systems

1. **OpenHands Bridge**: Enhanced payload structure with attack metadata
2. **Structured Findings**: Attack type analysis and categorization
3. **Prescriptive Plans**: Remediation based on attack type used

### Attack Metadata Tracking

Each attack execution now includes:
```python
{
    "attack_used": {
        "jailbreak": "DAN 1",
        "seed_prompt": "illegal", 
        "custom": "additional text"
    },
    "full_attack_message": "...",
    "response": "..."
}
```

## Security Considerations

⚠️ **Important**: These attack methods are designed for educational and security research purposes only. They should only be used against:
- Systems you own
- Systems you have explicit permission to test
- Controlled testing environments

## Files Modified

- `redbot_app.py`: Enhanced with attack selection UI and execution
- `attack_loader.py`: New attack management system
- `requirements.txt`: Added PyYAML dependency
- `ATTACK_INTEGRATION_README.md`: This documentation

## Testing

Run the integration test:
```bash
python3 test_attack_integration.py
```

Expected output:
- 140 total attacks loaded
- 46 jailbreak categories
- 2 seed prompt categories
- Successful attack application and prompt extraction

## Future Enhancements

- Dynamic attack effectiveness scoring
- Attack clustering and similarity analysis
- Automated attack recommendation based on target characteristics
- Attack success rate analytics
- Integration with security research databases

## Conclusion

The attack integration system successfully incorporates 140 attack methods into RedBot, providing researchers and security professionals with a comprehensive toolkit for testing AI system robustness and security posture.

The system maintains backward compatibility while adding powerful new capabilities for systematic security testing.
