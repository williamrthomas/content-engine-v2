/**
 * Home Page - Content Engine Dashboard
 */

import Head from 'next/head';
import Link from 'next/link';
import useSWR from 'swr';
import { apiClient } from '@/lib/api-client';

const fetcher = () => apiClient.getJobs(10);

export default function Home() {
  const { data: response, error, isLoading } = useSWR('/api/jobs', fetcher, {
    refreshInterval: 5000, // Refresh every 5 seconds
  });

  const jobs = response?.data?.jobs || [];

  return (
    <>
      <Head>
        <title>Content Engine V2 - Dashboard</title>
        <meta name="description" content="Professional content creation system" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900">
                  Content Engine V2
                </h1>
                <p className="text-gray-600 mt-1">
                  Professional content creation at scale
                </p>
              </div>
              <Link
                href="/jobs/new"
                className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition-colors font-medium shadow-sm"
              >
                + Create Job
              </Link>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Quick Stats */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
            <StatCard
              title="Total Jobs"
              value={jobs.length}
              icon="📊"
              color="blue"
            />
            <StatCard
              title="Completed"
              value={jobs.filter((j: any) => j.status === 'completed').length}
              icon="✅"
              color="green"
            />
            <StatCard
              title="In Progress"
              value={jobs.filter((j: any) => j.status === 'in_progress').length}
              icon="⚙️"
              color="yellow"
            />
            <StatCard
              title="Pending"
              value={jobs.filter((j: any) => j.status === 'pending').length}
              icon="⏳"
              color="gray"
            />
          </div>

          {/* Navigation */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            <NavCard
              title="Jobs"
              description="View and manage all content jobs"
              href="/jobs"
              icon="📋"
            />
            <NavCard
              title="Templates"
              description="Browse available templates"
              href="/templates"
              icon="📄"
            />
            <NavCard
              title="Agents"
              description="View registered agents"
              href="/agents"
              icon="🤖"
            />
          </div>

          {/* Recent Jobs */}
          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">
              Recent Jobs
            </h2>

            {isLoading ? (
              <div className="text-center py-8 text-gray-500">Loading...</div>
            ) : error ? (
              <div className="text-center py-8 text-red-500">
                Error loading jobs
              </div>
            ) : jobs.length === 0 ? (
              <div className="text-center py-8 text-gray-500">
                No jobs yet. Create your first job to get started!
              </div>
            ) : (
              <div className="space-y-3">
                {jobs.slice(0, 5).map((job: any) => (
                  <JobRow key={job.id} job={job} />
                ))}
              </div>
            )}

            {jobs.length > 5 && (
              <div className="mt-4 text-center">
                <Link
                  href="/jobs"
                  className="text-blue-600 hover:text-blue-700 font-medium"
                >
                  View all jobs →
                </Link>
              </div>
            )}
          </div>
        </div>
      </main>
    </>
  );
}

function StatCard({ title, value, icon, color }: any) {
  const colors = {
    blue: 'bg-blue-50 text-blue-600',
    green: 'bg-green-50 text-green-600',
    yellow: 'bg-yellow-50 text-yellow-600',
    gray: 'bg-gray-50 text-gray-600',
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm text-gray-600 mb-1">{title}</p>
          <p className="text-3xl font-bold text-gray-900">{value}</p>
        </div>
        <div className={`text-4xl ${colors[color as keyof typeof colors]}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}

function NavCard({ title, description, href, icon }: any) {
  return (
    <Link
      href={href}
      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow"
    >
      <div className="text-4xl mb-3">{icon}</div>
      <h3 className="text-lg font-bold text-gray-900 mb-2">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </Link>
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
      className="block p-4 border border-gray-200 rounded-lg hover:border-blue-300 hover:shadow-sm transition-all"
    >
      <div className="flex items-center justify-between">
        <div className="flex-1 min-w-0">
          <p className="text-sm font-medium text-gray-900 truncate">
            {job.display_name || job.name}
          </p>
          <p className="text-xs text-gray-500 mt-1">
            {job.template_name && (
              <span className="mr-3">📄 {job.template_name}</span>
            )}
            {job.completed_tasks}/{job.total_tasks} tasks
          </p>
        </div>
        <div className="ml-4 flex items-center space-x-3">
          {job.status === 'in_progress' && (
            <div className="text-xs text-gray-500">{progress}%</div>
          )}
          <span
            className={`px-3 py-1 rounded-full text-xs font-medium ${
              statusColors[job.status as keyof typeof statusColors]
            }`}
          >
            {job.status}
          </span>
        </div>
      </div>
    </Link>
  );
}
