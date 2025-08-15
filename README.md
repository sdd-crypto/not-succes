# AI Pentester Agent v1.0.0

A fully autonomous, AI-powered penetration testing agent designed for controlled lab environments with explicit permission for all testing activities, including destructive actions.

## 🎯 Features

### Dual Operation Modes
1. **AI Chat Mode**: Interactive security expert assistant for strategy discussions, vulnerability analysis, and educational purposes
2. **AI Pentest Mode**: Fully autonomous penetration testing with continuous planning and execution

### Autonomous Testing Capabilities
- **Reconnaissance**: Passive and active information gathering
- **Port Scanning**: Comprehensive service discovery using nmap
- **Web Application Testing**: SQL injection, XSS, directory traversal, and more
- **Network Services**: Brute force attacks, service enumeration
- **Post-Exploitation**: Reverse shells, privilege escalation, lateral movement
- **Continuous Planning**: AI-driven PLAN → EXECUTE → OBSERVE → REPLAN loop

### AI-Powered Intelligence
- Integrated with Perplexity AI (sonar-pro model) for advanced decision making
- Dynamic attack planning based on discovered information
- Intelligent vulnerability analysis and exploitation suggestions
- Automated report generation with remediation guidance

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+**
2. **Required Pentesting Tools**:
   ```bash
   # Ubuntu/Debian
   sudo apt update
   sudo apt install nmap sqlmap ffuf sshpass netcat-openbsd
   
   # Additional tools (optional but recommended)
   sudo apt install dirb gobuster nikto hydra john metasploit-framework
   ```

3. **Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Installation

1. **Clone or download the files**:
   ```bash
   # Ensure you have these files:
   # - ai_pentester.py (main application)
   # - requirements.txt (Python dependencies)
   # - scope.json (authorized targets)
   # - README.md (this file)
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure scope** (edit `scope.json`):
   ```json
   {
     "authorized_targets": [
       "192.168.1.0/24",
       "10.0.0.0/16",
       "testlab.local"
     ],
     "lab_mode": true,
     "destructive_allowed": true
   }
   ```

4. **Run the application**:
   ```bash
   python ai_pentester.py
   ```

## 📋 Usage

### Main Menu Options

```
🎯 AI Pentester Agent - Main Menu
1. 💬 AI Chat Mode (Security Q&A, Strategy Discussion)
2. 🔍 AI Pentest Mode (Autonomous Penetration Testing)
3. 📊 View Previous Reports
4. ⚙️  Configuration
5. 🚪 Exit
```

### AI Chat Mode

Interactive security expert assistant:
- Ask questions about vulnerabilities, exploits, and security concepts
- Get pentesting strategy recommendations
- Discuss specific attack vectors and defense mechanisms
- Educational cybersecurity conversations

**Example interactions**:
```
👤 You: How do I test for SQL injection in a login form?
🤖 AI Expert: [Detailed explanation of SQL injection testing techniques...]

👤 You: What's the best approach for testing a web application with rate limiting?
🤖 AI Expert: [Comprehensive rate limiting bypass strategies...]
```

### AI Pentest Mode

Fully autonomous penetration testing:

1. **Target Input**: Provide target domain or IP address
2. **Scope Validation**: Automatic verification against authorized scope
3. **Autonomous Testing**: AI plans and executes comprehensive tests
4. **Continuous Replanning**: Adapts strategy based on discovered information
5. **Report Generation**: Detailed findings with evidence and remediation

**Example workflow**:
```bash
🎯 Enter target (domain/IP): testlab.local
✅ Target 'testlab.local' is in authorized scope.
🚀 Starting autonomous penetration test...

🔄 Iteration 1/10
📋 PLANNING PHASE
🧠 AI Plan: Starting with reconnaissance and port scanning...

⚡ EXECUTION PHASE
🔍 Phase 1: Port Scanning
✅ Found 5 open ports
🌐 Phase 2: Service Enumeration
🔐 Phase 3: Credential Testing
💥 Phase 4: Exploitation

🎉 Significant vulnerabilities found!
📊 Reports generated: pentest_report_20240101_120000.md
```

## 🔧 Configuration

### Scope Management

Edit `scope.json` to define authorized targets:

```json
{
  "authorized_targets": [
    "192.168.1.0/24",      // CIDR notation
    "10.0.0.0/16",          // Private networks
    "*.lab.internal",       // Wildcard domains
    "testapp.local"         // Specific hosts
  ],
  "excluded_targets": [
    "192.168.1.1"          // Exclude specific IPs
  ],
  "lab_mode": true,         // Must be true for operation
  "destructive_allowed": true
}
```

### Application Settings

Access via Configuration menu (option 4):
- **Lab Mode**: Enable/disable lab-only operations
- **Destructive Actions**: Allow/disallow destructive testing
- **Max Depth**: Maximum testing iterations (default: 10)
- **Timeout**: Tool execution timeout (default: 30 seconds)
- **Threads**: Concurrent testing threads (default: 20)

## 📊 Reports

### Automatic Report Generation

Each pentest generates comprehensive reports:

1. **Markdown Report** (`pentest_report_TIMESTAMP.md`):
   - Executive summary
   - Target analysis
   - Detailed findings with evidence
   - Proof-of-concept code
   - Remediation recommendations

2. **JSON Report** (`pentest_report_TIMESTAMP.json`):
   - Machine-readable format
   - Complete test data
   - Severity breakdown
   - Timeline information

### Sample Report Structure

```
# Penetration Testing Report

