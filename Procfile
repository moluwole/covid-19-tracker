web: gunicorn --reload --workers=2 --bind 0.0.0.0:${PORT} app:app
clock: python core/cron.py