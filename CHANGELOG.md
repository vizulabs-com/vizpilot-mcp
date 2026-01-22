# Changelog

All notable changes to VIZPILOT MCP Server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-22

### Added
- Initial release of VIZPILOT MCP Server
- Six core MCP tools:
  - `list_technologies` - List all available technologies
  - `list_protocols` - List protocols for a technology
  - `get_protocol` - Get full protocol content
  - `get_steering_rules` - Get steering rules for IDE injection
  - `search_protocols` - Search across all protocols
  - `get_user_info` - Get subscription and usage info
- API key authentication
- Rate limiting based on subscription tier
- Content watermarking for security
- Redis caching for performance
- Support for multiple IDEs (Kiro, Cursor, VS Code)
- Comprehensive error handling
- Usage tracking and analytics
- Support for 20+ technologies/frameworks

### Security
- API key-based authentication
- Rate limiting per user tier
- Content watermarking
- HTTPS-only communication
- Secure token storage

### Performance
- Redis caching layer
- Optimized database queries
- Async/await support
- Connection pooling

## [Unreleased]

### Planned Features
- WebSocket support for real-time updates
- Offline protocol caching
- Custom protocol creation
- Team collaboration features
- Protocol versioning
- Advanced search with filters
- Protocol recommendations based on usage
- Integration with more IDEs
- Multi-language support
- Protocol templates
- Code snippet extraction
- Interactive protocol tutorials

### Planned Improvements
- Enhanced caching strategies
- Better error messages
- Improved rate limiting
- Performance optimizations
- Extended documentation
- More example configurations
- Video tutorials
- Community protocol contributions

---

## Version History

- **1.0.0** (2026-01-22) - Initial public release

## Support

For questions or issues, please:
- Open an issue on [GitHub](https://github.com/vizulabs/vizpilot-mcp/issues)
- Join our [Discord](https://discord.gg/vizpilot)
- Email [support@vizulabs.com](mailto:support@vizulabs.com)

## Links

- [Documentation](https://docs.vizpilot.vizulabs.com/mcp)
- [Website](https://vizpilot.vizulabs.com)
- [PyPI](https://pypi.org/project/vizpilot-mcp/)
