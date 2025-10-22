/**
 * API Route: /api/templates
 * GET: List available templates
 */

import { NextApiRequest, NextApiResponse } from 'next';
import fs from 'fs/promises';
import path from 'path';

interface Template {
  name: string;
  title: string;
  description: string;
  categories: string[];
  task_count: number;
}

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'GET') {
    res.setHeader('Allow', ['GET']);
    return res.status(405).json({ error: `Method ${req.method} Not Allowed` });
  }

  try {
    const templatesDir = path.join(process.cwd(), '..', 'src', 'templates', 'markdown');

    const files = await fs.readdir(templatesDir);
    const mdFiles = files.filter(f => f.endsWith('.md'));

    const templates: Template[] = [];

    for (const file of mdFiles) {
      const content = await fs.readFile(path.join(templatesDir, file), 'utf-8');

      // Parse basic template info (simple parsing)
      const nameMatch = file.replace('.md', '');
      const titleMatch = content.match(/^#\s+(.+)$/m);
      const title = titleMatch ? titleMatch[1] : nameMatch;

      // Count tasks (lines starting with numbers followed by a period)
      const taskMatches = content.match(/^\d+\.\s+\*\*/gm);
      const taskCount = taskMatches ? taskMatches.length : 0;

      // Determine categories
      const categories: string[] = [];
      if (content.includes('script') || content.includes('writing')) categories.push('script');
      if (content.includes('image') || content.includes('design')) categories.push('image');
      if (content.includes('audio') || content.includes('narration')) categories.push('audio');
      if (content.includes('video')) categories.push('video');

      templates.push({
        name: nameMatch,
        title,
        description: `Template for ${title.toLowerCase()}`,
        categories: categories.length > 0 ? categories : ['script'],
        task_count: taskCount,
      });
    }

    return res.status(200).json({ templates });

  } catch (error) {
    console.error('Error fetching templates:', error);
    return res.status(500).json({
      error: 'Failed to fetch templates',
      message: error instanceof Error ? error.message : 'Unknown error'
    });
  }
}
