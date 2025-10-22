/**
 * Job Detail Page - View job status and task results
 */

import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import useSWR from 'swr';
import { apiClient } from '@/lib/api-client';
import { useState } from 'react';

const fetcher = (id: string) => apiClient.getJob(id);

export default function JobDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [executing, setExecuting] = useState(false);

  const { data: response, error, isLoading, mutate } = useSWR(
    id ? `/api/jobs/${id}` : null,
    () => fetcher(id as string),
    { refreshInterval: 3000 }
  );

  const job = response?.data?.job;
  const tasks = response?.data?.tasks || [];
  const taskCounts = response?.data?.task_counts;

  const handleExecute = async () => {
    if (!id) return;
    setExecuting(true);
    const result = await apiClient.executeJob(id as string);
    if (result.error) {
      alert(`Error: ${result.error}`);
    } else {
      alert('Job execution started!');
      mutate(); // Refresh data
    }
    setExecuting(false);
  };

  if (isLoading) {
    return <Layout title="Loading..."><div className="text-center py-12">Loading job details...</div></Layout>;
  }

  if (error || !job) {
    return <Layout title="Error"><div className="text-center py-12 text-red-500">Job not found</div></Layout>;
  }

  const progress = taskCounts?.total > 0
    ? Math.round((taskCounts.completed / taskCounts.total) * 100)
    : 0;

  return (
    <Layout title={job.display_name || job.name}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Back button */}
        <Link href="/jobs" className="text-blue-600 hover:text-blue-700 mb-4 inline-block">
          ← Back to Jobs
        </Link>

        {/* Job Header */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-6">
          <div className="flex items-start justify-between">
            <div className="flex-1">
              <h1 className="text-2xl font-bold text-gray-900 mb-2">
                {job.display_name || job.name}
              </h1>
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                {job.template_name && (
                  <span>📄 {job.template_name}</span>
                )}
                <span>🕒 {new Date(job.created_at).toLocaleString()}</span>
                <StatusBadge status={job.status} />
              </div>
              {job.user_request && (
                <p className="mt-3 text-gray-700 bg-gray-50 p-3 rounded">
                  {job.user_request}
                </p>
              )}
            </div>

            {job.status === 'pending' && (
              <button
                onClick={handleExecute}
                disabled={executing}
                className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
              >
                {executing ? 'Starting...' : 'Execute Job'}
              </button>
            )}
          </div>

          {/* Progress Bar */}
          {taskCounts && taskCounts.total > 0 && (
            <div className="mt-6">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-gray-700">Progress</span>
                <span className="text-sm text-gray-600">{progress}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${progress}%` }}
                />
              </div>
              <div className="flex items-center justify-between mt-2 text-xs text-gray-600">
                <span>✅ {taskCounts.completed} completed</span>
                <span>⚙️ {taskCounts.in_progress} in progress</span>
                <span>❌ {taskCounts.failed} failed</span>
                <span>⏳ {taskCounts.pending} pending</span>
              </div>
            </div>
          )}
        </div>

        {/* Tasks */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">
            Tasks ({tasks.length})
          </h2>

          {tasks.length === 0 ? (
            <p className="text-gray-500 text-center py-8">No tasks yet</p>
          ) : (
            <div className="space-y-3">
              {tasks.map((task: any) => (
                <TaskCard key={task.id} task={task} />
              ))}
            </div>
          )}
        </div>
      </div>
    </Layout>
  );
}

function TaskCard({ task }: any) {
  const [expanded, setExpanded] = useState(false);

  const categoryIcons = {
    script: '📝',
    image: '🎨',
    audio: '🎵',
    video: '🎬',
  };

  const statusColors = {
    pending: 'bg-gray-100 text-gray-700',
    in_progress: 'bg-yellow-100 text-yellow-700',
    completed: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700',
  };

  return (
    <div className="border border-gray-200 rounded-lg p-4">
      <div
        className="flex items-center justify-between cursor-pointer"
        onClick={() => setExpanded(!expanded)}
      >
        <div className="flex items-center space-x-3 flex-1">
          <span className="text-2xl">{categoryIcons[task.category as keyof typeof categoryIcons]}</span>
          <div className="flex-1">
            <p className="font-medium text-gray-900">{task.task_name}</p>
            <p className="text-xs text-gray-500">
              {task.preferred_agent && `Agent: ${task.preferred_agent}`}
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-3">
          <span
            className={`px-3 py-1 rounded-full text-xs font-medium ${
              statusColors[task.status as keyof typeof statusColors]
            }`}
          >
            {task.status}
          </span>
          <span className="text-gray-400">{expanded ? '▼' : '▶'}</span>
        </div>
      </div>

      {expanded && (
        <div className="mt-4 pt-4 border-t border-gray-100">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="text-gray-600">Category:</span>
              <span className="ml-2 font-medium">{task.category}</span>
            </div>
            <div>
              <span className="text-gray-600">Sequence:</span>
              <span className="ml-2 font-medium">{task.sequence_order}</span>
            </div>
            {task.started_at && (
              <div>
                <span className="text-gray-600">Started:</span>
                <span className="ml-2 font-medium">{new Date(task.started_at).toLocaleString()}</span>
              </div>
            )}
            {task.completed_at && (
              <div>
                <span className="text-gray-600">Completed:</span>
                <span className="ml-2 font-medium">{new Date(task.completed_at).toLocaleString()}</span>
              </div>
            )}
          </div>

          {task.error_message && (
            <div className="mt-3 p-3 bg-red-50 border border-red-200 rounded text-sm text-red-700">
              <strong>Error:</strong> {task.error_message}
            </div>
          )}

          {task.parameters && Object.keys(task.parameters).length > 0 && (
            <details className="mt-3">
              <summary className="text-sm text-gray-600 cursor-pointer">Parameters</summary>
              <pre className="mt-2 p-3 bg-gray-50 rounded text-xs overflow-auto">
                {JSON.stringify(task.parameters, null, 2)}
              </pre>
            </details>
          )}
        </div>
      )}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  const colors = {
    pending: 'bg-gray-100 text-gray-700',
    in_progress: 'bg-yellow-100 text-yellow-700',
    completed: 'bg-green-100 text-green-700',
    failed: 'bg-red-100 text-red-700',
  };

  return (
    <span className={`px-3 py-1 rounded-full text-xs font-medium ${colors[status as keyof typeof colors]}`}>
      {status}
    </span>
  );
}

function Layout({ title, children }: any) {
  return (
    <>
      <Head>
        <title>{title} - Content Engine</title>
      </Head>
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <Link href="/" className="text-2xl font-bold text-gray-900">
              Content Engine V2
            </Link>
          </div>
        </header>
        {children}
      </main>
    </>
  );
}
