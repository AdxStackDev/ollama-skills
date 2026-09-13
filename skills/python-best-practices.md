---
name: python-best-practices
description: Modern Python development practices covering code style, patterns, testing, performance, and project structure
license: Complete terms in LICENSE.txt
---

# Python Best Practices

Write Python code that is clean, maintainable, performant, and Pythonic. Think like a senior Python engineer reviewing code for a production system that will be maintained by a team for years.

## Code Style & Conventions

**Follow PEP 8, but favor readability**. The style guide is a tool for consistency, not a strict rulebook. When PEP 8 conflicts with readability, choose readability.

### Naming Conventions

```python
# Modules and packages: lowercase with underscores
import my_module
from data_processing import utils

# Classes: PascalCase
class UserAccount:
    pass

# Functions and variables: snake_case
def calculate_total_price(items):
    total_price = 0
    return total_price

# Constants: UPPERCASE with underscores
MAX_RETRIES = 3
API_BASE_URL = "https://api.example.com"

# Private attributes/methods: single leading underscore
class MyClass:
    def __init__(self):
        self._internal_state = None
    
    def _helper_method(self):
        pass

# "Protected" (name mangling): double leading underscore
class Parent:
    def __init__(self):
        self.__private = "truly private"
```

### Import Organization

```python
# Standard library imports
import os
import sys
from datetime import datetime
from typing import List, Dict, Optional

# Third-party imports
import requests
import numpy as np
from flask import Flask, request

# Local application imports
from my_app.models import User
from my_app.utils import validate_email
```

**Import rules:**
- One import per line for readability
- Group imports: stdlib, third-party, local
- Use absolute imports over relative
- Avoid wildcard imports (`from module import *`)

## Type Hints

**Use type hints for better code clarity and IDE support:**

```python
from typing import List, Dict, Optional, Union, Tuple, Any

def process_users(
    users: List[Dict[str, Any]], 
    active_only: bool = True
) -> List[str]:
    """
    Process user list and return usernames.
    
    Args:
        users: List of user dictionaries
        active_only: Whether to filter for active users only
        
    Returns:
        List of usernames
    """
    return [u['username'] for u in users if not active_only or u.get('is_active')]

# Optional for values that can be None
def find_user(user_id: int) -> Optional[User]:
    return User.query.get(user_id)

# Union for multiple possible types
def parse_input(value: Union[str, int, float]) -> float:
    return float(value)

# Modern Python 3.10+ syntax
def process_data(items: list[dict[str, any]]) -> tuple[int, float]:
    return len(items), sum(i.get('value', 0) for i in items)
```

## Function Design

**Write small, focused functions that do one thing well:**

```python
# Bad: Function does too much
def process_and_save_user(data):
    # Validate
    if not data.get('email'):
        raise ValueError("Email required")
    # Transform
    user = User(email=data['email'].lower())
    # Save
    db.session.add(user)
    db.session.commit()
    # Send email
    send_welcome_email(user)
    return user

# Good: Separate concerns
def validate_user_data(data: Dict[str, Any]) -> None:
    """Validate user data or raise ValueError."""
    if not data.get('email'):
        raise ValueError("Email required")

def create_user(data: Dict[str, Any]) -> User:
    """Create user from validated data."""
    return User(email=data['email'].lower())

def save_user(user: User) -> User:
    """Persist user to database."""
    db.session.add(user)
    db.session.commit()
    return user
```

**Use default arguments carefully:**

```python
# Bad: Mutable default argument
def add_item(item, items=[]):  # Bug! List is shared across calls
    items.append(item)
    return items

# Good: Use None and create new list
def add_item(item: Any, items: Optional[List] = None) -> List:
    if items is None:
        items = []
    items.append(item)
    return items
```

**Keyword-only arguments for clarity:**

```python
def create_user(*, email: str, username: str, age: int = 18):
    """Force callers to use keyword arguments for clarity."""
    pass

# Must call as:
create_user(email="test@example.com", username="john", age=25)
# Not: create_user("test@example.com", "john", 25)
```

