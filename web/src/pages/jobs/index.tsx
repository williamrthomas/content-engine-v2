/**
 * Jobs List Page
 */

import Head from 'next/head';
import Link from 'next/link';
import useSWR from 'swr';
import { apiClient } from '@/lib/api-client';
import { useState } from 'react';

const fetcher = () => apiClient.getJobs(100);

export default function JobsList() {
  const [statusFilter, setStatusFilter] = useState<string>('all');

  const { data: response, error, isLoading } = useSWR('/api/jobs', fetcher, {
    refreshInterval: 5000,
  });

  const jobs = response?.data?.jobs || [];

  const filteredJobs = statusFilter === 'all'
    ? jobs
    : jobs.filter((j: any) => j.status === statusFilter);

  return (
    <>
      <Head>
        <title>Jobs - Content Engine</title>
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <Link href="/" className="text-2xl font-bold text-gray-900">
                Content Engine V2
              </Link>
              <Link
                href="/jobs/new"
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                + Create Job
              </Link>
            </div>
          </div>
        </header>

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            {/* Header */}
            <div className="flex items-center justify-between mb-6">
              <h1 className="text-2xl font-bold text-gray-900">
                All Jobs ({filteredJobs.length})
              </h1>

              {/* Filter */}
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Status</option>
                <option value="pending">Pending</option>
                <option value="in_progress">In Progress</option>
                <option value="completed">Completed</option>
                <option value="failed">Failed</option>
              </select>
            </div>

            {/* Jobs List */}
            {isLoading ? (
              <div className="text-center py-12 text-gray-500">Loading...</div>
            ) : error ? (
              <div className="text-center py-12 text-red-500">Error loading jobs</div>
            ) : filteredJobs.length === 0 ? (
              <div className="text-center py-12 text-gray-500">
                No jobs found. <Link href="/jobs/new" className="text-blue-600">Create one now!</Link>
              </div>
            ) : (
              <div className="space-y-3">
                {filteredJobs.map((job: any) => (
                  <JobRow key={job.id} job={job} />
                ))}
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  );
}

function JobRow({ job }: any) {
  const statusColors = {
    pending: 'bg-gray-100 text-gray-700',
    in_progress: 'bg-yellow-100 text-yellow-700',
    completed: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700',
  };

  const progress = job.total_tasks > 0
    ? Math.round((job.completed_tasks / job.total_tasks) * 100)
    : 0;

  return (
    <Link
      href={`/jobs/${job.id}`}
      className="block p-5 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-md transition-all"
    >
      <div className="flex items-start justify-between">
        <div className="flex-1 min-w-0">
          <div className="flex items-center space-x-2 mb-2">
            <h3 className="text-lg font-semibold text-gray-900 truncate">
              {job.display_name || job.name}
            </h3>
            <span
              className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap ${
                statusColors[job.status as keyof typeof statusColors]
              }`}
            >
              {job.status}
            </span>
          </div>

          <div className="flex items-center space-x-4 text-sm text-gray-600 mb-3">
            {job.template_name && (
              <span>📄 {job.template_name}</span>
            )}
            <span>🕒 {new Date(job.created_at).toLocaleDateString()}</span>
            <span>📋 {job.completed_tasks}/{job.total_tasks} tasks</span>
          </div>

          {/* Progress bar */}
          {job.status === 'in_progress' && (
            <div className="mt-3">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs text-gray-600">Progress</span>
                <span className="text-xs text-gray-600">{progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-1.5">
                <div
                  className="bg-blue-600 h-1.5 rounded-full transition-all"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}
        </div>

        <div className="ml-4 text-blue-600">
          →
        </div>
      </div>
    </Link>
  );
}
