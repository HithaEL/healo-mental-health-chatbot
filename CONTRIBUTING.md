# Contributing to Healo Mental Health Chatbot

Thank you for your interest in contributing to Healo! We welcome contributions from the community to help improve this mental health support tool.

## 🤝 How to Contribute

### 1. Reporting Issues
- Use the GitHub Issues tab to report bugs or suggest features
- Provide clear descriptions and steps to reproduce issues
- Include relevant system information (OS, Python version, etc.)

### 2. Adding Training Data
- Submit new mental health scenarios and responses
- Ensure responses are empathetic and professional
- Follow the existing format in the CSV files
- Include both friend and professional mode responses

### 3. Code Contributions
- Fork the repository
- Create a feature branch
- Make your changes
- Test thoroughly
- Submit a pull request

## 📋 Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- pip

### Setup Steps
1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/healo-mental-health-chatbot.git
   cd healo-mental-health-chatbot
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run tests:
   ```bash
   python simple_accuracy_test.py
   ```

## 🎯 Areas for Contribution

### High Priority
- **Response Time Optimization** - Currently 8.21s average
- **Mood Detection Improvement** - Currently 60% accuracy
- **Crisis Detection** - Enhanced suicide risk assessment
- **Mobile Responsiveness** - Better mobile experience

### Medium Priority
- **New Mental Health Categories** - Additional conditions
- **Multi-language Support** - Non-English languages
- **Voice Interface** - Speech-to-text capabilities
- **API Documentation** - Better API docs

### Low Priority
- **UI/UX Improvements** - Design enhancements
- **Documentation** - Better guides and tutorials
- **Testing** - More comprehensive test coverage
- **Performance** - General optimizations

## 📝 Code Style Guidelines

### Python
- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions
- Keep functions focused and small

### JavaScript
- Use ES6+ features
- Follow consistent naming conventions
- Add comments for complex logic
- Use meaningful variable names

### HTML/CSS
- Use semantic HTML
- Follow BEM methodology for CSS
- Ensure accessibility compliance
- Use responsive design principles

## 🧪 Testing

### Running Tests
```bash
# Test model accuracy
python simple_accuracy_test.py

# Test API endpoints
python -m pytest tests/

# Test specific functionality
python test_model.py
```

### Adding Tests
- Write tests for new features
- Ensure existing tests still pass
- Add edge case testing
- Include performance tests

## 📊 Training Data Guidelines

### Quality Standards
- **Empathetic**: Responses should show understanding and care
- **Professional**: Appropriate for mental health support
- **Accurate**: Factually correct information
- **Helpful**: Provide actionable advice or support

### Format Requirements
```csv
User Input,Friend Mode Response,Professional Mode Response
"I feel anxious about my job interview","That's totally normal! Job interviews can be nerve-wracking. What specifically is making you most nervous?","Job interview anxiety is very common. It's important to prepare and practice. What strategies have you tried to manage this anxiety?"
```

### Content Guidelines
- Avoid medical advice or diagnosis
- Include crisis resources when appropriate
- Use inclusive language
- Be culturally sensitive
- Maintain confidentiality

## 🚀 Pull Request Process

### Before Submitting
1. Ensure all tests pass
2. Update documentation if needed
3. Follow code style guidelines
4. Test your changes thoroughly

### PR Description
- Clearly describe what was changed
- Explain why the change was made
- Reference any related issues
- Include screenshots for UI changes

### Review Process
- All PRs require review
- Address feedback promptly
- Be open to suggestions
- Maintain respectful communication

## 🏷️ Issue Labels

- `bug` - Something isn't working
- `enhancement` - New feature or request
- `documentation` - Improvements to documentation
- `good first issue` - Good for newcomers
- `help wanted` - Extra attention is needed
- `priority: high` - High priority issue
- `priority: medium` - Medium priority issue
- `priority: low` - Low priority issue

## 💬 Community Guidelines

### Be Respectful
- Use welcoming and inclusive language
- Be respectful of differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Mental Health Sensitivity
- Remember this is a mental health tool
- Be sensitive to mental health topics
- Avoid triggering language
- Prioritize user safety and well-being

## 📞 Getting Help

### Questions?
- Open a GitHub Discussion
- Check existing issues and PRs
- Review the documentation
- Ask in the community chat

### Contact
- **Maintainer**: [Your Name]
- **Email**: maintainer@healo-chatbot.com
- **GitHub**: [@yourusername](https://github.com/yourusername)

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation
- Community highlights

Thank you for contributing to Healo! Together, we can make mental health support more accessible and effective.
