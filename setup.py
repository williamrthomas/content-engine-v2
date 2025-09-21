#!/usr/bin/env python3
"""Setup script for Content Engine V2"""

import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.core.database import init_database, close_database
from src.core.config import settings, ensure_directories
from src.templates.loader import template_loader


async def setup_system():
    """Complete system setup"""
    print("🚀 Setting up Content Engine V2...")
    
    try:
        # 1. Ensure directories exist
        print("📁 Creating directories...")
        ensure_directories()
        print("✓ Directories created")
        
        # 2. Initialize database
        print("🗄️  Initializing database...")
        await init_database()
        print("✓ Database initialized")
        
        # 3. Load templates
        print("📋 Loading templates...")
        templates = await template_loader.load_all_templates()
        print(f"✓ Loaded {len(templates)} templates")
        
        # 4. Show configuration
        print("\n⚙️  Configuration:")
        print(f"  Database: {settings.database_url[:50]}...")
        print(f"  Assets Dir: {settings.assets_dir}")
        print(f"  Templates Dir: {settings.templates_dir}")
        print(f"  Log Level: {settings.log_level}")
        
        print("\n🎉 Content Engine V2 setup complete!")
        print("\nNext steps:")
        print("1. Set your OpenRouter API key in .env file")
        print("2. Run: python cli.py --help")
        print("3. Create your first job: python cli.py create 'Write a blog post about AI'")
        
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        sys.exit(1)
    finally:
        await close_database()


if __name__ == "__main__":
    asyncio.run(setup_system())
