# 🚀 MOKSHA AI - GPU DEPLOYMENT GUIDE

**For:** RunPod / Vast.ai / Cloud GPU Deployment  
**When to Use:** After local mock tests pass ✅  
**GPU Required:** RTX 4090 / L40S / A100 (24GB+ VRAM)  
**Estimated Cost:** $3-5 for full deployment & testing  

---

## 📋 **PRE-DEPLOYMENT CHECKLIST**

### **✅ Step 1: Local Mock Tests (CPU)**

```bash
# Run this FIRST on your local machine (no GPU needed)
cd "c:\Amar\Project\AI-OS\Mokshya-AI"
python test_mock_pipeline.py
```

**Expected Output:**
```
✅ Voice Engine - PASS
✅ Avatar Engine - PASS (Code validation)
✅ Video Engine - PASS (Code validation)
✅ Layer Engine - PASS
✅ Script Engine - PASS (if API key available)
✅ Scene Planner - PASS

📈 Results: 6/6 tests passed
🎉 ALL TESTS PASSED!
✅ Ready for GPU deployment
```

**If ANY test fails:**
```
❌ Fix the error locally first
❌ Do NOT deploy to GPU until all tests pass
❌ Check COMPLETE_SYSTEM_FLOW.md for troubleshooting
```

---

## 🎯 **STEP 2: CHOOSE GPU PROVIDER**

### **Option A: RunPod (Recommended)** ⭐

**Pros:**
- ✅ Pay-per-use (per second billing)
- ✅ Network Volumes (models persist)
- ✅ Easy deployment
- ✅ Pre-built templates

**Cons:**
- ❌ Slightly expensive (~$0.70/hr for RTX 4090)

**Best For:** Short-term testing & deployment

---

### **Option B: Vast.ai** 💰

**Pros:**
- ✅ Cheapest option (~$0.35/hr for RTX 4090)
- ✅ Many GPU options
- ✅ Community hosts

**Cons:**
- ❌ Less reliable
- ❌ Security concerns (third-party hosts)
- ❌ More complex setup

**Best For:** Budget-conscious, longer deployments

---

### **Option C: Lambda Labs** 🏢

**Pros:**
- ✅ Professional grade
- ✅ Reliable infrastructure
- ✅ Good support

**Cons:**
- ❌ Minimum billing (1 month)
- ❌ Expensive for short tests

**Best For:** Production deployment (not testing)

---

## 🔧 **STEP 3: LAUNCH GPU POD (RUNPOD)**

### **3.1: Create RunPod Account**

1. Go to https://runpod.io
2. Click "Sign Up"
3. Add $5-10 credit (minimum for testing)

---

### **3.2: Launch Pod**

**Click:** `Deploy` → `Custom Pod`

**Configuration:**

```yaml
GPU Selection:
  - RTX 4090 (24GB VRAM) ← RECOMMENDED
  - OR L40S (48GB VRAM) ← BETTER FOR PRODUCTION
  - OR A100 (40GB VRAM) ← MOST EXPENSIVE

Container Image:
  - PyTorch 2.0 + CUDA 11.8
  - OR "RunPod Base" (clean Ubuntu)

Storage:
  - Container Storage: 50 GB (minimum)
  - Network Volume: Create new (100 GB) ← IMPORTANT!

Network Volume Name: moksha-models
Location: Same as pod location

Advanced Settings:
  - Expose HTTP Ports: 8000 (for FastAPI)
  - Expose TCP Ports: (none needed)
  - Environment Variables: (add later)

Auto-Shutdown:
  - Enable: YES ← CRITICAL FOR COST CONTROL!
  - Idle Timeout: 5 minutes
  
Start Command: (leave empty)
```

**Click:** `Continue` → `Deploy Pod`

**Cost:** ~$0.70/hour (RTX 4090)

---

## 📥 **STEP 4: SETUP POD ENVIRONMENT**

### **4.1: Connect to Pod**

1. Go to RunPod Dashboard
2. Find your running pod
3. Click `Connect` button
4. Terminal opens in browser

---

### **4.2: Clone Repository**

```bash
# Navigate to workspace
cd /workspace

# Clone Moksha AI repository
git clone https://github.com/swamiparneet-design/moksha-mve1.git
cd moksha-mve1

# Verify files
ls -la
# Should see: engines/, main_app.py, requirements.txt, etc.
```

---

### **4.3: Install Dependencies**

