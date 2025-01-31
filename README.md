# Speech to Text for micro-service implementation

# Folder structure

audio-summarization-service/
│
├── backend/                     # 後端目錄 (微服務部分)
│   ├── stt_service/             # 語音轉文字服務 (Whisper)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── stt_service.py
│   │   └── ...
│   │
│   ├── summarization_service/  # 摘要服務
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── summarization_service.py
│   │   └── ...
│   │
│   ├── api_gateway/            # API Gateway
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── api_gateway.py
│   │   └── ...
│   │
│   ├── docker-compose.yml      # Docker Compose 配置（開發環境使用）
│   ├── .gitignore
│   └── k8s/                    # Kubernetes 配置
│       ├── stt-service-deployment.yaml
│       ├── summarization-service-deployment.yaml
│       ├── api-gateway-deployment.yaml
│       ├── k8s-configmap.yaml   # 配置檔案（如環境變數）
│       ├── k8s-secrets.yaml     # 機密資訊
│       └── k8s-service.yaml     # Kubernetes 服務配置
│
├── frontend/                    # 前端目錄
│   ├── public/                  # 公用文件 (HTML, images 等)
│   ├── src/                     # 前端源代碼
│   │   ├── components/          # React 組件
│   │   ├── App.js               # 主要應用入口文件 (React)
│   │   ├── index.js             # 前端入口文件
│   │   ├── services/            # 與後端 API 通信的服務
│   │   └── ...
│   ├── package.json             # npm/yarn 配置文件
│   ├── Dockerfile               # 前端 Docker 配置
│   └── .gitignore               # 前端 Git 忽略規則
│
├── infrastructure/              # 基礎設施配置 (Terraform)
│   ├── aws/                     # AWS 基礎設施配置
│   │   ├── main.tf              # Terraform 配置
│   │   ├── variables.tf         # 輸入變數
│   │   ├── outputs.tf           # 輸出值
│   │   └── terraform.tfvars     # Terraform 配置變數
│   ├── docker/                  # Docker 資源配置
│   │   └── docker.tf            # Docker 基礎設施
│   └── k8s/                     # Kubernetes 配置
│       ├── k8s-cluster.tf        # Kubernetes 集群設置
│       ├── k8s-deployment.tf     # 微服務部署配置
│       └── k8s-services.tf       # 服務配置
│
├── .gitignore                   # 整個專案的 Git 忽略規則
├── README.md                    # 專案描述文件
└── LICENSE                      # 開源授權協議


---

### **1. Development environment **

#### **1.1. Local **

首先，您需要設置本地開發環境來運行微服務。

- **Step 1: install dependency **

進入 `backend` 目錄，並安裝每個微服務所需的 Python 依賴（例如 `stt_service`、`summarization_service` 和 `api_gateway`）。

```bash
# 進入 stt_service 目錄
cd backend/stt_service
# 安裝依賴
pip install -r requirements.txt

# 進入 summarization_service 目錄
cd ../summarization_service
# 安裝依賴
pip install -r requirements.txt

# 進入 api_gateway 目錄
cd ../api_gateway
# 安裝依賴
pip install -r requirements.txt
```

- **Step 2: launch backend (use Docker Compose)**

確保已安裝 Docker 和 Docker Compose，然後在專案根目錄中運行以下命令來啟動所有後端服務：

```bash
docker-compose up --build
```

這會根據 `docker-compose.yml` 文件啟動以下服務：

- `api-gateway`：處理外部 API 請求。
- `stt-service`：語音轉文字服務。
- `summarization-service`：文本摘要服務。
- `frontend`：前端應用。

這會將後端微服務啟動並映射到本地端口，通常 `api-gateway` 會暴露在 `localhost:8000` 上，`stt-service` 在 `localhost:8001`，`summarization-service` 在 `localhost:8002`。

#### **1.2. 啟動前端應用**

- **步驟 3: 啟動前端應用**

首先，確保您已經安裝了前端的依賴。

```bash
# 進入 frontend 目錄
cd frontend
# 安裝依賴
npm install
# 啟動前端應用
npm start
```

此命令會在本地啟動 React 應用，通常會映射到 `localhost:3000`，並且前端應用會與後端 API Gateway 進行交互。

---

### **2. 部署到生產環境 (AWS + Kubernetes)**

#### **2.1. 設置 Terraform 環境 (AWS 配置)**

- **步驟 1: 初始化 Terraform**

首先，在 `infrastructure/aws` 目錄中初始化 Terraform。

```bash
cd infrastructure/aws
terraform init
```

這將下載所需的 Terraform 提供者插件。

