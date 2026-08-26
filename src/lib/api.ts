const API_BASE = process.env.NEXT_PUBLIC_API_URL || '/api';

export interface Endpoint {
  id: number;
  name: string;
  url: string;
  method: string;
  timeout: number;
  is_active: boolean;
  created_at: string;
}

export interface MonitoringResult {
  id: number;
  endpoint_id: number;
  is_success: boolean;
  status_code: number | null;
  response_time_ms: number;
  error_message: string | null;
  checked_at: string;
}

export async function fetchEndpoints(): Promise<Endpoint[]> {
  const res = await fetch(`${API_BASE}/endpoints/`);
  if (!res.ok) throw new Error('Failed to fetch endpoints');
  return res.json();
}

export async function fetchEndpoint(id: number): Promise<Endpoint> {
  const res = await fetch(`${API_BASE}/endpoints/${id}`);
  if (!res.ok) throw new Error('Failed to fetch endpoint');
  return res.json();
}

export async function fetchEndpointResults(id: number): Promise<MonitoringResult[]> {
  const res = await fetch(`${API_BASE}/endpoints/${id}/results?limit=50`);
  if (!res.ok) throw new Error('Failed to fetch results');
  return res.json();
}

export async function createEndpoint(data: Partial<Endpoint>): Promise<Endpoint> {
  const res = await fetch(`${API_BASE}/endpoints/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!res.ok) throw new Error('Failed to create endpoint');
  return res.json();
}

export async function deleteEndpoint(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/endpoints/${id}`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to delete endpoint');
}

// <-- NEW: Trigger monitoring engine manually
export async function triggerChecks(): Promise<{ message: string, results: any[] }> {
  const res = await fetch(`${API_BASE}/engine/run-checks`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to run monitoring checks');
  return res.json();
}