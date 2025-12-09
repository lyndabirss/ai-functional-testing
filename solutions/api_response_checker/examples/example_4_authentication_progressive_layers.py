"""
Example 4: User Authentication - Progressive Testing Layers

REAL SCENARIO: Login API Security and Reliability
==================================================

Your recruitment system login endpoint authenticates users and returns:
- User account details
- Authentication token for API access
- Account permissions/roles
- Session metadata

This is critical security infrastructure - must be bulletproof.

THE PROGRESSION:
================
This example shows how testing sophistication builds in layers:

Layer 1: Structure Validation (Basic automated testing)
  → "Is it valid JSON with expected fields?"

Layer 2: Quality Assessment (Enhanced automated testing)  
  → "Are the values appropriate and secure?"

Layer 3: Intelligence (Context-aware testing)
  → "Does this meet security best practices?"

WHY THIS MATTERS:
=================
Login API vulnerabilities or poor responses cause:
- Security breaches (weak tokens, missing permissions)
- User lockouts (invalid session data)
- Support burden (users can't access system)
- Compliance failures (audit trail missing)

Let's see how different testing approaches catch different issues.
"""

from checker import ResponseQualityChecker
import json

# The API endpoint we're testing
print("="*70)
print("EXAMPLE 4: User Authentication - Progressive Testing Layers")
print("="*70)
print("\nAPI Endpoint: POST /api/auth/login")
print("Purpose: Authenticate user and return session data")
print("="*70)

# Define schema (what structure we expect)
login_response_schema = {
    "type": "object",
    "required": ["user_id", "username", "email", "token", "permissions", "session_expires_at"],
    "properties": {
        "user_id": {"type": "integer"},
        "username": {"type": "string"},
        "email": {"type": "string"},
        "token": {"type": "string"},
        "permissions": {"type": "array"},
        "session_expires_at": {"type": "string"}
    }
}

# Three different API responses to test
responses_to_test = [
    {
        "name": "Perfect Response",
        "response": {
            "user_id": 12345,
            "username": "john.smith",
            "email": "john.smith@example.com",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U",
            "permissions": ["view_candidates", "create_jobs", "manage_team"],
            "session_expires_at": "2024-12-10T14:30:00Z"
        }
    },
    {
        "name": "Structurally Valid But Insecure",
        "response": {
            "user_id": 12345,
            "username": "john.smith",
            "email": "john.smith@example.com",
            "token": "abc123",  # ← Too short, not JWT format
            "permissions": [],   # ← Empty permissions!
            "session_expires_at": "2024-12-10T14:30:00Z"
        }
    },
    {
        "name": "Missing Critical Field",
        "response": {
            "user_id": 12345,
            "username": "john.smith",
            "email": "john.smith@example.com",
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.dozjgNryP4J3jVmNHl0w5N_XgL0n3I9PlFUP0THsR8U"
            # Missing: permissions and session_expires_at
        }
    }
]

checker = ResponseQualityChecker()

# Test each response
for idx, test_case in enumerate(responses_to_test, 1):
    print(f"\n{'='*70}")
    print(f"TEST CASE {idx}: {test_case['name']}")
    print("="*70)
    
    response = test_case['response']
    
    # Layer 1: Structure Validation
    print("\nLAYER 1: STRUCTURE VALIDATION (Basic automated testing)")
    print("-" * 70)
    print("What it checks: JSON syntax, required fields, data types")
    print("\nRunning automated schema validation...")
    
    structure_result = checker.validate_structure(response, login_response_schema)
    
    if structure_result.is_valid:
        print("✓ PASSED - Structure is valid")
        print("  • Valid JSON")
        print("  • All required fields present")
        print("  • Correct data types")
    else:
        print("✗ FAILED - Structure problems detected:")
        for error in structure_result.errors:
            print(f"  • {error}")
    
    # Only do quality check if structure is valid
    if structure_result.is_valid:
        # Layer 2 & 3: Quality + Intelligence
        print("\nLAYER 2+3: QUALITY INTELLIGENCE (Enhanced testing)")
        print("-" * 70)
        print("What it checks: Security, appropriateness, best practices")
        print("\nRunning AI-powered quality assessment...")
        
        full_result = checker.check_response(response, login_response_schema)
        
        print(f"\nQuality Score: {full_result.quality.score}/100")
        
        if full_result.quality.score >= 90:
            print("✓ EXCELLENT - Production-ready")
        elif full_result.quality.score >= 75:
            print("⚠️  GOOD - Minor issues to address")
        elif full_result.quality.score >= 60:
            print("⚠️  ACCEPTABLE - Several issues to fix")
        else:
            print("✗ POOR - Significant problems detected")
        
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
    else:
        print("\n⚠️  Skipping quality check - fix structure issues first")

# Final Summary
print("\n" + "="*70)
print("SUMMARY: Progressive Testing Layers")
print("="*70)

print("\nLAYER 1: STRUCTURE VALIDATION")
print("Technology: jsonschema, basic automated tests")
print("Speed: Very fast (~1ms)")
print("Catches:")
print("  ✓ Missing required fields")
print("  ✓ Wrong data types (string instead of integer)")
print("  ✓ Invalid JSON syntax")
print("Misses:")
print("  ✗ Weak security (short tokens, empty permissions)")
print("  ✗ Business logic errors (inappropriate values)")
print("  ✗ Integration requirements (missing metadata)")

print("\nLAYER 2+3: QUALITY INTELLIGENCE")
print("Technology: Claude API + context-aware analysis")
print("Speed: Moderate (~500ms-2s)")
print("Catches:")
print("  ✓ Everything Layer 1 catches, PLUS:")
print("  ✓ Security issues (weak tokens, missing permissions)")
print("  ✓ Business logic problems (empty arrays, invalid states)")
print("  ✓ Best practice violations (missing timestamps, no expiry)")
print("  ✓ Integration concerns (missing required metadata)")

print("\n" + "="*70)
print("THE PROGRESSION IN PRACTICE")
print("="*70)
print("\nStartup/MVP Phase:")
print("  → Layer 1 only: Fast, catches obvious errors")
print("  → Good enough for rapid iteration")

print("\nGrowth Phase:")
print("  → Add Layer 2+3 to critical endpoints (auth, payments)")
print("  → Catches security and quality issues")
print("  → Prevents customer-impacting bugs")

print("\nEnterprise Phase:")
print("  → Layer 2+3 on all endpoints")
print("  → Comprehensive quality assurance")
print("  → Compliance and security requirements met")

print("\n" + "="*70)
print("REAL IMPACT: Choose testing depth based on risk")
print("="*70)
print("\nHigh-risk endpoints (auth, payments, PII):")
print("  → Use full Quality Intelligence")
print("  → Catch security and compliance issues")
print("\nMedium-risk endpoints (search, lists):")
print("  → Use Quality Intelligence on complex responses")
print("  → Structure validation on simple responses")
print("\nLow-risk endpoints (static data, lookups):")
print("  → Structure validation sufficient")
print("="*70 + "\n")