## Error Handling

**Be specific with exceptions:**

```python
# Bad: Catching everything
try:
    process_data()
except Exception:
    print("Something went wrong")

# Good: Catch specific exceptions
try:
    process_data()
except ValueError as e:
    logger.error(f"Invalid data: {e}")
    raise
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    retry_connection()
```

**Create custom exceptions for domain errors:**

```python
class ValidationError(Exception):
    """Raised when data validation fails."""
    pass

class UserNotFoundError(Exception):
    """Raised when user lookup fails."""
    def __init__(self, user_id: int):
        self.user_id = user_id
        super().__init__(f"User {user_id} not found")

# Usage
def get_user(user_id: int) -> User:
    user = db.query(User).get(user_id)
    if not user:
        raise UserNotFoundError(user_id)
    return user
```

**Use context managers for resource cleanup:**

```python
# Good: Always closes file
with open('data.txt', 'r') as f:
    data = f.read()

# Custom context manager
from contextlib import contextmanager

@contextmanager
def database_transaction():
    """Context manager for database transactions."""
    try:
        yield
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

# Usage
with database_transaction():
    create_user(data)
    update_stats()
```

## Data Structures

**Choose the right data structure:**

```python
# List: Ordered, mutable, allows duplicates
items = [1, 2, 3, 2]

# Tuple: Ordered, immutable, allows duplicates
coordinates = (10.5, 20.3)

# Set: Unordered, mutable, unique values
unique_ids = {1, 2, 3, 4}

# Dict: Key-value mapping
user = {'name': 'John', 'age': 30}

# Use sets for membership testing (O(1) vs O(n))
# Bad
allowed_users = ['user1', 'user2', 'user3']
if username in allowed_users:  # O(n) lookup
    pass

# Good
allowed_users = {'user1', 'user2', 'user3'}
if username in allowed_users:  # O(1) lookup
    pass
```

**List comprehensions over loops:**

```python
# Bad
squares = []
for x in range(10):
    squares.append(x**2)

# Good
squares = [x**2 for x in range(10)]

# With condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
user_emails = {user.id: user.email for user in users}

# Set comprehension
unique_lengths = {len(word) for word in words}

# Generator expression for memory efficiency
total = sum(x**2 for x in range(1000000))  # Doesn't create list
```

## Classes & OOP

**Use dataclasses for simple data containers:**

```python
from dataclasses import dataclass, field
from typing import List

@dataclass
class User:
    """User data container."""
    id: int
    username: str
    email: str
    is_active: bool = True
    tags: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Validate after initialization."""
        if '@' not in self.email:
            raise ValueError("Invalid email")

# Automatic __init__, __repr__, __eq__
user = User(1, "john", "john@example.com")
print(user)  # User(id=1, username='john', ...)
```

**Use properties for computed attributes:**

```python
class Circle:
    def __init__(self, radius: float):
        self._radius = radius
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        if value < 0:
            raise ValueError("Radius must be positive")
        self._radius = value
    
    @property
    def area(self) -> float:
        """Computed property."""
        return 3.14159 * self._radius ** 2

circle = Circle(5)
print(circle.area)  # Computed on access
```

**Use composition over inheritance:**

```python
# Bad: Deep inheritance hierarchy
class Animal:
    pass
class Mammal(Animal):
    pass
class Dog(Mammal):
    pass

# Good: Composition
class Animal:
    def __init__(self, movement: MovementStrategy):
        self.movement = movement
    
    def move(self):
        self.movement.execute()

class WalkingMovement:
    def execute(self):
        print("Walking")

class FlyingMovement:
    def execute(self):
        print("Flying")

dog = Animal(WalkingMovement())
bird = Animal(FlyingMovement())
```

## Working with Files & Data

**Use pathlib over os.path:**

```python
from pathlib import Path

# Good: Modern path handling
data_dir = Path('data')
file_path = data_dir / 'users.json'

if file_path.exists():
    with file_path.open('r') as f:
        data = json.load(f)

# Get all Python files recursively
py_files = list(Path('.').rglob('*.py'))
```

