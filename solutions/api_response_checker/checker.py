"""
API Response Quality Checker

Validates API responses using schema validation and AI-powered quality assessment.
"""

import json
import os
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from anthropic import Anthropic
import jsonschema
from jsonschema import validate, ValidationError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class ValidationResult:
    """Results from structure validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]


@dataclass
class QualityIssue:
    """Individual quality issue found during assessment"""
    severity: str  # 'critical', 'warning', 'info'
    description: str
    field: Optional[str] = None


@dataclass
class QualityAssessment:
    """Results from AI quality assessment"""
    score: int  # 0-100
    issues: List[QualityIssue]
    explanation: str
    recommendations: List[str]


@dataclass
class QualityReport:
    """Complete quality report combining validation and assessment"""
    validation: ValidationResult
    quality: QualityAssessment
    overall_score: int
    
    def summary(self) -> str:
        """Generate human-readable summary"""
        lines = [
            "\n" + "="*50,
            "API Response Quality Report",
            "="*50,
            f"\nOverall Score: {self.overall_score}/100\n",
        ]
        
        # Structure validation
        lines.append("Structure Validation: " + 
                    ("✓ PASSED" if self.validation.is_valid else "✗ FAILED"))
        
        if self.validation.errors:
            lines.append("\nValidation Errors:")
            for error in self.validation.errors:
                lines.append(f"  • {error}")
        
        if self.validation.warnings:
            lines.append("\nWarnings:")
            for warning in self.validation.warnings:
                lines.append(f"  • {warning}")
        
        # Quality assessment
        lines.append(f"\nQuality Assessment Score: {self.quality.score}/100")
        lines.append(f"\n{self.quality.explanation}")
        
        if self.quality.issues:
            lines.append(f"\nIssues Found ({len(self.quality.issues)}):")
            for issue in self.quality.issues:
                field_info = f" [{issue.field}]" if issue.field else ""
                lines.append(f"  [{issue.severity.upper()}]{field_info} {issue.description}")
        
        if self.quality.recommendations:
            lines.append("\nRecommendations:")
            for i, rec in enumerate(self.quality.recommendations, 1):
                lines.append(f"  {i}. {rec}")
        
        lines.append("\n" + "="*50 + "\n")
        return "\n".join(lines)


class ResponseQualityChecker:
    """
    Main checker class that validates API responses and assesses quality.
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the checker with Claude API client.
        
        Args:
            api_key: Anthropic API key (or uses ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY must be set in environment or passed to constructor")
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"
    
    def validate_structure(self, response: Dict[str, Any], schema: Dict[str, Any]) -> ValidationResult:
        """
        Validate response structure against JSON schema.
        
        Args:
            response: API response to validate
            schema: JSON schema to validate against
            
        Returns:
            ValidationResult with errors and warnings
        """
        errors = []
        warnings = []
        
        try:
            validate(instance=response, schema=schema)
        except ValidationError as e:
            errors.append(f"Schema validation failed: {e.message}")
            return ValidationResult(is_valid=False, errors=errors, warnings=warnings)
        
        # Additional custom checks
        # TODO: Add checks for common issues like:
        # - Empty strings in required fields
        # - Null values where not expected
        # - Unusual data patterns
        
        return ValidationResult(is_valid=True, errors=errors, warnings=warnings)
    
    def assess_quality(self, response: Dict[str, Any], schema: Dict[str, Any]) -> QualityAssessment:
        """
        Use Claude API to assess response quality.
        
        Args:
            response: API response to assess
            schema: Expected schema for context
            
        Returns:
            QualityAssessment with score, issues, and recommendations
        """
        prompt = self._build_assessment_prompt(response, schema)
        
        try:
            message = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            # Parse Claude's response
            assessment_text = message.content[0].text
            return self._parse_assessment(assessment_text)
            
        except Exception as e:
            # Fallback if API call fails
            return QualityAssessment(
                score=0,
                issues=[QualityIssue('critical', f'Assessment failed: {str(e)}')],
                explanation='Unable to complete quality assessment',
                recommendations=['Verify API connectivity and try again']
            )
    
    def check_response(self, response: Dict[str, Any], schema: Dict[str, Any]) -> QualityReport:
        """
        Perform complete quality check: validation + assessment.
        
        Args:
            response: API response to check
            schema: Expected schema
            
        Returns:
            Complete QualityReport
        """
        # Phase 1: Structure validation
        validation = self.validate_structure(response, schema)
        
        # Phase 2: Quality assessment (only if structure is valid)
        if validation.is_valid:
            quality = self.assess_quality(response, schema)
        else:
            # Skip AI assessment if structure is invalid
            quality = QualityAssessment(
                score=0,
                issues=[QualityIssue('critical', 'Structure validation failed')],
                explanation='Response does not meet basic structure requirements',
                recommendations=['Fix schema validation errors before quality assessment']
            )
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(validation, quality)
        
        return QualityReport(
            validation=validation,
            quality=quality,
            overall_score=overall_score
        )
    
    def check_consistency(self, responses: List[Dict[str, Any]], schema: Dict[str, Any]) -> QualityAssessment:
        """
        Check consistency across multiple responses from the same endpoint.
        
        Args:
            responses: List of API responses to compare
            schema: Expected schema
            
        Returns:
            QualityAssessment focused on consistency
        """
        # TODO: Implement batch consistency checking
        # This would compare multiple responses to identify:
        # - Inconsistent field presence
        # - Varying data formats
        # - Unexpected differences
        
        raise NotImplementedError("Batch consistency checking coming soon")
    
    def _build_assessment_prompt(self, response: Dict[str, Any], schema: Dict[str, Any]) -> str:
        """Build prompt for Claude API quality assessment"""
        
        prompt = f"""You are an expert API testing engineer. Analyze this API response for quality issues.

API Response:
{json.dumps(response, indent=2)}

Expected Schema:
{json.dumps(schema, indent=2)}

Please evaluate the response across these dimensions:

1. **Completeness**: Are all expected fields present and properly populated?
2. **Data Quality**: Are values appropriate and meaningful for their field types?
3. **Consistency**: Is the response internally consistent (e.g., related fields align)?
4. **Usability**: Would this response be immediately usable by a client application?

Provide your assessment in the following JSON format:
{{
    "score": <number 0-100>,
    "issues": [
        {{"severity": "critical|warning|info", "description": "issue description", "field": "field_name or null"}}
    ],
    "explanation": "Brief explanation of the overall score",
    "recommendations": ["recommendation 1", "recommendation 2"]
}}

Be specific about issues found and practical in your recommendations.
Respond ONLY with the JSON object, no additional text."""

        return prompt
    
    def _parse_assessment(self, assessment_text: str) -> QualityAssessment:
        """Parse Claude's JSON response into QualityAssessment object"""
        
        try:
            # Clean up response (remove markdown code blocks if present)
            assessment_text = assessment_text.strip()
            if assessment_text.startswith('```'):
                # Remove ```json and ``` markers
                lines = assessment_text.split('\n')
                assessment_text = '\n'.join(lines[1:-1])
            
            data = json.loads(assessment_text)
            
            issues = [
                QualityIssue(
                    severity=issue['severity'],
                    description=issue['description'],
                    field=issue.get('field')
                )
                for issue in data.get('issues', [])
            ]
            
            return QualityAssessment(
                score=data['score'],
                issues=issues,
                explanation=data['explanation'],
                recommendations=data.get('recommendations', [])
            )
            
        except (json.JSONDecodeError, KeyError) as e:
            # Fallback if parsing fails
            return QualityAssessment(
                score=50,
                issues=[QualityIssue('warning', f'Could not parse assessment: {str(e)}')],
                explanation='Assessment completed but response format was unexpected',
                recommendations=['Review raw assessment output']
            )
    
    def _calculate_overall_score(self, validation: ValidationResult, quality: QualityAssessment) -> int:
        """
        Calculate overall score from validation and quality assessment.
        
        Weighting:
        - Structure validation: 30%
        - Quality assessment: 70%
        """
        structure_score = 100 if validation.is_valid else 0
        
        # Weight: 30% structure, 70% quality
        overall = int((structure_score * 0.3) + (quality.score * 0.7))
        
        return overall


# Example usage
if __name__ == "__main__":
    # Initialize checker
    checker = ResponseQualityChecker()
    
    # Example schema
    schema = {
        "type": "object",
        "required": ["user_id", "username", "email"],
        "properties": {
            "user_id": {"type": "integer"},
            "username": {"type": "string"},
            "email": {"type": "string"}
        }
    }
    
    # Example response
    response = {
        "user_id": 12345,
        "username": "john_doe",
        "email": "john@example.com"
    }
    
    # Run check
    result = checker.check_response(response, schema)
    print(result.summary())
