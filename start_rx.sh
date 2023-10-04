rm -rf /app/.web
reflex init
reflex db init || true
reflex db makemigrations || true
reflex db migrate || true
yarn cache clean --cwd /app/.web
yarn install --update-checksums --cwd /app/.web
reflex export --no-zip