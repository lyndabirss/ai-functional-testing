# ⚠️ This Repository Has Been Superseded

> **This project has been rebuilt and greatly improved as [ai-toolkit](https://github.com/lyndabirss/ai-toolkit)**

---

## What Changed?

The original separate scripts have been integrated into a unified toolkit with:

- ✅ **All original functionality** (API validation, quality intelligence)
- ✅ **Plus code analysis** (new capability)
- ✅ **10 security protections** (rate limiting, path traversal prevention, audit logging, input/output sanitization, etc.)
- ✅ **Unified CLI** (single entry point for all tools)
- ✅ **Cost optimization** (intelligent Haiku/Sonnet selection)
- ✅ **Modular architecture** (shared security infrastructure, easy to extend)

---

## Migration

**Old approach:**
```bash
# Separate scripts, duplicated setup
python checker.py response.json schema.json
```

**New approach:**
```bash
# Unified CLI, consistent interface
python main.py validate response.json schema.json
python main.py analyze code.py --mode security
```

---

## Why the Rebuild?

After building these initial scripts, I recognized:
- Separate scripts meant duplicated API setup and error handling
- No shared security infrastructure
- Difficult to maintain and extend
- Inconsistent user experience

The new [ai-toolkit](https://github.com/lyndabirss/ai-toolkit) addresses all of these with a modular, production-ready architecture.

**→ Please use [ai-toolkit](https://github.com/lyndabirss/ai-toolkit) for all new work.**