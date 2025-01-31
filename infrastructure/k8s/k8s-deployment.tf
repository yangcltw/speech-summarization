resource "kubernetes_deployment" "summarization_service" {
  metadata {
    name      = "summarization-service"
    namespace = "default"
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "summarization-service"
      }
    }
    template {
      metadata {
        labels = {
          app = "summarization-service"
        }
      }
      spec {
        container {
          name  = "summarization-service"
          image = "summarization-service:latest"
          ports {
            container_port = 8002
          }
        }
      }
    }
  }
}

resource "kubernetes_deployment" "api_gateway" {
  metadata {
    name      = "api-gateway"
    namespace = "default"
  }
  spec {
    replicas = 2
    selector {
      match_labels = {
        app = "api-gateway"
      }
    }
    template {
      metadata {
        labels = {
          app = "api-gateway"
        }
      }
      spec {
        container {
          name  = "api-gateway"
          image = "api-gateway:latest"
          ports {
            container_port = 8000
          }
        }
      }
    }
  }
}
