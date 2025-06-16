resource "aws_vpc" "this" {
  cidr_block = var.vpc_cidr_block

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-vpc"
    Environment = var.environment_name
  })
}

resource "aws_internet_gateway" "this" {
  vpc_id = aws_vpc.this.id

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-igw"
    Environment = var.environment_name
  })
}

resource "aws_subnet" "public" {
  count             = length(var.public_subnet_cidrs)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.public_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index % length(var.availability_zones)]
  map_public_ip_on_launch = true

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-public-subnet-${count.index + 1}"
    Environment = var.environment_name
    Tier        = "Public"
  })
}

resource "aws_subnet" "private" {
  count             = length(var.private_subnet_cidrs)
  vpc_id            = aws_vpc.this.id
  cidr_block        = var.private_subnet_cidrs[count.index]
  availability_zone = var.availability_zones[count.index % length(var.availability_zones)]

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-private-subnet-${count.index + 1}"
    Environment = var.environment_name
    Tier        = "Private"
  })
}

resource "aws_eip" "nat_gateway" {
  count = length(aws_subnet.public) // One EIP per public subnet for NAT GWs
  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-nat-eip-${count.index + 1}"
    Environment = var.environment_name
  })
}

resource "aws_nat_gateway" "this" {
  count         = length(aws_subnet.public) // One NAT GW per public subnet
  allocation_id = aws_eip.nat_gateway[count.index].id
  subnet_id     = aws_subnet.public[count.index].id

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-nat-gateway-${count.index + 1}"
    Environment = var.environment_name
  })
  depends_on = [aws_internet_gateway.this]
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.this.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.this.id
  }

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-public-rt"
    Environment = var.environment_name
  })
}

resource "aws_route_table" "private" {
  count  = length(aws_subnet.private) // One private RT per private subnet, pointing to a NAT GW
  vpc_id = aws_vpc.this.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.this[count.index % length(aws_nat_gateway.this)].id # Distribute across NAT GWs
  }

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-private-rt-${count.index + 1}"
    Environment = var.environment_name
  })
}

resource "aws_route_table_association" "public" {
  count          = length(aws_subnet.public)
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "private" {
  count          = length(aws_subnet.private)
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}