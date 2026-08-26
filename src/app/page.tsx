"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Activity, Trash2, CheckCircle2, XCircle, RefreshCw } from 'lucide-react';
import { fetchEndpoints, deleteEndpoint, triggerChecks, Endpoint } from '@/lib/api';
import AddEndpointModal from '@/components/AddEndpointModal';
import { supabase } from '@/lib/supabase';

export default function Home() {
  const router = useRouter();
  const [endpoints, setEndpoints] = useState<Endpoint[]>([]);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [loading, setLoading] = useState(true);
  
  const [isChecking, setIsChecking] = useState(false);
  const [toastMessage, setToastMessage] = useState<string | null>(null);

  useEffect(() => {
    const checkAuth = async () => {
      const { data: { session } } = await supabase.auth.getSession();
      if (!session) {
        router.push('/login');
      } else {
        loadEndpoints();
      }
    };
    checkAuth();
  }, [router]);

  const loadEndpoints = async () => {
    try {
      const data = await fetchEndpoints();
      setEndpoints(data);
    } catch (error) {
      console.error("Failed to load endpoints:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this endpoint?")) return;
    try {
      await deleteEndpoint(id);
      loadEndpoints(); 
    } catch (error) {
      alert("Failed to delete endpoint");
    }
  };

  const handleRunChecks = async () => {
    setIsChecking(true);
    setToastMessage(null);
    try {
      const response = await triggerChecks();
      setToastMessage(response.message);
      setTimeout(() => { setToastMessage(null); }, 3000);
    } catch (error) {
      alert("Failed to run checks. Is the backend running?");
    } finally {
      setIsChecking(false);
    }
  };

  const activeCount = endpoints.filter(ep => ep.is_active).length;
  const inactiveCount = endpoints.length - activeCount;

  return (
    <div className="space-y-6 relative">
      {toastMessage && (
        <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -mt-2 bg-gray-900 text-white px-4 py-2 rounded-md shadow-lg text-sm font-medium z-50 animate-fade-in-down">
          {toastMessage}
        </div>
      )}

      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        
        <div className="flex gap-3">
          <button 
            onClick={handleRunChecks}
            disabled={isChecking || endpoints.length === 0}
            className="bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-50 transition-colors font-medium flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw className={`h-4 w-4 ${isChecking ? 'animate-spin text-indigo-600' : ''}`} />
            {isChecking ? 'Checking...' : 'Run Checks'}
          </button>

          <button 
            onClick={() => setIsModalOpen(true)}
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors font-medium flex items-center gap-2"
          >
            <Activity className="h-4 w-4" />
            Add Endpoint
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl p-5">
          <dt className="text-sm font-medium text-gray-500 truncate">Total Endpoints</dt>
          <dd className="mt-1 text-3xl font-semibold text-gray-900">{endpoints.length}</dd>
        </div>
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl p-5">
          <dt className="text-sm font-medium text-gray-500 truncate">Active Monitoring</dt>
          <dd className="mt-1 text-3xl font-semibold text-emerald-600">{activeCount}</dd>
        </div>
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl p-5">
          <dt className="text-sm font-medium text-gray-500 truncate">Inactive</dt>
          <dd className="mt-1 text-3xl font-semibold text-rose-600">{inactiveCount}</dd>
        </div>
      </div>

      <div className="bg-white shadow-sm border border-gray-100 rounded-xl overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-100">
          <h3 className="text-lg font-medium leading-6 text-gray-900">Monitored APIs</h3>
        </div>
        <div className="overflow-x-auto">
          {loading ? (
            <div className="p-12 text-center text-gray-500">Loading endpoints...</div>
          ) : endpoints.length === 0 ? (
            <div className="p-12 text-center text-gray-500">No endpoints found. Add one to get started!</div>
          ) : (
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Name / URL</th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                  <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {endpoints.map((ep) => (
                  <tr key={ep.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Link href={`/endpoints/${ep.id}`} className="block hover:opacity-80">
                        <div className="text-sm font-medium text-indigo-600">{ep.name}</div>
                        <div className="text-sm text-gray-500">{ep.method} • {ep.url}</div>
                      </Link>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        ep.is_active ? 'bg-emerald-100 text-emerald-800' : 'bg-gray-100 text-gray-800'
                      }`}>
                        {ep.is_active ? <CheckCircle2 className="w-3 h-3" /> : <XCircle className="w-3 h-3" />}
                        {ep.is_active ? 'Active' : 'Paused'}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                      <button 
                        onClick={() => handleDelete(ep.id)}
                        className="text-red-500 hover:text-red-700 transition-colors"
                        title="Delete endpoint"
                      >
                        <Trash2 className="w-4 h-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      </div>

      <AddEndpointModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        onSuccess={loadEndpoints}
      />
    </div>
  );
}