- **步驟 2: 設定環境變數**

在執行 Terraform 命令之前，請確保 AWS 的認證資料已經正確配置。您可以通過以下命令設置 AWS 認證：

```bash
export AWS_ACCESS_KEY_ID=<your-access-key-id>
export AWS_SECRET_ACCESS_KEY=<your-secret-access-key>
export AWS_DEFAULT_REGION=us-west-2
```

- **步驟 3: 應用 Terraform 配置**

運行以下命令來建立 AWS 資源（例如 VPC、EC2、S3 等）。

```bash
terraform apply
```

您將被提示確認應用更改，鍵入 `yes` 並按下 Enter。

#### **2.2. 構建並部署 Docker 映像**

- **步驟 4: 構建 Docker 映像**

您需要根據每個微服務的 `Dockerfile` 構建映像。

例如，對於 `stt-service`：

```bash
cd backend/stt_service
docker build -t stt-service:latest .
```

對於其他微服務，如 `summarization-service` 和 `api-gateway`，您也需要重複構建映像。

- **步驟 5: 推送 Docker 映像到 Docker Hub 或其他容器註冊庫**

假設您使用 Docker Hub，首先登錄到 Docker Hub：

```bash
docker login
```

然後將映像推送到 Docker Hub：

```bash
docker tag stt-service:latest <your-dockerhub-username>/stt-service:latest
docker push <your-dockerhub-username>/stt-service:latest
```

對其他微服務也進行相同的操作。

#### **2.3. 配置 Kubernetes**

- **步驟 6: 部署到 Kubernetes (AWS EKS 或其他 Kubernetes 集群)**

如果您使用 AWS EKS，首先配置您的 `kubectl` 並設置 AWS EKS 集群。

```bash
aws eks --region us-west-2 update-kubeconfig --name <eks-cluster-name>
```

然後，您可以使用 `kubectl` 部署微服務。

例如，部署 `stt-service`：

```bash
kubectl apply -f backend/k8s/stt-service-deployment.yaml
```

對 `summarization-service` 和 `api-gateway` 執行相同操作。

- **步驟 7: 部署 Kubernetes 服務**

部署 Kubernetes 服務來暴露服務給外部訪問。

```bash
kubectl apply -f backend/k8s/k8s-service.yaml
```

這樣，您的微服務就會通過負載均衡器對外提供服務。

#### **2.4. 驗證部署**

您可以使用以下命令檢查服務是否正常運行：

```bash
kubectl get pods
kubectl get svc
```

確保所有微服務的 pods 都在運行，並且可以通過負載均衡器訪問。

---

### **3. 結論**

這些命令涵蓋了從本地開發到生產環境部署的整個流程。總結來說：

1. **開發環境**：
   - 安裝 Python 依賴。
   - 使用 Docker Compose 啟動所有服務。
   - 使用 `npm start` 啟動前端應用。

2. **生產環境部署**：
   - 使用 Terraform 初始化並部署 AWS 基礎設施。
   - 構建並推送 Docker 映像到註冊庫。
   - 使用 `kubectl` 部署到 Kubernetes 集群。

按照這些步驟，您可以順利地開發並將應用部署到 AWS。





=========
你的專案目錄結構是正確的，只是我之前回應時將部分 Kubernetes 配置和基礎設施（Infrastructure）拆開來說明，但 **核心概念和內容是一樣的**。讓我們統一整理，並提供 **正確的開發 & 部署步驟**。

---

