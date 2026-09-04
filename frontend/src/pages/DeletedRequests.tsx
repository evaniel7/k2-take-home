import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchDeletedRequests, bulkPermanentDelete, restoreRequest } from '../api/requests';
import type { Request } from '../types';

function DeletedRequests() {
  const [requests, setRequests] = useState<Request[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedIds, setSelectedIds] = useState<Set<string>>(new Set());
  const [deleting, setDeleting] = useState(false);

  useEffect(() => {
    loadRequests();
  }, []);

  async function loadRequests() {
    try {
      setLoading(true);
      const data = await fetchDeletedRequests();
      setRequests(data.items);
      setSelectedIds(new Set());
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load deleted requests');
    } finally {
      setLoading(false);
    }
  }

  function toggleSelect(id: string) {
    const newSelected = new Set(selectedIds);
    if (newSelected.has(id)) {
      newSelected.delete(id);
    } else {
      newSelected.add(id);
    }
    setSelectedIds(newSelected);
  }

  function toggleSelectAll() {
    if (selectedIds.size === requests.length) {
      setSelectedIds(new Set());
    } else {
      setSelectedIds(new Set(requests.map(r => r.id)));
    }
  }

  async function handleBulkDelete() {
    if (selectedIds.size === 0) return;
    if (!confirm(`Are you sure you want to permanently delete ${selectedIds.size} request(s)? This cannot be undone.`)) {
      return;
    }

    try {
      setDeleting(true);
      await bulkPermanentDelete(Array.from(selectedIds));
      await loadRequests();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete requests');
    } finally {
      setDeleting(false);
    }
  }

  async function handleRestore(id: string) {
    try {
      await restoreRequest(id);
      await loadRequests();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to restore request');
    }
  }

  if (loading) return <p>Loading...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h1>Deleted Requests</h1>

      {requests.length === 0 ? (
        <p>No deleted requests.</p>
      ) : (
        <>
          <div className="bulk-actions">
            <label className="checkbox-label">
              <input
                type="checkbox"
                checked={selectedIds.size === requests.length && requests.length > 0}
                onChange={toggleSelectAll}
              />
              Select All ({selectedIds.size} selected)
            </label>
            <button
              className="danger"
              onClick={handleBulkDelete}
              disabled={selectedIds.size === 0 || deleting}
            >
              {deleting ? 'Deleting...' : 'Permanently Delete Selected'}
            </button>
          </div>

          <div className="request-list">
            {requests.map(request => (
              <div key={request.id} className="card request-item">
                <label className="checkbox-label">
                  <input
                    type="checkbox"
                    checked={selectedIds.has(request.id)}
                    onChange={() => toggleSelect(request.id)}
                  />
                </label>
                <div className="info">
                  <Link to={`/requests/${request.id}`}>
                    <strong>{request.title}</strong>
                  </Link>
                  <div style={{ fontSize: '14px', color: '#6b7280' }}>
                    Deleted: {request.deleted_at ? new Date(request.deleted_at).toLocaleString() : 'Unknown'}
                  </div>
                </div>
                <div className="meta">
                  <span className={`badge ${request.status}`}>{request.status}</span>
                  <button className="secondary" onClick={() => handleRestore(request.id)}>
                    Restore
                  </button>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}

export default DeletedRequests;
