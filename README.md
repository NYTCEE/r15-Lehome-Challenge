
Put ``dataset_replay_randomization.py`` under ``lehome-challenge/scripts``

The dataset used in this repo combines an official four_types dataset with depth information and additional self-generated datasets featuring variations in clothing colors and table colors.

The model is trained using SmolVLA and ACT with the following training configuration:

batch_size: 32 | steps: 60000 | save_freq: 1000 | log_freq: 500

Training is conducted on an NVIDIA GeForce RTX 5090 GPU.

### Detailed Instructions

https://hackmd.io/nXxix1F5Ta-QPMGBZ0Fqjw

### Model
https://huggingface.co/nytcee/r15_4a_lehome_policy/tree/main

https://huggingface.co/nytcee/r15_4s_lehome_policy/tree/main

### Datasets
https://huggingface.co/datasets/IntelligentDecisionLab/four_types_merged_combined

https://huggingface.co/IntelligentDecisionLab



## Conclusion Graph - Success Rate
Not going to evaluate the rest of the DPs, cuz I think the result won't be better than other models.
| **Model** | **Policy (Trained Under Which One)** | **Dataset (Given Which Kind of Task)** | **Garment Type (Evaluation Result Focus on Which One)** | **Success Rate** |
|:--------:|:--------:|:-------------:|:-------------:|:--------------------:|
| ACT | top_long_merged |  top_long  |  top_long  | 66.67% |
| ACT | top_short_merged |  top_short  |  top_short  | 48.33% |
| ACT | pant_long_merged |  pant_long  |  pant_long  | 38.33% |
| ACT | record_pant_long_release_10 |  pant_long  |  pant_long  |1.67%|
| ACT | pant_short_merged |  pant_short  |  pant_short  | 81.67% |
| ACT | four_types_merged |  top_long  |  top_long  | 36.67% |
| ACT | four_types_merged |  top_short  |  top_short  | 23.33% |
| ACT | four_types_merged |  pant_long  |  pant_long  | 26.67% |
| ACT | four_types_merged |  pant_short  | pant_short  | 73.33% |
| ACT | four_types_merged |  four_types_merged  | pant_short  | 75.00% |
| ACT | four_types_merged_combined_act |  four_types_merged   |  top_long  | 71.67% |
| ACT | four_types_merged_combined_act |  four_types_merged   |  top_short | 40.00% |
| ACT | four_types_merged_combined_act |  four_types_merged   |  pant_long  | 25.00% |
| ACT | four_types_merged_combined_act |  four_types_merged   |  pant_short  | 86.67% |
| DP | top_long_merged |  top_long  |  top_long | 3.33% |
| DP | top_short_merged |  top_short  |  top_short  | 1.67% |
| DP | pant_long_merged |  pant_long  |  pant_long  | ?% |
| DP | pant_short_merged |  pant_short  |  pant_short  | ?% |
| DP | four_types_merged |  top_long  |  top_long  | ?% |
| DP | four_types_merged |  top_short  |  top_short  | ?% |
| DP | four_types_merged |  pant_long  |  pant_long  | ?% |
| DP | four_types_merged |  pant_short  |  pant_short  | ?% |
| SmolVLA | top_long_merged |  top_long  |  top_long  | 60.00%, 73.33% |
| SmolVLA | top_short_merged |  top_short  |  top_short  | 43.33% |
| SmolVLA | pant_long_merged |  pant_long  |  pant_long  | 46.67% |
| SmolVLA | pant_short_merged |  pant_short  |  pant_short  | 78.33% |
| SmolVLA | four_types_merged |  top_long  |  top_long  | 53.33% |
| SmolVLA | four_types_merged |  top_short  |  top_short  | 11.67% |
| SmolVLA | four_types_merged |  pant_long  |  pant_long  | 41.67% |
| SmolVLA | four_types_merged |  pant_short  |  pant_short  | 76.67% |
| SmolVLA | four_types_merged_combined_smolvla |  four_types_merged   |  top_long  | 65.00% |
| SmolVLA | four_types_merged_combined_smolvla |  four_types_merged   |  top_short  | 23.33% |
| SmolVLA | four_types_merged_combined_smolvla |  four_types_merged   |  pant_long  | 41.67% |
| SmolVLA | four_types_merged_combined_smolvla |  four_types_merged   |  pant_short  | 86.67% |
| π₀.₅ | four_types_merged |  top_long  | top_long  | 3.33% |
| π₀.₅ | four_types_merged |  top_short  | top_short  | % |
| XVLA | four_types_merged |  top_long  |  top_long  | 1.33% |
| XVLA | four_types_merged |  top_short  |  top_short  | 0.00% |
| XVLA | four_types_merged |  pant_long  |  pant_long  | 3.33% |
| XVLA | four_types_merged |  pant_short  |  pant_short  | 28.33% |


## Best Performance Graph

| **Garment Type (Evaluation Result Focus on Which One)** | **Success Rate** | **Model** | **Policy (Trained Under Which One)** | **Dataset (Given Which Kind of Task)** | 
|:--------:|:--------:|:-------------:|:-------------:|:--------------------:|
| top_long | 71.67% | ACT |  four_types_merged_combined_act   |  four_types_merged   |
|  top_short |  48.33% | ACT | top_short_merged  |  top_short  |
| pant_short | 86.67% | ACT |  four_types_merged_combined_act   |  four_types_merged   | 
|   pant_long  |  41.67% | SmolVLA | four_types_merged_combined_smolvla |  four_types_merged|


---
### References
https://github.com/lehome-official/lehome-challenge

https://lehome-challenge.com/
