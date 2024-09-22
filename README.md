# AI Course Planner

This project provides a structured approach to creating comprehensive course outlines for AI-related topics, with a focus on Large Language Models (LLMs).

## Features

- Pydantic models for course structure representation
- Task definition for course planning
- Emphasis on lesson-specific and general course resources

## Usage

```python
from course_planner import CourseOutline, course_planner_task

# Initialize course planner with a topic
planner = course_planner_task(topic="AI Large Language Models")

# Generate course outline
outline = CourseOutline(**planner.execute())

# Access course details
print(outline.title)
print(outline.modules[0].lessons[0].resources)
```

## Requirements

- Python 3.7+
- Pydantic

## Installation

```
pip install pydantic
```

Customize the course planner by modifying the `course_planner_task` definition and `CourseOutline` model as needed.
