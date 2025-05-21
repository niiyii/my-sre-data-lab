terraform {
  required_providers {
    kubernetes = {
      source = "hashicorp/kubernetes"
      version = "2.28.0" # Use a compatible version
    }
  }
}