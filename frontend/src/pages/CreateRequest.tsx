import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createRequest } from '../api/requests';

interface FormErrors {
  title?: string;
  problem_statement?: string;
  expected_impact?: string;
  urgency?: string;
}

function CreateRequest() {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [errors, setErrors] = useState<FormErrors>({});

  const [formData, setFormData] = useState({
    title: '',
    problem_statement: '',
    expected_impact: '',
    urgency: '2',
  });

  function validate(): boolean {
    const newErrors: FormErrors = {};

    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }
    if (!formData.problem_statement.trim()) {
      newErrors.problem_statement = 'Problem statement is required';
    }
    if (!formData.expected_impact.trim()) {
      newErrors.expected_impact = 'Expected impact is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();

    if (!validate()) return;

    try {
      setLoading(true);
      setError(null);
      await createRequest({
        title: formData.title.trim(),
        problem_statement: formData.problem_statement.trim(),
        expected_impact: formData.expected_impact.trim(),
        urgency: parseInt(formData.urgency),
      });
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create request');
    } finally {
      setLoading(false);
    }
  }

  function handleChange(e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({ ...prev, [name]: undefined }));
    }
  }

  return (
    <div>
      <h1>Create New Request</h1>

      <div className="card" style={{ maxWidth: '600px' }}>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="title">Title *</label>
            <input
              id="title"
              name="title"
              type="text"
              value={formData.title}
              onChange={handleChange}
              placeholder="Brief title for the request"
            />
            {errors.title && <div className="error">{errors.title}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="problem_statement">Problem Statement *</label>
            <textarea
              id="problem_statement"
              name="problem_statement"
              rows={4}
              value={formData.problem_statement}
              onChange={handleChange}
              placeholder="Describe the problem or need"
            />
            {errors.problem_statement && <div className="error">{errors.problem_statement}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="expected_impact">Expected Impact *</label>
            <textarea
              id="expected_impact"
              name="expected_impact"
              rows={3}
              value={formData.expected_impact}
              onChange={handleChange}
              placeholder="What impact will this have if implemented?"
            />
            {errors.expected_impact && <div className="error">{errors.expected_impact}</div>}
          </div>

          <div className="form-group">
            <label htmlFor="urgency">Urgency *</label>
            <select
              id="urgency"
              name="urgency"
              value={formData.urgency}
              onChange={handleChange}
            >
              <option value="1">1 - Low</option>
              <option value="2">2 - Medium</option>
              <option value="3">3 - High</option>
              <option value="4">4 - Critical</option>
            </select>
          </div>

          {error && <div className="error">{error}</div>}

          <div className="button-group">
            <button type="submit" className="primary" disabled={loading}>
              {loading ? 'Creating...' : 'Create Request'}
            </button>
            <button type="button" className="secondary" onClick={() => navigate('/')}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default CreateRequest;
