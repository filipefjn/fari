# What is Fari?

Fari is a simple self-hosted music library manager with an web interface.

# Setup with Docker

Compile the frontend:

```bash
docker run -v "$(pwd):/srv/project/" --rm node:lts-buster bash -c "cd /srv/project/frontend && npm install && npm run build"
```

Build the Dockerfile:

```bash
docker build -t fari .
```

Run the Docker image:

```bash
docker run -v "<your-library-directory>:/srv/library" -p 80:80 -d fari
```
