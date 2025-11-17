# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the documentation project for MotrixSim, a high-performance physics simulation engine for multibody dynamics and robotics simulation. The documentation is built using Sphinx and targets both Chinese and English audiences.

## Key Commands

### Building Documentation
- **Build HTML**: `make html` or `sphinx-build -b html source build/html`
- **Clean build**: `make clean` followed by `make html`
- **Serve locally**: `python -m http.server 8000 -d build/html`
- **Watch mode**: Use `sphinx-autobuild source build/html --host 0.0.0.0 --port 8000`

### Development Tools
- **Check links**: `make linkcheck`
- **Build PDF**: `make latexpdf` (requires LaTeX)
- **Build single HTML**: `make singlehtml`
- **Build EPUB**: `make epub`

## Documentation Structure

### Source Organization
- **source/**: Main documentation source files
  - **index.md**: Landing page with project overview and videos
  - **user_guide/**: User documentation and tutorials
  - **api_reference/**: API documentation and reference
  - **en/**: English language content
  - **zh_CN/**: Chinese language content
  - **_static/**: Static assets (images, videos, CSS, JS)

### User Guide Structure
- **getting_started/**: Installation and quick start guides
- **overview/**: Project overview and comparisons
- **kinematics/**: Kinematics documentation (joints, bodies, sensors, etc.)
- **main_function/**: Core functionality documentation
- **render/**: Rendering and visualization documentation

### API Reference Structure
- **core/**: Core API modules
- **ik/**: Inverse kinematics API
- **rendering/**: Rendering and visualization API
- **low/**: Low-level API (excluded from main documentation)

## Build Configuration

### Sphinx Configuration (conf.py)
- **Theme**: PyData Sphinx Theme with custom branding
- **Extensions**:
  - sphinx.ext.autodoc (API documentation from docstrings)
  - sphinx.ext.napoleon (NumPy/Google style docstrings)
  - sphinx.ext.autosummary (automated summaries)
  - myst_parser (Markdown support)
  - sphinx-design (design components)
  - sphinx_copybutton (code copy functionality)
- **Language Support**: Chinese (zh_CN) and English with automatic content copying
- **Autodoc**: Automatic API documentation generation

### Dependencies
Documentation dependencies are managed in the parent `pyproject.toml`:
```toml
docs = [
    "sphinx",
    "autodocsumm",
    "pydata-sphinx-theme",
    "myst-parser",
    "sphinx-copybutton",
    "sphinx-subfigure",
    "sphinxcontrib-video",
    "sphinx-togglebutton",
    "sphinx-design",
]
```

## Content Guidelines

### Documentation Style
- **Primary Language**: Chinese (zh_CN) with English translations
- **Format**: Markdown (.md) files using MyST parser
- **Code Examples**: Include practical code examples with proper syntax highlighting
- **API Documentation**: Use NumPy/Google style docstrings for autodoc generation

### Important: Document Structure
**Critical**: The documentation has a specific structure that must be followed:

- **`source/user_guide/`**: This directory is **auto-generated** during build. **DO NOT** edit files here directly.
- **`source/zh_CN/`**: This directory contains the **manually written** Chinese documentation. All edits should be made here.
- **`source/en/`**: This directory contains the **manually written** English documentation.

The build system automatically copies content from language-specific directories (`zh_CN/`, `en/`) to the main structure during compilation. Always edit the source files in the appropriate language directory, not the auto-generated files.

### Media and Assets
- **Videos**: Embedded using sphinxcontrib-video extension
- **Images**: Stored in `_static/images/` with poster images for videos
- **Static Files**: Custom CSS and JavaScript in `_static/` directory
- **Logos**: Light and dark theme variants available

### Multilingual Support
- **Default Language**: Chinese (zh_CN)
- **Content Copying**: Automatic copying of language-specific content during build
- **Theme**: Supports both light and dark themes with appropriate logos

## Development Workflow

### Adding New Documentation
1. Create Markdown files in appropriate directory (user_guide/ or api_reference/)
2. Follow existing structure and naming conventions
3. Update table of contents in relevant index.md files
4. Test build locally before committing

### API Documentation
1. Write docstrings in Python source code using NumPy/Google style
2. Use autodoc directives to generate API documentation
3. Organize API docs by functional modules
4. Include examples and usage notes

### Building and Testing
1. Always build locally before committing: `make html`
2. Check for broken links: `make linkcheck`
3. Verify multilingual content works correctly
4. Test all embedded media and interactive elements

## Integration Notes
- This documentation project is part of the larger motrixsim-py package
- The build system automatically detects and documents the motrixsim package
- Documentation is deployed to ReadTheDocs at https://motrixsim.readthedocs.io
- Source code is hosted at https://github.com/Motphys/motrixsim-docs