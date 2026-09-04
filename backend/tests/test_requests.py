"""Tests for the requests API endpoints."""
import pytest


class TestCreateRequest:
    """Tests for POST /api/requests endpoint."""

    def test_create_request_success(self, client):
        """Test successful request creation."""
        response = client.post(
            "/api/requests/",
            json={
                "title": "Add dark mode",
                "problem_statement": "Users want a dark theme option",
                "expected_impact": "Improved user experience for night-time usage",
                "urgency": 3,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Add dark mode"
        assert data["status"] == "new"
        assert data["decision_reason"] is None

    def test_create_request_missing_title(self, client):
        """Test error when title is missing."""
        response = client.post(
            "/api/requests/",
            json={
                "problem_statement": "Some problem",
                "expected_impact": "Some impact",
                "urgency": 2,
            },
        )
        assert response.status_code == 422
        assert "title" in response.text.lower()

    def test_create_request_empty_title(self, client):
        """Test error when title is empty string."""
        response = client.post(
            "/api/requests/",
            json={
                "title": "",
                "problem_statement": "Some problem",
                "expected_impact": "Some impact",
                "urgency": 2,
            },
        )
        assert response.status_code == 422

    def test_create_request_missing_problem_statement(self, client):
        """Test error when problem_statement is missing."""
        response = client.post(
            "/api/requests/",
            json={
                "title": "Some title",
                "expected_impact": "Some impact",
                "urgency": 2,
            },
        )
        assert response.status_code == 422

    def test_create_request_invalid_urgency_too_low(self, client):
        """Test error when urgency is below valid range."""
        response = client.post(
            "/api/requests/",
            json={
                "title": "Some title",
                "problem_statement": "Some problem",
                "expected_impact": "Some impact",
                "urgency": 0,
            },
        )
        assert response.status_code == 422

    def test_create_request_invalid_urgency_too_high(self, client):
        """Test error when urgency is above valid range."""
        response = client.post(
            "/api/requests/",
            json={
                "title": "Some title",
                "problem_statement": "Some problem",
                "expected_impact": "Some impact",
                "urgency": 5,
            },
        )
        assert response.status_code == 422

    def test_create_request_strips_whitespace(self, client):
        """Test that whitespace is stripped from string fields."""
        response = client.post(
            "/api/requests/",
            json={
                "title": "  Trimmed title  ",
                "problem_statement": "  Trimmed statement  ",
                "expected_impact": "  Trimmed impact  ",
                "urgency": 2,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Trimmed title"
        assert data["problem_statement"] == "Trimmed statement"
        assert data["expected_impact"] == "Trimmed impact"


class TestGetRequest:
    """Tests for GET /api/requests/{id} endpoint."""

    def test_get_request_success(self, client):
        """Test successful request retrieval."""
        # Create a request first
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Test request",
                "problem_statement": "Test problem",
                "expected_impact": "Test impact",
                "urgency": 1,
            },
        )
        request_id = create_response.json()["id"]

        # Get the request
        response = client.get(f"/api/requests/{request_id}")
        assert response.status_code == 200
        assert response.json()["title"] == "Test request"

    def test_get_request_not_found(self, client):
        """Test error when request does not exist."""
        response = client.get("/api/requests/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_request_invalid_uuid(self, client):
        """Test error when request ID is not a valid UUID."""
        response = client.get("/api/requests/invalid-uuid")
        assert response.status_code == 422


class TestListRequests:
    """Tests for GET /api/requests endpoint."""

    def test_list_requests_empty(self, client):
        """Test listing requests when none exist."""
        response = client.get("/api/requests/")
        assert response.status_code == 200
        data = response.json()
        assert data["items"] == []
        assert data["total"] == 0

    def test_list_requests_with_data(self, client):
        """Test listing requests returns created requests."""
        # Create two requests
        client.post(
            "/api/requests/",
            json={
                "title": "Request 1",
                "problem_statement": "Problem 1",
                "expected_impact": "Impact 1",
                "urgency": 1,
            },
        )
        client.post(
            "/api/requests/",
            json={
                "title": "Request 2",
                "problem_statement": "Problem 2",
                "expected_impact": "Impact 2",
                "urgency": 2,
            },
        )

        response = client.get("/api/requests/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2

    def test_list_requests_filter_by_status(self, client):
        """Test filtering requests by status."""
        # Create a request
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 1,
            },
        )
        request_id = create_response.json()["id"]

        # Make a decision
        client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "accepted", "decision_reason": "Good idea"},
        )

        # Filter by status
        response = client.get("/api/requests/?status=accepted")
        assert response.status_code == 200
        assert response.json()["total"] == 1

        response = client.get("/api/requests/?status=new")
        assert response.status_code == 200
        assert response.json()["total"] == 0

    def test_list_requests_filter_by_urgency(self, client):
        """Test filtering requests by urgency."""
        client.post(
            "/api/requests/",
            json={
                "title": "Urgent",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 4,
            },
        )
        client.post(
            "/api/requests/",
            json={
                "title": "Not urgent",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 1,
            },
        )

        response = client.get("/api/requests/?urgency=4")
        assert response.status_code == 200
        assert response.json()["total"] == 1
        assert response.json()["items"][0]["title"] == "Urgent"


