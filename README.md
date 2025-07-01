# Pytest Automation Framework

A comprehensive cross-platform test automation framework built with Python, Pytest, Selenium, and Appium for web and mobile application testing.

## 🚀 Features

- **Cross-Platform Support**: Web (Chrome, Firefox, Safari) and Mobile (iOS iPhone/iPad, macOS)
- **Page Object Model**: Clean separation of test logic and page interactions
- **Allure Reporting**: Rich HTML reports with screenshots and video recordings
- **Configuration Management**: Environment-based configuration with YAML
- **Video Recording**: Automatic screen recording during test execution
- **Screenshot Capture**: Automatic screenshots on test failures
- **Parallel Execution**: Support for running tests in parallel
- **Custom Assertions**: Enhanced verification utilities with detailed failure reporting

## 📋 Prerequisites

- Python 3.8+
- Node.js (for Allure reporting)
- FFmpeg (for video recording)
- Appium Server (for mobile testing)
- iOS Simulator/Device (for iOS testing)
- macOS (for iOS and macOS app testing)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd pytest-project
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Allure commandline tool**
   ```bash
   npm install -g allure-commandline
   ```

4. **Install FFmpeg** (macOS)
   ```bash
   brew install ffmpeg
   ```

## ⚙️ Configuration

### Environment Configuration

The framework uses environment-based configuration. Create your environment file in `config/` directory

### Pytest Configuration

The framework is configured via `pytest.ini`:

```ini
[pytest]
addopts = -s -ra -vv -p no:warnings --tb=short --env=config
testpaths = tests
python_functions = test_ test*
python_files = test*
```

## 🏗️ Project Structure

```
pytest-project/
├── config/                 # Configuration files
│   └── config.yaml        # Environment configuration
├── src/                   # Source code
│   ├── apps/             # Application-specific code
│   │   ├── mobile/       # Mobile app components
│   │   └── web/          # Web app components
│   │       ├── component/ # Reusable UI components
│   │       └── page/      # Page Object Models
│   ├── data_object/      # Data models
│   ├── utils/            # Utility functions
│   ├── consts.py         # Constants
│   ├── data_runtime.py   # Runtime data management
│   ├── web_container.py  # Web application container
│   └── mobile_container.py # Mobile application container
├── tests/                # Test files
│   ├── conftest.py       # Pytest configuration
│   ├── web/              # Web tests
│   │   ├── credential/   # Authentication tests
│   │   └── trader/       # Trading functionality tests
│   └── mobile/           # Mobile tests
├── pytest.ini           # Pytest configuration
├── requirements.txt      # Python dependencies
```

## 🧪 Writing Tests

### Web Test Example

```python
# tests/web/credential/test_login.py
from src.data_runtime import DataRuntime
from src.utils import logger
from src.utils.assert_util import verify

def test_login_with_valid_credential(web):
    logger.info("Step 1: Navigate to web application")
    web.navigate_to_aquariux()

    logger.info("Step 2: Login with valid account")
    credential = [DataRuntime.config.user, DataRuntime.config.password]
    web.login_page.login_with_demo_account(*credential, wait_completed=True)
    
    verify(
        web.trade_page.top_navigation.is_setting_button_displayed(),
        "Verify setting button on Top Navigation displays"
    )
```

### Mobile Test Example

```python
# tests/mobile/test_mobile_app.py
from src.data_runtime import DataRuntime
from src.utils import logger
from src.utils.assert_util import verify

def test_mobile_app_launch(iphone):
    logger.info("Step 1: Launch mobile application")
    iphone.launch_flo_iphone()
    
    # Add your mobile test steps here
```

## 🚀 Running Tests

### Basic Test Execution

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/web/credential/test_TC1.py

# Run specific test function
pytest tests/web/credential/test_TC1.py::test_login_with_valid_credential
```

### Command Line Options

```bash
# Run with specific environment
pytest --env=config

# Run with debug logging
pytest --debuglog

# Run with video recording
pytest --record

# Run in headless mode
pytest --headless

# Run with specific browser
pytest --browser=firefox

# Run with custom credentials
pytest --user=testuser --password=testpass

# Run in remote mode
pytest --remote
```

### Parallel Execution

```bash
# Run tests in parallel (requires pytest-xdist)
pytest -n auto
```

## 📊 Test Reporting

### Allure Reports

```bash
# Generate Allure report
pytest --alluredir=./allure-results

# View Allure report
allure serve ./allure-results

# Generate static HTML report
allure generate ./allure-results --clean
```

### Console Output

The framework provides detailed console output including:
- Test execution status
- Step-by-step logging
- Execution time
- Screenshot attachments on failures

## 🔧 Utilities

### Screen Recording

The framework includes a screen recording utility:

```python
# main.py
from main import record_screen

# Record screen for 10 seconds
record_screen(filename="test_recording.mp4", duration=10)
```

### Custom Assertions

Use the enhanced verification utility:

```python
from src.utils.assert_util import verify

# Enhanced assertion with automatic screenshot capture
verify(
    element.is_displayed(),
    "Element should be displayed"
)
```

## 🏛️ Architecture

### Page Object Model

The framework follows the Page Object Model pattern:

```python
# src/apps/web/page/login_page.py
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.username_field = (By.ID, "username")
        self.password_field = (By.ID, "password")
        self.login_button = (By.ID, "login-btn")
    
    def login_with_demo_account(self, username, password, wait_completed=True):
        # Implementation
        pass
```

### Container Pattern

Applications are wrapped in containers for easy access:

```python
# src/web_container.py
class Web:
    def __init__(self, driver):
        self._driver = driver
        self.login_page = LoginPage(driver)
        self.trade_page = TradePage(driver)
```

## 🔐 Security

- Passwords are encoded in configuration files
- Sensitive data is handled securely
- API keys and credentials are externalized

## 🐛 Debugging

### Debug Logging

```bash
pytest --debuglog
```

### Screenshot Capture

Screenshots are automatically captured on test failures and attached to Allure reports.

### Video Recording

```bash
pytest --record
```

## 📝 Best Practices

1. **Test Organization**: Group tests by functionality in appropriate directories
2. **Page Objects**: Keep page objects clean and focused on UI interactions
3. **Assertions**: Use the `verify()` utility for enhanced failure reporting
4. **Logging**: Use descriptive step logging for better test documentation
5. **Configuration**: Externalize environment-specific configurations
6. **Data Management**: Use data objects for structured test data

## 🤝 Contributing

1. Follow the existing code structure and patterns
2. Add appropriate logging and assertions
3. Update documentation for new features
4. Ensure all tests pass before submitting

## 📄 License

[Add your license information here]

## 🆘 Support

For issues and questions:
- Check the existing documentation
- Review test examples in the `tests/` directory
- Check configuration in `config/` directory
- Review utility functions in `src/utils/`

---

**Note**: This framework is designed for cross-platform testing with a focus on web and mobile applications. Ensure all prerequisites are installed and configured before running tests. 