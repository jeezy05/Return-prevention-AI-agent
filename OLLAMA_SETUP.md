# 🚀 Ollama Setup Guide - Free LLM for Return Prevention Agent

## Why Ollama?

✅ **100% FREE** - No API costs
✅ **Self-hosted** - Data stays on your machine
✅ **Fast** - Local processing (no network latency)
✅ **Powerful** - Advanced models (Mistral, Llama2, etc.)
✅ **Easy setup** - Works out of the box
✅ **No API keys** - No signup required

---

## Quick Setup (5 Minutes)

### Step 1: Download Ollama

**Windows:**
1. Go to https://ollama.ai/download
2. Download Windows installer
3. Run installer and follow prompts
4. Restart your computer

**Mac:**
1. Go to https://ollama.ai/download
2. Download Mac installer
3. Run installer

**Linux:**
```bash
curl https://ollama.ai/install.sh | sh
```

### Step 2: Start Ollama

**Windows/Mac:**
- Ollama starts automatically after installation
- Look for Ollama icon in system tray/menu bar

**Linux:**
```bash
ollama serve
```

### Step 3: Pull a Model

Open terminal and run:
```bash
# Mistral - Fast, good quality (recommended for this project)
ollama pull mistral

# Or Llama2 - More capable but slower
ollama pull llama2

# Or Neural Chat - Specialized for chat
ollama pull neural-chat

# Or Openchat - Faster alternative
ollama pull openchat
```

**First time will take 5-10 minutes** (downloads ~4GB model)

### Step 4: Verify Ollama is Running

```bash
# Test if Ollama is accessible
curl http://localhost:11434/api/tags
```

Expected response:
```json
{"models":[{"name":"mistral:latest",...}]}
```

---

## Model Selection

### Best for Return Prevention Agent

| Model | Size | Speed | Quality | Recommendation |
|-------|------|-------|---------|-----------------|
| **mistral** | 5GB | ⚡⚡⚡ Fast | ⭐⭐⭐⭐ Great | ✅ **BEST** |
| llama2 | 3.5GB | ⚡⚡ Medium | ⭐⭐⭐⭐ Great | ✅ Good |
| neural-chat | 4GB | ⚡⚡ Medium | ⭐⭐⭐⭐ Great | ✅ Good |
| openchat | 3.8GB | ⚡⚡ Medium | ⭐⭐⭐ Good | ✅ Good |
| dolphin-mixtral | 26GB | ⚡ Slow | ⭐⭐⭐⭐⭐ Excellent | For powerful machines |

**Recommended:** Start with **mistral** (5GB, fast, high quality)

---

## Installation by Operating System

### Windows

#### Method 1: Installer (Easiest)
```
1. Download from https://ollama.ai
2. Run installer (.exe)
3. Follow prompts
4. Restart computer
5. Ollama runs automatically
```

#### Method 2: Manual (Advanced)
```powershell
# Download and install using Winget
winget install Ollama.Ollama

# Or download manually and add to PATH
# Then run: ollama serve
```

#### Verify Installation
```powershell
# Open PowerShell and run
ollama --version
ollama pull mistral
```

---

### Mac

#### Installation
```bash
# Option 1: Direct installer
# Download from https://ollama.ai and run .dmg

# Option 2: Homebrew
brew install ollama

# Then pull model
ollama pull mistral
```

#### Verify
```bash
ollama --version
ollama pull mistral
```

---

### Linux

#### Installation
```bash
# Ubuntu/Debian
curl https://ollama.ai/install.sh | sh

# Or manual
mkdir -p ~/ollama
cd ~/ollama
wget https://ollama.ai/download/ollama-linux-amd64.tar.gz
tar -xzf ollama-linux-amd64.tar.gz
```

#### Start Service
```bash
# Start Ollama in background
ollama serve &

# Or run in foreground
ollama serve
```

#### Verify
```bash
ollama --version
ollama pull mistral
```

---

## Running Ollama

### Windows
- **Automatic**: Ollama runs in background after installation
- **Manual**: Run `ollama.exe serve` in terminal
- **Check**: Look for Ollama in system tray

### Mac
- **Automatic**: Click Ollama in dock
- **Manual**: Open Applications → Ollama
- **Terminal**: `ollama serve`

### Linux
```bash
# Run in foreground (for testing)
ollama serve

# Run in background
ollama serve &

# Keep running with systemd
systemctl start ollama
systemctl enable ollama
```

---

## Switching Models

### Pull Different Model
```bash
# Download new model
ollama pull llama2

# List all downloaded models
ollama list

# Remove a model
ollama rm mistral
```

### Update Config

Edit `config.yaml`:
```yaml
ai_analysis:
  model: "llama2"  # Change here
  ollama_base_url: "http://localhost:11434"
```

---

## Testing Ollama Connection

### Test 1: Check if Running
```bash
curl http://localhost:11434/api/tags
```

### Test 2: Quick Chat
```bash
curl -X POST http://localhost:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{"model": "mistral", "prompt": "Hello", "stream": false}'
```

### Test 3: In Python
```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={"model": "mistral", "prompt": "test", "stream": False},
    timeout=60
)
print(response.json())
```

---

## Troubleshooting

### Issue: "Connection refused"
```
Problem: Ollama not running
Solution: Start Ollama
  Windows: Run ollama.exe
  Mac: Open Ollama from Applications
  Linux: ollama serve
```

### Issue: "Model not found"
```
Problem: Model not downloaded
Solution: Pull model first
  ollama pull mistral
```

### Issue: "Slow responses"
```
Problem: Using large model on weak machine
Solution: Use smaller model
  Mistral (5GB) instead of Llama2 (7GB)
  Or use 7B quantized version
```