```bash
# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
pip install -r requirements.txt

# Install additional GPU dependencies
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verify installation
python --version
# Should show: Python 3.10+

pip list | grep torch
# Should show: torch with CUDA support
```

---

### **4.4: Setup Environment Variables**

```bash
# Create .env file
cat > .env << EOF
# DeepSeek API (REQUIRED for script generation)
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# Groq API (OPTIONAL for fact-checking)
GROQ_API_KEY=your_groq_api_key_here

# Pexels API (REQUIRED for B-roll footage)
PEXELS_API_KEY=your_pexels_api_key_here

# YouTube API (REQUIRED for upload)
YOUTUBE_API_KEY=your_youtube_api_key_here
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret

# RunPod API (OPTIONAL for serverless)
RUNPOD_API_KEY=your_runpod_api_key
RUNPOD_ENDPOINT_ID=your_endpoint_id

# FFmpeg Paths (auto-detected on Linux)
FFMPEG_PATH=ffmpeg
FFPROBE_PATH=ffprobe

# Debug Mode
DEBUG_MODE=true
EOF

# Verify .env file
cat .env
```

---

## 📦 **STEP 5: DOWNLOAD MODELS**

### **5.1: Download Fish-Speech S2 Pro (11GB)**

```bash
# Navigate to workspace
cd /workspace/moksha-mve1

# Create checkpoints directory
mkdir -p checkpoints

# Download Fish-Speech models
cd fish-speech
python download_models.py

# Or manually from HuggingFace
git lfs install
git clone https://huggingface.co/fishaudio/fish-speech-1.4 checkpoints/s2-pro
```

**Expected:**
```
✅ Downloaded: s2-pro/model.pth (11GB)
✅ Models ready for inference
```

---

### **5.2: Download LivePortrait (2GB)**

```bash
cd /workspace/moksha-mve1

# Clone LivePortrait
git clone https://github.com/KwaiVGI/LivePortrait
cd LivePortrait

# Install dependencies
pip install -r requirements.txt

# Download models
python download_models.py
```

**Expected:**
```
✅ Downloaded: liveportrait/models/ (2GB)
✅ Ready for lip-sync inference
```

---

### **5.3: Download LTX-Video (4-6GB)**

```bash
cd /workspace/moksha-mve1

# Clone LTX-Video
git clone https://github.com/Lightricks/LTX-Video
cd LTX-Video

# Install dependencies
pip install -r requirements.txt

# Download models (check their docs for exact command)
python scripts/download_models.py
```

**Expected:**
```
✅ Downloaded: LTX-Video/models/ (4-6GB)
✅ Ready for AI video generation
```

---

### **5.4: Move Models to Network Volume (PERSISTENCE)**

**CRITICAL:** Models delete when pod terminates unless saved to Network Volume!

```bash
# Create network volume directories
mkdir -p /runpod-volume/checkpoints
mkdir -p /runpod-volume/LivePortrait
mkdir -p /runpod-volume/LTX-Video

# Copy models to network volume
cp -r /workspace/moksha-mve1/checkpoints/* /runpod-volume/checkpoints/
cp -r /workspace/moksha-mve1/LivePortrait/* /runpod-volume/LivePortrait/
cp -r /workspace/moksha-mve1/LTX-Video/* /runpod-volume/LTX-Video/

# Verify
ls -lh /runpod-volume/checkpoints/
# Should show: s2-pro/ (11GB)

ls -lh /runpod-volume/LivePortrait/
# Should show: models/ (2GB)

ls -lh /runpod-volume/LTX-Video/
# Should show: models/ (4-6GB)
```

**Total Model Size:** ~17-19GB

---

## 🧪 **STEP 6: RUN MOCK TESTS (VALIDATION)**

```bash
cd /workspace/moksha-mve1

# Run mock test pipeline
python test_mock_pipeline.py
```

