import os
import json
import random
import subprocess
from pathlib import Path

# ==========================================
# CONFIGURATION
# ==========================================
NUM_EPISODES_PER_BATCH = 15
NUM_REPLAY_PER_EPISODE = 1
# Number of replays to generate per episode, so total episodes is NUM_EPISODES_PER_BATCH * NUM_REPLAY_PER_EPISODE
GPU_ID = "0"  # CUDA_VISIBLE_DEVICES index
INPUT_BASE_DIR = Path("Datasets/example")
OUTPUT_BASE_DIR = Path("Datasets/augmented")
TEXTURES_DIR = Path("Assets/objects/Challenge_Garment/Release/Color_Texture")
GARMENT_BASE_DIR = Path("Assets/objects/Challenge_Garment/Release")
DEVICE = "cuda"
TASK_NAME = "LeHome-BiSO101-Direct-Garment-v2"
START_EPISODE = 10

# Weights for different texture types
# If texture name contains 'Fabric' or 'Tiles', it gets higher probability.
TEXTURE_WEIGHTS = {
    "Fabric": 5.0,  # 5x more likely than standard
    "Tiles": 3.0,   # 3x more likely than standard
    "Default": 1.0
}

DATASETS = [
    # "record_pant_long_release_10",
     "record_pant_short_release_10",
    # "record_top_long_release_10",
    # "record_top_short_release_10"
]
# ==========================================

def get_all_textures_with_weights():
    """Retrieve textues and calculate weights based on their type."""
    if not TEXTURES_DIR.exists():
        raise FileNotFoundError(f"Texture directory not found: {TEXTURES_DIR}")
    
    textures = list(TEXTURES_DIR.glob("*.usd"))
    weights = []
    
    for tex in textures:
        weight = TEXTURE_WEIGHTS["Default"]
        name = tex.name
        if "Fabric" in name:
            weight = TEXTURE_WEIGHTS["Fabric"]
        elif "Tiles" in name:
            weight = TEXTURE_WEIGHTS["Tiles"]
        weights.append(weight)
        
    return textures, weights

def get_garment_type(garment_name):
    """Parse 'Pant_Long_Seen_1' into 'Pant_Long'."""
    parts = garment_name.split("_")
    return f"{parts[0]}_{parts[1]}"

def process_datasets():
    all_textures, texture_weights = get_all_textures_with_weights()
    if not all_textures:
        raise ValueError("No textures found!")
        
    print(f"Found {len(all_textures)} textures.")
    print(f"Applying biased sampling: Fabric({TEXTURE_WEIGHTS['Fabric']}x), Tiles({TEXTURE_WEIGHTS['Tiles']}x)")
    
    original_configs = {}

    for ds_name in DATASETS:
        ds_path = INPUT_BASE_DIR / ds_name
        if not ds_path.exists():
            continue
            
        print(f"\n================ Processing {ds_name} ================")
        
        for episode_dir in sorted(ds_path.iterdir()):
            if not episode_dir.is_dir() or not episode_dir.name.isdigit():
                continue
                
            print(f"---> Batch: {episode_dir.name}")
            
            garment_info_path = episode_dir / "meta" / "garment_info.json"
            if not garment_info_path.exists():
                continue
                
            with open(garment_info_path, 'r') as f:
                garment_info = json.load(f)
                
            garment_name = list(garment_info.keys())[0]
            garment_type = get_garment_type(garment_name)
            
            garment_json_dir = GARMENT_BASE_DIR / garment_type / garment_name
            if not garment_json_dir.exists():
                continue
                
            garment_jsons = list(garment_json_dir.glob("*.json"))
            if not garment_jsons:
                continue
                
            garment_json_path = garment_jsons[0]
            
            with open(garment_json_path, 'r') as f:
                garment_cfg = json.load(f)
                
            original_paths = garment_cfg.get("visual_usd_paths", [])
            
            if str(garment_json_path) not in original_configs:
                original_configs[str(garment_json_path)] = original_paths
                
            num_to_pick = max(1, len(original_paths))
            
            # Weighted random sampling
            picked_textures = random.choices(all_textures, weights=texture_weights, k=num_to_pick)
            
            new_visual_paths = [f"/{str(tex.as_posix())}" for tex in picked_textures]
            garment_cfg["visual_usd_paths"] = new_visual_paths
            
            with open(garment_json_path, 'w') as f:
                json.dump(garment_cfg, f, indent=4)
                
            print(f"Randomized {garment_name} with: {[Path(p).name for p in new_visual_paths]}")
            
            output_root = OUTPUT_BASE_DIR / ds_name / episode_dir.name
            
            cmd = [
                "xvfb-run", "-a", "python", "-m", "scripts.dataset_sim", "replay",
                "--dataset_root", str(episode_dir),
                "--output_root", str(output_root),
                "--task", TASK_NAME,
                "--num_replays", str(NUM_REPLAY_PER_EPISODE),
                "--device", DEVICE,
                "--enable_cameras",
                "--start_episode", str(START_EPISODE),
                "--end_episode", str(NUM_EPISODES_PER_BATCH),
                "--save_successful_only"
            ]
            
            env = os.environ.copy()
            env["CUDA_VISIBLE_DEVICES"] = GPU_ID
            subprocess.run(cmd, env=env)

    # Cleanup and Restore
    backup_file = "original_garment_textures_backup.json"
    with open(backup_file, 'w') as f:
        json.dump(original_configs, f, indent=4)
        
    print("\nRestoring original designs...")
    for path_str, orig_paths in original_configs.items():
        with open(path_str, 'r') as f:
            cfg = json.load(f)
        cfg["visual_usd_paths"] = orig_paths
        with open(path_str, 'w') as f:
            json.dump(cfg, f, indent=4)
            
    print("Done!")

if __name__ == "__main__":
    process_datasets()
