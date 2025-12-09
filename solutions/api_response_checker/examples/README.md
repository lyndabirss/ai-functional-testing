# Examples - Real-World Testing Scenarios

These examples demonstrate Quality Intelligence in action using real recruitment system testing scenarios.

## Running the Examples

### Interactive Menu
```bash
python demo.py
```
Shows menu where you can select which example to run.

### Run All Examples
```bash
python demo.py --all
```
Runs all 4 examples in sequence.

### Quick Demo (Example 1 only)
```bash
python demo.py --quick
```
Runs just the first example for a quick demonstration.

### Run Individual Examples
```bash
cd examples
python example_1_candidate_status_hidden_fields.py
```

---

## The 4 Examples

### Example 1: Candidate Status Dropdown
**File:** `example_1_candidate_status_hidden_fields.py`

**Real Problem:**
API returns status options for candidate dropdown, but includes internal test statuses (TEST_STATUS_INTERNAL, SYSTEM_ARCHIVED) that shouldn't be visible to recruiters.

**What Automated API Tests Check:**
- ✅ Valid JSON structure
- ✅ Required fields present
- ✅ Correct data types
- → Tests PASS

**What They Miss:**
- ✗ Internal/test values in user-facing dropdown
- ✗ Contextually inappropriate data
- ✗ Unprofessional UI appearance

**What Quality Intelligence Catches:**
- Identifies test/internal patterns in field labels
- Flags contextually inappropriate data
- Prevents unprofessional UI before deployment

**Real Impact:**
Prevents embarrassing "TEST_STATUS" values appearing in production dropdowns.

---

### Example 2: Candidate Search Results
**File:** `example_2_search_results_logical_consistency.py`

**Real Problem:**
Search API returns candidate counts with logical inconsistencies:
- Total candidates: 50
- Active candidates: 65 ← Impossible!

**What Automated API Tests Check:**
- ✅ Valid JSON structure
- ✅ All required fields present
- ✅ Correct data types (integers)
- → Tests PASS

**What They Miss:**
- ✗ Mathematical impossibilities
- ✗ Logical inconsistencies
- ✗ Data corruption indicators

**What Quality Intelligence Catches:**
- Analyzes logical relationships between fields
- Identifies mathematically impossible values
- Flags data corruption before it reaches users

**Real Impact:**
Prevents loss of trust in system accuracy, stops bad data reaching client reports.

---

### Example 3: Dashboard Statistics
**File:** `example_3_dashboard_stats_integration_gap.py`

**Real Problem:**
Dashboard polls statistics API for real-time updates. API returns data but missing timestamp field. Result: Postman tests pass, but UI can't determine if data is fresh and doesn't update display.

**What Automated Postman Tests Check:**
- ✅ API returns expected data fields
- ✅ Valid structure
- ✅ Reasonable values
- → Postman collection PASSES

**What Happens in the UI:**
- ✗ Dashboard shows stale data
- ✗ Refresh appears broken
- ✗ Users report "dashboard not updating"

**What They Miss:**
- ✗ Missing metadata UI needs
- ✗ Integration requirements
- ✗ Actual usability of response

**What Quality Intelligence Catches:**
- Tests against complete UI requirements, not just API schema
- Identifies missing fields that break integration
- Validates response usability, not just validity

**Real Impact:**
Catches "works in Postman, broken in app" issues at API test level instead of UAT.

---

### Example 4: User Authentication
**File:** `example_4_authentication_progressive_layers.py`

**Purpose:**
Shows how testing sophistication builds in layers, using login API as example.

**Layer 1: Structure Validation** (Basic automated testing)
- Checks: Valid JSON, required fields, correct types
- Speed: Very fast (~1ms)
- Catches: Obvious structural errors

**Layer 2+3: Quality Intelligence** (Enhanced testing)
- Checks: Security, appropriateness, best practices
- Speed: Moderate (~500ms-2s)
- Catches: Weak tokens, empty permissions, missing metadata

**Demonstrates:**
- When to use each testing layer
- Risk-based testing approach
- Progressive sophistication based on endpoint criticality

**Real Impact:**
Choose appropriate testing depth: full Quality Intelligence for high-risk endpoints (auth, payments), structure validation sufficient for low-risk lookups.

---

## What Each Example Shows

### Common Theme:
**Automated API schema validation catches structure errors.**
**Quality Intelligence catches context, logic, and integration errors.**

### The Testing Gap:
```
Traditional Automated API Tests:
  ✓ Is it valid JSON?
  ✓ Are required fields present?
  ✓ Are data types correct?
  → Tests pass, deploy to production
  → Users report: "This is broken/wrong/confusing"

Quality Intelligence:
  ✓ Everything above, PLUS:
  ✓ Are values contextually appropriate?
  ✓ Do related fields make logical sense?
  ✓ Does this meet UI/integration requirements?
  → Catches issues before deployment
```

### Real-World Value:
- **Example 1:** Prevents unprofessional UI
- **Example 2:** Catches data corruption
- **Example 3:** Finds integration gaps
- **Example 4:** Secures critical endpoints

---

## Understanding the Output

Each example shows three sections:

### 1. Automated API Schema Validation
What your existing Postman/pytest tests check:
- Structure
- Types
- Required fields

### 2. The Problem Automated Tests Miss
What passes validation but is actually wrong:
- Logic errors
- Context issues
- Integration gaps

### 3. Quality Intelligence Analysis
What AI-powered assessment catches:
- Quality score (0-100)
- Specific issues with severity
- Actionable recommendations

---

## Terminology Used

These examples use explicit terminology about testing types to avoid confusion:

**"Automated API schema validation"**
- Postman collections
- pytest with jsonschema
- CI/CD pipeline checks

**"Manual QA review"**
- Human tester checking UI
- Manual Postman exploration
- User acceptance testing

**"Quality Intelligence"**
- This tool
- Automated + AI-powered
- Context-aware validation

---

## Adapting These Examples

These examples use recruitment scenarios but the patterns apply universally:

**Hidden Fields** → Any internal data exposed to users
**Logical Inconsistency** → Any impossible mathematical relationships
**Integration Gap** → Any missing fields that break downstream systems
**Progressive Layers** → Risk-based testing for any endpoint

Change the domain (e-commerce, healthcare, finance) but keep the testing patterns.

---

## Next Steps

1. **Run the examples** - See Quality Intelligence in action
2. **Adapt to your domain** - Replace recruitment scenarios with your API examples
3. **Integrate into tests** - Add quality checking to your test suite
4. **Start with critical endpoints** - Apply to high-risk APIs first

---

**Built by:** Lynda M Birss  
**Purpose:** Demonstrate practical Quality Intelligence in QA workflows
