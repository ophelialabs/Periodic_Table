# Deployment & Maintenance Guide

## Current Version
- **Framework**: Flask 2.3.3
- **Python**: 3.10+
- **Status**: Phase 1 Complete (70%), Phase 3 Ready
- **Last Updated**: November 21, 2025

## Production Deployment

### Prerequisites
- Python 3.10 or higher
- 50MB disk space (including dependencies)
- Modern web browser for testing

### Deployment Steps

#### 1. Environment Setup
```bash
# Clone/setup project
git clone [repository-url] periodic-table-app
cd periodic-table-app

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### 2. Production Server Setup
```bash
# Install production WSGI server
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 'src.app:create_app()'

# Or use uWSGI
pip install uwsgi
uwsgi --http :8000 --wsgi-file src/app/__init__.py --callable app --processes 4
```

#### 3. Reverse Proxy (Nginx Example)
```nginx
server {
    listen 80;
    server_name periodic-table.example.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /static {
        alias /path/to/app/src/app/static;
        expires 30d;
    }
}
```

#### 4. SSL Certificate (Let's Encrypt)
```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Generate certificate
sudo certbot certonly --nginx -d periodic-table.example.com

# Auto-renewal
sudo systemctl enable certbot.timer
```

## Development Workflow

### Local Development
```bash
# Start dev server (with hot reload)
python run_server.py

# Server runs on http://127.0.0.1:5000
# Debug mode: ON
# Auto-reload: ON
```

### Code Changes
- Edit files as needed
- Browser auto-reloads due to Flask debug mode
- Check console for any errors

### Testing Changes
```bash
# Test database functionality
python -c "from src.element_database import ElementDatabase; print(ElementDatabase().get_element_count())"

# Run analysis generator
python generate_analysis.py

# Quick Python syntax check
python -m py_compile src/*.py
```

## Maintenance Tasks

### Regular Maintenance
- [ ] Check server logs daily in production
- [ ] Monitor disk usage (reports folder)
- [ ] Review error logs weekly
- [ ] Test visualizations monthly
- [ ] Update dependencies quarterly

### Performance Monitoring
```bash
# Check server resource usage
top -o %MEM
ps aux | grep python

# View Flask error logs
tail -f /var/log/app.log

# Monitor response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:5000/
```

### Database Maintenance
```bash
# Export element data
python generate_analysis.py
# Creates elements_data.csv in src/reports/

# Backup periodic table JSON
cp src/lib/Periodic-Table-JSON/PeriodicTableJSON.json backup/

# Validate JSON integrity
python src/lib/Periodic-Table-JSON/scripts/validate_json.py
```

## Security Configuration

### Essential Security Headers
Add to `src/app/__init__.py`:
```python
@app.after_request
def set_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000'
    return response
```

### CSRF Protection
```bash
pip install flask-wtf
```

### Rate Limiting
```bash
pip install flask-limiter
```

## Troubleshooting

### Server Won't Start
```bash
# Check if port is in use
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill process
kill -9 [PID]  # macOS/Linux
taskkill /PID [PID] /F  # Windows

# Try different port
python run_server.py --port 8000
```

### Database Not Loading
```bash
# Verify JSON file exists
ls -la src/lib/Periodic-Table-JSON/PeriodicTableJSON.json

# Test JSON validity
python -m json.tool src/lib/Periodic-Table-JSON/PeriodicTableJSON.json

# Check file permissions
chmod 644 src/lib/Periodic-Table-JSON/PeriodicTableJSON.json
```

### Visualizations Not Working
```bash
# Check browser console for errors (F12)
# Verify API endpoints respond
curl http://localhost:5000/api/elements/all

# Check matplotlib installation
python -c "import matplotlib; print(matplotlib.__version__)"
```

### CSS Not Loading
```bash
# Hard refresh browser
Cmd+Shift+R (macOS)
Ctrl+Shift+R (Windows)

# Check static files path
ls src/app/static/css/
```

## Updating Dependencies

### Check for Updates
```bash
pip list --outdated
pip index versions Flask
```

### Safe Update Process
```bash
# Update single package
pip install --upgrade Flask

# Update all dependencies
pip install --upgrade -r requirements.txt

# Save new versions
pip freeze > requirements.txt

# Test thoroughly after updates
python -c "from src.app import create_app; print('App loads successfully')"
```

### Version Pinning
Current `requirements.txt` uses specific versions for stability:
```
Flask==2.3.3  # Specific version prevents breaking changes
numpy==1.24.3
```

## Backup & Recovery

### Backup Script
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d)
tar -czf backup/periodic-table-$DATE.tar.gz \
    src/lib/Periodic-Table-JSON/PeriodicTableJSON.json \
    src/reports/elements_data.csv \
    requirements.txt
echo "Backup created: backup/periodic-table-$DATE.tar.gz"
```

### Recovery
```bash
tar -xzf backup/periodic-table-[DATE].tar.gz
pip install -r requirements.txt
python run_server.py
```

## Scaling Considerations

### Current Limitations
- Single-threaded by default
- All elements loaded into memory (119 × ~2KB = ~240KB)
- Suitable for <100 concurrent users

### To Scale Up
1. Use Gunicorn with multiple workers: `gunicorn -w 8`
2. Add caching layer (Redis)
3. Implement CDN for static files
4. Use database instead of JSON (PostgreSQL/MongoDB)
5. Add queue system for reports (Celery)

### Load Testing
```bash
# Install Apache Bench
brew install httpd  # macOS

# Run test
ab -n 1000 -c 10 http://localhost:5000/

# Results show requests/sec and response times
```

## Logging Configuration

### Add Proper Logging
```python
# In src/app/__init__.py
import logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)
```

### Log Levels
- DEBUG: Development info
- INFO: General app events
- WARNING: Unexpected conditions
- ERROR: Error conditions
- CRITICAL: Critical failures

## Monitoring & Alerts

### Health Check Endpoint
```python
@app.route('/health')
def health():
    return jsonify({
        'status': 'healthy',
        'elements': app.db.get_element_count(),
        'timestamp': datetime.now()
    })
```

### Status Page
Monitor at: `http://localhost:5000/health`

## Version Control

### Git Setup
```bash
git init
git add .
git commit -m "Initial commit: Phase 1 complete"

# Tags for releases
git tag -a v1.0.0 -m "Phase 1 complete"
git push origin v1.0.0
```

### Commit Messages
```
feat: Add feature name
fix: Fix bug description
docs: Update documentation
style: Code style changes
refactor: Code refactoring
test: Add tests
chore: Build, dependencies, etc.
```

## CI/CD Pipeline (GitHub Actions Example)

```yaml
name: Test & Deploy
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - run: python -m pytest tests/
      - run: python -m py_compile src/*.py
```

## Contact & Support

- **Issues**: Check browser console (F12)
- **Logs**: Check `app.log` or server output
- **Database**: Verify `PeriodicTableJSON.json` exists
- **API**: Test endpoints with curl or Postman

## Roadmap

- **Phase 3** (Next): 3D visualizations, matplotlib charts
- **Phase 4**: PDF report generation
- **Phase 5-8**: Database, quantum integration, AI agent

See `PHASE3_GUIDE.md` for implementation details.

---

**Last Updated**: November 21, 2025
**Maintenance Status**: Active
**Support Level**: Full development support available