### Issue: "Out of memory"
```
Problem: Machine doesn't have enough RAM
Solution: Use smaller model or quantized version
  Mistral 7B: ~5GB RAM needed
  Check available RAM: free -h (Linux/Mac) or Task Manager (Windows)
```

### Issue: "Ollama service won't start"
```
Problem: Port 11434 already in use
Solution: Kill process and restart
  Linux/Mac: lsof -i :11434 then kill PID
  Windows: netstat -ano | find "11434"
```

---

## Performance Tips

### Optimize for Speed
```yaml
# config.yaml
ai_analysis:
  model: "mistral"          # Fastest quality option
  temperature: 0.5          # Lower = faster, more predictable
```

### Optimize for Quality
```yaml
ai_analysis:
  model: "neural-chat"      # Better reasoning
  temperature: 0.7          # More creative
```

### First Time Setup
1. Pull model: `ollama pull mistral` (~10 mins)
2. First query slower (~30 seconds) - GPU warming up
3. Subsequent queries faster (~5-10 seconds)

---

## GPU Acceleration (Optional)

### NVIDIA GPU
```bash
# CUDA support (faster with GPU)
# Ollama auto-detects NVIDIA GPU
# Just install CUDA toolkit: https://developer.nvidia.com/cuda-downloads
```

### AMD GPU
```bash
# ROCm support
# Set environment variable
export HSA_OVERRIDE_GFX_VERSION=gfx90a
ollama serve
```

### Apple Silicon (M1/M2/M3)
```bash
# Metal support built-in
# Automatic GPU acceleration
# No additional setup needed
```

---

## Models Comparison for Return Analysis

### Mistral (RECOMMENDED)
```
Size: 5GB
Speed: ⚡⚡⚡ Very Fast
Quality: ⭐⭐⭐⭐⭐ Excellent
Memory: ~8GB needed
Best for: Quick analysis, good quality
```

### Llama2
```
Size: 3.5GB
Speed: ⚡⚡ Moderate
Quality: ⭐⭐⭐⭐ Great
Memory: ~8GB needed
Best for: Balanced performance
```

### Neural Chat
```
Size: 4GB
Speed: ⚡⚡ Moderate
Quality: ⭐⭐⭐⭐ Great
Memory: ~8GB needed
Best for: Conversation-focused
```

### Dolphin Mixtral
```
Size: 26GB
Speed: ⚡ Slow
Quality: ⭐⭐⭐⭐⭐ Excellent
Memory: ~28GB needed
Best for: Powerful machines, best quality
```

---

## Running Return Prevention Agent with Ollama

### Step 1: Start Ollama
```bash
ollama serve
# Leave this running in background
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Pipeline
```bash
python main.py
```

### Pipeline Will Automatically:
1. ✓ Connect to Ollama
2. ✓ Use Mistral model
3. ✓ Generate root cause analysis
4. ✓ Create recommendations
5. ✓ Generate reports

---

## Advanced: Custom Model Configuration

### Using Different Model Sizes

**Mistral quantized versions:**
```bash
# Full model
ollama pull mistral:latest

# Quantized (smaller)
ollama pull mistral:7b-instruct-q4_K_M
```

### Memory Requirements

| Model | Full Size | Quantized | Min RAM |
|-------|-----------|-----------|---------|
| Mistral 7B | 15GB | 5GB | 8GB |
| Llama2 7B | 13GB | 4GB | 8GB |
| Llama2 13B | 26GB | 8GB | 16GB |

---

## Monitoring Ollama

### Check Running Models
```bash
ollama list
```

### View Ollama Logs
```bash
# Linux/Mac
tail -f /var/log/ollama/

# Or check Ollama app logs
```

### Stop Ollama
```bash
# Linux/Mac
killall ollama

# Or stop in menu (Mac) / system tray (Windows)
```

---

## Cost Comparison

| Solution | Cost | Setup Time | Performance |
|----------|------|-----------|-------------|
| **Ollama** | $0 | 15 min | ⭐⭐⭐⭐⭐ |
| OpenAI API | $50/month | 5 min | ⭐⭐⭐⭐⭐ |
| Other SaaS | $100+/month | 10 min | ⭐⭐⭐⭐ |

**Ollama wins on cost!** 🏆

---

## FAQ

**Q: Can I use Ollama remotely?**
A: Yes, configure OLLAMA_BASE_URL to point to remote machine

**Q: Can I run multiple models?**
A: Yes, but only one at a time (shares memory)

**Q: Is it secure?**
A: Yes, runs locally with no external connections

**Q: Can I use without GPU?**
A: Yes, CPU only (slower but works)

**Q: Which model is best?**
A: Mistral for return analysis (fast + good quality)

**Q: How much disk space needed?**
A: ~10-15GB for model + system

---

## Next Steps

1. **Install Ollama**: Download from ollama.ai
2. **Pull model**: `ollama pull mistral`
3. **Verify**: `curl http://localhost:11434/api/tags`
4. **Run pipeline**: `python main.py`
5. **Check report**: Open HTML in browser

---

## Support

### Ollama Docs
- https://ollama.ai/docs
- https://github.com/ollama/ollama

### Troubleshooting
- Check logs: See above
- Restart Ollama: Stop and start again
- Clear cache: `ollama rm <model>`

---

## Summary

✅ **Completely FREE** - No subscriptions
✅ **Easy setup** - 15 minutes
✅ **Fast** - Local processing
✅ **Powerful** - Enterprise-grade models
✅ **Secure** - Your data stays private

**Let's get started! 🚀**

```bash
# 1. Download from https://ollama.ai
# 2. Run: ollama pull mistral
# 3. Run: python main.py
# Done! 🎉
```
