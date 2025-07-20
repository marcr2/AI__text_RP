# AI Political Debate Simulator 🤖

An automated web application that simulates political debates between multiple AI commentators with different political perspectives and personalities.

## Features

- **Multiple AI Commentators**: Various political personalities including Democrats, Republicans, Libertarians, and more
- **Automated Conversations**: The AIs automatically respond to each other in a debate format
- **Customizable Characters**: Choose from 15+ different political personalities
- **Web Interface**: Modern, responsive web interface built with Streamlit
- **Session Management**: Save and replay debate sessions
- **Real-time Output**: Watch the debate unfold in real-time
- **Character Positioning**: Random left/right side assignment for visual debate layout

## Installation

1. **Clone or download this project**

2. **(Optional) Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:
   - Create a `.env` file in the project directory
   - Add your OpenAI API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   - Get an API key from [OpenAI's website](https://platform.openai.com/api-keys)

## Usage

### Running the Application

**Option 1: Direct Streamlit Command**
```bash
streamlit run streamlit_app.py
```

**Option 2: Using Launcher Scripts**
- Windows: Double-click `run_streamlit.bat`
- PowerShell: Right-click `run_streamlit.ps1` → "Run with PowerShell"

### Using the Web Interface

1. **Select Characters**: Choose from the available political personalities
2. **Configure Settings**: Set the number of debate rounds (default: 5)
3. **Start Debate**: Click "Start Debate" to begin the simulation
4. **Watch & Control**: The debate runs automatically with a stop button available
5. **Replay Sessions**: Load and replay previous debate sessions

### Available Characters

The application includes various political personalities:

- **Democrats**: Market Liberal Democrat, Progressive Socialist
- **Republicans**: MAGA Nationalist, Traditional Conservative
- **Third Parties**: Libertarian, Green Party Activist
- **International**: Chinese Communist Party
- **Special Characters**: Master Baiter, Redditor, Random American
- **Religious**: Catholic Theocrat, Islamic Extremist
- **Authoritarian**: Absolute Monarchist, Marxist Leninist
- **And more...**

Each character has unique:
- Political perspectives and beliefs
- Communication styles (Boomer, Gen X, Millennial, Gen Z)
- Visual styling with custom colors and emojis
- Age-appropriate characteristics

## Configuration

### Customizing Characters

You can modify character personalities by editing the character definitions in `streamlit_app.py`. Each character includes:
- Political ideology and beliefs
- Communication style and texting patterns
- Visual appearance (colors, emojis)
- Age and generation characteristics

### Adding New Characters

To add new characters, add them to the `characters` dictionary in the `PoliticalDebateSimulator` class with the required attributes:
- `name`: Character name
- `personality`: Political beliefs and personality
- `style`: Communication style
- `emoji`: Character emoji
- `background_color`: CSS color for message bubbles

## Output

### Web Interface Features
- **Real-time Debate Display**: Messages appear as they're generated
- **Character Styling**: Each character has unique colors and emojis
- **Side Positioning**: Characters are randomly assigned to left/right sides
- **Session Management**: Save and load debate sessions
- **Responsive Design**: Works on desktop and mobile devices

### Session Files
Debate sessions are automatically saved and can be replayed:
- Sessions include full conversation history
- Character assignments and styling are preserved
- Easy replay functionality

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for API calls

## Dependencies

- `openai>=1.0.0` - OpenAI API client
- `python-dotenv>=0.19.0` - Environment variable management
- `streamlit>=1.28.0` - Web interface framework

## Notes

- The application uses GPT-4o by default for enhanced debate quality
- Responses are limited to maintain focused conversations
- Characters use generation-appropriate communication styles
- The interface includes modern styling with dark backgrounds and custom colors
- Stop button allows users to halt debates at any time

## Disclaimer

This application is for educational and entertainment purposes. The AI responses represent simulated political commentary and should not be taken as actual political advice or positions. The application is designed to demonstrate AI capabilities in simulating political discourse.

## Project Structure

The application has been refactored from a monolithic design into a clean, modular architecture following Domain-Driven Design (DDD) principles and the Single Responsibility Principle (SRP). The codebase is organized into distinct layers with clear separation of concerns:

### Directory Layout

```
src/
└── debate_simulator/                # Main application package
    ├── domain/                      # Domain layer - core business logic
    │   ├── characters/              # Character domain models and factories
    │   │   ├── base.py             # Base character models and abstractions
    │   │   ├── predefined.py       # Predefined character factory with detailed personalities
    │   │   └── random_generators.py # Random character generation (American, Redditor)
    │   ├── debate/                  # Debate domain models and logic
    │   │   ├── models.py           # Core debate models (Message, Round, Conversation, etc.)
    │   │   ├── judge.py            # Debate judging system (AI, mock, rule-based)
    │   │   └── orchestrator.py     # Debate flow orchestration and AI coordination
    │   └── topics.py               # Debate topics management and validation
    ├── infrastructure/              # Infrastructure layer - external concerns
    │   ├── ai_client.py            # AI client abstraction and OpenAI implementation
    │   ├── config.py               # Application configuration and environment management
    │   └── logging_config.py       # Centralized logging configuration
    ├── application/                 # Application layer - use cases and coordination
    │   ├── character_service.py    # Character creation, caching, and management
    │   └── debate_service.py       # High-level debate session coordination
    └── presentation/                # Presentation layer - UI and user interaction
        ├── streamlit_app.py        # Main Streamlit application (thin UI layer)
        └── ui/                     # UI components and styling
            ├── components.py       # Reusable UI components (messages, controls, etc.)
            └── styles.py           # CSS styles for Streamlit UI

tests/                              # Comprehensive test suite
├── unit/                           # Unit tests by layer
│   ├── test_characters/            # Character model and factory tests
│   ├── test_debate/                # Debate logic and orchestration tests
│   ├── test_application/           # Application service tests
│   └── test_infrastructure/        # Infrastructure component tests
├── integration/                    # Integration tests
│   └── test_debate_flow.py        # End-to-end debate flow testing
└── fixtures/                       # Test data and utilities
```

### Component Responsibilities

#### Domain Layer (`src/debate_simulator/domain/`)
Contains the core business logic and domain models, independent of external frameworks:

- **Characters Module**: Defines character abstractions, predefined personalities, and random generation
- **Debate Module**: Core debate models, judging logic, and orchestration of debate flow
- **Topics Module**: Manages debate topics, categories, and validation rules

#### Infrastructure Layer (`src/debate_simulator/infrastructure/`)
Handles external dependencies and cross-cutting concerns:

- **AI Client**: Abstracts OpenAI API interactions with mock implementations for testing
- **Configuration**: Manages environment variables, API keys, and application settings
- **Logging**: Centralized logging with rotating files, console output, and context management

#### Application Layer (`src/debate_simulator/application/`)
Coordinates between domain and infrastructure layers to implement use cases:

- **Character Service**: Manages character creation, validation, caching, and position assignment
- **Debate Service**: Orchestrates debate sessions, UI callbacks, and statistics collection

#### Presentation Layer (`src/debate_simulator/presentation/`)
Handles user interface and interaction:

- **Streamlit App**: Main application entry point, acts as a thin UI layer using application services
- **UI Components**: Modular, reusable components for messages, controls, and layout
- **Styles**: CSS styling for consistent, responsive design

### Key Architectural Benefits

1. **Separation of Concerns**: Each layer has a single, well-defined responsibility
2. **Testability**: Comprehensive unit and integration tests with >80% coverage
3. **Maintainability**: Modular design makes changes and extensions easier
4. **Scalability**: Clean architecture supports future feature additions
5. **Flexibility**: Abstract interfaces allow easy swapping of implementations (e.g., AI providers)

### Testing Strategy

The test suite follows the same architectural layers:

- **Unit Tests**: Test individual components in isolation with extensive mocking
- **Integration Tests**: Test interactions between components and external services
- **Fixtures**: Provide consistent test data and utilities
- **Coverage**: Aims for >80% code coverage with focus on critical business logic

## License

This project is open source and available under the MIT License. 