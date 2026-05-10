
<img width="1002" height="910" alt="LUMINA" src="https://github.com/user-attachments/assets/c211c12d-b719-4976-a864-d18012fc1400" />

---


# Lumina

A RAG-based chatbot that lets you interact with your PDF documents using open-source LLMs. Upload your books or documents into the `books/` directory, and Lumina will index them into a FAISS vector store so you can ask questions and get context-aware answers — all running locally or in the cloud.
 
Built with LangChain, Mistral-7B, FAISS, and Flask. Deployable via Docker and AWS App Runner with a Jenkins CI/CD pipeline.
 
---
 
## Table of Contents
 
- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Jenkins Setup](#jenkins-setup)
- [GitHub Integration with Jenkins](#github-integration-with-jenkins)
- [Build, Scan, and Push to AWS ECR](#build-scan-and-push-to-aws-ecr)
- [Deploy to AWS App Runner](#deploy-to-aws-app-runner)
- [License](#license)
---
 
## Overview
 
Lumina uses a Retrieval-Augmented Generation (RAG) pipeline to answer questions grounded in your own documents. Place your PDF files in the `books/` directory before running the app. Lumina will chunk and embed them into a FAISS vector store, then use Mistral-7B (via HuggingFace) to generate answers at query time.
 
The app exposes a Flask web interface running on port `5000`.
 
---
 
## Tech Stack
 
| Component | Technology |
|---|---|
| LLM | Mistral-7B-Instruct-v0.3 (HuggingFace) |
| Embeddings | LangChain HuggingFace Embeddings |
| Vector Store | FAISS |
| PDF Parsing | PyPDF |
| Backend | Flask |
| Containerization | Docker |
| CI/CD | Jenkins (Docker-in-Docker) |
| Registry | AWS ECR |
| Deployment | AWS App Runner |
 
---
 
## Getting Started
 
### Prerequisites
 
- Python 3.10+
- Docker (for containerized deployment)
- A HuggingFace account and API token
### Clone the Repository
 
```bash
git clone https://github.com/AryaAhmadii/lumina.git
cd lumina
```
 
### Create a Virtual Environment
 
```bash
# Linux / macOS
python -m venv venv
source venv/bin/activate
 
# Windows
python -m venv venv
venv\Scripts\activate
```
 
### Install Dependencies
 
```bash
pip install -e .
```
 
### Add Your Documents
 
Place your PDF files inside the `books/` directory before starting the app. Lumina reads from this directory at startup to build the vector store.
 
### Run the App
 
```bash
python app/app.py
```
 
The app will be available at `http://localhost:5000`.
 
---
 
## Configuration
 
Copy `.env.example` to `.env` and fill in the required values:
 
```bash
cp .env.example .env
```
 
| Variable | Description |
|---|---|
| `HUGGINGFACE_TOKEN` | Your HuggingFace API token |
| `DATA_PATH` | Path to the PDF directory (default: `books/`) |
| `CHUNK_SIZE` | Text chunk size for splitting documents (default: `500`) |
| `CHUNK_OVERLAP` | Overlap between chunks (default: `50`) |
| `DB_FAISS_PATH` | Path where the FAISS vector store is saved |
| `HF_REPO_ID` | HuggingFace model ID (default: `mistralai/Mistral-7B-Instruct-v0.3`) |
 
---
 
## Jenkins Setup
 
This section covers setting up a Jenkins CI/CD server using Docker-in-Docker.
 
### Step 1 — Build the Jenkins Image
 
Navigate to the `jenkins/` directory and build the custom image:
 
```bash
cd jenkins
docker build -t jenkins-dind .
```
 
### Step 2 — Run the Jenkins Container
 
```bash
docker run -d \
  --name jenkins-dind \
  --privileged \
  -p 8080:8080 \
  -p 50000:50000 \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v jenkins_home:/var/jenkins_home \
  jenkins-dind
```
 
On Windows, replace the backslashes `\` with `^`.
 
### Step 3 — Retrieve the Initial Admin Password
 
```bash
docker logs jenkins-dind
```
 
If the password is not visible in the logs:
 
```bash
docker exec jenkins-dind cat /var/jenkins_home/secrets/initialAdminPassword
```
 
### Step 4 — Access the Jenkins Dashboard
 
Open your browser and go to `http://localhost:8080`. Complete the initial setup wizard.
 
### Step 5 — Install Python Inside the Jenkins Container
 
```bash
docker exec -u root -it jenkins-dind bash
apt update -y
apt install -y python3 python3-pip
ln -s /usr/bin/python3 /usr/bin/python
exit
 
docker restart jenkins-dind
```
 
---
 
## GitHub Integration with Jenkins
 
### Step 1 — Generate a GitHub Personal Access Token
 
Go to **GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)** and generate a new token with the following scopes:
 
- `repo` — full control of repositories
- `admin:repo_hook` — webhook management
Save the token securely; you will not be able to view it again.
 
### Step 2 — Add the Token to Jenkins Credentials
 
Go to **Jenkins Dashboard → Manage Jenkins → Credentials → (Global) → Add Credentials** and fill in:
 
- **Kind:** Username with password
- **Username:** Your GitHub username
- **Password:** The token you just generated
- **ID:** `github-token`
### Step 3 — Create a Pipeline Job
 
Go to **Jenkins Dashboard → New Item**, select **Pipeline**, give it a name, and click **OK**.
 
### Step 4 — Generate the Checkout Script
 
Inside the pipeline project, go to **Pipeline Syntax** in the sidebar. Select `checkout: General SCM`, fill in your repository URL and credentials, then click **Generate Pipeline Script**. Copy the output — you will need it in your `Jenkinsfile`.
 
### Step 5 — Trigger the Pipeline
 
Go to your pipeline job and click **Build Now**. A successful run means Jenkins has cloned your repository into its workspace.
 
---
 
## Build, Scan, and Push to AWS ECR
 
### Step 1 — Install Trivy in the Jenkins Container
 
```bash
docker exec -u root -it jenkins-dind bash
curl -LO https://github.com/aquasecurity/trivy/releases/download/v0.62.1/trivy_0.62.1_Linux-64bit.deb
dpkg -i trivy_0.62.1_Linux-64bit.deb
exit
 
docker restart jenkins-dind
```
 
### Step 2 — Install AWS Plugins in Jenkins
 
Go to **Manage Jenkins → Plugins** and install:
 
- AWS SDK
- AWS Credentials
Restart the container after installation.
 
### Step 3 — Create an IAM User in AWS
 
Go to **AWS Console → IAM → Users → Add User**, enable programmatic access, and attach the `AmazonEC2ContainerRegistryFullAccess` policy. Generate and save the access key and secret.
 
### Step 4 — Add AWS Credentials to Jenkins
 
Go to **Manage Jenkins → Credentials → (Global) → Add Credentials**, select **AWS Credentials**, and enter your Access Key ID and Secret Access Key. Set the ID to `aws-ecr-creds`.
 
### Step 5 — Install the AWS CLI Inside Jenkins
 
```bash
docker exec -u root -it jenkins-dind bash
apt update && apt install -y unzip curl
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip && ./aws/install
exit
```
 
### Step 6 — Create an ECR Repository
 
Go to **AWS Console → ECR → Create Repository**. Note the repository URI — it will be used in the Jenkinsfile.
 
### Step 7 — Fix Docker Socket Permissions (if needed)
 
If you run into Docker permission errors during the pipeline:
 
```bash
docker exec -u root -it jenkins-dind bash
chown root:docker /var/run/docker.sock
chmod 660 /var/run/docker.sock
usermod -aG docker jenkins
exit
 
docker restart jenkins-dind
```
 
> By default, Trivy is configured with `--exit-code 0`, meaning the pipeline will not fail on found vulnerabilities. Change it to `--exit-code 1` if you want the pipeline to halt on any detected issue.
 
---
 
## Deploy to AWS App Runner
 
### IAM Permissions
 
Attach the `AWSAppRunnerFullAccess` policy to the IAM user used by Jenkins.
 
### Create the App Runner Service
 
1. Go to **AWS Console → App Runner → Create service**
2. Set the source to **Container registry (ECR)** and select your image
3. Configure CPU, memory, and environment variables (mirror your `.env` values)
4. Optionally enable auto-deploy on new ECR pushes
5. Deploy the service
### Run the Full Pipeline
 
Go to your Jenkins pipeline and click **Build Now**. The pipeline will run through the following stages:
 
1. Checkout from GitHub
2. Build Docker image
3. Scan image with Trivy
4. Push image to AWS ECR
5. Deploy to AWS App Runner
A successful run means Lumina is live and accessible via the App Runner URL.
 
---
 
## License
 
This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