class TestRecordDecision:
    """Tests for POST /api/requests/{id}/decision endpoint."""

    def test_record_decision_accept(self, client):
        """Test recording an accept decision."""
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 2,
            },
        )
        request_id = create_response.json()["id"]

        response = client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "accepted", "decision_reason": "Aligns with roadmap"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "accepted"
        assert data["decision_reason"] == "Aligns with roadmap"

    def test_record_decision_defer(self, client):
        """Test recording a defer decision."""
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 2,
            },
        )
        request_id = create_response.json()["id"]

        response = client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "deferred", "decision_reason": "Revisit next quarter"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "deferred"

    def test_record_decision_decline(self, client):
        """Test recording a decline decision."""
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 2,
            },
        )
        request_id = create_response.json()["id"]

        response = client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "declined", "decision_reason": "Out of scope"},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "declined"

    def test_record_decision_missing_reason(self, client):
        """Test error when decision reason is missing."""
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 2,
            },
        )
        request_id = create_response.json()["id"]

        response = client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "accepted"},
        )
        assert response.status_code == 422

    def test_record_decision_empty_reason(self, client):
        """Test error when decision reason is empty."""
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 2,
            },
        )
        request_id = create_response.json()["id"]

        response = client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "accepted", "decision_reason": ""},
        )
        assert response.status_code == 422

    def test_record_decision_cannot_set_new(self, client):
        """Test error when trying to set status back to new."""
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 2,
            },
        )
        request_id = create_response.json()["id"]

        response = client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "new", "decision_reason": "Some reason"},
        )
        assert response.status_code == 422

    def test_record_decision_already_decided(self, client):
        """Test error when request already has a decision."""
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 2,
            },
        )
        request_id = create_response.json()["id"]

        # First decision
        client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "accepted", "decision_reason": "First decision"},
        )

        # Try to change decision
        response = client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "declined", "decision_reason": "Changed mind"},
        )
        assert response.status_code == 400
        assert "already has status" in response.json()["detail"].lower()

    def test_record_decision_request_not_found(self, client):
        """Test error when request does not exist."""
        response = client.post(
            "/api/requests/00000000-0000-0000-0000-000000000000/decision",
            json={"status": "accepted", "decision_reason": "Reason"},
        )
        assert response.status_code == 404


class TestArchivedRequests:
    """Tests for GET /api/requests/archived endpoint."""

    def test_archived_requests_empty(self, client):
        """Test listing archived requests when none are declined."""
        response = client.get("/api/requests/archived")
        assert response.status_code == 200
        assert response.json()["total"] == 0

    def test_archived_requests_shows_declined(self, client):
        """Test that archived endpoint shows only declined requests."""
        # Create and decline a request
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "Declined request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 1,
            },
        )
        request_id = create_response.json()["id"]
        client.post(
            f"/api/requests/{request_id}/decision",
            json={"status": "declined", "decision_reason": "Not needed"},
        )

        # Create and accept another request
        client.post(
            "/api/requests/",
            json={
                "title": "Accepted request",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 2,
            },
        )

        # Check archived
        response = client.get("/api/requests/archived")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["items"][0]["title"] == "Declined request"


class TestDeleteRequest:
    """Tests for DELETE /api/requests/{id} endpoint."""

    def test_delete_request_success(self, client):
        """Test successful request deletion."""
        create_response = client.post(
            "/api/requests/",
            json={
                "title": "To delete",
                "problem_statement": "Problem",
                "expected_impact": "Impact",
                "urgency": 1,
            },
        )
        request_id = create_response.json()["id"]

        response = client.delete(f"/api/requests/{request_id}")
        assert response.status_code == 204

        # Verify deletion
        get_response = client.get(f"/api/requests/{request_id}")
        assert get_response.status_code == 404

    def test_delete_request_not_found(self, client):
        """Test error when deleting non-existent request."""
        response = client.delete("/api/requests/00000000-0000-0000-0000-000000000000")
        assert response.status_code == 404


class TestHealthCheck:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test health check returns healthy status."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
