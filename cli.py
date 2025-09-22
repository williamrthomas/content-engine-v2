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
        "  [cyan]python cli.py run <id>[/cyan]        # Execute job tasks\n\n"
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
    job_id: str = typer.Argument(..., help="🆔 Job ID to execute (get from 'create' or 'list' command)"),
    monitor: bool = typer.Option(False, "--monitor", "-m", help="📊 Watch progress in real-time")
):
    """⚡ Execute a job by running all its tasks sequentially"""
    
    try:
        await init_database()
        
        try:
            job_uuid = UUID(job_id)
        except ValueError:
            console.print(f"[red]Invalid job ID format: {job_id}[/red]")
            console.print("[dim]💡 Get job ID from 'python cli.py list'[/dim]")
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
    job_id: str = typer.Argument(..., help="🆔 Job ID to check (get from 'list' command)")
):
    """📊 Check the detailed status of a specific job"""
    
    try:
        await init_database()
        
        try:
            job_uuid = UUID(job_id)
        except ValueError:
            console.print(f"[red]Invalid job ID format: {job_id}[/red]")
            console.print("[dim]💡 Get job ID from 'python cli.py list'[/dim]")
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
    status: Optional[str] = typer.Option(None, "--status", "-s", help="🔍 Filter by status (pending, completed, failed)"),
    limit: int = typer.Option(10, "--limit", "-l", help="📊 Maximum jobs to show")
):
    """📋 List recent jobs with their status"""
    
    try:
        await init_database()
        engine = ContentEngine()
        
        status_filter = None
        if status:
            try:
                status_filter = JobStatus(status.lower())
            except ValueError:
                console.print(f"[red]Invalid status: {status}. Use: pending, completed, failed[/red]")
                raise typer.Exit(1)
        
        jobs = await engine.list_jobs(status=status_filter, limit=limit)
        
        if not jobs:
            console.print("[yellow]No jobs found[/yellow]")
            console.print("[dim]💡 Create your first job: python cli.py create \"Your request\"[/dim]")
            return
        
        table = Table(title=f"Recent Jobs ({len(jobs)})", show_header=True)
        table.add_column("ID", style="dim", width=8)
        table.add_column("Name", style="white", min_width=30)
        table.add_column("Template", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Created", style="blue")
        
        for job in jobs:
            status_emoji = {
                "pending": "⏳",
                "in_progress": "🔄", 
                "completed": "✅",
                "failed": "❌"
            }.get(job.status, "❓")
            
            short_id = str(job.id)[:8]
            display_name = job.display_name or job.name
            if len(display_name) > 40:
                display_name = display_name[:37] + "..."
            
            table.add_row(
                short_id,
                display_name,
                job.template_name or "None",
                f"{status_emoji} {job.status}",
                job.created_at.strftime('%m/%d %H:%M')
            )
        
        console.print(table)
        console.print(f"\n[dim]💡 Use full job ID for commands: python cli.py status <full-job-id>[/dim]")
        
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


@app.command()
def freepik_test():
    """Test Freepik Mystic agent integration"""
    asyncio.run(_freepik_test())


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


if __name__ == "__main__":
    app()
