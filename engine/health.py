"""
System health and diagnostics
"""
import os
import time
from typing import Dict, Any
from .utils import DATA_DIR, MODELS_DIR, CACHE_DIR, log


def check_health() -> Dict[str, Any]:
    """Check system health and return status"""
    health = {
        "status": "healthy",
        "checks": {},
        "warnings": [],
        "errors": [],
        "timestamp": time.time(),
    }
    
    # Check directories
    for name, path in [("data", DATA_DIR), ("models", MODELS_DIR), ("cache", CACHE_DIR)]:
        exists = os.path.exists(path)
        writable = os.access(path, os.W_OK) if exists else False
        health["checks"][f"{name}_dir"] = {
            "exists": exists,
            "writable": writable,
            "path": path,
        }
        if not exists:
            health["warnings"].append(f"{name} directory does not exist: {path}")
        elif not writable:
            health["warnings"].append(f"{name} directory is not writable: {path}")
    
    # Check model cache
    model_cache_size = 0
    if os.path.exists(MODELS_DIR):
        try:
            for root, dirs, files in os.walk(MODELS_DIR):
                model_cache_size += sum(os.path.getsize(os.path.join(root, f)) for f in files)
        except Exception as e:
            health["warnings"].append(f"Could not calculate model cache size: {e}")
    
    health["checks"]["model_cache"] = {
        "size_mb": round(model_cache_size / (1024 * 1024), 2),
        "exists": model_cache_size > 0,
    }
    
    # Check data cache
    cache_files = 0
    if os.path.exists(CACHE_DIR):
        try:
            cache_files = len([f for f in os.listdir(CACHE_DIR) if f.endswith('.json')])
        except Exception as e:
            health["warnings"].append(f"Could not count cache files: {e}")
    
    health["checks"]["data_cache"] = {
        "files": cache_files,
    }
    
    # Try to import key dependencies
    dependencies = {}
    for module_name in ["streamlit", "pandas", "altair", "sentence_transformers", "faiss", "transformers"]:
        try:
            __import__(module_name)
            dependencies[module_name] = "ok"
        except ImportError:
            dependencies[module_name] = "missing"
            health["errors"].append(f"Missing dependency: {module_name}")
        except Exception as e:
            dependencies[module_name] = f"error: {e}"
            health["warnings"].append(f"Dependency issue with {module_name}: {e}")
    
    health["checks"]["dependencies"] = dependencies
    
    # Determine overall status
    if health["errors"]:
        health["status"] = "unhealthy"
    elif health["warnings"]:
        health["status"] = "degraded"
    
    return health


def clear_model_cache() -> Dict[str, Any]:
    """Clear the model cache directory"""
    import shutil
    result = {
        "success": False,
        "message": "",
        "freed_mb": 0,
    }
    
    if not os.path.exists(MODELS_DIR):
        result["message"] = "Model cache directory does not exist"
        result["success"] = True
        return result
    
    try:
        # Calculate size before
        size_before = 0
        for root, dirs, files in os.walk(MODELS_DIR):
            size_before += sum(os.path.getsize(os.path.join(root, f)) for f in files)
        
        # Remove directory
        shutil.rmtree(MODELS_DIR)
        os.makedirs(MODELS_DIR, exist_ok=True)
        
        result["freed_mb"] = round(size_before / (1024 * 1024), 2)
        result["message"] = f"Cleared {result['freed_mb']} MB from model cache"
        result["success"] = True
        log.info(result["message"])
        
    except Exception as e:
        result["message"] = f"Failed to clear model cache: {e}"
        log.error(result["message"])
    
    return result


def clear_data_cache() -> Dict[str, Any]:
    """Clear the data cache directory"""
    import shutil
    result = {
        "success": False,
        "message": "",
        "files_removed": 0,
    }
    
    if not os.path.exists(CACHE_DIR):
        result["message"] = "Data cache directory does not exist"
        result["success"] = True
        return result
    
    try:
        # Count files
        files = [f for f in os.listdir(CACHE_DIR) if f.endswith('.json')]
        
        # Remove cache files
        for f in files:
            os.remove(os.path.join(CACHE_DIR, f))
        
        result["files_removed"] = len(files)
        result["message"] = f"Removed {len(files)} cache files"
        result["success"] = True
        log.info(result["message"])
        
    except Exception as e:
        result["message"] = f"Failed to clear data cache: {e}"
        log.error(result["message"])
    
    return result

