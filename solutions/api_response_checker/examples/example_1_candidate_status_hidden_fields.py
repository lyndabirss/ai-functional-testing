"""
Example 1: Candidate Status Dropdown - Hidden Field Detection

REAL SCENARIO: Recruitment System Status Field
================================================

Your recruitment system has a dropdown for candidate status.
The dropdown is populated by calling GET /api/fields/candidate-status
which returns available status options.

THE PROBLEM:
The API returns ALL status values from the database, including:
- Production statuses (Active, Interview, Placed)
- Internal test statuses (TEST_STATUS, DO_NOT_USE)
- Hidden administrative statuses (SYSTEM_ARCHIVED)

These internal/test statuses shouldn't be visible to recruiters,
but they appear in the UI dropdown - looks unprofessional and confusing.

WHY AUTOMATED API TESTS MISS THIS:
====================================

Your automated Postman collection or pytest suite checks:
✓ HTTP 200 response
✓ Valid JSON structure
✓ Required fields present (field_name, options array)
✓ Correct data types (strings, integers)
→ Automated test PASSES ✓

Manual QA tester testing the UI would spot:
"Why is TEST_STATUS_INTERNAL showing in the dropdown?"

This tool (Quality Intelligence) catches it automatically by:
- Analyzing field labels for internal/test patterns
- Flagging contextually inappropriate data
- Understanding this is user-facing, not internal API

THE VALUE:
==========
- Prevents unprofessional UI
- Catches data leakage before production
- Automates what manual testers would catch
- Finds issues that pass all automated API schema validation
"""

from checker import ResponseQualityChecker

# Schema that automated API tests validate against
# This checks STRUCTURE only - not appropriateness of content
candidate_status_schema = {
    "type": "object",
    "required": ["field_name", "options"],
    "properties": {
        "field_name": {"type": "string"},
        "options": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["id", "label", "value"],
                "properties": {
                    "id": {"type": "integer"},
                    "label": {"type": "string"},
                    "value": {"type": "string"}
                }
            }
        }
    }
}

# What the API actually returns (includes hidden/internal values)
api_response = {
    "field_name": "Candidate Status",
    "options": [
        {"id": 1, "label": "Active", "value": "active"},
        {"id": 2, "label": "Interview Scheduled", "value": "interview"},
        {"id": 3, "label": "Offer Extended", "value": "offer"},
        {"id": 4, "label": "Placed", "value": "placed"},
        {"id": 5, "label": "On Hold", "value": "on_hold"},
        {"id": 99, "label": "TEST_STATUS_INTERNAL", "value": "test_internal"},  # ← Problem!
        {"id": 100, "label": "SYSTEM_ARCHIVED", "value": "sys_archived"}        # ← Problem!
    ]
}

print("="*70)
print("EXAMPLE 1: Candidate Status Dropdown - Hidden Field Detection")
print("="*70)

# Initialize checker
checker = ResponseQualityChecker()

# Step 1: What automated API schema validation checks
print("\n1. AUTOMATED API SCHEMA VALIDATION (Postman/pytest):")
print("-" * 70)
structure_result = checker.validate_structure(api_response, candidate_status_schema)

if structure_result.is_valid:
    print("✓ Structure validation PASSED")
    print("  - Valid JSON")
    print("  - Required fields present (field_name, options)")
    print("  - Correct data types (array of objects)")
    print("  - All option objects have id, label, value")
    print("\n→ Automated test suite marks this as PASSING")
else:
    print("✗ Structure validation FAILED")
    for error in structure_result.errors:
        print(f"  - {error}")

# Step 2: What Quality Intelligence adds
print("\n2. QUALITY INTELLIGENCE ANALYSIS (This Tool + Claude API):")
print("-" * 70)
full_result = checker.check_response(api_response, candidate_status_schema)

print(f"\nOverall Quality Score: {full_result.quality.score}/100")
print(f"\nAnalysis: {full_result.quality.explanation}")

if full_result.quality.issues:
    print(f"\nIssues Detected ({len(full_result.quality.issues)}):")
    for issue in full_result.quality.issues:
        severity_symbol = "🔴" if issue.severity == "critical" else "⚠️" if issue.severity == "warning" else "ℹ️"
        print(f"  {severity_symbol} [{issue.severity.upper()}] {issue.description}")

if full_result.quality.recommendations:
    print(f"\nRecommendations:")
    for i, rec in enumerate(full_result.quality.recommendations, 1):
        print(f"  {i}. {rec}")

# Summary
print("\n" + "="*70)
print("SUMMARY: What Each Testing Layer Catches")
print("="*70)
print("\nAutomated API Schema Validation (Postman, pytest):")
print("  ✓ Catches: Structure errors, missing fields, wrong data types")
print("  ✗ Misses: Inappropriate content, hidden field values, context issues")

print("\nManual QA Testing in UI:")
print("  ✓ Catches: User-visible problems like test statuses in dropdowns")
print("  ✗ Limitations: Time-consuming, inconsistent, doesn't scale")

print("\nQuality Intelligence (This Tool):")
print("  ✓ Catches: Context-inappropriate data, hidden fields, logic errors")
print("  ✓ Automates: Human-like quality assessment at API level")
print("  ✓ Scale: Every API response, every test run")

print("\n" + "="*70)
print("REAL IMPACT: Prevents unprofessional UI before users see it")
print("="*70 + "\n")
