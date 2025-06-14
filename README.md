# Github Trending

![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/tomowang/github-trending/publish.yml)
![GitHub Tag](https://img.shields.io/github/v/tag/tomowang/github-trending)
![GitHub License](https://img.shields.io/github/license/tomowang/github-trending)

Service to crawler <https://github.com/trending> and response structured JSON
list.

## Usage

```bash
# run docker image
docker run -d \
    -p 18000:8000 \
    --name github-trending \
    ghcr.io/tomowang/github-trending:latest

# testing
curl http://localhost:18000/api/trending
# or specify language
curl http://localhost:18000/api/trending/python
```
