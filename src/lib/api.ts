import { supabase } from './supabase';

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

// Helper function to get auth headers
async function getHeaders(): Promise<HeadersInit> {
  const { data: { session } } = await supabase.auth.getSession();
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  
  if (session?.access_token) {
    headers['Authorization'] = `Bearer ${session.access_token}`;
  }
  return headers;
}

export async function fetchEndpoints(): Promise<Endpoint[]> {
  const res = await fetch(`${API_BASE}/endpoints`, {
    headers: await getHeaders(),
  });
  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`Failed to fetch endpoints: ${res.status} - ${errorDetail}`);
  }
  return res.json();
}

export async function fetchEndpoint(id: number): Promise<Endpoint> {
  const res = await fetch(`${API_BASE}/endpoints/${id}`, {
    headers: await getHeaders(),
  });
  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`Failed to fetch endpoint: ${res.status} - ${errorDetail}`);
  }
  return res.json();
}

export async function fetchEndpointResults(id: number): Promise<MonitoringResult[]> {
  const res = await fetch(`${API_BASE}/endpoints/${id}/results?limit=50`, {
    headers: await getHeaders(),
  });
  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`Failed to fetch results: ${res.status} - ${errorDetail}`);
  }
  return res.json();
}

export async function createEndpoint(data: Partial<Endpoint>): Promise<Endpoint> {
  const res = await fetch(`${API_BASE}/endpoints`, {
    method: 'POST',
    headers: await getHeaders(),
    body: JSON.stringify(data),
  });
  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`Failed to create endpoint: ${res.status} - ${errorDetail}`);
  }
  return res.json();
}

export async function deleteEndpoint(id: number): Promise<void> {
  const res = await fetch(`${API_BASE}/endpoints/${id}`, {
    method: 'DELETE',
    headers: await getHeaders(),
  });
  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`Failed to delete endpoint: ${res.status} - ${errorDetail}`);
  }
}

export async function triggerChecks(): Promise<{ message: string, results: any[] }> {
  const res = await fetch(`${API_BASE}/engine/run-checks`, {
    method: 'POST',
    headers: await getHeaders(),
  });
  if (!res.ok) {
    const errorDetail = await res.text();
    throw new Error(`Failed to run monitoring checks: ${res.status} - ${errorDetail}`);
  }
  return res.json();
}