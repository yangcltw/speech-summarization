provider "kubernetes" {
  config_path = "~/.kube/config"
}

resource "kubernetes_deployment" "stt_service" {
  metadata {
    name      = "stt-service"
    namespace = "default"
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "stt-service"
      }
    }
    template {
      metadata {
        labels = {
          app = "stt-service"
        }
      }
      spec {
        container {
          name  = "stt-service"
          image = "stt-service:latest"
          ports {
            container_port = 8001
          }
        }
      }
    }
  }
}

# 類似的配置也可以用於 summarization-service 和 api-gateway
