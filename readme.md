####練習：

本地開發＋自動化測試＋Docker容器化並透過GitHub Action做自動化部署到GCP

![alt text](image.png)


```mermaid
graph LR
    subgraph Local[本地開發]
        A[Flask App] -->|測試| B[自動化測試]
    end

    subgraph Deploy[自動化部署]
        B -->|通過| C[Docker 容器化]
        C -->|GitHub Actions| D[GCP Cloud Run]
    end

    D -->|產生| E[公開服務 URL]

```