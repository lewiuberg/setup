from macsetup.sections.base import clear_items_cache
from macsetup.sections.registry import ALL_SECTIONS, SECTIONS_BY_SLUG
from macsetup.state import PlanState


def test_registry_has_unique_slugs() -> None:
    slugs = [s.slug for s in ALL_SECTIONS]
    assert len(slugs) == len(set(slugs))


def test_registry_indexed_by_slug() -> None:
    for s in ALL_SECTIONS:
        assert SECTIONS_BY_SLUG[s.slug] is s


def test_all_item_configs_resolve() -> None:
    clear_items_cache()
    for section in ALL_SECTIONS:
        if section.items_config is None:
            continue
        items = section.load_items()
        assert isinstance(items, list), f"{section.slug} did not load a list"


def test_initial_plan_state_enables_all_sections() -> None:
    clear_items_cache()
    state = PlanState.initial(ALL_SECTIONS)
    assert state.enabled_sections == {s.slug for s in ALL_SECTIONS}


def test_initial_plan_state_respects_item_defaults() -> None:
    clear_items_cache()
    state = PlanState.initial(ALL_SECTIONS)
    brews = SECTIONS_BY_SLUG["brews"].load_items()
    expected = {i.name for i in brews if i.default}
    assert state.enabled_items["brews"] == expected


def test_toggle_section_round_trip() -> None:
    clear_items_cache()
    state = PlanState.initial(ALL_SECTIONS)
    assert state.is_section_enabled("brews")
    state.toggle_section("brews")
    assert not state.is_section_enabled("brews")
    state.toggle_section("brews")
    assert state.is_section_enabled("brews")


def test_set_items_replaces_selection() -> None:
    clear_items_cache()
    state = PlanState.initial(ALL_SECTIONS)
    state.set_items("brews", ["git", "gh"])
    assert state.enabled_items["brews"] == {"git", "gh"}
    assert state.selected_count("brews") == 2
