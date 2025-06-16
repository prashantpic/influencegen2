resource "aws_security_group" "this" {
  for_each    = var.security_group_definitions
  name_prefix = "${var.project_name}-${var.environment_name}-${each.key}-sg-"
  description = each.value.description
  vpc_id      = var.vpc_id

  tags = merge(var.tags, var.default_tags, {
    Name        = "${var.project_name}-${var.environment_name}-${each.key}-sg"
    Environment = var.environment_name
    Role        = each.key
  })
}

resource "aws_security_group_rule" "ingress" {
  for_each          = {
    for sg_name, sg_def in var.security_group_definitions :
    "${sg_name}-${index}" => {
      sg_id = aws_security_group.this[sg_name].id
      rule  = rule
    }
    for sg_name, sg_def in var.security_group_definitions :
    index = count.index
    rule  = sg_def.ingress[count.index]
    : if length(sg_def.ingress) > 0
  }

  type              = "ingress"
  from_port         = each.value.rule.from_port
  to_port           = each.value.rule.to_port
  protocol          = each.value.rule.protocol
  cidr_blocks       = lookup(each.value.rule, "cidr_blocks", null)
  source_security_group_id = lookup(each.value.rule, "source_security_group_id", null)
  description       = lookup(each.value.rule, "description", null)
  security_group_id = each.value.sg_id
}

resource "aws_security_group_rule" "egress" {
  for_each          = {
    for sg_name, sg_def in var.security_group_definitions :
    "${sg_name}-${index}" => {
      sg_id = aws_security_group.this[sg_name].id
      rule  = rule
    }
    for sg_name, sg_def in var.security_group_definitions :
    index = count.index
    rule  = sg_def.egress[count.index]
    : if length(sg_def.egress) > 0
  }

  type              = "egress"
  from_port         = each.value.rule.from_port
  to_port           = each.value.rule.to_port
  protocol          = each.value.rule.protocol
  cidr_blocks       = lookup(each.value.rule, "cidr_blocks", ["0.0.0.0/0"]) # Default egress to all
  description       = lookup(each.value.rule, "description", null)
  security_group_id = each.value.sg_id
}