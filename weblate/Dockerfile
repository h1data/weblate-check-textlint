FROM weblate/weblate:5.15.2.0

USER 1000

COPY --chown=1000:1000 settings-override.py /app/data/
COPY --chown=1000:1000 customize/textlint/ /app/data/python/customize/textlint/
