/**
 * API Route: /api/agents
 * GET: List all registered agents
 */

import { NextApiRequest, NextApiResponse } from 'next';
import { query, Agent } from '@/lib/db';

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    res.setHeader('Allow', ['GET']);
    return res.status(405).json({ error: `Method ${req.method} Not Allowed` });
  }

  try {
    const result = await query<Agent>(
      `SELECT * FROM agents
       ORDER BY category, name ASC`
    );

    const agents = result.rows;

    // Group by category
    const grouped = agents.reduce((acc, agent) => {
      if (!acc[agent.category]) {
        acc[agent.category] = [];
      }
      acc[agent.category].push(agent);
      return acc;
    }, {} as Record<string, Agent[]>);

    return res.status(200).json({
      agents,
      grouped,
      total: agents.length,
    });

  } catch (error) {
    console.error('Error fetching agents:', error);
    return res.status(500).json({
      error: 'Failed to fetch agents',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
