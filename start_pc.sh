rm -rf .web
pc init
yarn cache clean --cwd /app/.web
yarn install --update-checksums --cwd /app/.web
pc export --no-zip