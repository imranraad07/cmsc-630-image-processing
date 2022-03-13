import numpy as np


# https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale
def rgb_to_gray(img, color_spectrum=None):
  copy_image = img.copy()

  R = np.array(copy_image[:, :, 0])
  G = np.array(copy_image[:, :, 1])
  B = np.array(copy_image[:, :, 2])
  if color_spectrum is None:
    R = (R * .299)
    G = (G * .587)
    B = (B * .114)

    Avg = (R + G + B)
    return Avg
  if color_spectrum == 'R':
    return R
  elif color_spectrum == 'G':
    return G
  return B


def histogram(img):
  hist = np.zeros(256)
  for i in range(len(hist)):
    hist[i] = np.sum(img == i)
  hist = hist.astype(int)
  return hist


def calc_avg_histogram(hist_list):
  hist_arr = np.array(hist_list)
  hist = np.mean(hist_arr, axis=0)
  hist = np.rint(hist)
  hist = hist.astype(int)
  return hist


def gaussian_noise(img, sigma):
  copy_image = img.copy()

  mean = 0.0
  noise = np.random.normal(mean, sigma, copy_image.size)
  shaped_noise = noise.reshape(copy_image.shape)
  gauss = copy_image + shaped_noise
  return gauss


def salt_pepper_noise(img, strength):
  copy_image = img.copy()

  out = np.copy(copy_image)
  m, n = copy_image.shape

  num_salt = np.ceil(strength * copy_image.size * 0.5)
  for i in range(int(num_salt)):
    x = np.random.randint(0, m - 1)
    y = np.random.randint(0, n - 1)
    out[x][y] = 0

  num_pepper = np.ceil(strength * copy_image.size * 0.5)
  for i in range(int(num_pepper)):
    x = np.random.randint(0, m - 1)
    y = np.random.randint(0, n - 1)
    out[x][y] = 0

  return out


def equalized_histogram(img):
  copy_image = img.copy()

  img_hist = histogram(copy_image)
  cum_sum = np.cumsum(img_hist)
  cum_sum = (cum_sum - cum_sum.min()) * 255 / (cum_sum.max() - cum_sum.min())
  cum_sum = cum_sum.astype(np.uint8)
  equalized = cum_sum[copy_image.flatten().astype(np.uint8)]

  img_new = np.reshape(equalized, copy_image.shape)
  return img_hist, histogram(img_new), img_new


def mean_square_error(original_img, quantized_img):
  mse = (np.square(original_img - quantized_img)).mean()
  return mse


def linear_filter(img, filter):
  copy_image = img.copy()

  x, y = filter.shape
  scale = x * y

  m, n = copy_image.shape
  out = np.zeros((m, n))

  for i in range(m):
    for j in range(n):
      neighborhood = copy_image[i: min(i + x, m), j: min(j + y, n)]
      if neighborhood.shape != filter.shape:
        result = np.sum(filter[0:len(neighborhood), 0:len(neighborhood[0])] * neighborhood)
        scaled_image = result / scale
      else:
        result = np.sum(filter * neighborhood)
        scaled_image = result / scale
      out[i, j] = scaled_image
  out = np.rint(out)
  return out.astype(np.uint8)


def median_filter(img, filter_size):
  copy_image = img.copy()

  m, n = copy_image.shape
  out = np.zeros((m, n))
  indexer = filter_size / 2

  for i in range(m):
    for j in range(n):
      pixel_list = []
      for z in range(filter_size):
        if i + z - indexer < 0 or i + z - indexer > m - 1:
          for c in range(filter_size):
            pixel_list.append(0)
        else:
          if j + z - indexer < 0 or j + indexer > n - 1:
            pixel_list.append(0)
          else:
            for k in range(filter_size):
              pixel_list.append(copy_image[i + z - indexer][j + k - indexer])
      pixel_list.sort()
      out[i][j] = pixel_list[len(pixel_list) / 2]
  out = np.rint(out)
  return out