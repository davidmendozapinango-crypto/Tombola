from pathlib import Path


def test_acceptance_evidence_checklist_exists():
    """Placeholder checklist verifying FR/SC traceability exists in quickstart."""
    quickstart = Path('specs/001-define-calculation-rules/quickstart.md')
    assert quickstart.exists()
    content = quickstart.read_text(encoding='utf-8')
    assert 'Validation Scenarios' in content
    assert 'Automated Verification' in content