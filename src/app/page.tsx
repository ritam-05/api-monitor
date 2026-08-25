export default function Home() {
  return (
    <div className="space-y-6">
      {/* Header section */}
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <button className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 transition-colors font-medium">
          + Add Endpoint
        </button>
      </div>

      {/* Stats Row Placeholder */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3">
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl p-5">
          <dt className="text-sm font-medium text-gray-500 truncate">Total Endpoints</dt>
          <dd className="mt-1 text-3xl font-semibold text-gray-900">0</dd>
        </div>
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl p-5">
          <dt className="text-sm font-medium text-gray-500 truncate">Healthy</dt>
          <dd className="mt-1 text-3xl font-semibold text-emerald-600">0</dd>
        </div>
        <div className="bg-white overflow-hidden shadow-sm border border-gray-100 rounded-xl p-5">
          <dt className="text-sm font-medium text-gray-500 truncate">Unhealthy</dt>
          <dd className="mt-1 text-3xl font-semibold text-rose-600">0</dd>
        </div>
      </div>

      {/* Endpoints List Placeholder */}
      <div className="bg-white shadow-sm border border-gray-100 rounded-xl overflow-hidden">
        <div className="px-6 py-5 border-b border-gray-100">
          <h3 className="text-lg font-medium leading-6 text-gray-900">Monitored APIs</h3>
        </div>
        <div className="px-6 py-12 text-center text-gray-500">
          <p>Data table will go here in Phase 8 when we connect the API.</p>
        </div>
      </div>
    </div>
  );
}