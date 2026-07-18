from src.core.application_impact import add_impact_record, make_impact_record, make_impact_store

def test_impact_record_fields():
    record = make_impact_record(impact_id='IMP-001', interaction_point='calculator_screen', before_behavior='No calculation result shown', after_behavior='Calculation result displayed with path id', validation_reference='test_gui_trigger_success')
    assert record['impact_id'] == 'IMP-001'
    assert record['validation_reference'] == 'test_gui_trigger_success'

def test_impact_store_lists_records():
    store = make_impact_store()
    add_impact_record(store, make_impact_record(impact_id='IMP-001', interaction_point='calculator_screen', before_behavior='before', after_behavior='after', validation_reference='ref'))
    assert len(store) == 1