**Expected Output:**
```
🧪 Mock Test System Initialized (CPU Mode)
📁 Test directory: outputs/mock_tests

============================================================
🎤 Testing Voice Engine (Mock Mode)
============================================================
✅ Mock audio created: outputs/mock_tests/test_voice.wav
   Duration: 5s, Size: 441078 bytes

============================================================
🎭 Testing Avatar Engine (Code Validation)
============================================================
✅ AvatarEngine initialized successfully
ℹ️  LivePortrait found - will use for GPU deployment
⚠️  Skipping inference (requires GPU)
🔧 Testing fallback avatar generation...
✅ Fallback avatar created: outputs/mock_tests/test_avatar.mp4

============================================================
🎬 Testing Video Engine (Code Validation)
============================================================
✅ VideoEngine initialized successfully
ℹ️  LTX-Video found - will use for GPU deployment
⚠️  Skipping inference (requires GPU)
🔧 Testing fallback video generation...
✅ Fallback video created: outputs/mock_tests/test_video.mp4

============================================================
✂️  Testing Layer Engine (Concatenation)
============================================================
✅ LayerEngine initialized successfully
✅ Final video compiled: outputs/mock_tests/test_final.mp4

============================================================
📝 Testing Script Engine (API Call)
============================================================
✅ ScriptEngine initialized successfully
📝 Generating test script...
✅ Script generated: 5 scenes

============================================================
🎭 Testing Scene Planner (NLP Logic)
============================================================
✅ ScenePlanner initialized successfully
✅ Scenes planned: 5 total

============================================================
📊 MOCK TEST SUMMARY
============================================================
✅ PASS - Voice Engine
✅ PASS - Avatar Engine
✅ PASS - Video Engine
✅ PASS - Layer Engine
✅ PASS - Script Engine
✅ PASS - Scene Planner

📈 Results: 6/6 tests passed

🎉 ALL TESTS PASSED!
✅ Code flow validated successfully
✅ Ready for GPU deployment

⚠️  Note: GPU-based inference will be tested during cloud deployment
```

---

## 🔥 **STEP 7: ACTUAL GPU TESTS**

### **7.1: Test Fish-Speech Audio Generation**

```bash
cd /workspace/moksha-mve1

# Create test script
cat > test_fish_speech.py << 'EOF'
import asyncio
from engines.voice_engine import VoiceEngine

async def test():
    engine = VoiceEngine()
    
    # Test Hindi audio generation
    audio_path = await engine.generate(
        text="Namaste! Main AI hoon",
        language="hindi",
        emotion="neutral",
        voice_type="male"
    )
    
    if audio_path and Path(audio_path).exists():
        print(f"✅ Fish-Speech SUCCESS!")
        print(f"Audio: {audio_path}")
        print(f"Size: {Path(audio_path).stat().st_size} bytes")
    else:
        print("❌ Fish-Speech FAILED")

if __name__ == "__main__":
    asyncio.run(test())
EOF

# Run test
python test_fish_speech.py
```

**Expected:**
```
🐟 Using Fish-Speech S2 Pro for natural voice generation
✅ Voice generated with Fish-Speech: e0cc6e62097598fad2f4f2e0a9059c50.wav
✅ Fish-Speech SUCCESS!
Audio: cache/voices/e0cc6e62097598fad2f4f2e0a9059c50.wav
Size: 882078 bytes
```

---

### **7.2: Test LivePortrait Lip-Sync**

```bash
cd /workspace/moksha-mve1

# Create test script
cat > test_liveportrait.py << 'EOF'
import asyncio
import subprocess
from pathlib import Path

async def test():
    # Use audio from previous test
    audio_path = "cache/voices/e0cc6e62097598fad2f4f2e0a9059c50.wav"
    
    if not Path(audio_path).exists():
        print("❌ No audio file found - run Fish-Speech test first")
        return
    
    # Test LivePortrait
    cmd = [
        "python",
        "LivePortrait/inference.py",
        "--source_image", "assets/default_avatar.jpg",
        "--driving_video", audio_path,
        "--output_path", "outputs/test_avatar_lipsync.mp4"
    ]
    
    print("🎭 Running LivePortrait lip-sync test...")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    
    if result.returncode == 0:
        output = Path("outputs/test_avatar_lipsync.mp4")
        if output.exists():
            print(f"✅ LivePortrait SUCCESS!")
            print(f"Video: {output}")
            print(f"Size: {output.stat().st_size} bytes")
        else:
            print("❌ Output file not created")
    else:
        print(f"❌ LivePortrait FAILED: {result.stderr}")

if __name__ == "__main__":
    asyncio.run(test())
EOF

# Run test
python test_liveportrait.py
```

**Expected:**
```
🎭 Running LivePortrait lip-sync test...
✅ LivePortrait SUCCESS!
Video: outputs/test_avatar_lipsync.mp4
Size: 1234567 bytes
```

---

### **7.3: Test LTX-Video Generation**

