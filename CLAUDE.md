# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an Advent of Code solution repository for 2025, written in Python 3.13+. Solutions are organized by day in the `y2025/` directory, with shared utilities in the `tools/` package.

## Commands

### Running Solutions
```bash
# Run a specific day's solution
python -m y2025.d1.main

# Run tests for a specific day
python -m unittest y2025.d1.test

# Run all tests in a day's directory
python -m unittest discover -s y2025/d1 -p "test.py"
```

### Type Checking
```bash
mypy y2025/d1/main.py
```

### Dependency Management
```bash
# Install dependencies using Poetry
poetry install

# Add a new dependency
poetry add <package-name>
```

## Architecture

### Directory Structure

Each day's solution follows this pattern:
```
y2025/dN/
├── main.py         # Solution implementation
├── test.py         # Unit tests using unittest
├── input.txt       # Full puzzle input
└── input_test.txt  # Test input from puzzle description
```

Some days may have additional test files like `input_test_p2.txt` for part 2 specific tests.

### Shared Utilities (`tools/`)

The `tools/` package provides common utilities used across solutions:

**Decorators** (`tools/decorators.py`):
- `@timeit`: Measures and prints execution time
- `@to_list`: Converts generator output to list
- `@print_result(start=None, end=None)`: Prints function results with optional formatting

**File Operations** (`tools/file.py`):
- `read_last_line(filename)`: Reads the last line of a file
- `read_last_lines(filename, n)`: Reads the last n lines of a file

**Data Structures** (`tools/datastructures/`):
- `Point2`, `Point3`: 2D and 3D point classes with vector operations
- `Segment`, `Rectangle`: Geometric primitives with containment checks
- `bitarray2d.py`: Utilities for working with BitArray2D (rotate, flip operations)
- `intersections.py`: Geometric intersection algorithms

### Common Patterns

**Parsing Input Files:**
Solutions typically define a `parse_inputs(file)` function that reads from the input file and returns structured data. Example pattern:
```python
def parse_inputs(file) -> DataType:
    with open(file) as f:
        # Parse file contents
        return parsed_data
```

**Testing:**
Tests use `unittest` framework with a consistent pattern:
```python
import unittest
import os

TESTDATA_FILENAME = os.path.join(os.path.dirname(__file__), 'input_test.txt')

class Test(unittest.TestCase):
    def test_part_one(self):
        result = solve_part_one(get_data(TESTDATA_FILENAME))
        self.assertEqual(expected, result)
```

**Decorator Usage:**
Recent solutions use decorators for tracking state and memoization. See `y2025/d11/main.py` for an example of using custom decorators with `@cache` for path counting problems.

**BitArray2D Integration:**
Day 12 demonstrates integration with the `BitArray2D` library for 2D grid operations, including rotation and flipping transformations.

## Dependencies

Core dependencies:
- `more-itertools`: Extended iteration utilities
- `BitArray2D`: 2D bit array operations
- `mypy`: Static type checking

The project uses `tools` package (version ~1.0.15) as an internal dependency.

## Development Notes

- Solutions are implemented as standalone modules under `y2025/dN/`
- Each day's solution should be self-contained but can import from `tools/`
- Use dataclasses for structured data (see `y2025/d11/main.py` and `y2025/d12/main.py` for examples)
- Prefer frozen dataclasses for immutable data structures
- Type hints are used throughout the codebase
- **IMPORTANT**: Do NOT read full `input.txt` files as they can be very large. Only read first 20 or so lines and `input_test.txt` or `input_test_p2.txt` files when analyzing puzzle inputs
