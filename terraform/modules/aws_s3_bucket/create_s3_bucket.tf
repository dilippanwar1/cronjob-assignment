resource "aws_s3_bucket" "bucket" {
    bucket = var.bucket_name
    #bucket_prefix = var.bucket_prefix
    tags = var.tags    
}

resource "aws_s3_bucket_public_access_block" "block_pub_access" {
  bucket = aws_s3_bucket.bucket.id

  block_public_acls   = true
  block_public_policy = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