```bash
cd /workspace/moksha-mve1

# Create test script
cat > test_ltx_video.py << 'EOF'
import asyncio
import subprocess
from pathlib import Path

async def test():
    # Test LTX-Video
    cmd = [
        "python",
        "LTX-Video/sample/edit.py",
        "--prompt", "A beautiful sunset over mountains, cinematic",
        "--output_path", "outputs/test_video_ltx.mp4",
        "--width", "1920",
        "--height", "1080",
        "--num_frames", "120"  # 5 seconds @ 24fps
    ]
    
    print("🎬 Running LTX-Video test...")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    
    if result.returncode == 0:
        output = Path("outputs/test_video_ltx.mp4")
        if output.exists():
            print(f"✅ LTX-Video SUCCESS!")
            print(f"Video: {output}")
            print(f"Size: {output.stat().st_size} bytes")
        else:
            print("❌ Output file not created")
    else:
        print(f"❌ LTX-Video FAILED: {result.stderr}")

if __name__ == "__main__":
    asyncio.run(test())
EOF

# Run test
python test_ltx_video.py
```

**Expected:**
```
🎬 Running LTX-Video test...
✅ LTX-Video SUCCESS!
Video: outputs/test_video_ltx.mp4
Size: 2345678 bytes
```

---

## 🎬 **STEP 8: FULL PIPELINE TEST**

```bash
cd /workspace/moksha-mve1

# Create full pipeline test
cat > test_full_pipeline_gpu.py << 'EOF'
import asyncio
from main_app import MokshaMVE1

async def test():
    print("🚀 FULL PIPELINE GPU TEST")
    print("="*60)
    
    # Initialize system
    moksha = MokshaMVE1()
    
    # Initialize engines
    print("Initializing engines...")
    moksha.initialize_engines()
    print("✅ All engines initialized\n")
    
    # Create test video job
    print("Creating test video job...")
    result = await moksha.create_video(
        topic="Climate Change",
        language="hindi",
        style="educational",
        duration_minutes=1,  # Short test
        viral_mode=True
    )
    
    # Check result
    if result["status"] == "success":
        print("\n🎉 FULL PIPELINE SUCCESS!")
        print(f"Job ID: {result['job_id']}")
        print(f"Video: {result['video_path']}")
        print(f"Thumbnail: {result['thumbnail_path']}")
        print(f"Upload: {result.get('upload_result', {})}")
    else:
        print("\n❌ PIPELINE FAILED")
        print(f"Error: {result.get('error', 'Unknown')}")

if __name__ == "__main__":
    asyncio.run(test())
EOF

# Run test
python test_full_pipeline_gpu.py
```

**Expected:**
```
🚀 FULL PIPELINE GPU TEST
============================================================
Initializing engines...
✅ All engines initialized

Creating test video job...
🎯 Starting job: job_Climate_Change
📝 Step 1: Director-level script generation...
✅ Script generated: 5 scenes
🎭 Step 2: Scene planning with emotion flow...
✅ Scenes planned: 5 total
🎤 Step 3: Voice generation with natural breathing...
✅ Voice generated: cache/voices/xxx.wav
🎬 Step 4: Parallel video generation...
✅ Avatar generated: temp/avatar_xxx.mp4
✅ Video generated: temp/video_xxx.mp4
✂️ Step 5: Editing with retention optimization...
✅ Final video compiled: outputs/job_Climate_Change_final.mp4
🖼️ Step 6: Creating thumbnail...
✅ Thumbnail generated: outputs/job_Climate_Change_thumbnail.jpg
📊 Step 7: Generating SEO data...
✅ SEO data generated
📤 Step 8: Uploading to YouTube...
✅ Uploaded successfully

🎉 FULL PIPELINE SUCCESS!
Job ID: job_Climate_Change
Video: outputs/job_Climate_Change_final.mp4
```

---

## 💾 **STEP 9: DOWNLOAD FINAL VIDEO**

### **Option A: RunPod File Browser**

1. Go to RunPod Dashboard
2. Click your pod
3. Click `Files` tab
4. Navigate to: `/workspace/moksha-mve1/outputs/`
5. Right-click final video → `Download`

---

### **Option B: SCP Command**

```bash
# From your local machine (PowerShell/CMD)
scp -P <pod_port> root@<pod_ip>:/workspace/moksha-mve1/outputs/*.mp4 ./downloads/
```

---

### **Option C: Direct Link (if HTTP enabled)**

```bash
# In pod terminal
cd /workspace/moksha-mve1/outputs
python -m http.server 8000

# Then in browser:
# http://<pod_ip>:8000/final_video.mp4
```

---

