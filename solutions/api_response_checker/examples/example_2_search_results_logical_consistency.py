"""
Example 2: Candidate Search Results - Logical Consistency Checking

REAL SCENARIO: Recruitment System Search API
=============================================

Recruiter searches for candidates matching "Java Developer, Edinburgh"
The search API returns results summary showing:
- Total candidates found
- Currently active candidates
- Candidates in interview process
- Recently placed candidates

THE PROBLEM:
Database corruption or query error causes inconsistent counts:
- Total candidates: 50
- Active candidates: 65  ← IMPOSSIBLE! Can't have more active than total
- In interview: 30
- Recently placed: 15

THE USER EXPERIENCE:
Recruiter sees impossible numbers and questions:
- Is the data reliable?
- Are candidates missing from my view?
- Can I trust this system for client reporting?

WHY AUTOMATED API TESTS MISS THIS:
===================================

Your automated pytest suite or Postman collection checks:
✓ HTTP 200 response
✓ Valid JSON structure  
✓ Required fields present (total, active, in_interview, placed)
✓ Correct data types (all integers)
✓ No null values
✓ Response time < 500ms
→ All automated checks PASS ✓

Manual QA tester reviewing the UI would immediately spot:
"This makes no sense - 65 active but only 50 total?"

This tool (Quality Intelligence) catches it automatically by:
- Analyzing logical relationships between fields
- Understanding that active_count ≤ total_count must be true
- Flagging mathematically impossible data
- Checking that sum of categories doesn't exceed total

THE VALUE:
==========
- Catches data corruption before recruiters see it
- Prevents loss of trust in system accuracy
- Stops bad data from reaching client reports
- Automates logical consistency checking
- Finds issues that pass all schema validation
"""

from checker import ResponseQualityChecker

# Schema that automated API tests validate against
# This checks STRUCTURE and TYPES only - not logical relationships
search_results_schema = {
    "type": "object",
    "required": ["query", "total_candidates", "active_candidates", "in_interview", "recently_placed"],
    "properties": {
        "query": {"type": "string"},
        "total_candidates": {"type": "integer"},
        "active_candidates": {"type": "integer"},
        "in_interview": {"type": "integer"},
        "recently_placed": {"type": "integer"}
    }
}

# What the API returns (with logical inconsistency)
api_response = {
    "query": "Java Developer, Edinburgh",
    "total_candidates": 50,
    "active_candidates": 65,      # ← IMPOSSIBLE! More active than total
    "in_interview": 30,
    "recently_placed": 15
}

print("="*70)
print("EXAMPLE 2: Candidate Search Results - Logical Consistency")
print("="*70)

# Initialize checker
checker = ResponseQualityChecker()

# Step 1: What automated API schema validation checks
print("\n1. AUTOMATED API SCHEMA VALIDATION (pytest/Postman):")
print("-" * 70)
structure_result = checker.validate_structure(api_response, search_results_schema)

if structure_result.is_valid:
    print("✓ Structure validation PASSED")
    print("  - Valid JSON structure")
    print("  - All required fields present")
    print("  - Correct data types (all integers)")
    print("  - No null values")
    print("  - Fields match schema definition")
    print("\n→ Automated CI/CD pipeline marks this as PASSING")
    print("→ Test report shows: 100% API tests passing ✓")
else:
    print("✗ Structure validation FAILED")

# Show the problem that automated tests miss
print("\n2. THE PROBLEM AUTOMATED TESTS DON'T CATCH:")
print("-" * 70)
print(f"Total candidates: {api_response['total_candidates']}")
print(f"Active candidates: {api_response['active_candidates']} ← More than total!")
print(f"In interview: {api_response['in_interview']}")
print(f"Recently placed: {api_response['recently_placed']}")
print(f"\nSum of categories: {api_response['active_candidates'] + api_response['in_interview'] + api_response['recently_placed']}")
print(f"Total candidates: {api_response['total_candidates']}")
print("\n⚠️  Mathematical impossibility: active_candidates > total_candidates")
print("⚠️  This indicates database corruption or query error")

# Step 3: What Quality Intelligence adds
print("\n3. QUALITY INTELLIGENCE ANALYSIS (This Tool + Claude API):")
print("-" * 70)
full_result = checker.check_response(api_response, search_results_schema)

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
print("\nAutomated API Schema Validation (pytest, Postman collections):")
print("  ✓ Catches: Missing fields, wrong types, null values, structure errors")
print("  ✗ Misses: Logical inconsistencies, impossible values, data corruption")

print("\nManual QA Review:")
print("  ✓ Catches: 'This doesn't make sense' - human intuition spots logic errors")
print("  ✗ Limitations: Can't review every API response, slow, doesn't scale")

print("\nQuality Intelligence (This Tool):")
print("  ✓ Catches: Logical inconsistencies, impossible relationships")
print("  ✓ Validates: Mathematical relationships between fields")
print("  ✓ Automates: Human-like logic checking at scale")

print("\n" + "="*70)
print("REAL IMPACT: Prevents data corruption reaching recruiters and clients")
print("="*70)
print("\nBUSINESS CONSEQUENCES OF MISSING THIS:")
print("  • Recruiters lose trust in system accuracy")
print("  • Bad data in client reports damages credibility")
print("  • Time wasted investigating 'phantom' candidates")
print("  • Potential compliance issues with incorrect reporting")
print("="*70 + "\n")
