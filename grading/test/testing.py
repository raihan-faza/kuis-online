from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Test grading fully
# def test_1():
#     response = client.post("localhost:8080/grade", json={"user_id": 123, "quiz_id": 456, "questions": "[{\"id\":1,\"correct_id\":2},{\"id\":2,\"correct_id\":3}]", "user_answers": "[{\"q_id\":1,\"answer\":\"correct\"},{\"q_id\":2,\"answer\":\"incorrect\"}]", "correct_answers": "[{\"id\":1,\"text\":\"false\"},{\"id\":2,\"text\":\"correct\"},{\"id\":3,\"text\":\"true\"}]", "points": 10 })
#     # assert response.status_code == 409
#     assert response.json() == {
#         "message": "Succeed"
#     }

# Testing on simulation
def test_2():
    response = client.post("localhost:8080/simulation", json={"user_id": 123, "quiz_id": 456, "questions": "[{\"id\":1,\"correct_id\":2},{\"id\":2,\"correct_id\":3}]", "user_answers": "[{\"q_id\":1,\"answer\":\"correct\"},{\"q_id\":2,\"answer\":\"incorrect\"}]", "correct_answers": "[{\"id\":1,\"text\":\"false\"},{\"id\":2,\"text\":\"correct\"},{\"id\":3,\"text\":\"true\"}]", "points": 10})
    assert response.json() == {
        "message": "Simulation Succeed"
    }