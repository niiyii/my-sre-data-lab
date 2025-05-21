provider "kubernetes" {
  # Configuration for Kubernetes provider.
  # By default, it uses ~/.kube/config
}

resource "kubernetes_namespace" "data_namespace" {
  metadata {
    name = "data-processing"
    labels = {
      purpose = "data-lab"
    }
  }
}

output "data_namespace_name" {
  value = kubernetes_namespace.data_namespace.metadata[0].name
  description = "The name of the created Kubernetes namespace."
}