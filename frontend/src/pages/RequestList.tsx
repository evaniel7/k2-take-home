import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchRequests, updateStatus } from '../api/requests';
import type { Request, RequestStatus } from '../types';

function RequestList() {
  const [requests, setRequests] = useState<Request[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [urgencyFilter, setUrgencyFilter] = useState<string>('');
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState('desc');
  const [updatingId, setUpdatingId] = useState<string | null>(null);

  useEffect(() => {
    loadRequests();
  }, [statusFilter, urgencyFilter, sortBy, sortOrder]);

  async function loadRequests() {
    try {
      setLoading(true);
      const data = await fetchRequests({
        status: statusFilter || undefined,
        urgency: urgencyFilter ? parseInt(urgencyFilter) : undefined,
        sort_by: sortBy,
        sort_order: sortOrder,
      });
      setRequests(data.items);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load requests');
    } finally {
      setLoading(false);
    }
  }

  async function handleStatusChange(requestId: string, currentStatus: RequestStatus, newStatus: RequestStatus) {
    if (newStatus === currentStatus) return;

    const isChangingToOrFromDeclined = newStatus === 'declined' || currentStatus === 'declined';
    if (isChangingToOrFromDeclined) {
      if (!confirm(`Are you sure you want to change status to "${newStatus}"?`)) {
        return;
      }
    }

    try {
      setUpdatingId(requestId);
      const updated = await updateStatus(requestId, newStatus);
      setRequests(prev => prev.map(r => r.id === requestId ? updated : r));
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update status');
    } finally {
      setUpdatingId(null);
    }
  }

  function renderStatusDropdown(request: Request) {
    return (
      <select
        className={`status-dropdown ${request.status}`}
        value={request.status}
        onChange={(e) => handleStatusChange(request.id, request.status, e.target.value as RequestStatus)}
        disabled={updatingId === request.id}
        onClick={(e) => e.preventDefault()}
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
    return <span className={`urgency-${urgency}`}>{labels[urgency]}</span>;
  }

  return (
    <div>
      <h1>Decision Queue</h1>

      <div className="filters">
        <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
          <option value="">All Statuses</option>
          <option value="new">New</option>
          <option value="accepted">Accepted</option>
          <option value="deferred">Deferred</option>
        </select>

        <select value={urgencyFilter} onChange={e => setUrgencyFilter(e.target.value)}>
          <option value="">All Urgencies</option>
          <option value="1">Low</option>
          <option value="2">Medium</option>
          <option value="3">High</option>
          <option value="4">Critical</option>
        </select>

        <select value={`${sortBy}-${sortOrder}`} onChange={e => {
          const [field, order] = e.target.value.split('-');
          setSortBy(field);
          setSortOrder(order);
        }}>
          <optgroup label="Date">
            <option value="created_at-desc">Newest First</option>
            <option value="created_at-asc">Oldest First</option>
          </optgroup>
          <optgroup label="Urgency">
            <option value="urgency-desc">Critical First</option>
            <option value="urgency-asc">Low First</option>
          </optgroup>
          <optgroup label="Title">
            <option value="title-asc">A to Z</option>
            <option value="title-desc">Z to A</option>
          </optgroup>
        </select>

        <Link to="/create">
          <button className="primary">+ New Request</button>
        </Link>
      </div>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <div className="request-list">
          {requests.length === 0 ? (
            <p>No requests found.</p>
          ) : (
            requests.map(request => (
              <div key={request.id} className="card request-item">
                <div className="info">
                  <Link to={`/requests/${request.id}`}>
                    <h3>{request.title}</h3>
                  </Link>
                  <p>{request.problem_statement.substring(0, 150)}...</p>
                </div>
                <div className="meta">
                  {getUrgencyLabel(request.urgency)}
                  {renderStatusDropdown(request)}
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default RequestList;
