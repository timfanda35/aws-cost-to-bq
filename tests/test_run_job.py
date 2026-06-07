import pytest
from unittest.mock import patch
import run_job


def _make_env():
    return {
        "SOURCE_TYPE": "s3",
        "SOURCE_BUCKET": "src-bucket",
        "SOURCE_PREFIX": "exports",
        "EXPORT_NAME": "my-export",
        "GCS_BUCKET": "dest-bucket",
        "GCS_DESTINATION_PREFIX": "billing",
        "BQ_PROJECT_ID": "my-project",
        "BQ_DATASET_ID": "billing",
        "BQ_TABLE_ID": "daily",
        "AWS_REGION": "us-east-1",
    }


def test_job_exits_zero_on_success(monkeypatch):
    for k, v in _make_env().items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv("PARTITION", raising=False)

    with patch("run_job.run_pipeline", return_value={"run_id": "20260607-1234567890"}) as mock_pipeline:
        with pytest.raises(SystemExit) as exc_info:
            run_job.main()
        assert exc_info.value.code == 0
    mock_pipeline.assert_called_once_with(partition=None)


def test_job_exits_one_on_failure(monkeypatch):
    for k, v in _make_env().items():
        monkeypatch.setenv(k, v)
    monkeypatch.delenv("PARTITION", raising=False)

    with patch("run_job.run_pipeline", side_effect=RuntimeError("pipeline exploded")):
        with pytest.raises(SystemExit) as exc_info:
            run_job.main()
        assert exc_info.value.code == 1


def test_job_passes_partition_env_var(monkeypatch):
    for k, v in _make_env().items():
        monkeypatch.setenv(k, v)
    monkeypatch.setenv("PARTITION", "2026-04")

    with patch("run_job.run_pipeline", return_value={"run_id": "20260607-1234567890"}) as mock_pipeline:
        with pytest.raises(SystemExit) as exc_info:
            run_job.main()
        assert exc_info.value.code == 0
    mock_pipeline.assert_called_once_with(partition="2026-04")
