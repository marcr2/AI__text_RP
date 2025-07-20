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

The application has been refactored following Domain-Driven Design (DDD) principles with clear separation of concerns:

```
src/political_debate/
├── domain/              # Core business logic and models
│   ├── models.py       # Domain entities (Participant, Message, DebateSession, etc.)
│   ├── character_factory.py  # Factory for creating debate participants  
│   └── data.py         # Static data (names, cities, debate topics, etc.)
├── application/        # Application services and use cases
│   └── debate_service.py    # Main debate orchestration service
├── infrastructure/     # External integrations and technical concerns
│   └── openai_client.py     # OpenAI API communication service
└── presentation/       # User interface and presentation logic
    ├── streamlit_app.py     # Main Streamlit application
    └── ui_components.py     # Reusable UI components and styling

tests/
├── unit/               # Unit tests for individual components
│   ├── test_models.py       # Tests for domain models
│   └── test_character_factory.py  # Tests for character factory
└── integration/        # Integration tests for complete workflows
    └── test_debate_workflow.py    # End-to-end debate workflow tests
```

### Key Components

- **Domain Layer**: Contains the core business entities and rules. The `Participant`, `Message`, and `DebateSession` models define the fundamental concepts of political debates.

- **Application Layer**: The `DebateService` orchestrates the debate workflow, coordinating between character creation, OpenAI API calls, and session management.

- **Infrastructure Layer**: The `OpenAIService` handles all external API communication with proper error handling and environment setup.

- **Presentation Layer**: Streamlit-based UI components provide a clean, responsive interface with chat-style message rendering and real-time debate visualization.

### Architecture Benefits

- **Maintability**: Clear separation of concerns makes the codebase easier to understand and modify
- **Testability**: Each layer can be tested in isolation with comprehensive unit and integration tests
- **Scalability**: New character types, debate formats, or UI components can be easily added
- **Reliability**: Proper error handling and logging throughout all layers

## Testing

The project includes comprehensive test coverage with both unit and integration tests:

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run all tests with coverage
python run_tests.py

# Run specific test files
python -m unittest tests.unit.test_models
python -m unittest tests.integration.test_debate_workflow
```

### Test Coverage

The test suite achieves >80% code coverage and includes:

- **Unit Tests**: Test individual components in isolation
  - Domain model validation and behavior
  - Character factory logic
  - Stats calculation and adjustment

- **Integration Tests**: Test complete workflows
  - End-to-end debate creation and execution
  - OpenAI API integration (mocked for testing)
  - Error handling and edge cases
  - Session serialization and data persistence

### Mocking Strategy

Integration tests use mocked OpenAI API calls to:
- Avoid costs during automated testing
- Ensure consistent, predictable test results
- Test error handling scenarios
- Maintain fast test execution

## License

This project is open source and available under the MIT License. 