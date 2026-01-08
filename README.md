# 2026 NBA Draft Prompt Pipeline (Amazon Bedrock CI/CD)

This project demonstrates a **GitHub-based CI/CD pipeline** that generates AI-powered content using **Amazon Bedrock (Claude 3 Sonnet)** and deploys the output to **Amazon S3 static website hosting** using environment-based workflows.

The pipeline supports **beta (pull request)** and **production (merge)** deployments, ensuring safe preview and controlled promotion of AI-generated content.

---

## 🏗️ Architecture Overview

**Flow:**
1. Prompt variables are defined in a JSON config (`prompts/`)
2. Prompt templates are stored separately (`prompt_templates/`)
3. A Python script renders the prompt and invokes Amazon Bedrock
4. Generated output is saved as HTML
5. CI/CD uploads content to S3 under environment-specific prefixes

**Environments:**
- **beta/** → Pull Requests
- **prod/** → Main branch merges

---

## 📁 Project Structure


---

## 🤖 Model Configuration

- **Provider:** Amazon Bedrock
- **Model:** Claude 3 Sonnet  
- **Model ID:**  
- **Invocation Type:** Real-time (on-demand only)
- **Provisioned throughput:** ❌ Not used (per project constraints)

---

## 🔐 GitHub Secrets Required

Set the following **repository secrets**:

| Secret Name | Description |
|------------|-------------|
| `AWS_ACCESS_KEY_ID` | IAM access key |
| `AWS_SECRET_ACCESS_KEY` | IAM secret |
| `AWS_REGION` | AWS region (e.g. `us-east-1`) |
| `S3_BUCKET_BETA` | S3 bucket for beta deployments |
| `S3_BUCKET_PROD` | S3 bucket for production deployments |

---

## 🚀 CI/CD Workflows

### Pull Request Workflow (`on_pull_requests.yml`)
- Trigger: PRs targeting `main`
- Output location:

### Merge Workflow (`on_merge.yml`)
- Trigger: Pushes to `main`
- Output location:

---

## 🧪 Local Execution (Optional)

```bash
pip install -r requirements.txt
python3 process_prompt.py prompts/welcome_prompt.json

---

## ✅ Final steps (2 commands)

After pasting the README at the repo root:

```bash
git add README.md
git commit -m "Add project README"
git push
