import tensorflow as tf
from Trainer import Trainer, parse_args
import os
from model import *


data_path, epochs = parse_args()

sess = tf.InteractiveSession(config=tf.ConfigProto())

x = tf.placeholder(tf.float32, shape=[None, 240, 320, 3])
y_ = tf.placeholder(tf.float32, shape=[None, 3])

W_conv1 = weight_variable('layer1',[6, 6, 3, 64])
b_conv1 = bias_variable('layer1',[64])
h_conv1 = tf.tanh(conv2d(x, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)

W_conv2 = weight_variable('layer2',[1, 1, 64, 4])
b_conv2 = bias_variable('layer2',[4])
h_conv2 = tf.tanh(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

W_conv3 = weight_variable('layer3',[6, 6, 4, 4])
b_conv3 = bias_variable('layer3',[4])
h_conv3 = tf.tanh(conv2d(h_pool2, W_conv3) + b_conv3)
h_pool3 = max_pool_2x2(h_conv3)

W_conv4 = weight_variable('layer4',[6, 6, 4, 4])
b_conv4 = bias_variable('layer4',[4])
h_conv4 = tf.tanh(conv2d(h_pool3, W_conv4) + b_conv4)
h_pool4 = max_pool_2x2(h_conv4)

W_fc1 = weight_variable('layer5',[15 * 20 * 4, 4])
b_fc1 = bias_variable('layer5',[4])

h_pool4_flat = tf.reshape(h_pool4, [-1, 15 * 20 * 4])
h_fc1 = tf.nn.relu(tf.matmul(h_pool4_flat, W_fc1) + b_fc1)

dropout_keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, dropout_keep_prob)

W_fc2 = weight_variable('layer6',[4, 3])
b_fc2 = bias_variable('layer6',[3])

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

model_file = os.path.dirname(os.path.realpath(__file__)) + '/' + os.path.basename(__file__)
trainer = Trainer(data_path=data_path, model_file=model_file,epochs=epochs, max_sample_records=100)
trainer.train(sess=sess, x=x, y_=y_,
              accuracy=accuracy,
              train_step=train_step,
              train_feed_dict={dropout_keep_prob:0.5},
              test_feed_dict={dropout_keep_prob:1.0})