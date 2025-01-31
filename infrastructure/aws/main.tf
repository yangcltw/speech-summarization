# TODO
provider "aws" {
  region = "us-west-2"
}

# 建立 VPC、子網路、EC2 等 AWS 基礎設施資源
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_security_group" "default" {
  name_prefix = "default-"
  vpc_id      = aws_vpc.main.id
}

# 其他 AWS 配置，根據需求進行擴展
