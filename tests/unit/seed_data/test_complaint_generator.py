import datetime as dt
import pytest
from dateutil.relativedelta import relativedelta
from seed_data.generators.complaint_generator import generate_complaints

USER_IDS = [1, 2, 3]
BIKE_IDS = [4, 5, 6]
COMPLAINT_TYPE_IDS = [7, 8, 9, 10]


def test_generate_complaints_returns_correct_amount():
    complaints = generate_complaints(5, USER_IDS, BIKE_IDS, COMPLAINT_TYPE_IDS)
    assert len(complaints) == 5


def test_generate_zero_complaints_returns_empty_list():
    complaints = generate_complaints(0, USER_IDS, BIKE_IDS, COMPLAINT_TYPE_IDS)
    assert complaints == []


def test_generate_negative_complaints_raises_value_error():
    with pytest.raises(ValueError):
        generate_complaints(-1, USER_IDS, BIKE_IDS, COMPLAINT_TYPE_IDS)


def test_generated_complaints_use_existing_ids():
    complaints = generate_complaints(10, USER_IDS, BIKE_IDS, COMPLAINT_TYPE_IDS)

    for complaint in complaints:
        assert complaint.user_id in USER_IDS
        assert complaint.bike_id in BIKE_IDS
        assert complaint.complaint_type_id in COMPLAINT_TYPE_IDS


def test_generated_complaints_use_correct_date_range():
    complaints = generate_complaints(10, USER_IDS, BIKE_IDS, COMPLAINT_TYPE_IDS)
    now = dt.datetime.now()

    for complaint in complaints:
        assert (
            (now - relativedelta(months=6))
            <= dt.datetime.strptime(complaint.report_date, "%Y-%m-%d %H:%M:%S")
            <= now
        )
