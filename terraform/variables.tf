variable "bucket_name" {
  type        = string
  description = "Nombre del bucket S3 a crear"
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
  description = "Región de AWS donde se creará la infraestructura"
}
