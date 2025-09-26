# Install claude Code
npm install -g @anthropic-ai/claude-code

uv sync --all-groups

cd src/aichhoernchen
uv run ./manage.py migrate
cd -
