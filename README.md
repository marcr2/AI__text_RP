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
src/political_debate/               # Main application package
├── domain/                         # Domain layer - core business logic
│   ├── models.py                  # Domain entities (Participant, Message, DebateSession, etc.)
│   ├── character_factory.py      # Factory for creating debate participants with detailed personalities
│   └── data.py                    # Static data (names, cities, debate topics, character definitions)
├── application/                   # Application layer - use cases and coordination
│   └── debate_service.py          # Main debate orchestration service and workflow management
├── infrastructure/                # Infrastructure layer - external concerns
│   └── openai_client.py           # OpenAI API communication service with error handling
└── presentation/                  # Presentation layer - UI and user interaction
    ├── streamlit_app.py           # Main Streamlit application (thin UI layer)
    └── ui_components.py           # Reusable UI components and CSS styling

tests/                             # Comprehensive test suite
├── unit/                          # Unit tests for individual components
│   ├── test_models.py            # Tests for domain models and business logic
│   └── test_character_factory.py # Tests for character creation and factory patterns
└── integration/                   # Integration tests for complete workflows
    └── test_debate_workflow.py   # End-to-end debate workflow and API integration tests

Additional Files:
├── app.py                         # Main application entry point
├── run_tests.py                   # Test runner with coverage reporting
├── requirements-dev.txt           # Development and testing dependencies
└── REFACTORING_SUMMARY.md         # Detailed refactoring documentation
```

### Component Responsibilities

#### Domain Layer (`src/political_debate/domain/`)
Contains the core business logic and domain models, independent of external frameworks:

- **Models**: Defines core entities (Participant, Message, DebateSession) with business rules and validation
- **Character Factory**: Creates diverse political personalities with unique traits, speaking styles, and ideologies
- **Data Management**: Centralizes static data including character definitions, names, cities, and debate topics

#### Infrastructure Layer (`src/political_debate/infrastructure/`)
Handles external dependencies and cross-cutting concerns:

- **OpenAI Client**: Abstracts OpenAI API interactions with proper error handling and environment setup
- **API Management**: Manages API keys, request formatting, and response processing
- **Error Recovery**: Graceful handling of API failures and network issues

#### Application Layer (`src/political_debate/application/`)
Coordinates between domain and infrastructure layers to implement use cases:

- **Debate Service**: Orchestrates the complete debate workflow from character creation to result display
- **Session Management**: Handles debate rounds, stat tracking, competitive judging, and UI coordination
- **Business Logic**: Implements debate rules, participant behavior, and outcome determination

#### Presentation Layer (`src/political_debate/presentation/`)
Handles user interface and interaction:

- **Streamlit App**: Main application entry point with clean session state management
- **UI Components**: Reusable components for message display, controls, styling, and user interaction
- **Visual Design**: Chat-style message rendering with character-specific styling and responsive layout

### Key Architectural Benefits

1. **Separation of Concerns**: Each layer has a single, well-defined responsibility with minimal coupling
2. **Testability**: Comprehensive unit and integration tests with >80% coverage and extensive mocking
3. **Maintainability**: Modular design makes changes and extensions straightforward
4. **Scalability**: Clean architecture supports new character types, debate formats, and UI enhancements
5. **Reliability**: Proper error handling, logging, and graceful degradation throughout all layers
6. **Flexibility**: Abstract interfaces allow easy swapping of AI providers or UI frameworks

### Testing Strategy

The test suite follows the same architectural layers with comprehensive coverage:

- **Unit Tests (28 tests)**: Test individual components in isolation with extensive mocking
  - Domain model validation, character factory logic, and stats calculation
  - Boundary testing, error conditions, and business rule enforcement
  
- **Integration Tests (6 tests)**: Test complete workflows and component interactions
  - End-to-end debate creation and execution with mocked OpenAI API
  - Error handling scenarios, data persistence, and session management
  
- **Test Infrastructure**: Custom test runner with HTML coverage reports and CI/CD integration
- **Mocking Strategy**: Comprehensive OpenAI API mocking to avoid costs and ensure consistency

## License

This project is open source and available under the MIT License. 