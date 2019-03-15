samples = 0
indexes = []
# depth rows cols
img_size = [30, 60, 60]
img_data = ['./Actions/Hello/', './Actions/Dog/', './Actions/Eat/']
batch_size = 100
class_cnt = len(img_data)
epoch_cnt = 200
filters = [16, 16]
pool_size = [3, 3, 3]
kernal_shape = [2, 2, 2]
