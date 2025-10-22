/**
 * Create New Job Page
 */

import { useState } from 'react';
import { useRouter } from 'next/router';
import Head from 'next/head';
import Link from 'next/link';
import useSWR from 'swr';
import { apiClient } from '@/lib/api-client';

const templatesFetcher = () => apiClient.getTemplates();

export default function NewJob() {
  const router = useRouter();
  const [userRequest, setUserRequest] = useState('');
  const [templateName, setTemplateName] = useState('');
  const [creating, setCreating] = useState(false);

  const { data: templatesResponse } = useSWR('/api/templates', templatesFetcher);
  const templates = templatesResponse?.data?.templates || [];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!userRequest.trim()) {
      alert('Please enter a content request');
      return;
    }

    setCreating(true);

    const result = await apiClient.createJob({
      user_request: userRequest,
      template_name: templateName || undefined,
    });

    if (result.error) {
      alert(`Error: ${result.error}`);
      setCreating(false);
    } else {
      const jobId = result.data?.job?.id;
      router.push(`/jobs/${jobId}`);
    }
  };

  return (
    <>
      <Head>
        <title>Create New Job - Content Engine</title>
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <Link href="/" className="text-2xl font-bold text-gray-900">
              Content Engine V2
            </Link>
          </div>
        </header>

        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <Link href="/" className="text-blue-600 hover:text-blue-700 mb-4 inline-block">
            ← Back to Dashboard
          </Link>

          <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-8">
            <h1 className="text-2xl font-bold text-gray-900 mb-6">
              Create New Content Job
            </h1>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Content Request */}
              <div>
                <label htmlFor="request" className="block text-sm font-medium text-gray-700 mb-2">
                  What would you like to create?
                </label>
                <textarea
                  id="request"
                  value={userRequest}
                  onChange={(e) => setUserRequest(e.target.value)}
                  rows={4}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  placeholder="E.g., Write a blog post about AI trends in 2024..."
                  required
                />
                <p className="mt-2 text-sm text-gray-500">
                  Describe your content needs in natural language. Our LLM will analyze and select the best template.
                </p>
              </div>

              {/* Template Selection */}
              <div>
                <label htmlFor="template" className="block text-sm font-medium text-gray-700 mb-2">
                  Template (Optional)
                </label>
                <select
                  id="template"
                  value={templateName}
                  onChange={(e) => setTemplateName(e.target.value)}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="">🧠 Auto-select (LLM Intelligence)</option>
                  {templates.map((template: any) => (
                    <option key={template.name} value={template.name}>
                      {template.title} ({template.task_count} tasks)
                    </option>
                  ))}
                </select>
                <p className="mt-2 text-sm text-gray-500">
                  Leave blank to let the LLM choose the best template based on your request.
                </p>
              </div>

              {/* Template Preview */}
              {templateName && (
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
                  <h3 className="font-medium text-blue-900 mb-2">Selected Template</h3>
                  {templates
                    .filter((t: any) => t.name === templateName)
                    .map((template: any) => (
                      <div key={template.name} className="text-sm text-blue-700">
                        <p className="mb-1">{template.description}</p>
                        <p>Categories: {template.categories.join(', ')}</p>
                        <p>Tasks: {template.task_count}</p>
                      </div>
                    ))}
                </div>
              )}

              {/* Submit */}
              <div className="flex items-center justify-between pt-4">
                <Link
                  href="/"
                  className="text-gray-600 hover:text-gray-700"
                >
                  Cancel
                </Link>
                <button
                  type="submit"
                  disabled={creating}
                  className="bg-blue-600 text-white px-8 py-3 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 font-medium"
                >
                  {creating ? 'Creating...' : 'Create Job'}
                </button>
              </div>
            </form>
          </div>

          {/* Info Box */}
          <div className="mt-6 bg-white rounded-xl shadow-sm border border-gray-200 p-6">
            <h2 className="font-bold text-gray-900 mb-3">💡 What happens next?</h2>
            <ol className="space-y-2 text-sm text-gray-700">
              <li>1. 🧠 LLM analyzes your request and selects optimal template (if not specified)</li>
              <li>2. 📋 Job is created with tasks based on the template</li>
              <li>3. ⚙️ You can execute the job to start content generation</li>
              <li>4. 🤖 Specialized agents (Research, Writing, Freepik) process each task</li>
              <li>5. ✅ View results including real generated images and content</li>
            </ol>
          </div>
        </div>
      </main>
    </>
  );
}
