import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { fetchRequest, recordDecision, deleteRequest, updateStatus } from '../api/requests';
import type { Request, RequestStatus } from '../types';

function RequestDetail() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [request, setRequest] = useState<Request | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Decision modal state
  const [showDecisionModal, setShowDecisionModal] = useState(false);
  const [decisionType, setDecisionType] = useState<'accepted' | 'deferred' | 'declined'>('accepted');
  const [decisionReason, setDecisionReason] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [reasonError, setReasonError] = useState<string | null>(null);
  const [statusUpdating, setStatusUpdating] = useState(false);

  useEffect(() => {
    loadRequest();
  }, [id]);

  async function loadRequest() {
    if (!id) return;
    try {
      setLoading(true);
      const data = await fetchRequest(id);
      setRequest(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load request');
    } finally {
      setLoading(false);
    }
  }

  async function handleDecision(e: React.FormEvent) {
    e.preventDefault();
    if (!id) return;

    if (!decisionReason.trim()) {
      setReasonError('Please provide a reason for your decision');
      return;
    }

    try {
      setSubmitting(true);
      const updated = await recordDecision(id, {
        status: decisionType,
        decision_reason: decisionReason.trim(),
      });
      setRequest(updated);
      setShowDecisionModal(false);
      setDecisionReason('');
    } catch (err) {
      setReasonError(err instanceof Error ? err.message : 'Failed to record decision');
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDelete() {
    if (!id) return;
    if (!confirm('Are you sure you want to delete this request?')) return;

    try {
      await deleteRequest(id);
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete request');
    }
  }

  function openDecisionModal(type: 'accepted' | 'deferred' | 'declined') {
    setDecisionType(type);
    setDecisionReason('');
    setReasonError(null);
    setShowDecisionModal(true);
  }

  async function handleStatusChange(newStatus: RequestStatus) {
    if (!id || !request) return;
    if (newStatus === request.status) return;

    const isChangingToOrFromDeclined = newStatus === 'declined' || request.status === 'declined';
    if (isChangingToOrFromDeclined) {
      if (!confirm(`Are you sure you want to change status to "${newStatus}"?`)) {
        return;
      }
    }

    try {
      setStatusUpdating(true);
      const updated = await updateStatus(id, newStatus);
      setRequest(updated);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update status');
    } finally {
      setStatusUpdating(false);
    }
  }

  function renderStatusDropdown(status: RequestStatus) {
    return (
      <select
        className={`status-dropdown ${status}`}
        value={status}
        onChange={(e) => handleStatusChange(e.target.value as RequestStatus)}
        disabled={statusUpdating}
      >
        <option value="new">New</option>
        <option value="accepted">Accepted</option>
        <option value="deferred">Deferred</option>
        <option value="declined">Declined</option>
      </select>
    );
  }

  function getUrgencyLabel(urgency: number) {
    const labels = ['', 'Low', 'Medium', 'High', 'Critical'];
    return <span className={`urgency-${urgency}`}>{labels[urgency]} (Urgency {urgency})</span>;
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="error">{error}</p>;
  if (!request) return <p>Request not found</p>;

  return (
    <div>
      <button className="secondary" onClick={() => navigate(-1)} style={{ marginBottom: '20px' }}>
        &larr; Back
      </button>

      <div className="card">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '20px' }}>
          <h1>{request.title}</h1>
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            {getUrgencyLabel(request.urgency)}
            {renderStatusDropdown(request.status)}
          </div>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <h3>Problem Statement</h3>
          <p>{request.problem_statement}</p>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <h3>Expected Impact</h3>
          <p>{request.expected_impact}</p>
        </div>

        {request.decision_reason && (
          <div style={{ marginBottom: '20px' }}>
            <h3>Decision Reason</h3>
            <p>{request.decision_reason}</p>
          </div>
        )}

        <div style={{ fontSize: '14px', color: '#6b7280' }}>
          <p>Created: {new Date(request.created_at).toLocaleString()}</p>
          <p>Updated: {new Date(request.updated_at).toLocaleString()}</p>
        </div>

        {request.status === 'new' && (
          <div className="button-group" style={{ marginTop: '24px' }}>
            <button className="success" onClick={() => openDecisionModal('accepted')}>
              Accept
            </button>
            <button className="warning" onClick={() => openDecisionModal('deferred')}>
              Defer
            </button>
            <button className="danger" onClick={() => openDecisionModal('declined')}>
              Decline
            </button>
          </div>
        )}

        <div style={{ marginTop: '24px', borderTop: '1px solid #e5e7eb', paddingTop: '16px' }}>
          <button className="danger" onClick={handleDelete}>
            Delete Request
          </button>
        </div>
      </div>

      {showDecisionModal && (
        <div className="modal-overlay" onClick={() => setShowDecisionModal(false)}>
          <div className="modal" onClick={e => e.stopPropagation()}>
            <h2>
              {decisionType === 'accepted' && 'Accept Request'}
              {decisionType === 'deferred' && 'Defer Request'}
              {decisionType === 'declined' && 'Decline Request'}
            </h2>
            <form onSubmit={handleDecision}>
              <div className="form-group">
                <label htmlFor="reason">Reason for Decision *</label>
                <textarea
                  id="reason"
                  rows={4}
                  value={decisionReason}
                  onChange={e => {
                    setDecisionReason(e.target.value);
                    setReasonError(null);
                  }}
                  placeholder="Explain the reasoning behind this decision..."
                />
                {reasonError && <div className="error">{reasonError}</div>}
              </div>
              <div className="button-group">
                <button
                  type="submit"
                  className={decisionType === 'accepted' ? 'success' : decisionType === 'deferred' ? 'warning' : 'danger'}
                  disabled={submitting}
                >
                  {submitting ? 'Saving...' : 'Confirm'}
                </button>
                <button type="button" className="secondary" onClick={() => setShowDecisionModal(false)}>
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default RequestDetail;
