# Security Policy

## Supported Versions

We actively support and provide security updates for all language files in this repository. If you discover a security vulnerability, please report it using the process outlined below.

## Reporting a Vulnerability

### What to Report

While this is a translation repository and security vulnerabilities are less common than in code repositories, please report:

- **Malicious content** in translation files (e.g., XSS attempts, code injection)
- **Sensitive information** accidentally committed (API keys, tokens, personal data)
- **Supply chain risks** (malicious dependencies if any are added in the future)
- **Repository access issues** (unauthorized access, compromised accounts)

### What NOT to Report

The following are not considered security vulnerabilities for this repository:

- Translation errors or typos
- Missing translations
- JSON syntax errors (these are caught during validation)
- Style or formatting issues

For these issues, please open a regular [issue](../../issues) or submit a [pull request](../../pulls).

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them by one of the following methods:

1. **Email**: Send an email to [INSERT SECURITY EMAIL] with:
   - A clear description of the vulnerability
   - Steps to reproduce (if applicable)
   - Potential impact
   - Your suggested fix (if any)

2. **Private Security Advisory**: If you have access, create a private security advisory on GitHub:
   - Go to the "Security" tab
   - Click "Advisories"
   - Click "New draft security advisory"

### What to Include

When reporting a security vulnerability, please include:

- **Description**: Clear description of the vulnerability
- **Impact**: Potential impact if exploited
- **Steps to Reproduce**: Detailed steps to reproduce the issue
- **Affected Files**: Which translation files or repository components are affected
- **Suggested Fix**: If you have a solution, please include it
- **Timeline**: When you discovered the vulnerability

### Response Timeline

We aim to:

- **Acknowledge** your report within 48 hours
- **Provide an initial assessment** within 5 business days
- **Resolve critical issues** as quickly as possible
- **Keep you informed** of our progress

### Disclosure Policy

We follow a **coordinated disclosure** process:

1. We will acknowledge receipt of your report
2. We will investigate and verify the vulnerability
3. We will develop a fix (if needed)
4. We will release the fix and credit you (unless you prefer to remain anonymous)
5. We will publish a security advisory if the issue is significant

**Please do not disclose the vulnerability publicly** until we have had a chance to address it.

### Recognition

We appreciate security researchers who help keep our repository safe. With your permission, we will:

- Credit you in any security advisories
- Add you to our security acknowledgments (if you wish)
- Thank you publicly for your responsible disclosure

### Safe Harbor

We support safe harbor for security researchers. If you:

- Act in good faith
- Do not access or modify data that does not belong to you
- Do not violate any laws or breach any agreements
- Give us reasonable time to address the issue before public disclosure

Then we will not pursue legal action against you.

## Security Best Practices for Contributors

When contributing translations:

- **Never commit sensitive information** (API keys, tokens, passwords)
- **Validate JSON syntax** before submitting
- **Review your changes** for any unexpected content
- **Use trusted tools** for editing JSON files
- **Report suspicious content** if you encounter it

## Questions?

If you have questions about this security policy or need clarification on whether something is a security issue, please contact us here or on discord at hugsndnugs.

Thank you for helping keep Event Sentinel Languages secure!
