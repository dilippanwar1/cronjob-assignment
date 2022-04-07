locals {
  s3_bucket_name = "dilip-panwar-pletform-challenge"
  s3_prefix      = toset(["qa", "staging"])
}
provider "aws" {
  region = var.region
}
module "create_s3_bucket" {
  for_each = local.s3_prefix
  source   = "./modules/aws_s3_bucket"
  #bucket_prefix = "qa"
  bucket_name = "${each.key}-${local.s3_bucket_name}"
  tags        = var.tags
}


