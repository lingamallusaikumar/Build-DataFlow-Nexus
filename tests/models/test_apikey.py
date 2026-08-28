import pytest
from app.domain_models.apikey import ApiKey

def test_apikey_creation():
    instance = ApiKey()
    assert instance.id is not None
    assert instance.is_deleted is False
    assert instance.version == 1

def test_apikey_to_dict():
    instance = ApiKey()
    d = instance.to_dict()
    assert 'id' in d
    assert 'created_at' in d
    assert 'updated_at' in d

def test_apikey_soft_delete(mocker):
    mocker.patch('app.extensions.db.session.commit')
    instance = ApiKey()
    instance.soft_delete()
    assert instance.is_deleted is True

def test_apikey_attribute_1_validation():
    instance = ApiKey(attribute_1="test_value")
    assert instance.attribute_1 == "test_value"

def test_apikey_attribute_2_validation():
    instance = ApiKey(attribute_2="test_value")
    assert instance.attribute_2 == "test_value"

def test_apikey_attribute_3_validation():
    instance = ApiKey(attribute_3="test_value")
    assert instance.attribute_3 == "test_value"

def test_apikey_attribute_4_validation():
    instance = ApiKey(attribute_4="test_value")
    assert instance.attribute_4 == "test_value"

def test_apikey_attribute_5_validation():
    instance = ApiKey(attribute_5="test_value")
    assert instance.attribute_5 == "test_value"

def test_apikey_attribute_6_validation():
    instance = ApiKey(attribute_6="test_value")
    assert instance.attribute_6 == "test_value"

def test_apikey_attribute_7_validation():
    instance = ApiKey(attribute_7="test_value")
    assert instance.attribute_7 == "test_value"

def test_apikey_attribute_8_validation():
    instance = ApiKey(attribute_8="test_value")
    assert instance.attribute_8 == "test_value"

def test_apikey_attribute_9_validation():
    instance = ApiKey(attribute_9="test_value")
    assert instance.attribute_9 == "test_value"

def test_apikey_attribute_10_validation():
    instance = ApiKey(attribute_10="test_value")
    assert instance.attribute_10 == "test_value"

def test_apikey_attribute_11_validation():
    instance = ApiKey(attribute_11="test_value")
    assert instance.attribute_11 == "test_value"

def test_apikey_attribute_12_validation():
    instance = ApiKey(attribute_12="test_value")
    assert instance.attribute_12 == "test_value"

def test_apikey_attribute_13_validation():
    instance = ApiKey(attribute_13="test_value")
    assert instance.attribute_13 == "test_value"

def test_apikey_attribute_14_validation():
    instance = ApiKey(attribute_14="test_value")
    assert instance.attribute_14 == "test_value"

def test_apikey_attribute_15_validation():
    instance = ApiKey(attribute_15="test_value")
    assert instance.attribute_15 == "test_value"

def test_apikey_attribute_16_validation():
    instance = ApiKey(attribute_16="test_value")
    assert instance.attribute_16 == "test_value"

def test_apikey_attribute_17_validation():
    instance = ApiKey(attribute_17="test_value")
    assert instance.attribute_17 == "test_value"

def test_apikey_attribute_18_validation():
    instance = ApiKey(attribute_18="test_value")
    assert instance.attribute_18 == "test_value"

def test_apikey_attribute_19_validation():
    instance = ApiKey(attribute_19="test_value")
    assert instance.attribute_19 == "test_value"

def test_apikey_attribute_20_validation():
    instance = ApiKey(attribute_20="test_value")
    assert instance.attribute_20 == "test_value"

def test_apikey_attribute_21_validation():
    instance = ApiKey(attribute_21="test_value")
    assert instance.attribute_21 == "test_value"

def test_apikey_attribute_22_validation():
    instance = ApiKey(attribute_22="test_value")
    assert instance.attribute_22 == "test_value"

def test_apikey_attribute_23_validation():
    instance = ApiKey(attribute_23="test_value")
    assert instance.attribute_23 == "test_value"

