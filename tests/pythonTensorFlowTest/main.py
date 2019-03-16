import os
import skimage
import numpy
import matplotlib.pyplot as plt
from skimage import transform
from skimage.color import rgb2gray
import tensorflow as tf
import random


def load_data(data_directory):
    directories = [d for d in os.listdir(data_directory)
                   if os.path.isdir(os.path.join(data_directory, d))]
    labels = []
    images = []
    for d in directories:
        label_directory = os.path.join(data_directory, d)
        file_names = [os.path.join(label_directory, f)
                      for f in os.listdir(label_directory)
                      if f.endswith(".ppm")]
        for f in file_names:
            images.append(skimage.data.imread(f))
            labels.append(int(d))
    return images, labels


ROOT_PATH = "C:/Users/Sean McHale/Documents/DataSets/BelgianTrafficSigns"
train_data_directory = os.path.join(ROOT_PATH, "Training")
test_data_directory = os.path.join(ROOT_PATH, "Testing")

images, labels = load_data(train_data_directory)

# print(numpy.array(images).ndim)
# print(numpy.array(images).size)
# print(images[0])

# print(numpy.array(labels).ndim)
# print(numpy.array(labels).size)
# print(len(set(labels)))
images28 = [transform.resize(image, (28, 28)) for image in images]
images28 = numpy.array(images28)
images28 = rgb2gray(images28)

traffic_signs = [300, 2250, 3650, 4000]
for i in range(len(traffic_signs)):
    plt.subplot(1, 4, i+1)
    plt.axis('off')
    plt.imshow(images28[traffic_signs[i]], cmap="gray")
    plt.subplots_adjust(wspace=0.5)
    plt.show()
    print("shape: {0}, min: {1}, max: {2}".format(images28[traffic_signs[i]].shape,
                                                  images28[traffic_signs[i]].min(),
                                                  images28[traffic_signs[i]].max()))

unique_labels = set(labels)

plt.figure(figsize=(15, 15))

i = 1

for label in unique_labels:
    image = images[labels.index(label)]
    plt.subplot(8, 8, i)
    plt.axis('off')
    plt.title("Label {0} ({1})".format(label, labels.count(label)))
    i += 1
    plt.imshow(image)

plt.show()

# Initialize Placeholders
x = tf.placeholder(dtype=tf.float32, shape=[None, 28, 28])
y = tf.placeholder(dtype=tf.int32, shape=[None])

# Flatten the Input Data
images_flat = tf.contrib.layers.flatten(x)

# Fully Connected Layer
logits = tf.contrib.layers.fully_connected(images_flat, 62, tf.nn.relu)

# Define a Loss Function
loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits))

# Define An Optimizer
train_op = tf.train.AdamOptimizer(learning_rate=0.001).minimize(loss)

# Covert logits to label indexes
correct_pred = tf.argmax(logits, 1)

# Define an Accuracy Matrix
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

print("images_flat: ", images_flat)
print("logits: ", logits)
print("loss: ", loss)
print("predicted_labels : ", correct_pred)

tf.set_random_seed(1234)
sess = tf.Session()

sess.run(tf.global_variables_initializer())
for i in range(201):
    print('Epoch', i)
    _, accuracy_val = sess.run([train_op, accuracy], feed_dict={x: images28, y: labels})
    if i % 10 == 0:
        print("Loss", loss)
    print('DONE WITH EPOCH')

# Pick 10 Random Images
sample_indexes = random.sample(range(len(images28)), 15)
sample_images = [images28[i] for i in sample_indexes]
sample_labels = [labels[i] for i in sample_indexes]

# Run the correct pred operation
predicted = sess.run([correct_pred], feed_dict={x: sample_images})[0]

# print the real and predicted labels
print(sample_labels)
print(predicted)

# Display tje predictions and the ground truth visually
fig = plt.figure(figsize=(10, 10))
for i in range(len(sample_images)):
    truth = sample_labels[i]
    prediction = predicted[i]
    plt.subplot(5, 3, 1+i)
    plt.axis('off')
    color = 'green' if truth == prediction else 'red'
    plt.text(40, 10, "Truth:           {0}\nPrediction: {1}".format(truth, prediction),
             fontsize=12, color=color)
    plt.imshow(sample_images[i], cmap="gray")
plt.show()

# Load the test data
test_images, test_labels = load_data(test_data_directory)

# Transform the images to 28 by 28 pixels
test_images28 = [transform.resize(image, (28, 28)) for image in test_images]

# Convert to gray scale
test_images28 = rgb2gray(numpy.array(test_images28))

# Run Predictions against the full test set
predicted = sess.run([correct_pred], feed_dict={x: test_images28})[0]

# Calculate Correct Matches
match_count = sum([int(y == y) for y, y_ in zip(test_labels, predicted)])

# Calculate correct matches
accuracy = match_count / len(test_labels)

# Print Accuracy
print("Accuracy: {:.3f}".format(accuracy))
