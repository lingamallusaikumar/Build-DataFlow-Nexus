import pytest
from app.domain_services.dataset_service import DatasetService
from app.domain_models.dataset import Dataset

def test_dataset_service_get_all(mocker):
    mocker.patch('app.domain_models.dataset.Dataset.query')
    result = DatasetService.get_all()
    assert result is not None

def test_dataset_service_create(mocker):
    mocker.patch('app.extensions.db.session.add')
    mocker.patch('app.extensions.db.session.commit')
    data = {'attribute_1': 'val'}
    record = DatasetService.create(data)
    assert record.attribute_1 == 'val'

def test_dataset_service_update(mocker):
    mocker.patch('app.extensions.db.session.commit')
    mock_get = mocker.patch('app.domain_services.dataset_service.DatasetService.get_by_id')
    mock_instance = Dataset()
    mock_get.return_value = mock_instance
    
    updated = DatasetService.update('123', {'attribute_1': 'new_val'})
    assert updated.attribute_1 == 'new_val'
