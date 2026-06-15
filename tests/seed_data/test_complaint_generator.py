from seed_data.generators.complaint_generator import generate_complaints

USER_IDS = [1, 2, 3]
BIKE_IDS = [4, 5, 6]
COMPLAINT_TYPE_IDS = [7, 8, 9, 10]


def test_generate_complaints_returns_correct_amount():
    complaints = generate_complaints(5, USER_IDS, BIKE_IDS, COMPLAINT_TYPE_IDS)
    assert len(complaints) == 5
    assert len(complaints) == 5
