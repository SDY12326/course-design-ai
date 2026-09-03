import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fastapi.testclient import TestClient
from backend.main import app
from model.train import make_dataset
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

def test_health_and_equipment():
    with TestClient(app) as client:
        assert client.get('/api/health').json()['status'] == 'ok'
        assets = client.get('/api/equipment').json()
        assert len(assets) >= 4 and 'latest' in assets[0]

def test_predict_persists_result():
    body = {'equipment_id': 'T-01', 'sensors': {'temperature': 96, 'vibration': 5.1, 'pressure': 205, 'rpm': 1510, 'oil_quality': 145, 'power': 118}}
    with TestClient(app) as client:
        result = client.post('/api/predict', json=body)
        assert result.status_code == 200
        payload = result.json()
        assert payload['is_risk'] is True and payload['anomaly_sensors']
        assert any(x['equipment_id'] == 'T-01' for x in client.get('/api/predictions').json())

def test_supervised_model_has_signal():
    X, y = make_dataset(240, 160)
    x_train, x_val, y_train, y_val = train_test_split(X, y, test_size=.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=30, max_depth=8, random_state=42, class_weight='balanced').fit(x_train, y_train)
    assert f1_score(y_val, model.predict(x_val)) > .9
