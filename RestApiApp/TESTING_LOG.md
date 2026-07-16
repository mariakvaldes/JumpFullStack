# Testing Log

## Failure 1: BSON InvalidId
- **Date:** 2026-07-16
- **Error:** `bson.errors.InvalidId: '123' is not a valid ObjectId`
- **Cause:** Attempted to use "123" as an `account_id` in unit tests, but `account_service.py` requires a valid 24-character hex `ObjectId`.
- **Resolution:** Updated test cases to use a valid `ObjectId` hex string (`507f1f77bcf86cd799439011`).
- **Status:** Resolved (Tests passing)

## Improvement 1: Deprecation Warning
- **Date:** 2026-07-16
- **Warning:** `DeprecationWarning: datetime.utcnow() is deprecated`
- **Cause:** Using the legacy `datetime.utcnow()` method which is scheduled for removal.
- **Resolution:** Updated `account_service.py` to use `datetime.now(datetime.UTC)` to ensure timezone-aware compliance. Status: Tests passing, 0 warnings.