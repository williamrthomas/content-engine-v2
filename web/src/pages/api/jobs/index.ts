/**
 * API Route: /api/jobs
 * GET: List all jobs
 * POST: Create a new job
 */

import { NextApiRequest, NextApiResponse } from 'next';
import { query, Job } from '@/lib/db';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method === 'GET') {
    return handleGetJobs(req, res);
  } else if (req.method === 'POST') {
    return handleCreateJob(req, res);
  } else {
    res.setHeader('Allow', ['GET', 'POST']);
    return res.status(405).json({ error: `Method ${req.method} Not Allowed` });
  }
}

async function handleGetJobs(req: NextApiRequest, res: NextApiResponse) {
  try {
    const limit = parseInt(req.query.limit as string) || 50;
    const offset = parseInt(req.query.offset as string) || 0;
    const status = req.query.status as string | undefined;

    let sql = `
      SELECT
        j.*,
        COUNT(t.id) as total_tasks,
        COUNT(CASE WHEN t.status = 'completed' THEN 1 END) as completed_tasks,
        COUNT(CASE WHEN t.status = 'failed' THEN 1 END) as failed_tasks
      FROM jobs j
      LEFT JOIN tasks t ON t.job_id = j.id
    `;

    const params: any[] = [];

    if (status) {
      sql += ' WHERE j.status = $1';
      params.push(status);
    }

    sql += `
      GROUP BY j.id
      ORDER BY j.created_at DESC
      LIMIT $${params.length + 1} OFFSET $${params.length + 2}
    `;
    params.push(limit, offset);

    const result = await query(sql, params);

    return res.status(200).json({
      jobs: result.rows,
      total: result.rows.length,
      limit,
      offset,
    });
  } catch (error) {
    console.error('Error fetching jobs:', error);
    return res.status(500).json({
      error: 'Failed to fetch jobs',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}

async function handleCreateJob(req: NextApiRequest, res: NextApiResponse) {
  try {
    const { user_request, template_name } = req.body;

    if (!user_request || typeof user_request !== 'string') {
      return res.status(400).json({ error: 'user_request is required' });
    }

    // Generate a simple job name (in production, you'd call the LLM service)
    const jobName = user_request
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '-')
      .substring(0, 100);

    const result = await query<Job>(
      `INSERT INTO jobs (name, display_name, template_name, user_request, status)
       VALUES ($1, $2, $3, $4, 'pending')
       RETURNING *`,
      [jobName, user_request, template_name || null, user_request]
    );

    const job = result.rows[0];

    return res.status(201).json({
      job,
      message: 'Job created successfully. Use the CLI to execute it or call /api/jobs/{id}/execute'
    });
  } catch (error) {
    console.error('Error creating job:', error);
    return res.status(500).json({
      error: 'Failed to create job',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
