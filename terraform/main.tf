provider "aws" {
  region = var.aws_region
}

# 1. S3 Bucket
resource "aws_s3_bucket" "poc_bucket" {
  bucket = var.bucket_name

  # Opcional: activar versionado
  versioning {
    enabled = true
  }

  # Opcional: etiquetas
  tags = {
    Environment = "POC"
    Name        = var.bucket_name
  }
}

# 2. IAM Role para Glue, Airflow y SES
#    Asume quelos servicios (por jemplo, AWS Glue o MWAA para el Airflow)

data "aws_iam_policy_document" "assume_role_policy" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = [
        "glue.amazonaws.com",
        "airflow.amazonaws.com",
        "ec2.amazonaws.com"
        # Agrega aquí otros servicios si los necesitas
      ]
    }
    actions = [
      "sts:AssumeRole"
    ]
  }
}

resource "aws_iam_role" "poc_role" {
  name               = "POC_Role"
  assume_role_policy = data.aws_iam_policy_document.assume_role_policy.json
}

# 3. Definimos la política que otorga permisos para S3, Glue y SES
data "aws_iam_policy_document" "poc_policy_doc" {
  statement {
    sid     = "AllowS3Access"
    effect  = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject",
      "s3:PutObject"
    ]
    resources = [
      aws_s3_bucket.poc_bucket.arn,
      "${aws_s3_bucket.poc_bucket.arn}/*"
    ]
  }

  statement {
    sid     = "AllowGlueOperations"
    effect  = "Allow"
    actions = [
      "glue:*"
    ]
    resources = ["*"]
  }

  statement {
    sid     = "AllowSESSendEmail"
    effect  = "Allow"
    actions = [
      "ses:SendEmail",
      "ses:SendRawEmail"
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "poc_policy" {
  name        = "POCPolicy"
  description = "Policy for S3, Glue, and SES for the POC"
  policy      = data.aws_iam_policy_document.poc_policy_doc.json
}

# 4. Adjuntamos la política al rol
resource "aws_iam_role_policy_attachment" "attach_poc_policy" {
  role       = aws_iam_role.poc_role.name
  policy_arn = aws_iam_policy.poc_policy.arn
}
