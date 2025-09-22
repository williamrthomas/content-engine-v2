"""PostgreSQL database connection and operations for Content Engine V2"""

import asyncio
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional, Dict, Any, AsyncGenerator
from uuid import UUID
import asyncpg
from asyncpg import Pool, Connection

from .config import get_database_url
from .models import Job, Task, Agent, JobStatus, TaskStatus, TaskCategory, AgentStatus

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages PostgreSQL database connections and operations"""
    
    def __init__(self):
        self.pool: Optional[Pool] = None
        self._database_url = get_database_url()
    
    def _row_to_task(self, row) -> Task:
        """Convert database row to Task object, handling JSONB parsing"""
        row_dict = dict(row)
        if row_dict.get('parameters'):
            row_dict['parameters'] = json.loads(row_dict['parameters']) if isinstance(row_dict['parameters'], str) else row_dict['parameters']
        return Task(**row_dict)
    
    def _row_to_agent(self, row) -> Agent:
        """Convert database row to Agent object, handling JSONB parsing"""
        row_dict = dict(row)
        if row_dict.get('config'):
            row_dict['config'] = json.loads(row_dict['config']) if isinstance(row_dict['config'], str) else row_dict['config']
        return Agent(**row_dict)
    
    async def initialize(self) -> None:
        """Initialize database connection pool"""
        try:
            self.pool = await asyncpg.create_pool(
                self._database_url,
                min_size=2,
                max_size=10,
                command_timeout=60
            )
            logger.info("Database connection pool initialized")
        except Exception as e:
            logger.error(f"Failed to initialize database pool: {e}")
            raise
    
    async def close(self) -> None:
        """Close database connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Database connection pool closed")
    
    @asynccontextmanager
    async def get_connection(self) -> AsyncGenerator[Connection, None]:
        """Get a database connection from the pool"""
        if not self.pool:
            raise RuntimeError("Database pool not initialized")
        
        async with self.pool.acquire() as connection:
            yield connection
    
    async def create_schema(self) -> None:
        """Create database schema with all required tables"""
        schema_sql = """
        -- Enable UUID extension
        CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
        
        -- Jobs table
        CREATE TABLE IF NOT EXISTS jobs (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(200) NOT NULL,
            display_name VARCHAR(200),
            template_name VARCHAR(100),
            user_request TEXT,
            status VARCHAR(20) DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT NOW(),
            completed_at TIMESTAMP
        );
        
        -- Tasks table
        CREATE TABLE IF NOT EXISTS tasks (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
            task_name VARCHAR(100) NOT NULL,
            category VARCHAR(20) NOT NULL,
            sequence_order INTEGER NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            assigned_agent_id UUID,
            preferred_agent VARCHAR(100),
            parameters JSONB NOT NULL DEFAULT '{}',
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT
        );
        
        -- Agents table
        CREATE TABLE IF NOT EXISTS agents (
            id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
            name VARCHAR(100) NOT NULL,
            instance_key VARCHAR(50) NOT NULL UNIQUE,
            category VARCHAR(20) NOT NULL,
            provider VARCHAR(50),
            model VARCHAR(50),
            specialization TEXT,
            config JSONB DEFAULT '{}',
            status VARCHAR(20) DEFAULT 'active',
            created_at TIMESTAMP DEFAULT NOW()
        );
        
        -- Create indexes for better performance
        CREATE INDEX IF NOT EXISTS idx_tasks_job_id ON tasks(job_id);
        CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
        CREATE INDEX IF NOT EXISTS idx_tasks_category ON tasks(category);
        CREATE INDEX IF NOT EXISTS idx_agents_category ON agents(category);
        CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status);
        CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
        """
        
        async with self.get_connection() as conn:
            await conn.execute(schema_sql)
            logger.info("Database schema created successfully")
    
    # Job Operations
    
    async def create_job(self, job: Job) -> Job:
        """Create a new job in the database"""
        query = """
        INSERT INTO jobs (id, name, display_name, template_name, user_request, status, created_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7)
        RETURNING *
        """
        
        async with self.get_connection() as conn:
            row = await conn.fetchrow(
                query,
                job.id, job.name, job.display_name, job.template_name,
                job.user_request, job.status, job.created_at
            )
            return Job(**dict(row))
    
    async def get_job(self, job_id: UUID) -> Optional[Job]:
        """Get a job by ID"""
        query = "SELECT * FROM jobs WHERE id = $1"
        
        async with self.get_connection() as conn:
            row = await conn.fetchrow(query, job_id)
            return Job(**dict(row)) if row else None
    
    async def get_jobs(self, status: Optional[JobStatus] = None, limit: int = 50) -> List[Job]:
        """Get jobs with optional status filter"""
        if status:
            query = "SELECT * FROM jobs WHERE status = $1 ORDER BY created_at DESC LIMIT $2"
            params = [status, limit]
        else:
            query = "SELECT * FROM jobs ORDER BY created_at DESC LIMIT $1"
            params = [limit]
        
        async with self.get_connection() as conn:
            rows = await conn.fetch(query, *params)
            return [Job(**dict(row)) for row in rows]
    
    async def update_job_status(self, job_id: UUID, status: JobStatus, completed_at: Optional[datetime] = None) -> None:
        """Update job status"""
        if completed_at:
            query = "UPDATE jobs SET status = $1, completed_at = $2 WHERE id = $3"
            params = [status, completed_at, job_id]
        else:
            query = "UPDATE jobs SET status = $1 WHERE id = $2"
            params = [status, job_id]
        
        async with self.get_connection() as conn:
            await conn.execute(query, *params)
    
    # Task Operations
    
    async def create_task(self, task: Task) -> Task:
        """Create a new task in the database"""
        query = """
        INSERT INTO tasks (id, job_id, task_name, category, sequence_order, status, 
                          assigned_agent_id, preferred_agent, parameters, started_at, completed_at, error_message)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
        RETURNING *
        """
        
        async with self.get_connection() as conn:
            row = await conn.fetchrow(
                query,
                task.id, task.job_id, task.task_name, task.category,
                task.sequence_order, task.status, task.assigned_agent_id, task.preferred_agent,
                json.dumps(task.parameters), task.started_at, task.completed_at, task.error_message
            )
            return self._row_to_task(row)
    
    async def get_tasks_for_job(self, job_id: UUID) -> List[Task]:
        """Get all tasks for a job, ordered by category and sequence"""
        query = """
        SELECT * FROM tasks 
        WHERE job_id = $1 
        ORDER BY 
            CASE category 
                WHEN 'script' THEN 1 
                WHEN 'image' THEN 2 
                WHEN 'audio' THEN 3 
                WHEN 'video' THEN 4 
            END,
            sequence_order
        """
        
        async with self.get_connection() as conn:
            rows = await conn.fetch(query, job_id)
            return [self._row_to_task(row) for row in rows]
    
    async def get_next_pending_task(self, job_id: UUID) -> Optional[Task]:
        """Get the next pending task for a job (sequential execution)"""
        query = """
        SELECT * FROM tasks 
        WHERE job_id = $1 AND status = 'pending'
        ORDER BY 
            CASE category 
                WHEN 'script' THEN 1 
                WHEN 'image' THEN 2 
                WHEN 'audio' THEN 3 
                WHEN 'video' THEN 4 
            END,
            sequence_order
        LIMIT 1
        """
        
        async with self.get_connection() as conn:
            row = await conn.fetchrow(query, job_id)
            return self._row_to_task(row) if row else None
    
    async def get_tasks_for_category(self, job_id: UUID, category: TaskCategory) -> List[Task]:
        """Get all tasks for a specific category"""
        query = """
        SELECT * FROM tasks 
        WHERE job_id = $1 AND category = $2 
        ORDER BY sequence_order
        """
        
        async with self.get_connection() as conn:
            rows = await conn.fetch(query, job_id, category)
            return [self._row_to_task(row) for row in rows]
    
    async def update_task_status(self, task_id: UUID, status: TaskStatus, 
                               assigned_agent_id: Optional[UUID] = None,
                               started_at: Optional[datetime] = None,
                               completed_at: Optional[datetime] = None,
                               error_message: Optional[str] = None) -> None:
        """Update task status and related fields"""
        query = """
        UPDATE tasks 
        SET status = $1, assigned_agent_id = $2, started_at = $3, 
            completed_at = $4, error_message = $5
        WHERE id = $6
        """
        
        async with self.get_connection() as conn:
            await conn.execute(
                query, status, assigned_agent_id, started_at, 
                completed_at, error_message, task_id
            )
    
    async def update_task_parameters(self, task_id: UUID, parameters: Dict[str, Any]) -> None:
        """Update task parameters"""
        query = "UPDATE tasks SET parameters = $1 WHERE id = $2"
        
        async with self.get_connection() as conn:
            await conn.execute(query, json.dumps(parameters), task_id)
    
    # Agent Operations
    
    async def create_agent(self, agent: Agent) -> Agent:
        """Create a new agent in the database"""
        query = """
        INSERT INTO agents (id, name, instance_key, category, provider, model, 
                           specialization, config, status, created_at)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
        RETURNING *
        """
        
        async with self.get_connection() as conn:
            row = await conn.fetchrow(
                query,
                agent.id, agent.name, agent.instance_key, agent.category,
                agent.provider, agent.model, agent.specialization,
                json.dumps(agent.config), agent.status, agent.created_at
            )
            return self._row_to_agent(row)
    
    async def get_agents_for_category(self, category: TaskCategory, 
                                    status: AgentStatus = AgentStatus.ACTIVE) -> List[Agent]:
        """Get all agents for a specific category"""
        query = "SELECT * FROM agents WHERE category = $1 AND status = $2 ORDER BY name"
        
        async with self.get_connection() as conn:
            rows = await conn.fetch(query, category, status)
            return [self._row_to_agent(row) for row in rows]
    
    async def get_agent(self, agent_id: UUID) -> Optional[Agent]:
        """Get an agent by ID"""
        query = "SELECT * FROM agents WHERE id = $1"
        
        async with self.get_connection() as conn:
            row = await conn.fetchrow(query, agent_id)
            return self._row_to_agent(row) if row else None
    
    async def get_agent_by_key(self, instance_key: str) -> Optional[Agent]:
        """Get an agent by instance key"""
        query = "SELECT * FROM agents WHERE instance_key = $1"
        
        async with self.get_connection() as conn:
            row = await conn.fetchrow(query, instance_key)
            return self._row_to_agent(row) if row else None
    
    async def get_all_agents(self) -> List[Agent]:
        """Get all agents"""
        query = "SELECT * FROM agents ORDER BY category, name"
        
        async with self.get_connection() as conn:
            rows = await conn.fetch(query)
            return [self._row_to_agent(row) for row in rows]
    
    # System Operations
    
    async def get_system_stats(self) -> Dict[str, int]:
        """Get system statistics"""
        queries = {
            'total_jobs': "SELECT COUNT(*) FROM jobs",
            'active_jobs': "SELECT COUNT(*) FROM jobs WHERE status IN ('pending', 'in_progress')",
            'total_tasks': "SELECT COUNT(*) FROM tasks",
            'pending_tasks': "SELECT COUNT(*) FROM tasks WHERE status = 'pending'",
            'total_agents': "SELECT COUNT(*) FROM agents",
            'active_agents': "SELECT COUNT(*) FROM agents WHERE status = 'active'"
        }
        
        stats = {}
        async with self.get_connection() as conn:
            for key, query in queries.items():
                result = await conn.fetchval(query)
                stats[key] = result or 0
        
        return stats
    
    async def health_check(self) -> bool:
        """Check database connectivity"""
        try:
            async with self.get_connection() as conn:
                await conn.fetchval("SELECT 1")
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False


# Global database manager instance
db_manager = DatabaseManager()


# Convenience functions
async def init_database() -> None:
    """Initialize database connection and create schema"""
    await db_manager.initialize()
    await db_manager.create_schema()


async def close_database() -> None:
    """Close database connections"""
    await db_manager.close()
