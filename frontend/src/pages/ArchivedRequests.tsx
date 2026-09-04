import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { fetchArchivedRequests } from '../api/requests';
import type { Request } from '../types';

function ArchivedRequests() {
  const [requests, setRequests] = useState<Request[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadRequests();
  }, []);

  async function loadRequests() {
    try {
      setLoading(true);
      const data = await fetchArchivedRequests();
      setRequests(data.items);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load declined requests');
    } finally {
      setLoading(false);
    }
  }

  function getUrgencyLabel(urgency: number) {
    const labels = ['', 'Low', 'Medium', 'High', 'Critical'];
    return <span className={`urgency-${urgency}`}>{labels[urgency]}</span>;
  }

  return (
    <div>
      <h1>Declined Requests</h1>

      {loading && <p>Loading...</p>}
      {error && <p className="error">{error}</p>}

      {!loading && !error && (
        <div className="request-list">
          {requests.length === 0 ? (
            <p>No declined requests.</p>
          ) : (
            requests.map(request => (
              <div key={request.id} className="card request-item">
                <div className="info">
                  <Link to={`/requests/${request.id}`}>
                    <h3>{request.title}</h3>
                  </Link>
                  <p style={{ color: '#6b7280', fontSize: '14px' }}>
                    {request.decision_reason}
                  </p>
                </div>
                <div className="meta">
                  {getUrgencyLabel(request.urgency)}
                  <span className="badge declined">Declined</span>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}

export default ArchivedRequests;
