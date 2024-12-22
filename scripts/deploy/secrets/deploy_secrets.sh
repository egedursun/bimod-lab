#!/bin/bash

#
# Copyright (c) 2024 BMD™ Autonomous Holdings. All rights reserved.
#
# Project: Bimod.io™
# File: deploy_secrets.sh
# Last Modified: 2024-12-21 16:43:35
# Author: Ege Dogan Dursun (Co-Founder & Chief Executive Officer / CEO @ BMD™ Autonomous Holdings)
# Created: 2024-12-21 16:45:10
#
# This software is proprietary and confidential. Unauthorized copying,
# distribution, modification, or use of this software, whether for
# commercial, academic, or any other purpose, is strictly prohibited
# without the prior express written permission of BMD™ Autonomous
# Holdings.
#
#  For permission inquiries, please contact: admin@Bimod.io.
#
#

# Define variables
SERVER_URL="185.170.198.44"
USERNAME="root"
LOCAL_DEV_FILE="../../../.env.dev"
LOCAL_PROD_FILE="../../../.env.prod"
REMOTE_DEV_PATH="/var/www/bimod_dev/.env"
REMOTE_PROD_PATH="/var/www/bimod_prod/.env"

# Deploy .env.dev to /var/www/bimod_dev/.env
echo "Deploying $LOCAL_DEV_FILE to $REMOTE_DEV_PATH..."
scp -o StrictHostKeyChecking=no -P 22 "$LOCAL_DEV_FILE" "$USERNAME@$SERVER_URL:$REMOTE_DEV_PATH"
if [ $? -eq 0 ]; then
  echo "Successfully deployed $LOCAL_DEV_FILE to $REMOTE_DEV_PATH"
else
  echo "Failed to deploy $LOCAL_DEV_FILE to $REMOTE_DEV_PATH"
  exit 1
fi

# Restart the development server
ssh -o StrictHostKeyChecking=no -p 22 "$USERNAME@$SERVER_URL" "systemctl restart gunicorn_dev"
if [ $? -eq 0 ]; then
  echo "Successfully restarted gunicorn_dev"
else
  echo "Failed to restart gunicorn_dev"
  exit 1
fi

# Deploy .env.prod to /var/www/bimod_prod/.env
echo "Deploying $LOCAL_PROD_FILE to $REMOTE_PROD_PATH..."
scp -o StrictHostKeyChecking=no -P 22 "$LOCAL_PROD_FILE" "$USERNAME@$SERVER_URL:$REMOTE_PROD_PATH"
if [ $? -eq 0 ]; then
  echo "Successfully deployed $LOCAL_PROD_FILE to $REMOTE_PROD_PATH"
else
  echo "Failed to deploy $LOCAL_PROD_FILE to $REMOTE_PROD_PATH"
  exit 1
fi

# Restart the production server
ssh -o StrictHostKeyChecking=no -p 22 "$USERNAME@$SERVER_URL" "systemctl restart gunicorn_prod"
if [ $? -eq 0 ]; then
  echo "Successfully restarted gunicorn_prod"
else
  echo "Failed to restart gunicorn_prod"
  exit 1
fi

# Restart Nginx
ssh -o StrictHostKeyChecking=no -p 22 "$USERNAME@$SERVER_URL" "systemctl restart nginx"
if [ $? -eq 0 ]; then
  echo "Successfully restarted nginx"
else
  echo "Failed to restart nginx"
  exit 1
fi

# Print completion message
echo "Deployment and server restarts completed successfully."
