import Link from 'next/link';
import { Activity } from 'lucide-react';

export default function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link href="/" className="flex items-center gap-2 text-xl font-bold text-slate-800">
              <Activity className="h-6 w-6 text-indigo-600" />
              <span>API Monitor</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}