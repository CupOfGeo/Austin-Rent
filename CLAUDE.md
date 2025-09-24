When working I expect
- module, class, function, and variable names should be descriptive, unambiguous and communicate the design’s intent and purpose clearly.
- Use appropriate design patterns. Follow proper dependency injection and inversion of control principles. Ensure code is DRY (Don't Repeat Yourself).
- Write clean, maintainable, and well-documented code. Write doc strings for all modules, classes and functions. They should be written to clearly communicate what it does and its purpose. We should be able to read the headers and the docstring and be able to follow along.
- Don't do more than is tasked of you. Which means on extra functions then what is agreed upon. if you want to add extra functions or things thats not needed for the current task please ask first.
- Never use emojis or they will set us both on fire
- feel free to make a simple poc file to prove a concept in an isolated environment to get working fist then go back and make the correct changes.

- To us uv instead of pip. and to let me run the mcp server and I will paste the logs
- Include proper structured logging with structlog and monitoring capabilities. Writing lots of debug logs!
- Use pydantic for models. And store any settings in the appropriate config.py.
- Write tests in pytest. We are looking for meaningful unit tests not just coverage.
- Don't use a ORM Write raw SQL. Create a migration file of any new tables or adjustments to tables.

Python Naming Conventions Summary
Class Names:

Use CapWords or UpperCamelCase (e.g., StudentRecord, GradeCalculator)
Use singular nouns, not plural
Be descriptive but not overly long
Avoid implementation details like "Manager" or "Widget"
Don't replicate Python builtin type names
Base classes often use prefixes like Base, Abstract, or Meta

Object/Instance Names:

Use lowercase_with_underscores (e.g., student_record, grade_calc)
Be descriptive and unambiguous
Avoid single letters except for counters/iterators
Should differ from the class name
Abbreviations are acceptable if meaning is clear

Method Names:

Use lowercase_underscore format
Use verb phrases that describe the action
Private methods prefix with single underscore _method_name

Private Attributes:

Single underscore prefix for internal use: _private_attr
Double underscore prefix to avoid name collisions: __private_attr

Key Principles:

Names should clearly communicate purpose
Maintain consistency across the codebase
Follow PEP 8 guidelines
Avoid Python keywords and builtin names
Balance descriptiveness with brevity

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.
