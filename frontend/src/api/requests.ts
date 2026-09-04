import type { Request, RequestListResponse, CreateRequestPayload, DecisionPayload } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: 'An error occurred' }));
    throw new Error(error.detail || `HTTP error ${response.status}`);
  }
  if (response.status === 204) {
    return null as T;
  }
  return response.json();
}

export async function fetchRequests(params?: {
  status?: string;
  urgency?: number;
  sort_by?: string;
  sort_order?: string;
  include_archived?: boolean;
}): Promise<RequestListResponse> {
  const searchParams = new URLSearchParams();
  if (params?.status) searchParams.set('status', params.status);
  if (params?.urgency) searchParams.set('urgency', params.urgency.toString());
  if (params?.sort_by) searchParams.set('sort_by', params.sort_by);
  if (params?.sort_order) searchParams.set('sort_order', params.sort_order);
  if (params?.include_archived) searchParams.set('include_archived', 'true');

  const url = `${API_URL}/api/requests/${searchParams.toString() ? '?' + searchParams.toString() : ''}`;
  const response = await fetch(url);
  return handleResponse<RequestListResponse>(response);
}

export async function fetchArchivedRequests(): Promise<RequestListResponse> {
  const response = await fetch(`${API_URL}/api/requests/archived`);
  return handleResponse<RequestListResponse>(response);
}

export async function fetchRequest(id: string): Promise<Request> {
  const response = await fetch(`${API_URL}/api/requests/${id}`);
  return handleResponse<Request>(response);
}

export async function createRequest(data: CreateRequestPayload): Promise<Request> {
  const response = await fetch(`${API_URL}/api/requests/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Request>(response);
}

export async function recordDecision(id: string, decision: DecisionPayload): Promise<Request> {
  const response = await fetch(`${API_URL}/api/requests/${id}/decision`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(decision),
  });
  return handleResponse<Request>(response);
}

export async function deleteRequest(id: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/requests/${id}`, {
    method: 'DELETE',
  });
  return handleResponse<void>(response);
}

export async function fetchDeletedRequests(): Promise<RequestListResponse> {
  const response = await fetch(`${API_URL}/api/requests/deleted`);
  return handleResponse<RequestListResponse>(response);
}

export async function permanentDeleteRequest(id: string): Promise<void> {
  const response = await fetch(`${API_URL}/api/requests/${id}/permanent`, {
    method: 'DELETE',
  });
  return handleResponse<void>(response);
}

export async function bulkPermanentDelete(ids: string[]): Promise<void> {
  const response = await fetch(`${API_URL}/api/requests/permanent-delete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ids }),
  });
  return handleResponse<void>(response);
}

export async function restoreRequest(id: string): Promise<Request> {
  const response = await fetch(`${API_URL}/api/requests/${id}/restore`, {
    method: 'POST',
  });
  return handleResponse<Request>(response);
}

export async function updateStatus(id: string, status: string): Promise<Request> {
  const response = await fetch(`${API_URL}/api/requests/${id}/status`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status }),
  });
  return handleResponse<Request>(response);
}