**Generated:** 2024-01-01 12:00:00
**Scope:** 1 targets analyzed
**Findings:** 3 security issues identified

## Executive Summary
- **CRITICAL**: Weak SSH Credentials
- **HIGH**: SQL Injection on port 80
- **MEDIUM**: Cross-Site Scripting

## Detailed Findings

### Finding 1: Weak SSH Credentials
**Severity:** critical
**Description:** Default credentials found on SSH service
**Evidence:** Username: admin, Password: admin
**PoC:** ssh admin@target.local
**Remediation:** Enforce strong password policy
```

## 🛡️ Security & Safety

### Lab Environment Only

⚠️ **CRITICAL SAFETY INFORMATION**:
- This tool is designed EXCLUSIVELY for controlled lab environments
- All targets must be explicitly authorized in `scope.json`
- Lab mode must be enabled for operation
- Destructive actions are performed only within authorized scope

### Built-in Safety Mechanisms

1. **Scope Validation**: Automatic target verification against authorized list
2. **Lab Mode Enforcement**: Operations blocked unless lab mode is active
3. **Destructive Action Controls**: Configurable destructive testing permissions
4. **Audit Logging**: Complete execution logs for all activities

### Legal Compliance

- Only use on systems you own or have explicit written permission to test
- Ensure compliance with local laws and regulations
- Maintain proper documentation of authorization
- Follow responsible disclosure practices for any vulnerabilities found

## 🔧 Advanced Features

### Custom Exploit Modules

The system includes modular exploit capabilities:

- **Web Exploits**: SQL injection, XSS, CSRF, SSRF, RCE
- **Network Exploits**: Port scanning, service fingerprinting, credential attacks
- **Post-Exploitation**: Reverse shells, privilege escalation, persistence
- **Custom Payloads**: AI-generated exploit code based on discovered vulnerabilities

### AI Integration

- **Perplexity API**: Advanced language model for intelligent decision making
- **Dynamic Planning**: Real-time strategy adaptation based on results
- **Contextual Analysis**: Deep understanding of security implications
- **Automated Documentation**: Intelligent report generation with explanations

### Tool Integration

Seamless integration with industry-standard tools:
- **nmap**: Port scanning and service detection
- **sqlmap**: SQL injection testing and exploitation
- **ffuf**: Web fuzzing and directory discovery
- **sshpass**: SSH credential testing
- **netcat**: Network connections and reverse shells

## 🐛 Troubleshooting

### Common Issues

1. **"Target not in scope" error**:
   - Verify target is listed in `scope.json`
   - Check CIDR notation and wildcard patterns
   - Ensure `lab_mode` is set to `true`

2. **Missing tools warning**:
   - Install required pentesting tools (nmap, sqlmap, ffuf)
   - Verify tools are in system PATH
   - Check tool permissions and execution rights

3. **API connection errors**:
   - Verify internet connectivity
   - Check Perplexity API key validity
   - Review firewall and proxy settings

4. **Permission denied errors**:
   - Ensure script has execution permissions
   - Check file system permissions for output directory
   - Verify user has rights to execute pentesting tools

### Debug Mode

Enable verbose logging by modifying the configuration:
```python
CONFIG = {
    "debug": True,
    "verbose_logging": True,
    # ... other settings
}
```

## 📈 Performance Optimization

### Resource Management

- **Concurrent Operations**: Adjustable thread count for parallel testing
- **Timeout Controls**: Configurable timeouts prevent hanging operations
- **Memory Management**: Efficient handling of large result sets
- **Rate Limiting**: Built-in delays to avoid overwhelming targets

### Scaling Considerations

- **Target Limits**: Designed for individual host testing
- **Network Impact**: Respectful scanning to minimize network load
- **Resource Usage**: Optimized for standard lab environments
- **Result Storage**: Efficient report generation and storage

## 🤝 Contributing

### Development Guidelines

1. **Security First**: All code must prioritize security and safety
2. **Lab Only**: Features must respect lab-only operation model
3. **Documentation**: Comprehensive documentation for all features
4. **Testing**: Thorough testing in isolated environments

### Code Structure

```
ai_pentester.py          # Main application (single file architecture)
├── AIEngine             # Perplexity API integration
├── ExploitModules       # Modular exploit capabilities
├── ReportGenerator      # Report generation engine
├── ScopeValidator       # Target authorization validation
└── AIPentester          # Main application class
```

## 📄 License

This software is provided for educational and authorized testing purposes only. Users are responsible for ensuring compliance with all applicable laws and regulations.

## 🆘 Support

For questions, issues, or contributions:
1. Review this documentation thoroughly
2. Check troubleshooting section
3. Verify lab environment setup
4. Ensure all dependencies are installed

---

**⚠️ Remember: With great power comes great responsibility. Use this tool ethically and only in authorized environments.**
