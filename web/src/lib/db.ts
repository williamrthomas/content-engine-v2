/**
 * Database connection and types for Content Engine Web Interface
 */

import { Pool, QueryResult } from 'pg';

// Database Types
export interface Job {
  id: string;
  name: string;
  display_name: string | null;
  template_name: string | null;
  user_request: string | null;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  created_at: Date;
  completed_at: Date | null;
}

export interface Task {
  id: string;
  job_id: string;
  task_name: string;
  category: 'script' | 'image' | 'audio' | 'video';
  sequence_order: number;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  assigned_agent_id: string | null;
  preferred_agent: string | null;
  parameters: Record<string, any>;
  started_at: Date | null;
  completed_at: Date | null;
  error_message: string | null;
}

export interface Agent {
  id: string;
  name: string;
  instance_key: string;
  category: 'script' | 'image' | 'audio' | 'video';
  provider: string | null;
  model: string | null;
  specialization: string | null;
  config: Record<string, any>;
  status: 'active' | 'inactive' | 'error';
  created_at: Date;
}

// Connection pool (singleton)
let pool: Pool | null = null;

/**
 * Get or create the database connection pool
 */
function getPool(): Pool {
  if (!pool) {
    const connectionString = process.env.DATABASE_URL;

    if (!connectionString) {
      throw new Error('DATABASE_URL environment variable is not set');
    }

    pool = new Pool({
      connectionString,
      max: 10,
      idleTimeoutMillis: 30000,
      connectionTimeoutMillis: 10000,
    });

    // Handle pool errors
    pool.on('error', (err) => {
      console.error('Unexpected database pool error:', err);
    });
  }

  return pool;
}

/**
 * Execute a database query
 * @param text SQL query text
 * @param params Query parameters
 * @returns Query result
 */
export async function query<T = any>(
  text: string,
  params?: any[]
): Promise<QueryResult<T>> {
  const pool = getPool();
  const start = Date.now();

  try {
    const result = await pool.query<T>(text, params);
    const duration = Date.now() - start;

    // Log slow queries in development
    if (process.env.NODE_ENV === 'development' && duration > 1000) {
      console.warn(`Slow query (${duration}ms):`, text);
    }

    return result;
  } catch (error) {
    console.error('Database query error:', error);
    console.error('Query:', text);
    console.error('Params:', params);
    throw error;
  }
}

/**
 * Close the database connection pool
 * Call this during graceful shutdown
 */
export async function closePool(): Promise<void> {
  if (pool) {
    await pool.end();
    pool = null;
  }
}

/**
 * Test database connectivity
 */
export async function healthCheck(): Promise<boolean> {
  try {
    await query('SELECT 1');
    return true;
  } catch (error) {
    console.error('Database health check failed:', error);
    return false;
  }
}
