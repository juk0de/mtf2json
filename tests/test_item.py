import pytest
from mtf2json.items import (
    item,
    ItemClass,
    ItemCategory,
    ItemTechBase,
    ItemTag,
    ItemEntry,
    ItemError,
)


def test_item_category_validation() -> None:
    """
    Try to create items with valid and invalid categories.
    Expect validation errors.
    """
    # Test with valid category
    valid_item = item(
        _name="Test Weapon",
        _category=(ItemClass.WEAPON, ItemCategory.ENERGY),
        _tech_base=ItemTechBase.IS,
        _mtf_names=["TestWeapon"],
    )
    assert valid_item.category == (ItemClass.WEAPON, ItemCategory.ENERGY)

    # Test with invalid ItemClass
    with pytest.raises(ItemError):
        invalid_item_class = item(
            _name="Invalid Weapon",
            _category=("InvalidClass", ItemCategory.ENERGY),  # type: ignore[arg-type]
            _tech_base=ItemTechBase.IS,
            _mtf_names=["InvalidWeapon"],
        )
        print(invalid_item_class)  # silence ruff

    # Test with invalid ItemCategory
    with pytest.raises(ItemError):
        invalid_item_category = item(
            _name="Invalid Weapon",
            _category=(ItemClass.WEAPON, "InvalidCategory"),  # type: ignore[arg-type]
            _tech_base=ItemTechBase.IS,
            _mtf_names=["InvalidWeapon"],
        )
        print(invalid_item_category)  # silence ruff


def test_item_tech_base_validation() -> None:
    """
    Try to create items with valid and invalid tech bases.
    Expect validation errors.
    """
    # Test with valid tech base
    valid_item = item(
        _name="Test Equipment",
        _category=(ItemClass.EQUIPMENT, ItemCategory.ELECTRONICS),
        _tech_base=ItemTechBase.CLAN,
        _mtf_names=["TestEquipment"],
    )
    assert valid_item.tech_base == ItemTechBase.CLAN

    # Test with invalid tech base
    with pytest.raises(ItemError):
        invalid_tech_base_item = item(
            _name="Invalid Equipment",
            _category=(ItemClass.EQUIPMENT, ItemCategory.ELECTRONICS),
            _tech_base="InvalidTechBase",  # type: ignore[arg-type]
            _mtf_names=["InvalidEquipment"],
        )
        print(invalid_tech_base_item)  # silence ruff


def test_item_tags_validation() -> None:
    """
    Try to create items with valid and invalid tags.
    Expect validation errors.
    """
    # Test with valid tags
    valid_item = item(
        _name="Tagged Equipment",
        _category=(ItemClass.EQUIPMENT, ItemCategory.ELECTRONICS),
        _tech_base=ItemTechBase.CLAN,
        _mtf_names=["TaggedEquipment"],
        _tags=[ItemTag.OMNIPOD, ItemTag.ARMORED],
    )
    assert valid_item.tags == [ItemTag.OMNIPOD, ItemTag.ARMORED]

    # Test with invalid tag
    with pytest.raises(ItemError):
        invalid_tag_item = item(
            _name="Invalid Tagged Equipment",
            _category=(ItemClass.EQUIPMENT, ItemCategory.ELECTRONICS),
            _tech_base=ItemTechBase.CLAN,
            _mtf_names=["InvalidTaggedEquipment"],
            _tags=["InvalidTag"],  # type: ignore[list-item]
        )
        print(invalid_tag_item)  # silence ruff

    # Try adding invalid tag
    with pytest.raises(ItemError):
        valid_item.add_tag("InvalidTag")  # type: ignore[arg-type]


def test_item_entry_validation() -> None:
    """
    Try to create items with valid and invalid entry types.
    Expect validation errors.
    """
    # Test with valid entry type
    valid_item = item(
        _name="Test Equipment",
        _category=(ItemClass.EQUIPMENT, ItemCategory.ELECTRONICS),
        _tech_base=ItemTechBase.CLAN,
        _mtf_names=["TestEquipment"],
        _entry=ItemEntry.ONCE,
    )
    assert valid_item.entry == ItemEntry.ONCE

    # Test with invalid entry type
    with pytest.raises(ItemError):
        invalid_entry_item = item(
            _name="Invalid Equipment",
            _category=(ItemClass.EQUIPMENT, ItemCategory.ELECTRONICS),
            _tech_base=ItemTechBase.CLAN,
            _mtf_names=["InvalidEquipment"],
            _entry="InvalidEntry",  # type: ignore[arg-type]
        )
        print(invalid_entry_item)  # silence ruff
