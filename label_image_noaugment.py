import os, sys
import tensorflow as tf
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# change this as you see fit
class LabelImage():
    def __init__(self, image_path, retrained_graph_path, retrained_labels_path):
        cwd = os.path.dirname(os.path.realpath(__file__))      #path to current file
        self.image_path = os.path.join(cwd, image_path)
        self.retrained_graph_path = retrained_graph_path
        self.retrained_labels_path = retrained_labels_path

    def run(self):
        # Read in the image_data

        image_data = tf.gfile.FastGFile(self.image_path, 'rb').read()

        # Loads label file, strips off carriage return
        label_lines = [line.rstrip() for line
                           in tf.gfile.GFile(self.retrained_labels_path)]

        # Unpersists graph from file
        with tf.gfile.FastGFile(self.retrained_graph_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')
        with tf.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

            prediction = sess.run(softmax_tensor, \
                     {'DecodeJpeg\contents:0': image_data})
        return label_lines, prediction

if __name__=='__main__':
    labelimage = LabelImage(sys.argv[1],sys.argv[2],sys.argv[3])
    label_lines, predictions = labelimage.run()
    # Sort to show labels of first prediction in order of confidence
    top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    for node_id in top_k:
        human_string = label_lines[node_id]
        score = predictions[0][node_id]
        print('%s (score = %.5f)' % (human_string, score))

# python label_image.py testing/test.jpg retrained_graph_original.pb retrained_labels_original.txt
