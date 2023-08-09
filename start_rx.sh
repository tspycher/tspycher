rm -rf .web
reflex init
yarn cache clean --cwd /app/.web
yarn install --update-checksums --cwd /app/.web
reflex export --no-zip