/**
 * API Route: /api/jobs/:id/execute
 * POST: Trigger job execution via Python CLI
 *
 * ⚠️ IMPORTANT: This endpoint requires a Python runtime and will NOT work on
 * Vercel's default serverless environment. This is designed for local development
 * or platforms that support Python execution (Railway, Render, Fly.io, etc.)
 *
 * For Vercel deployment:
 * - This endpoint will return 500 errors due to missing Python runtime
 * - Consider deploying the Python backend separately
 * - Or implement a job queue system (BullMQ, Inngest, Trigger.dev)
 * - Or run jobs manually via the Python CLI
 *
 * For production, consider using a job queue (Bull, BullMQ, etc.)
 */

import { NextApiRequest, NextApiResponse } from 'next';
import { query } from '@/lib/db';
import { exec } from 'child_process';
import { promisify } from 'util';
import path from 'path';

const execAsync = promisify(exec);

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST']);
    return res.status(405).json({ error: `Method ${req.method} Not Allowed` });
  }

  try {
    const { id } = req.query;

    if (!id || typeof id !== 'string') {
      return res.status(400).json({ error: 'Job ID is required' });
    }

    // Verify job exists
    const jobResult = await query(
      'SELECT id, status FROM jobs WHERE id = $1',
      [id]
    );

    if (jobResult.rows.length === 0) {
      return res.status(404).json({ error: 'Job not found' });
    }

    const job = jobResult.rows[0];

    if (job.status === 'in_progress') {
      return res.status(400).json({ error: 'Job is already running' });
    }

    if (job.status === 'completed') {
      return res.status(400).json({ error: 'Job is already completed' });
    }

    // Check if we're running on Vercel (serverless environment without Python)
    const isVercel = process.env.VERCEL === '1';

    if (isVercel) {
      return res.status(501).json({
        error: 'Job execution not supported on this platform',
        message: 'This endpoint requires Python runtime which is not available on Vercel. Please run jobs using the Python CLI locally, or deploy the Python backend to a platform like Railway, Render, or Fly.io.',
        job_id: id,
        alternatives: [
          'Run locally: python cli.py run ' + id,
          'Deploy Python backend to Railway/Render',
          'Implement a job queue system (BullMQ, Inngest)',
        ]
      });
    }

    // Trigger execution via CLI (async, don't wait)
    // In production, use a job queue instead
    const projectRoot = path.join(process.cwd(), '..');
    const cliPath = path.join(projectRoot, 'cli.py');

    // Execute in background - don't await
    execAsync(`python ${cliPath} run ${id}`, {
      cwd: projectRoot,
    }).catch(error => {
      console.error('Background job execution error:', error);
    });

    return res.status(202).json({
      message: 'Job execution started',
      job_id: id,
      status: 'accepted',
      note: 'Job is processing in the background. Check status via GET /api/jobs/:id'
    });

  } catch (error) {
    console.error('Error executing job:', error);
    return res.status(500).json({
      error: 'Failed to execute job',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