## **📌 最終專案目錄結構**
```
audio-summarization-service/
│
├── backend/                     # 後端目錄 (微服務)
│   ├── stt_service/             # 語音轉文字服務 (Whisper)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── stt_service.py
│   │   ├── config.yaml
│   │   └── ...
│   │
│   ├── summarization_service/   # 文字摘要服務
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── summarization_service.py
│   │   ├── config.yaml
│   │   └── ...
│   │
│   ├── api_gateway/             # API Gateway (FastAPI)
│   │   ├── Dockerfile
│   │   ├── requirements.txt
│   │   ├── api_gateway.py
│   │   ├── config.yaml
│   │   └── ...
│   │
│   ├── docker-compose.yml       # Docker Compose 配置（開發環境用）
│   ├── .gitignore
│   └── k8s/                     # Kubernetes 配置
│       ├── deployments/
│       │   ├── stt-service-deployment.yaml
│       │   ├── summarization-service-deployment.yaml
│       │   ├── api-gateway-deployment.yaml
│       │   ├── frontend-deployment.yaml
│       ├── services/
│       │   ├── stt-service.yaml
│       │   ├── summarization-service.yaml
│       │   ├── api-gateway-service.yaml
│       │   ├── frontend-service.yaml
│       ├── k8s-configmap.yaml   # 配置檔案（如環境變數）
│       ├── k8s-secrets.yaml     # 機密資訊
│       ├── kustomization.yaml   # Kustomize 配置
│       └── namespace.yaml       # Kubernetes Namespace
│
├── frontend/                    # 前端目錄
│   ├── public/                  # 公用文件 (HTML, images)
│   ├── src/                     # 前端源代碼
│   │   ├── components/          # React/Vue/Svelte 組件
│   │   ├── App.js               # 主要應用入口 (React)
│   │   ├── index.js             # 前端入口文件
│   │   ├── services/            # 與後端 API 通信
│   │   └── ...
│   ├── package.json             # npm/yarn 配置文件
│   ├── Dockerfile               # 前端 Docker 配置
│   └── .gitignore               # 前端 Git 忽略規則
│
├── infrastructure/              # 基礎設施配置 (Terraform)
│   ├── aws/                     # AWS EKS (Production)
│   │   ├── main.tf              # Terraform 主要配置
│   │   ├── variables.tf         # 輸入變數
│   │   ├── outputs.tf           # 輸出值
│   │   └── terraform.tfvars     # AWS 變數配置
│   ├── docker/                  # Docker 本地開發環境配置
│   │   └── docker.tf            # Docker 相關 Terraform 配置
│   ├── k8s/                     # Kubernetes 叢集與服務
│   │   ├── k8s-cluster.tf        # EKS Kubernetes 叢集
│   │   ├── k8s-deployment.tf     # 微服務部署
│   │   └── k8s-services.tf       # 服務配置
│   ├── kustomization/            # Kustomize for Dev/Prod
│   │   ├── base/
│   │   │   ├── kustomization.yaml
│   │   ├── overlays/
│   │   │   ├── dev/
│   │   │   │   ├── kustomization.yaml
│   │   │   ├── prod/
│   │   │   │   ├── kustomization.yaml
│   ├── terraform.tfstate        # Terraform 狀態檔案
│
├── .gitignore                   # 整個專案的 Git 忽略規則
├── README.md                    # 專案描述文件
└── LICENSE                      # 開源授權協議
```

---

## **📌 開發 & 部署步驟**
### **本地開發 (Development)**
1. **安裝 Docker、Docker Compose**
   ```bash
   brew install docker
   brew install docker-compose
   ```

2. **使用 `docker-compose` 啟動所有服務**
   ```bash
   cd backend/
   docker-compose up --build
   ```

3. **檢查 API Gateway 是否正常運行**
   ```bash
   curl http://localhost:8000/docs
   ```

4. **啟動前端應用**
   ```bash
   cd frontend/
   npm install
   npm run dev
   ```

---

### **本地 Kubernetes（開發環境）**
📌 **方式 1：使用 kind**
1. **建立本地 Kubernetes 叢集**
   ```bash
   kind create cluster --config infrastructure/k8s/kind-cluster.yaml
   ```

2. **部署微服務**
   ```bash
   kubectl apply -f backend/k8s/
   ```

3. **確認 Kubernetes 服務**
   ```bash
   kubectl get pods -n dev
   kubectl get services -n dev
   ```

---

📌 **方式 2：使用 Minikube**
1. **啟動 Minikube**
   ```bash
   minikube start --cpus=4 --memory=8192
   ```

2. **部署微服務**
   ```bash
   kubectl apply -f backend/k8s/
   ```

---

### **Production 部署（AWS EKS）**
1. **初始化 Terraform**
   ```bash
   cd infrastructure/aws/
   terraform init
   ```

2. **部署 AWS EKS**
   ```bash
   terraform apply -auto-approve
   ```

3. **取得 Kubernetes 叢集資訊**
   ```bash
   aws eks --region <your-region> update-kubeconfig --name audio-summarization-cluster
   ```

4. **部署微服務**
   ```bash
   kubectl apply -f backend/k8s/
   ```

5. **驗證服務**
   ```bash
   kubectl get pods -n prod
   kubectl get services -n prod
   ```

---

## **✅ 結論**
- **本地端使用 Docker Compose 開發**
- **本地端 Kubernetes（kind 或 Minikube）模擬 AWS 環境**
- **生產環境使用 AWS EKS，透過 Terraform 自動部署**
- **使用 Kustomize 管理 `development` & `production` 環境**
- **GitHub Actions 或 ArgoCD 可進一步 CI/CD**

這樣你的開發流程就會符合 **最佳實踐 (Best Practice)**，讓本地開發、測試和生產部署統一 🚀