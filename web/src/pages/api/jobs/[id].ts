/**
 * API Route: /api/jobs/:id
 * GET: Get job details with tasks
 */

import { NextApiRequest, NextApiResponse } from 'next';
import { query, Job, Task } from '@/lib/db';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    res.setHeader('Allow', ['GET']);
    return res.status(405).json({ error: `Method ${req.method} Not Allowed` });
  }

  try {
    const { id } = req.query;

    if (!id || typeof id !== 'string') {
      return res.status(400).json({ error: 'Job ID is required' });
    }

    // Get job details
    const jobResult = await query<Job>(
      'SELECT * FROM jobs WHERE id = $1',
      [id]
    );

    if (jobResult.rows.length === 0) {
      return res.status(404).json({ error: 'Job not found' });
    }

    const job = jobResult.rows[0];

    // Get all tasks for this job
    const tasksResult = await query<Task>(
      `SELECT * FROM tasks
       WHERE job_id = $1
       ORDER BY sequence_order ASC`,
      [id]
    );

    const tasks = tasksResult.rows;

    // Calculate task statistics
    const taskCounts = {
      total: tasks.length,
      completed: tasks.filter(t => t.status === 'completed').length,
      failed: tasks.filter(t => t.status === 'failed').length,
      pending: tasks.filter(t => t.status === 'pending').length,
      in_progress: tasks.filter(t => t.status === 'in_progress').length,
    };

    return res.status(200).json({
      job,
      tasks,
      task_counts: taskCounts,
    });
  } catch (error) {
    console.error('Error fetching job:', error);
    return res.status(500).json({
      error: 'Failed to fetch job',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
