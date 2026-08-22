# Project Guide - Deterministic RNG System

## Project Overview
This project implements a deterministic random number generation (RNG) system for game mechanics and validation in the Godot Engine. The system ensures reproducible gameplay outcomes while maintaining randomness through carefully designed algorithms.

**Key Technologies:**
- Godot Engine (version 4.x)
- GDScript (primary programming language)
- Deterministic RNG algorithms (LCG, etc.)
- Game mechanics validation system

**High-Level Architecture:**
```
Deterministic RNG System
├── Core System
│   ├── deterministic/ - RNG implementations and context management
│   ├── mechanics/ - Game mechanics implementation
│   ├── validation/ - Validation and result processing
│   └── simulation/ - Simulation result handling
├── Tests
│   ├── RNGArchitectureTest.gd
│   └── DeterministicLCGStatelessTest.gd
├── Data Models
│   ├── FrameSnapshot.gd
│   └── FamilyAssets.gd
└── Challenges
    ├── CHALLENGE_001.json
    └── CHALLENGE_002.json
```

## Getting Started

### Prerequisites
- Godot Engine 4.x installed
- Basic understanding of GDScript
- Python 3.x for build scripts

### Installation
1. Clone the repository
2. Open the project in Godot Engine using `project.godot`
3. Ensure all required assets are in place (see `docs/` for specifications)

### Basic Usage
```gdscript
# Example of using the RNG system
var generator = GeneradorMaestro.new()
var result = generator.generate_for_mechanic("parking")
print("Generated result:", result)
```

### Running Tests
To run the test suite:
```bash
# Assuming you have a test runner script
godot --headless --path . --script tests/RNGArchitectureTest.gd
```

## Project Structure

### Main Directories
- `core/` - Core system implementation
- `tests/` - Unit and integration tests
- `challenges/` - Challenge definitions in JSON format
- `docs/` - Documentation and specifications
- `output/` - Build output directory
- `icon.svg` - Project icon

### Key Files
- `GeneradorMaestro.gd` - Main RNG system class
- `Main.tscn` - Main scene file
- `project.godot` - Godot project configuration
- `README_INTEGRATION.md` - Integration documentation
- `build_factory.py` - Build automation script

### Important Configuration Files
- `.godot/` - Godot Engine configuration files
- `.gitignore` - Git version control configuration
- `.editorconfig` - Code style configuration

## Development Workflow

### Coding Standards
- Follow Godot's GDScript style guide
- Use snake_case for variable and function names
- Maintain consistent indentation (4 spaces)

### Testing Approach
- Unit tests in `tests/` directory
- Integration tests using challenge definitions
- Validation of game mechanics through `core/validation/`

### Build and Deployment
- Use `build_factory.py` for automation
- Export through Godot's export system
- Version control with Git

### Contribution Guidelines
1. Create a feature branch for changes
2. Write tests for new functionality
3. Follow the code style guide
4. Document new features in `docs/`

## Key Concepts

### Domain-Specific Terminology
- **RNG Context**: A container for random number generation parameters
- **Mechanic**: A specific game system or feature
- **Challenge**: A defined test scenario with expected outcomes
- **Frame Snapshot**: A record of game state at a specific point in time

### Core Abstractions
- `RNGStreamRegistry.gd` - Manages RNG streams
- `MechanicRegistry.gd` - Registers and manages game mechanics
- `ChallengeDefinitionValidator.gd` - Validates challenge definitions
- `SimulationResult.gd` - Represents results from game simulations

### Design Patterns
- Singleton pattern for core systems
- Factory pattern for object creation
- Observer pattern for event handling
- Strategy pattern for different RNG implementations

## Common Tasks

### Setting Up a New Mechanic
1. Create a new GDScript file in `core/mechanics/`
2. Implement the `Mechanic` interface
3. Register the mechanic in `MechanicRegistry.gd`
4. Add test cases in `tests/`

### Creating a New Challenge
1. Create a new JSON file in `challenges/`
2. Define the challenge parameters
3. Implement validation in `core/validation/`
4. Add test cases for the challenge

### Debugging Tips
- Use `print()` statements for basic debugging
- Use Godot's debugger for step-through debugging
- Use `FrameSnapshot.gd` to inspect game state
- Use `ValidationResult.gd` to analyze validation outcomes

## Troubleshooting

### Common Issues and Solutions
- **RNG not producing expected results**: Verify the seed value and LCG parameters
- **Mechanic not triggering**: Check registration in `MechanicRegistry.gd`
- **Validation failures**: Review `ChallengeValidator.gd` and test cases
- **Missing assets**: Ensure all required files are in the project directory

### Debugging Tips
- Use the Godot debugger to step through complex logic
- Add logging to RNG context classes
- Use the `FrameSnapshot.gd` class to inspect game state at specific points
- Use the `ValidationResult.gd` class to analyze validation outcomes


## References

### Documentation
- `docs/ARCHITECTURE_V0.1.md` - System architecture
- `docs/MECHANICS_SPECIFICATION_V0.1.md` - Game mechanics specs
- `docs/VALIDATION_PROTOCOL.md` - Validation process
- `docs/TESTING_STRATEGY_V0.1.md` - Testing approach

### Resources
- Godot Engine documentation: https://docs.godotengine.org/
- GDScript style guide: https://docs.godotengine.org/en/4.x/tutorials/gdscript/gdscript_style_guide.html
- Project roadmap: `docs/ROADMAP_PHASES.md`

This guide provides a comprehensive overview of the project structure and development workflow. Please review and edit the file as needed to ensure it accurately reflects your project's specific requirements and conventions.

### Convenciones de código específicas del proyecto
- Los nombres de clases y archivos usan **PascalCase** (ej: `GeneradorMaestro.gd`).
- Las funciones y variables usan **snake_case** (ej: `generar_resultado()`).
- Los archivos de desafíos (JSON) deben seguir el esquema definido en `docs/VALIDATION_PROTOCOL.md`.

### Dependencias externas
- Este proyecto no usa plugins externos de Godot más allá del motor base.
- Los scripts de Python (`build_factory.py`) requieren Python 3.8+ y las bibliotecas `json` y `os` (estándar).