output "bucket_name" {
  description = "Nombre del bucket S3 creado"
  value       = aws_s3_bucket.poc_bucket.bucket
}

output "poc_role_arn" {
  description = "ARN del rol IAM para la POC"
  value       = aws_iam_role.poc_role.arn
}
