/**
 * API Route: /api/jobs/:id/execute
 * POST: Trigger job execution via Python CLI
 *
 * Note: This spawns the Python CLI process to execute the job
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
