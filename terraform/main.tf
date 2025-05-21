# File: ~/my-sre-data-lab/terraform/main.tf

provider "kubernetes" {
  # REMOVE OR COMMENT OUT THIS LINE:
  # config_path = "~/.kube/config"
}

resource "kubernetes_namespace" "data_namespace" {
  metadata {
    name = "data-namespace"
    labels = {
      purpose = "data-lab"
    }
  }
}

output "data_namespace_name" {
  value = kubernetes_namespace.data_namespace.metadata[0].name
  description = "The name of the created Kubernetes namespace."
}