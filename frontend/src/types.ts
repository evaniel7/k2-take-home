export type RequestStatus = 'new' | 'accepted' | 'deferred' | 'declined';

export interface Request {
  id: string;
  title: string;
  problem_statement: string;
  expected_impact: string;
  urgency: number;
  status: RequestStatus;
  decision_reason: string | null;
  created_at: string;
  updated_at: string;
  deleted_at: string | null;
}

export interface RequestListResponse {
  items: Request[];
  total: number;
}

export interface CreateRequestPayload {
  title: string;
  problem_statement: string;
  expected_impact: string;
  urgency: number;
}

export interface DecisionPayload {
  status: 'accepted' | 'deferred' | 'declined';
  decision_reason: string;
}
