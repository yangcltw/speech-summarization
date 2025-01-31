variable "region" {
  description = "AWS region to deploy to"
  default     = "us-west-2"
}

variable "instance_type" {
  description = "Type of EC2 instance"
  default     = "t2.micro"
}

# 其他基礎設施變數
