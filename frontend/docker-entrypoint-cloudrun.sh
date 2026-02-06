#!/bin/sh
set -e

# Substituer les variables d'environnement dans la config Nginx
envsubst '${PORT}' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf

# Démarrer Nginx
exec nginx -g 'daemon off;'
