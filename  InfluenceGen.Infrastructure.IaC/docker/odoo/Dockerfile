# syntax=docker/dockerfile:1.4

ARG ODOO_VERSION=18.0
FROM odoo:${ODOO_VERSION}

# This Dockerfile is primarily for building a base Odoo image with custom addons baked in.
# For easier updates, consider mounting addons as volumes in docker-compose instead.

USER root # Temporarily switch to root for installations

# Install system dependencies for custom modules if any
# Example: Add necessary packages required by specific custom addons
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     package1 package2 \
#     && rm -rf /var/lib/apt/lists/*

USER odoo # Switch back to the odoo user

# Copy custom InfluenceGen addons into the image
# Assuming the custom addons are in a directory named 'influence_gen_addons'
# relative to the Dockerfile build context.
# This approach bakes the addons into the image.
# Alternative: Manage addons outside the image and mount as volumes in docker-compose.
COPY ./influence_gen_addons/ /mnt/extra-addons/influence_gen_addons/

# Add other custom addons if they are part of this build context
# COPY ./other_addons/ /mnt/extra-addons/other_addons/

# Ensure odoo.conf is picked up or specific env vars are set for addons path
# The default odoo entrypoint often looks for /etc/odoo/odoo.conf or uses env vars.
# If you need a specific odoo.conf, copy it here:
# COPY ./odoo.conf /etc/odoo/odoo.conf
# Ensure the addons_path in odoo.conf includes /mnt/extra-addons/

# Alternatively, set environment variable if entrypoint respects it:
# ENV ODOO_EXTRA_ADDONS_PATH=/mnt/extra-addons

# Optional: Install Python dependencies specific to custom modules
# If custom modules have their own requirements.txt
# COPY ./influence_gen_addons/requirements.txt /tmp/requirements.txt
# RUN pip install --no-cache-dir -r /tmp/requirements.txt

# The default Odoo image entrypoint usually handles starting the server.
# If you need a custom entrypoint, define it here.

# Expose the default Odoo port
EXPOSE 8069

# Default command to run the Odoo server
# CMD ["odoo"] # Or use the default ENTRYPOINT defined in the base image