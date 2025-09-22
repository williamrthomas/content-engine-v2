#!/usr/bin/env python3
"""
Content Engine V2 - Professional Content Creation CLI

A comprehensive command-line interface for the Content Engine V2 system,
providing LLM-powered content creation with real asset generation capabilities.

Features:
- LLM-intelligent template selection and job naming
- Real image generation via Freepik Mystic API
- Template-driven agent selection for deterministic workflows
- Complete job lifecycle management with rich progress indicators
- Built-in testing and validation commands

Usage:
    python cli.py setup                    # Initialize system
    python cli.py create "Your request"    # Create content job
    python cli.py run <job-id>             # Execute job tasks
    python cli.py status <job-id>          # Check job status
    python cli.py help                     # Show usage guide

Author: Content Engine V2 Team
Version: Phase 3+ Complete
"""

import asyncio
import functools
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List
from uuid import UUID

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Confirm
from rich import print as rprint

from src.core.config import settings, ensure_directories
from src.core.database import db_manager, init_database, close_database
from src.core.models import Job, JobStatus, TaskStatus, JobCreateRequest
from src.templates.loader import template_loader
from src.engine.content_engine import ContentEngine

# Initialize Rich console
console = Console()

# Main app
app = typer.Typer(
    name="content-engine",
    help="🚀 Content Engine V2 - LLM-Orchestrated Content Creation System",
    rich_markup_mode="rich",
    no_args_is_help=True,
    add_completion=False
)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.log_file) if settings.log_file else logging.NullHandler(),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def setup_async(func):
    """Decorator to run async functions in CLI commands"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return asyncio.run(func(*args, **kwargs))
    return wrapper


@app.command("help")
def show_help():
    """📚 Show detailed usage examples and tips"""
    
    console.print(Panel.fit(
        "[bold cyan]🚀 Content Engine V2 - Usage Guide[/bold cyan]\n\n"
        "[bold yellow]📋 QUICK START:[/bold yellow]\n"
        "  [cyan]python cli.py setup[/cyan]                           # Initialize system\n"
        "  [cyan]python cli.py templates[/cyan]                       # See available templates\n"
        "  [cyan]python cli.py create <template> \"Your context\"[/cyan]  # Create job\n"
        "  [cyan]python cli.py run <job-id>[/cyan]                    # Execute job\n\n"
        "[bold yellow]🎯 DETERMINISTIC WORKFLOWS:[/bold yellow]\n"
        "  Blog Posts:\n"
        "    [cyan]python cli.py create blog-post \"Sustainable energy trends for 2024\"[/cyan]\n"
        "  \n"
        "  YouTube Content:\n"
        "    [cyan]python cli.py create youtube-tutorial \"Docker containerization basics\"[/cyan]\n"
        "  \n"
        "  Daily Lists (with real images):\n"
        "    [cyan]python cli.py create top-x-daily-list \"Top 5 AI breakthroughs today\"[/cyan]\n\n"
        "[bold yellow]🔧 SYSTEM TESTING:[/bold yellow]\n"
        "  [cyan]python cli.py llm-test[/cyan]        # Test LLM integration\n"
        "  [cyan]python cli.py freepik-test[/cyan]    # Test image generation\n"
        "  [cyan]python cli.py templates[/cyan]       # Show available templates\n\n"
        "[bold yellow]📊 JOB MANAGEMENT:[/bold yellow]\n"
        "  [cyan]python cli.py list[/cyan]            # Show recent jobs\n"
        "  [cyan]python cli.py status <id>[/cyan]     # Check job details\n"
        "  [cyan]python cli.py run <id>[/cyan]        # Execute job tasks\n"
        "  [cyan]python cli.py review <id>[/cyan]     # Review job outputs\n\n"
        "[bold yellow]💡 Template-driven workflow ensures deterministic agent selection![/bold yellow]",
        border_style="blue"
    ))


@app.command("create")
def create(
    template: str = typer.Argument(..., help="Template name (use 'templates' command to see options)"),
    context: str = typer.Argument(..., help="Your specific context/topic for this template")
):
    """🚀 Create a new content job with deterministic template selection"""
    asyncio.run(_create_job_deterministic(template, context))


@app.command("run")
@setup_async
async def run_job(
    job_id: str = typer.Argument(..., help="🆔 Job number (1, 2, 3...) or full UUID"),
    monitor: bool = typer.Option(False, "--monitor", "-m", help="📊 Watch progress in real-time")
):
    """⚡ Execute a job by running all its tasks sequentially"""
    
    try:
        await init_database()
        
        try:
            resolved_job_id = await _resolve_job_id(job_id)
            job_uuid = UUID(resolved_job_id)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            console.print("[dim]💡 Use 'python cli.py list' to see job numbers[/dim]")
            raise typer.Exit(1)
        
        engine = ContentEngine()
        job_response = await engine.get_job_status(job_uuid)
        if not job_response:
            console.print(f"[red]Job not found: {job_id}[/red]")
            raise typer.Exit(1)
        
        job = job_response.job
        console.print(f"\n[bold blue]Processing job: {job.display_name or job.name}[/bold blue]")
        console.print(f"Job ID: [dim]{job.id}[/dim]")
        console.print(f"Tasks: [yellow]{len(job_response.tasks)}[/yellow]")
        
        if job.status == JobStatus.COMPLETED:
            console.print("[yellow]Job is already completed ✅[/yellow]")
            return
        
        if job.status == JobStatus.IN_PROGRESS:
            console.print("[yellow]Job is already in progress 🔄[/yellow]")
            if not Confirm.ask("Continue processing?"):
                return
        
        console.print("\n[blue]Starting job processing...[/blue]")
        
        if monitor:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("Processing job...", total=None)
                
                success = await engine.process_job(job_uuid)
                
                if success:
                    progress.update(task, description="Job completed successfully!")
                    console.print("\n[green]✓ Job processing completed successfully! 🎉[/green]")
                else:
                    progress.update(task, description="Job processing failed!")
                    console.print("\n[red]✗ Job processing failed ❌[/red]")
        else:
            success = await engine.process_job(job_uuid)
            
            if success:
                console.print("\n[green]✓ Job processing completed successfully! 🎉[/green]")
            else:
                console.print("\n[red]✗ Job processing failed ❌[/red]")
        
        # Show final status
        final_response = await engine.get_job_status(job_uuid)
        if final_response:
            status_color = "green" if final_response.job.status == "completed" else "red"
            console.print(f"\nFinal status: [{status_color}]{final_response.job.status}[/{status_color}]")
            
            completed_tasks = sum(1 for t in final_response.tasks if t.status == TaskStatus.COMPLETED)
            failed_tasks = sum(1 for t in final_response.tasks if t.status == TaskStatus.FAILED)
            
            console.print(f"Tasks completed: [green]{completed_tasks}[/green]")
            if failed_tasks > 0:
                console.print(f"Tasks failed: [red]{failed_tasks}[/red]")
        
    except Exception as e:
        console.print(f"[red]Error processing job: {e}[/red]")
        raise typer.Exit(1)
    finally:
        await close_database()


@app.command("status")
@setup_async
async def job_status(
    job_id: str = typer.Argument(..., help="🆔 Job number (1, 2, 3...) or full UUID")
):
    """📊 Check the detailed status of a specific job"""
    
    try:
        await init_database()
        
        try:
            resolved_job_id = await _resolve_job_id(job_id)
            job_uuid = UUID(resolved_job_id)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            console.print("[dim]💡 Use 'python cli.py list' to see job numbers[/dim]")
            raise typer.Exit(1)
        
        engine = ContentEngine()
        job_response = await engine.get_job_status(job_uuid)
        
        if not job_response:
            console.print(f"[red]Job not found: {job_id}[/red]")
            raise typer.Exit(1)
        
        job = job_response.job
        
        # Job info panel
        job_info = (
            f"[bold]Name:[/bold] {job.display_name or job.name}\n"
            f"[bold]ID:[/bold] {job.id}\n"
            f"[bold]Template:[/bold] {job.template_name or 'None'}\n"
            f"[bold]Status:[/bold] {job.status}\n"
            f"[bold]Created:[/bold] {job.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"[bold]Request:[/bold] {job.user_request}"
        )
        
        console.print(Panel(job_info, title="Job Details", border_style="blue"))
        
        # Tasks table
        if job_response.tasks:
            table = Table(title=f"Tasks ({len(job_response.tasks)})", show_header=True)
            table.add_column("Task", style="white", min_width=20)
            table.add_column("Category", style="cyan")
            table.add_column("Status", style="yellow")
            table.add_column("Order", style="dim")
            
            for task in sorted(job_response.tasks, key=lambda t: (t.category, t.sequence_order)):
                status_emoji = {
                    "pending": "⏳",
                    "in_progress": "🔄",
                    "completed": "✅",
                    "failed": "❌"
                }.get(task.status, "❓")
                
                table.add_row(
                    task.task_name,
                    task.category,
                    f"{status_emoji} {task.status}",
                    str(task.sequence_order)
                )
            
            console.print(table)
            
            # Summary
            status_counts = {}
            for task in job_response.tasks:
                if task.status not in status_counts:
                    status_counts[task.status] = 0
                status_counts[task.status] += 1
            
            summary = " | ".join([f"{status}: {count}" for status, count in status_counts.items()])
            console.print(f"\n[dim]Summary: {summary}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error getting job status: {e}[/red]")
        raise typer.Exit(1)
    finally:
        await close_database()


@app.command("list")
@setup_async
async def list_jobs(
    limit: int = typer.Option(10, "--limit", "-l", help="🔢 Number of jobs to show (default: 10)")
):
    """📋 List recent jobs with their status"""
    
    try:
        await init_database()
        
        jobs = await db_manager.get_recent_jobs(limit)
        
        if not jobs:
            console.print("[yellow]No jobs found. Create your first job with:[/yellow]")
            console.print("[dim]python cli.py create <template> \"Your context\"[/dim]")
            return
        
        # Create table with index numbers
        table = Table(title=f"Recent Jobs ({len(jobs)})", show_lines=False)
        table.add_column("#", style="bold magenta", justify="center", width=3)
        table.add_column("Name", style="cyan", max_width=35)
        table.add_column("Template", style="green", max_width=15)
        table.add_column("Status", style="yellow", max_width=12)
        table.add_column("Tasks", justify="center", width=7)
        table.add_column("Created", style="dim", width=8)
        table.add_column("ID", style="blue", width=8)
        
        for i, job in enumerate(jobs, 1):
            # Get task count
            tasks = await db_manager.get_tasks_for_job(job.id)
            completed_tasks = len([t for t in tasks if t.status == TaskStatus.COMPLETED])
            total_tasks = len(tasks)
            
            # Format status with emoji
            status_emoji = {
                JobStatus.PENDING: "⏳",
                JobStatus.IN_PROGRESS: "🔄", 
                JobStatus.COMPLETED: "✅",
                JobStatus.FAILED: "❌"
            }
            
            status_display = f"{status_emoji.get(job.status, '❓')} {job.status}"
            
            table.add_row(
                str(i),
                job.display_name or job.name,
                job.template_name or "Unknown",
                status_display,
                f"{completed_tasks}/{total_tasks}",
                job.created_at.strftime("%m/%d %H:%M"),
                str(job.id)[:8]
            )
        
        console.print(table)
        console.print(f"\n[dim]💡 Quick commands:[/dim]")
        console.print(f"[dim]   python cli.py status 1      # Check job #1 details[/dim]")
        console.print(f"[dim]   python cli.py review 2      # Review job #2 outputs[/dim]")
        console.print(f"[dim]   python cli.py run 3         # Execute job #3[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error listing jobs: {e}[/red]")
        raise typer.Exit(1)
    finally:
        await close_database()


@app.command("templates")
@setup_async
async def show_templates():
    """📋 Show available content templates"""
    
    try:
        await template_loader.load_all_templates()
        template_names = template_loader.list_templates()
        
        if not template_names:
            console.print("[yellow]No templates found[/yellow]")
            return
        
        table = Table(title="Available Templates", show_header=True)
        table.add_column("Name", style="cyan")
        table.add_column("Description", style="white")
        table.add_column("Tasks", style="green")
        table.add_column("Categories", style="yellow")
        
        for name in template_names:
            template = template_loader.get_template(name)
            categories = {}
            for task in template.tasks:
                if task.category not in categories:
                    categories[task.category] = 0
                categories[task.category] += 1
            
            category_str = ", ".join([f"{cat}: {count}" for cat, count in categories.items()])
            
            table.add_row(
                name,
                template.description or template.title,
                str(len(template.tasks)),
                category_str
            )
        
        console.print(table)
        console.print(f"\n[dim]💡 Use --template <name> when creating jobs[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error loading templates: {e}[/red]")
        raise typer.Exit(1)


@app.command("setup")
@setup_async
async def setup_system():
    """🔧 Initialize the Content Engine system"""
    
    console.print("[blue]🚀 Setting up Content Engine V2...[/blue]")
    
    try:
        ensure_directories()
        console.print("✓ Directories created")
        
        await init_database()
        console.print("✓ Database initialized")
        
        templates = await template_loader.load_all_templates()
        console.print(f"✓ Loaded {len(templates)} templates")
        
        # Test LLM connection
        engine = ContentEngine()
        llm_status = await engine.test_llm_connection()
        if llm_status["connected"]:
            console.print("✓ LLM service connected (Phase 2 features enabled)")
        else:
            console.print("[yellow]⚠ LLM service unavailable (using fallback methods)[/yellow]")
        
        console.print("\n[green]🎉 Setup complete![/green]")
        console.print("\n[bold]Next steps:[/bold]")
        console.print("1. [cyan]python cli.py create \"Your content request\"[/cyan]")
        console.print("2. [cyan]python cli.py list[/cyan] - to see your jobs")
        console.print("3. [cyan]python cli.py llm-test[/cyan] - test LLM integration")
        console.print("4. [cyan]python cli.py help[/cyan] - for more examples")
        
    except Exception as e:
        console.print(f"[red]Setup failed: {e}[/red]")
        raise typer.Exit(1)
    finally:
        await close_database()


@app.command()
def llm_test():
    """Test LLM service connectivity and capabilities"""
    asyncio.run(_llm_test())


@app.command("freepik-test")
def freepik_test():
    """Test Freepik Mystic agent integration"""
    asyncio.run(_freepik_test())


@app.command("review")
def review(
    job_id: str = typer.Argument(..., help="Job number (1, 2, 3...) or full UUID"),
    category: Optional[str] = typer.Option(None, "--category", "-c", help="Filter by category (script, image, audio, video)"),
    export: bool = typer.Option(False, "--export", "-e", help="Export review to markdown file"),
    open_files: bool = typer.Option(False, "--open", "-o", help="Open asset files in default applications")
):
    """📋 Review job outputs and generated content"""
    asyncio.run(_review_job(job_id, category, export, open_files))


async def _resolve_job_id(job_identifier: str) -> str:
    """Resolve job identifier (number or UUID) to full UUID"""
    from uuid import UUID
    
    # If it's already a valid UUID, return as-is
    try:
        UUID(job_identifier)
        return job_identifier
    except ValueError:
        pass
    
    # If it's a number, resolve to UUID from recent jobs
    try:
        job_number = int(job_identifier)
        if job_number < 1:
            raise ValueError("Job number must be positive")
        
        # Get recent jobs and find the one at this index
        jobs = await db_manager.get_recent_jobs(50)  # Get more jobs to ensure we find it
        if job_number > len(jobs):
            raise ValueError(f"Job #{job_number} not found. Only {len(jobs)} recent jobs available.")
        
        # Return the UUID of the job at this index (1-based)
        return str(jobs[job_number - 1].id)
        
    except ValueError as e:
        if "invalid literal" in str(e):
            raise ValueError(f"Invalid job identifier: {job_identifier}. Use job number (1, 2, 3...) or full UUID.")
        raise e


async def _create_job_deterministic(template: str, context: str):
    """Create a job with explicit template selection and user context"""
    from src.engine.content_engine import ContentEngine
    from src.core.models import JobCreateRequest
    from src.templates.loader import template_loader
    
    console.print(f"\n[bold blue]Creating content job...[/bold blue]")
    console.print(f"Template: [bold green]{template}[/bold green]")
    console.print(f"Context: [italic]{context}[/italic]")
    
    try:
        await init_database()
        
        # Load templates to validate selection
        await template_loader.load_all_templates()
        available_templates = template_loader.get_template_names()
        
        if template not in available_templates:
            console.print(f"\n[red]❌ Template '{template}' not found[/red]")
            console.print(f"[yellow]Available templates:[/yellow]")
            for tmpl in available_templates:
                console.print(f"  • {tmpl}")
            console.print(f"\n[dim]💡 Use: python cli.py templates[/dim]")
            raise typer.Exit(1)
        
        # Create job with explicit template and context
        engine = ContentEngine()
        job_request = JobCreateRequest(
            user_request=context,
            template_name=template  # Force specific template
        )
        
        job_response = await engine.create_job(job_request)
        
        console.print(f"\n[green]✓ Job created successfully![/green]")
        console.print(f"Job ID: [bold cyan]{job_response.job.id}[/bold cyan]")
        console.print(f"Job Name: [bold]{job_response.job.name}[/bold]")
        console.print(f"Display Name: [bold]{job_response.job.display_name}[/bold]")
        console.print(f"Template: [bold green]{job_response.job.template_name}[/bold green] [dim](deterministic)[/dim]")
        console.print(f"Tasks Created: [bold yellow]{len(job_response.tasks)}[/bold yellow]")
        
        # Show task breakdown with agent assignments
        if job_response.tasks:
            console.print(f"\n[blue]Tasks breakdown:[/blue]")
            task_counts = {}
            agent_assignments = {}
            
            for task in job_response.tasks:
                # Count by category
                if task.category not in task_counts:
                    task_counts[task.category] = 0
                task_counts[task.category] += 1
                
                # Track agent assignments
                if task.preferred_agent:
                    if task.preferred_agent not in agent_assignments:
                        agent_assignments[task.preferred_agent] = 0
                    agent_assignments[task.preferred_agent] += 1
            
            for category, count in task_counts.items():
                console.print(f"  {category}: {count} tasks")
            
            if agent_assignments:
                console.print(f"\n[blue]Agent assignments:[/blue]")
                for agent, count in agent_assignments.items():
                    console.print(f"  {agent}: {count} tasks")
        
        console.print(f"Status: [yellow]{job_response.job.status}[/yellow]")
        console.print(f"\n[dim]💡 Next: python cli.py run {job_response.job.id}[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error creating job: {e}[/red]")
        raise typer.Exit(1)
    finally:
        await close_database()


async def _freepik_test():
    """Test Freepik agent functionality"""
    from src.agents.registry import agent_registry
    from src.core.models import Task, TaskCategory, TaskStatus
    from uuid import uuid4
    from rich.progress import Progress, SpinnerColumn, TextColumn
    
    console.print("🎨 [bold blue]Testing Freepik Integration...[/bold blue]")
    
    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Testing Freepik agent...", total=None)
            
            # Test agent availability
            freepik_agent = agent_registry.get_agent('freepik_mystic')
            progress.update(task, description="Freepik agent loaded!")
        
        # Display results
        if freepik_agent:
            console.print(f"\n[green]✅ Freepik Agent: {freepik_agent.name}[/green]")
            console.print(f"API Key Configured: {hasattr(freepik_agent, 'api_key') and freepik_agent.api_key is not None}")
            
            # Get capabilities
            capabilities = await freepik_agent.get_capabilities()
            console.print(f"Specializations: {len(capabilities['specializations'])}")
            
            # Test with sample task
            thumbnail_task = Task(
                id=uuid4(),
                job_id=uuid4(),
                task_name='design_thumbnail',
                category=TaskCategory.IMAGE,
                sequence_order=1,
                status=TaskStatus.PENDING,
                parameters={
                    'inputs': {'user_request': 'Test YouTube thumbnail'},
                    'requirements': {'style': 'bold', 'ai_visual_elements': True}
                }
            )
            
            result = await freepik_agent.execute(thumbnail_task)
            console.print(f"Test Execution: {result.status}")
            console.print(f"Quality Score: {result.metadata.get('quality_score', 'N/A')}")
            
            if result.outputs.get('api_available', True):
                console.print("\n[green]🎉 Freepik API integration ready![/green]")
                console.print("• Real image generation enabled")
                console.print("• Professional quality output")
                console.print("• Multi-format support")
            else:
                console.print("\n[yellow]📋 Specification mode active[/yellow]")
                console.print("• Detailed prompts generated")
                console.print("• API parameters optimized")
                console.print("• Ready for manual generation")
                console.print("\n[blue]💡 To enable image generation:[/blue]")
                console.print("export FREEPIK_API_KEY=your-api-key-here")
        else:
            console.print("\n[red]❌ Freepik agent not found[/red]")
            
    except Exception as e:
        console.print(f"\n[red]❌ Freepik test failed: {e}[/red]")


async def _llm_test():
    """Test LLM service functionality"""
    from src.engine.content_engine import ContentEngine
    from rich.progress import Progress, SpinnerColumn, TextColumn
    
    console.print("🧠 [bold blue]Testing LLM Integration...[/bold blue]")
    
    try:
        engine = ContentEngine()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("Testing LLM connection...", total=None)
            
            llm_status = await engine.test_llm_connection()
            
            progress.update(task, description="LLM test completed!")
        
        # Display results
        if llm_status["connected"]:
            console.print("\n[green]✅ LLM Service Status: Connected[/green]")
            console.print(f"Status: {llm_status['status']}")
            
            # Show usage stats if available
            if "usage_stats" in llm_status:
                stats = llm_status["usage_stats"]
                console.print(f"\n[blue]Usage Statistics:[/blue]")
                console.print(f"  Total requests: {stats.get('total_requests', 0)}")
                console.print(f"  Total tokens: {stats.get('total_tokens', 0)}")
                console.print(f"  Estimated cost: ${stats.get('estimated_cost', 0.0):.4f}")
            
            console.print("\n[green]🎉 Phase 2 features are fully operational![/green]")
            console.print("• Intelligent template selection")
            console.print("• Smart job naming")
            console.print("• Context-aware processing")
            
        else:
            console.print("\n[yellow]⚠️ LLM Service Status: Unavailable[/yellow]")
            if "error" in llm_status:
                console.print(f"Error: {llm_status['error']}")
            
            console.print("\n[blue]Fallback Mode Active:[/blue]")
            console.print("• Keyword-based template selection")
            console.print("• Simple job naming")
            console.print("• Basic processing (Phase 1 features)")
            
            console.print("\n[dim]💡 To enable LLM features:[/dim]")
            console.print("1. Set OPENROUTER_API_KEY in your .env file")
            console.print("2. Ensure internet connectivity")
            console.print("3. Run this test again")
        
    except Exception as e:
        console.print(f"[red]LLM test failed: {e}[/red]")
        raise typer.Exit(1)
    finally:
        await close_database()


async def _review_job(job_id: str, category: Optional[str], export: bool, open_files: bool):
    """Review job outputs and generated content"""
    from src.engine.content_engine import ContentEngine
    from src.core.database import db_manager
    from uuid import UUID
    from pathlib import Path
    import json
    
    console.print(f"\n[bold blue]📋 Reviewing Job Outputs[/bold blue]")
    console.print(f"Job: [cyan]{job_id}[/cyan]")
    
    try:
        await init_database()
        
        # Resolve job ID
        try:
            resolved_job_id = await _resolve_job_id(job_id)
            job_uuid = UUID(resolved_job_id)
        except ValueError as e:
            console.print(f"[red]{e}[/red]")
            console.print("[dim]💡 Use 'python cli.py list' to see job numbers[/dim]")
            raise typer.Exit(1)
        
        # Get job details
        engine = ContentEngine()
        job_response = await engine.get_job_status(job_uuid)
        if not job_response:
            console.print(f"[red]Job not found: {job_id}[/red]")
            raise typer.Exit(1)
        
        job = job_response.job
        tasks = job_response.tasks
        
        # Filter by category if specified
        if category:
            tasks = [t for t in tasks if t.category.lower() == category.lower()]
            if not tasks:
                console.print(f"[yellow]No tasks found for category: {category}[/yellow]")
                return
        
        # Display job overview
        console.print(f"\n[bold green]✅ Job: {job.display_name}[/bold green]")
        console.print(f"Template: [bold]{job.template_name}[/bold]")
        console.print(f"Status: [bold green]{job.status}[/bold green]")
        console.print(f"Created: {job.created_at}")
        if job.completed_at:
            console.print(f"Completed: {job.completed_at}")
        
        # Group tasks by category
        task_groups = {}
        for task in tasks:
            if task.category not in task_groups:
                task_groups[task.category] = []
            task_groups[task.category].append(task)
        
        # Review outputs by category
        review_content = []
        
        for cat, cat_tasks in task_groups.items():
            console.print(f"\n[bold yellow]📂 {cat.upper()} TASKS ({len(cat_tasks)})[/bold yellow]")
            review_content.append(f"\n## {cat.upper()} TASKS ({len(cat_tasks)})\n")
            
            for task in sorted(cat_tasks, key=lambda x: x.sequence_order):
                console.print(f"\n[cyan]🔹 {task.task_name}[/cyan]")
                console.print(f"   Status: [green]{task.status}[/green]")
                
                review_content.append(f"\n### {task.task_name}\n")
                review_content.append(f"- **Status**: {task.status}\n")
                
                # Get task details from database
                task_details = await db_manager.get_task_by_id(task.id)
                if task_details and hasattr(task_details, 'parameters'):
                    params = task_details.parameters
                    
                    # Show outputs if available
                    if 'outputs' in params:
                        outputs = params['outputs']
                        
                        # Display different types of outputs
                        if 'content' in outputs:
                            content = outputs['content']
                            if isinstance(content, str) and len(content) > 200:
                                console.print(f"   Content: [dim]{content[:200]}...[/dim]")
                                review_content.append(f"- **Content**: {content[:500]}{'...' if len(content) > 500 else ''}\n")
                            else:
                                console.print(f"   Content: [dim]{content}[/dim]")
                                review_content.append(f"- **Content**: {content}\n")
                        
                        if 'specifications' in outputs:
                            specs = outputs['specifications']
                            console.print(f"   Specifications: [dim]{len(specs)} items[/dim]")
                            review_content.append(f"- **Specifications**: {len(specs)} items\n")
                        
                        if 'image_url' in outputs:
                            image_url = outputs['image_url']
                            console.print(f"   Image: [green]{image_url}[/green]")
                            review_content.append(f"- **Image**: {image_url}\n")
                        
                        # Show quality score if available
                        if 'quality_score' in outputs:
                            score = outputs['quality_score']
                            color = "green" if score > 0.7 else "yellow" if score > 0.5 else "red"
                            console.print(f"   Quality: [{color}]{score:.2f}[/{color}]")
                            review_content.append(f"- **Quality Score**: {score:.2f}\n")
                        
                        # Show agent used
                        if 'agent_used' in outputs:
                            agent = outputs['agent_used']
                            console.print(f"   Agent: [blue]{agent}[/blue]")
                            review_content.append(f"- **Agent**: {agent}\n")
        
        # Export to markdown if requested
        if export:
            export_path = Path(f"job_review_{job_id[:8]}.md")
            with open(export_path, 'w') as f:
                f.write(f"# Job Review: {job.display_name}\n\n")
                f.write(f"**Job ID**: {job_id}\n")
                f.write(f"**Template**: {job.template_name}\n")
                f.write(f"**Status**: {job.status}\n")
                f.write(f"**Created**: {job.created_at}\n")
                if job.completed_at:
                    f.write(f"**Completed**: {job.completed_at}\n")
                f.write("\n---\n")
                f.writelines(review_content)
            
            console.print(f"\n[green]📄 Review exported to: {export_path}[/green]")
        
        # Show helpful commands
        console.print(f"\n[dim]💡 Helpful commands:[/dim]")
        console.print(f"[dim]   python cli.py review {job_id} --export    # Export to markdown[/dim]")
        console.print(f"[dim]   python cli.py review {job_id} -c script   # Review only script tasks[/dim]")
        
    except Exception as e:
        console.print(f"[red]Error reviewing job: {e}[/red]")
        raise typer.Exit(1)
    finally:
        await close_database()


if __name__ == "__main__":
    app()