def test_apikey_attribute_24_validation():
    instance = ApiKey(attribute_24="test_value")
    assert instance.attribute_24 == "test_value"

def test_apikey_attribute_25_validation():
    instance = ApiKey(attribute_25="test_value")
    assert instance.attribute_25 == "test_value"

def test_apikey_attribute_26_validation():
    instance = ApiKey(attribute_26="test_value")
    assert instance.attribute_26 == "test_value"

def test_apikey_attribute_27_validation():
    instance = ApiKey(attribute_27="test_value")
    assert instance.attribute_27 == "test_value"

def test_apikey_attribute_28_validation():
    instance = ApiKey(attribute_28="test_value")
    assert instance.attribute_28 == "test_value"

def test_apikey_attribute_29_validation():
    instance = ApiKey(attribute_29="test_value")
    assert instance.attribute_29 == "test_value"

def test_apikey_attribute_30_validation():
    instance = ApiKey(attribute_30="test_value")
    assert instance.attribute_30 == "test_value"

def test_apikey_attribute_31_validation():
    instance = ApiKey(attribute_31="test_value")
    assert instance.attribute_31 == "test_value"

def test_apikey_attribute_32_validation():
    instance = ApiKey(attribute_32="test_value")
    assert instance.attribute_32 == "test_value"

def test_apikey_attribute_33_validation():
    instance = ApiKey(attribute_33="test_value")
    assert instance.attribute_33 == "test_value"

def test_apikey_attribute_34_validation():
    instance = ApiKey(attribute_34="test_value")
    assert instance.attribute_34 == "test_value"

def test_apikey_attribute_35_validation():
    instance = ApiKey(attribute_35="test_value")
    assert instance.attribute_35 == "test_value"

def test_apikey_attribute_36_validation():
    instance = ApiKey(attribute_36="test_value")
    assert instance.attribute_36 == "test_value"

def test_apikey_attribute_37_validation():
    instance = ApiKey(attribute_37="test_value")
    assert instance.attribute_37 == "test_value"

def test_apikey_attribute_38_validation():
    instance = ApiKey(attribute_38="test_value")
    assert instance.attribute_38 == "test_value"

def test_apikey_attribute_39_validation():
    instance = ApiKey(attribute_39="test_value")
    assert instance.attribute_39 == "test_value"

def test_apikey_attribute_40_validation():
    instance = ApiKey(attribute_40="test_value")
    assert instance.attribute_40 == "test_value"

def test_apikey_attribute_41_validation():
    instance = ApiKey(attribute_41="test_value")
    assert instance.attribute_41 == "test_value"

def test_apikey_attribute_42_validation():
    instance = ApiKey(attribute_42="test_value")
    assert instance.attribute_42 == "test_value"

def test_apikey_attribute_43_validation():
    instance = ApiKey(attribute_43="test_value")
    assert instance.attribute_43 == "test_value"

def test_apikey_attribute_44_validation():
    instance = ApiKey(attribute_44="test_value")
    assert instance.attribute_44 == "test_value"

def test_apikey_attribute_45_validation():
    instance = ApiKey(attribute_45="test_value")
    assert instance.attribute_45 == "test_value"

def test_apikey_attribute_46_validation():
    instance = ApiKey(attribute_46="test_value")
    assert instance.attribute_46 == "test_value"

def test_apikey_attribute_47_validation():
    instance = ApiKey(attribute_47="test_value")
    assert instance.attribute_47 == "test_value"

def test_apikey_attribute_48_validation():
    instance = ApiKey(attribute_48="test_value")
    assert instance.attribute_48 == "test_value"

def test_apikey_attribute_49_validation():
    instance = ApiKey(attribute_49="test_value")
    assert instance.attribute_49 == "test_value"

def test_apikey_attribute_50_validation():
    instance = ApiKey(attribute_50="test_value")
    assert instance.attribute_50 == "test_value"
