"""
Basic tests for API Response Quality Checker
"""

import pytest
from checker import ResponseQualityChecker, ValidationResult, QualityIssue


def test_structure_validation_valid():
    """Test that valid responses pass structure validation"""
    checker = ResponseQualityChecker()
    
    schema = {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"}
        }
    }
    
    response = {
        "id": 1,
        "name": "test"
    }
    
    result = checker.validate_structure(response, schema)
    assert result.is_valid is True
    assert len(result.errors) == 0


def test_structure_validation_missing_field():
    """Test that missing required fields fail validation"""
    checker = ResponseQualityChecker()
    
    schema = {
        "type": "object",
        "required": ["id", "name"],
        "properties": {
            "id": {"type": "integer"},
            "name": {"type": "string"}
        }
    }
    
    response = {
        "id": 1
        # 'name' is missing
    }
    
    result = checker.validate_structure(response, schema)
    assert result.is_valid is False
    assert len(result.errors) > 0


def test_structure_validation_wrong_type():
    """Test that wrong data types fail validation"""
    checker = ResponseQualityChecker()
    
    schema = {
        "type": "object",
        "required": ["id"],
        "properties": {
            "id": {"type": "integer"}
        }
    }
    
    response = {
        "id": "not an integer"
    }
    
    result = checker.validate_structure(response, schema)
    assert result.is_valid is False


def test_overall_score_calculation():
    """Test overall score calculation logic"""
    checker = ResponseQualityChecker()
    
    # Valid structure
    validation = ValidationResult(is_valid=True, errors=[], warnings=[])
    
    # Mock quality assessment
    from checker import QualityAssessment
    quality = QualityAssessment(
        score=80,
        issues=[],
        explanation="Good quality",
        recommendations=[]
    )
    
    overall = checker._calculate_overall_score(validation, quality)
    
    # Should be weighted: 30% structure (100) + 70% quality (80) = 86
    assert overall == 86


def test_overall_score_invalid_structure():
    """Test that invalid structure heavily impacts overall score"""
    checker = ResponseQualityChecker()
    
    # Invalid structure
    validation = ValidationResult(is_valid=False, errors=["Schema error"], warnings=[])
    
    from checker import QualityAssessment
    quality = QualityAssessment(
        score=100,  # Even perfect quality assessment
        issues=[],
        explanation="Quality is good but structure failed",
        recommendations=[]
    )
    
    overall = checker._calculate_overall_score(validation, quality)
    
    # Structure failure: 30% * 0 + 70% * 100 = 70
    assert overall == 70


# Add more tests as needed:
# - test_assess_quality_with_mock
# - test_check_response_integration
# - test_parse_assessment
# - test_quality_report_summary_format
