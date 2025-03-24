# MCP Example Project

This is a simple example of a Model Context Protocol (MCP) server implementation in Python. The server demonstrates basic MCP features including resources, tools, and prompts.

## Features

- Resource endpoint for getting greetings
- Tool for calculating mathematical operations
- Prompt template for generating responses

## Requirements

- Python 3.8+
- MCP SDK

## Installation

```bash
pip install mcp
```

## Usage

Run the server:

```bash
python main.py
```

## API Endpoints

### Resources
- `greeting://{name}` - Get a personalized greeting

### Tools
- `calculate` - Perform basic mathematical operations

### Prompts
- `response` - Generate a response based on input 