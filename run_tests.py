#!/usr/bin/env python3
"""
Test runner script for the Political Debate Simulator
Runs all unit and integration tests with coverage reporting
"""

import sys
import unittest
import coverage
import os
from pathlib import Path

def run_tests():
    """Run all tests with coverage reporting"""
    
    # Initialize coverage
    cov = coverage.Coverage(
        source=['src'],
        omit=[
            '*/tests/*',
            '*/test_*',
            '*/__pycache__/*',
            '*/venv/*',
            '*/env/*'
        ]
    )
    
    cov.start()
    
    # Discover and run tests
    loader = unittest.TestLoader()
    test_dir = Path(__file__).parent / 'tests'
    
    # Load all tests
    suite = loader.discover(str(test_dir), pattern='test_*.py')
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Stop coverage and generate report
    cov.stop()
    cov.save()
    
    print("\n" + "="*60)
    print("COVERAGE REPORT")
    print("="*60)
    
    # Generate coverage report
    cov.report(show_missing=True)
    
    # Generate HTML coverage report
    html_dir = Path(__file__).parent / 'htmlcov'
    cov.html_report(directory=str(html_dir))
    print(f"\nHTML coverage report generated in: {html_dir}")
    
    # Check if minimum coverage threshold is met
    total_coverage = cov.report(show_missing=False)
    min_coverage = 80
    
    print(f"\nTotal coverage: {total_coverage:.1f}%")
    print(f"Minimum required: {min_coverage}%")
    
    if total_coverage >= min_coverage:
        print("✅ Coverage requirement met!")
        coverage_passed = True
    else:
        print("❌ Coverage requirement not met!")
        coverage_passed = False
    
    # Return overall success
    tests_passed = result.wasSuccessful()
    
    print(f"\nTests passed: {'✅' if tests_passed else '❌'}")
    print(f"Coverage passed: {'✅' if coverage_passed else '❌'}")
    
    return tests_passed and coverage_passed


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)