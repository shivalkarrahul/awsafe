# **awsafe**

**awsafe** is a lightweight, Python-based AWS security scanning CLI tool built primarily as a **learning project** to understand:

* Python development
* AWS services & security
* How real-world security tools are designed

This tool helps identify common AWS misconfigurations in **EC2** and **S3**, and it is actively evolving.

---

## 🎯 Project Goals

This project was created to:

* Practice **Python programming**
* Learn **AWS security best practices**
* Understand how **rule engines** work

This is a learning-first project and not intended to replace enterprise security tools.

---

## ✨ Current Features

### ✅ EC2 Security Checks

* Detects public IP exposure
* Validates allowed instance types
* Checks for missing IAM roles

### ✅ S3 Security Checks

* Detects public access risks using block public access
* Detects missing server-side encryption

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/shivalkarrahul/awsafe.git
cd awsafe
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install in editable mode:

```bash
pip install -e .
```

---

## 🔐 AWS Credentials Setup

You must configure AWS credentials before running the tool.

### Using Environment Variables

```bash
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

⚠️ Never commit AWS credentials to Git repositories.

---

## 🚀 How to Use

Run EC2 scan:

```bash
awsafe scan ec2-scan
```

Run S3 scan:

```bash
awsafe scan s3-scan
```

---

## ⚙️ Rule Configuration

Rules can be enabled/disabled via:

```
config/rules_config.json
```

Example:

```json
{
  "EC2_PUBLIC_IP": true,
  "EC2_INSTANCE_TYPE": true,
  "EC2_IAM_ROLE": true,
  "S3_PUBLIC_ACCESS": true,
  "S3_ENCRYPTION": true
}
```

---

## 📦 Project Structure

```
awsafe/
├── cli.py
├── resources/
│   ├── ec2_resource.py
│   └── s3_resource.py
├── rules/
│   ├── ec2_rules.py
│   └── s3_rules.py
├── config/
│   └── rules_config.json
```

---

## 🧪 Learning Focus

This project is a personal learning journey to:

* Write clean, modular Python code
* Build real-world CLI tools
* Work with AWS APIs using `boto3`
* Understand cloud security fundamentals

The code intentionally prioritizes clarity over complexity.

---

## 🛣️ Future Roadmap

Planned improvements for learning and experimentation:

* ✅ Multi-region scanning
* ✅ JSON / CSV report export
* ✅ Logging support
* ✅ Advanced IAM policy checks
* ✅ CIS benchmark inspired rules
* ✅ Plugin system for custom rules
* ✅ CI/CD pipeline integration

---

## 🤝 Contributions

This project welcomes:

* Suggestions
* Issues
* Ideas
* Learning discussions

---

## 👨‍💻 Author

**Rahul Shivalkar**
Built with ❤️ to learn Python, AWS, and security engineering.
