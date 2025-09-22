"""Template loading and parsing from markdown files"""

import re
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional
import yaml

from ..core.models import Template, TemplateTask, TaskCategory
from ..core.config import settings

logger = logging.getLogger(__name__)


class TemplateLoader:
    """Loads and parses markdown templates"""
    
    def __init__(self, templates_dir: Optional[Path] = None):
        self.templates_dir = templates_dir or settings.templates_dir
        self.templates: Dict[str, Template] = {}
    
    async def load_all_templates(self) -> Dict[str, Template]:
        """Load all templates from the templates directory"""
        if not self.templates_dir.exists():
            logger.warning(f"Templates directory does not exist: {self.templates_dir}")
            return {}
        
        templates = {}
        for template_file in self.templates_dir.glob("*.md"):
            try:
                template = await self.load_template(template_file.stem)
                if template:
                    templates[template.name] = template
                    logger.info(f"Loaded template: {template.name}")
            except Exception as e:
                logger.error(f"Failed to load template {template_file}: {e}")
        
        self.templates = templates
        return templates
    
    async def load_template(self, template_name: str) -> Optional[Template]:
        """Load a specific template by name"""
        template_path = self.templates_dir / f"{template_name}.md"
        
        if not template_path.exists():
            logger.error(f"Template file not found: {template_path}")
            return None
        
        try:
            content = template_path.read_text(encoding='utf-8')
            return self.parse_template(template_name, content)
        except Exception as e:
            logger.error(f"Failed to load template {template_name}: {e}")
            return None
    
    def parse_template(self, template_name: str, content: str) -> Template:
        """Parse markdown template content into a Template object"""
        lines = content.split('\n')
        
        # Extract title (first # heading)
        title = template_name.replace('-', ' ').title()
        description = ""
        category = "general"
        metadata = {}
        tasks = []
        
        current_section = None
        current_task = None
        current_category = None
        sequence_counters = {"script": 0, "image": 0, "audio": 0, "video": 0}
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip empty lines
            if not line:
                i += 1
                continue
            
            # Extract title from first heading
            if line.startswith('# ') and not title:
                title = line[2:].strip()
                i += 1
                continue
            
            # Extract metadata from bold fields
            if line.startswith('**') and line.endswith('**') and ':' in line:
                key_value = line[2:-2].split(':', 1)
                if len(key_value) == 2:
                    key = key_value[0].strip().lower().replace(' ', '_')
                    value = key_value[1].strip()
                    
                    if key == 'category':
                        category = value
                    else:
                        metadata[key] = value
                i += 1
                continue
            
            # Detect task sections
            if line.startswith('### ') and 'Tasks' in line:
                current_section = 'tasks'
                current_category = self._extract_category_from_heading(line)
                i += 1
                continue
            
            # Parse task items
            if current_section == 'tasks' and current_category:
                # Task number and name (e.g., "1. **task_name**")
                task_match = re.match(r'^\d+\.\s*\*\*([^*]+)\*\*', line)
                if task_match:
                    # Save previous task if exists
                    if current_task:
                        tasks.append(current_task)
                    
                    # Start new task
                    task_name = task_match.group(1).strip()
                    sequence_counters[current_category] += 1
                    
                    current_task = TemplateTask(
                        name=task_name,
                        description="",
                        category=TaskCategory(current_category),
                        sequence_order=sequence_counters[current_category],
                        parameters={}
                    )
                    i += 1
                    continue
                
                # Task description (next line after task name)
                if current_task and line.startswith('   - ') and not current_task.description and not line.startswith('   - Agent:') and not line.startswith('   - Parameters:'):
                    current_task.description = line[5:].strip()
                    i += 1
                    continue
                
                # Task agent specification (e.g., "   - Agent: freepik_mystic")
                if current_task and line.startswith('   - Agent:'):
                    agent_name = line[11:].strip()
                    current_task.preferred_agent = agent_name
                    i += 1
                    continue
                
                # Task parameters (e.g., "   - Parameters: {key: value}")
                if current_task and line.startswith('   - Parameters:'):
                    params_text = line[17:].strip()
                    try:
                        # Simple parameter parsing - could be enhanced
                        if params_text.startswith('{') and params_text.endswith('}'):
                            # Remove braces and parse key-value pairs
                            params_content = params_text[1:-1]
                            params = {}
                            for param in params_content.split(','):
                                if ':' in param:
                                    key, value = param.split(':', 1)
                                    key = key.strip().strip('"\'')
                                    value = value.strip().strip('"\'')
                                    # Try to convert to appropriate type
                                    if value.lower() == 'true':
                                        value = True
                                    elif value.lower() == 'false':
                                        value = False
                                    elif value.isdigit():
                                        value = int(value)
                                    params[key] = value
                            current_task.parameters = params
                    except Exception as e:
                        logger.warning(f"Failed to parse parameters for task {current_task.name}: {e}")
                    i += 1
                    continue
            
            i += 1
        
        # Save last task if exists
        if current_task:
            tasks.append(current_task)
        
        return Template(
            name=template_name,
            title=title,
            description=description,
            category=category,
            tasks=tasks,
            metadata=metadata
        )
    
    def _extract_category_from_heading(self, heading: str) -> str:
        """Extract task category from section heading"""
        heading_lower = heading.lower()
        if 'script' in heading_lower:
            return 'script'
        elif 'image' in heading_lower:
            return 'image'
        elif 'audio' in heading_lower:
            return 'audio'
        elif 'video' in heading_lower:
            return 'video'
        else:
            return 'script'  # Default to script
    
    def get_template(self, template_name: str) -> Optional[Template]:
        """Get a loaded template by name"""
        return self.templates.get(template_name)
    
    def get_templates(self) -> List[Template]:
        """Get all loaded templates"""
        return list(self.templates.values())
    
    def get_template_names(self) -> List[str]:
        """Get list of available template names"""
        return list(self.templates.keys())
    
    def get_templates_by_category(self, category: str) -> List[Template]:
        """Get templates filtered by category"""
        return [t for t in self.templates.values() if t.category == category]


# Global template loader instance
template_loader = TemplateLoader()