**JSON handling:**

```python
import json
from typing import Any

def save_json(data: Any, filepath: Path) -> None:
    """Save data to JSON file."""
    with filepath.open('w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_json(filepath: Path) -> Any:
    """Load data from JSON file."""
    with filepath.open('r') as f:
        return json.load(f)
```

**Environment variables:**

```python
import os
from dotenv import load_dotenv

# Load from .env file
load_dotenv()

# Access with defaults
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///dev.db')
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
```

## Testing

**Write tests for everything:**

```python
import pytest
from my_app.utils import validate_email

def test_validate_email_valid():
    """Test email validation with valid email."""
    assert validate_email("test@example.com") is True

def test_validate_email_invalid():
    """Test email validation with invalid email."""
    assert validate_email("invalid") is False

def test_validate_email_empty():
    """Test email validation with empty string."""
    with pytest.raises(ValueError):
        validate_email("")

# Fixtures for reusable test data
@pytest.fixture
def sample_user():
    """Create a sample user for tests."""
    return User(id=1, username="test", email="test@example.com")

def test_user_creation(sample_user):
    """Test user object creation."""
    assert sample_user.username == "test"
```

**Use mocking for external dependencies:**

```python
from unittest.mock import Mock, patch

def test_api_call():
    """Test API call with mocked requests."""
    with patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {'status': 'ok'}
        mock_get.return_value.status_code = 200
        
        result = fetch_data_from_api()
        assert result['status'] == 'ok'
        mock_get.assert_called_once()
```

## Performance

**Profile before optimizing:**

```python
import cProfile
import pstats

# Profile a function
cProfile.run('my_function()', 'output.prof')

# Analyze results
stats = pstats.Stats('output.prof')
stats.sort_stats('cumulative')
stats.print_stats(10)  # Top 10 slowest
```

**Use generators for large datasets:**

```python
# Bad: Loads everything into memory
def read_large_file(filepath):
    with open(filepath) as f:
        return [line.strip() for line in f]

# Good: Generator yields one line at a time
def read_large_file(filepath):
    with open(filepath) as f:
        for line in f:
            yield line.strip()

# Usage
for line in read_large_file('huge.txt'):
    process(line)  # Memory efficient
```

**Cache expensive computations:**

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def expensive_computation(n: int) -> int:
    """Cached function result."""
    # Complex calculation
    return result
```

## Project Structure

```
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── user_service.py
│       └── utils/
│           ├── __init__.py
│           └── validators.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   └── test_services/
│       └── test_user_service.py
├── .env.example
├── .gitignore
├── requirements.txt
├── setup.py
└── README.md
```

## Logging

**Use logging, not print:**

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Use appropriate levels
logger.debug("Detailed debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred", exc_info=True)
logger.critical("Critical failure")
```

## Common Anti-Patterns

❌ Using `eval()` or `exec()` (security risk)
❌ Mutable default arguments
❌ Catching Exception without re-raising
❌ Not using context managers for resources
❌ String concatenation in loops (`+=`)
❌ Using `==` for boolean comparison (`if x == True:`)
❌ Not using virtual environments
❌ Hardcoding credentials
❌ Not using type hints
❌ Reinventing the wheel (use stdlib/packages)
❌ Not writing tests
❌ Global variables everywhere

## Tools & Best Practices

**Code quality tools:**
- `black`: Auto-formatter
- `flake8`: Linting
- `mypy`: Type checking
- `pytest`: Testing
- `pylint`: Code analysis
- `isort`: Import sorting

**Dependency management:**
- Use `requirements.txt` or `pyproject.toml`
- Pin versions for production (`==`)
- Separate dev dependencies
- Use virtual environments (venv, conda)

**Security:**
- Never commit secrets
- Use environment variables
- Validate all inputs
- Use parameterized queries for SQL
- Keep dependencies updated
