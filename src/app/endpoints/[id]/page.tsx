"use client";

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Link from 'next/link';
import { format } from 'date-fns';
import { ArrowLeft, CheckCircle2, XCircle, Clock } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { fetchEndpoint, fetchEndpointResults, Endpoint, MonitoringResult } from '@/lib/api';

export default function EndpointDetails() {
  const params = useParams();
  const id = Number(params.id);

  const [endpoint, setEndpoint] = useState<Endpoint | null>(null);
  const [results, setResults] = useState<MonitoringResult[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const [epData, resData] = await Promise.all([
          fetchEndpoint(id),
          fetchEndpointResults(id)
        ]);
        setEndpoint(epData);
        setResults(resData);
      } catch (error) {
        console.error("Failed to load details:", error);
      } finally {
        setLoading(false);
      }
    }
    if (id) loadData();
  }, [id]);

  if (loading) return <div className="text-center py-12 text-gray-500">Loading details...</div>;
  if (!endpoint) return <div className="text-center py-12 text-gray-500">Endpoint not found.</div>;

  const totalChecks = results.length;
  const successfulChecks = results.filter(r => r.is_success).length;
  const uptime = totalChecks > 0 ? ((successfulChecks / totalChecks) * 100).toFixed(2) : '0.00';
  
  const avgResponseTime = totalChecks > 0 
    ? Math.round(results.reduce((acc, curr) => acc + curr.response_time_ms, 0) / totalChecks)
    : 0;

  const chartData = [...results].reverse().map(r => ({
    time: format(new Date(r.checked_at), 'HH:mm:ss'),
    ms: r.response_time_ms,
    success: r.is_success
  }));

  return (
    <div className="space-y-6">
      <div>
        <Link href="/" className="inline-flex items-center text-sm text-indigo-600 hover:text-indigo-800 mb-4">
          <ArrowLeft className="w-4 h-4 mr-1" /> Back to Dashboard
        </Link>
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{endpoint.name}</h1>
            <p className="text-gray-500">{endpoint.method} • {endpoint.url}</p>
          </div>
          <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${
            endpoint.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-gray-100 text-gray-800'
          }`}>
            {endpoint.is_active ? <CheckCircle2 className="w-4 h-4" /> : <XCircle className="w-4 h-4" />}
            {endpoint.is_active ? 'Monitoring Active' : 'Paused'}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl p-5">
          <dt className="text-sm font-medium text-gray-500">Uptime (Last 50 checks)</dt>
          <dd className="mt-1 text-3xl font-semibold text-gray-900">{uptime}%</dd>
        </div>
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl p-5">
          <dt className="text-sm font-medium text-gray-500">Avg Response Time</dt>
          <dd className="mt-1 text-3xl font-semibold text-gray-900 flex items-center gap-2">
            {avgResponseTime} ms <Clock className="w-5 h-5 text-gray-400" />
          </dd>
        </div>
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl p-5">
          <dt className="text-sm font-medium text-gray-500">Total Checks Recorded</dt>
          <dd className="mt-1 text-3xl font-semibold text-gray-900">{totalChecks}</dd>
        </div>
      </div>

      <div className="bg-white shadow-sm border border-gray-100 rounded-xl p-6">
        <h3 className="text-lg font-medium text-gray-900 mb-6">Response Time History</h3>
        {chartData.length > 0 ? (
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                <XAxis dataKey="time" tick={{fontSize: 12}} tickMargin={10} stroke="#9CA3AF" />
                <YAxis tick={{fontSize: 12}} unit="ms" stroke="#9CA3AF" />
                <Tooltip 
                  contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Line 
                  type="monotone" 
                  dataKey="ms" 
                  stroke="#4F46E5" 
                  strokeWidth={2} 
                  dot={false}
                  activeDot={{ r: 6 }} 
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">No monitoring data available yet. Run checks to see the chart.</div>
        )}
      </div>
    </div>
  );
}