## 🗑️ **STEP 10: TERMINATE POD (COST CONTROL!)**

**CRITICAL:** Terminate immediately after downloading to avoid charges!

```
RunPod Dashboard → Select Pod → Click "Terminate"

⚠️  WARNING: 
- Network Volume persists (models safe)
- Container storage deleted (code must be re-cloned)
- Billing stops ONLY after termination
```

**Confirm:**
```
✅ Pod terminated
✅ Billing stopped
✅ Models safe in Network Volume
```

---

## 📊 **COST BREAKDOWN**

### **One-Time Setup (First Time Only):**

```
Model Downloads: 3 hours × $0.70 = $2.10
Setup & Config: 1 hour × $0.70 = $0.70
────────────────────────────────────
First Day Total: ~$2.80
```

### **Subsequent Sessions (Using Saved Models):**

```
Testing: 2 hours × $0.70 = $1.40
Deployment: 1 hour × $0.70 = $0.70
Termination: FREE
────────────────────────────────
Per Session: ~$2.10
```

### **Monthly Budget (4 sessions):**

```
Initial Setup: $2.80
4 Testing Sessions: 4 × $2.10 = $8.40
Buffer: $3.80
────────────────────────────────
Monthly Total: ~$15.00 ✅
```

---

## 🚨 **TROUBLESHOOTING**

### **Issue 1: CUDA Out of Memory**

**Error:**
```
RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB
```

**Solution:**
```bash
# Reduce resolution in video_engine.py
resolution: "720p" instead of "1080p"

# Or reduce batch size in model config
batch_size: 1
```

---

### **Issue 2: Models Not Found**

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'checkpoints/s2-pro'
```

**Solution:**
```bash
# Check if models downloaded
ls -lh checkpoints/

# If missing, re-download
cd fish-speech
python download_models.py

# Or copy from network volume
cp -r /runpod-volume/checkpoints/* ./checkpoints/
```

---

### **Issue 3: FFmpeg Not Found**

**Error:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**Solution:**
```bash
# Install FFmpeg
apt-get update
apt-get install -y ffmpeg

# Verify
ffmpeg -version
```

---

### **Issue 4: API Key Errors**

**Error:**
```
DeepSeek API error: 401 Unauthorized
```

**Solution:**
```bash
# Check .env file
cat .env | grep DEEPSEEK

# Verify API key is correct (no spaces, no quotes)
# Correct: DEEPSEEK_API_KEY=sk-xxxxx
# Wrong: DEEPSEEK_API_KEY="sk-xxxxx"

# Restart pod after fixing .env
```

---

## ✅ **POST-DEPLOYMENT CHECKLIST**

```
✅ All mock tests passed locally
✅ GPU pod launched successfully
✅ Models downloaded and saved to Network Volume
✅ Fish-Speech audio test passed
✅ LivePortrait lip-sync test passed
✅ LTX-Video generation test passed
✅ Full pipeline test passed
✅ Final video downloaded
✅ Pod terminated (billing stopped)
✅ Costs tracked (under budget)
```

---

## 🎯 **SUCCESS CRITERIA**

### **Technical Success:**
```
✅ Voice sounds natural (no robotic artifacts)
✅ Lip-sync is perfect (92%+ accuracy)
✅ Video quality is 1080p (smooth motion)
✅ Total processing time <10 minutes
✅ No errors in logs
```

### **Cost Success:**
```
✅ Total cost under $15 budget
✅ Per-session cost under $3
✅ No surprise charges
✅ Billing stopped after termination
```

### **Quality Success:**
```
✅ Hollywood-level output
✅ Indian language support working
✅ Regional accents authentic
✅ Emotion expression natural
✅ Viewer can't tell it's AI
```

---

## 📞 **NEXT STEPS AFTER DEPLOYMENT**

1. **Test with Real User Content** (Day 1-2)
   - Create 5-10 test videos
   - Different topics, languages, styles
   - Validate consistency

2. **Optimize for Cost** (Day 3)
   - Reduce model sizes if possible
   - Optimize inference parameters
   - Batch processing for efficiency

3. **Production Deployment** (Day 4-5)
   - Set up automated pipeline
   - Configure YouTube auto-upload
   - Enable monitoring & alerts

4. **Launch!** (Day 6-7)
   - Create first public video
   - Upload to YouTube
   - Monitor performance

---

**MOKSHA AI - READY FOR PRODUCTION!** 🚀  
**Budget: $15 | Quality: Hollywood | Timeline: TODAY**
