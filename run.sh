python main.py --base_path 'data/Cancerous cell smears' \
  --output_path 'output' \
  --image_type 'BMP' \
  --batch_size 10 \
  --color_channel 'R' \
  --linear_filter_weights '1 1 1 1 1 1 1 1 1' \
  --linear_filter_mask 3 \
  --median_filter_weights '1 1 1 1 1 1 1 1 1' \
  --median_filter_mask 3 \
  --salt_pepper_noise_strength 0.1 \
  --gaussian_strength 1
