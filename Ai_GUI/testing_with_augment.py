import os, sys
import augment_images_random_fortesting as augment
import tensorflow as tf
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

class Testing():
    def __init__(self, image_dir, retrained_graph_path, retrained_labels_path):
        cwd = os.path.dirname(os.path.realpath(__file__))      #path to current file
        self.image_dir = os.path.join(cwd, image_dir)
        self.retrained_graph_path = retrained_graph_path
        self.retrained_labels_path = retrained_labels_path

    def run(self):
        # Read in the image_data

        label_lines = [line.rstrip() for line
                           in tf.gfile.GFile(self.retrained_labels_path)]
        # Unpersists graph from file
        with tf.gfile.FastGFile(self.retrained_graph_path, 'rb') as f:
            graph_def = tf.GraphDef()
            graph_def.ParseFromString(f.read())
            tf.import_graph_def(graph_def, name='')

        subdirs = ["benign", "malignant"]
        count = 0.0
        correct = 0.0
        for subdir in subdirs:
            files = os.listdir(os.path.join(self.image_dir, subdir))
            for filename in files:
                if "_test" in filename:
                    img_name = os.path.splitext(filename)[0]
                    augmented_images = augment.augment_image(os.path.join(self.image_dir, subdir, img_name))
                    # Loads label file, strips off carriage return
                    predictions = []
                    for i in range(len(augmented_images)):
                        with tf.Session() as sess:
                            # Feed the image_data as input to the graph and get first prediction
                            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

                            prediction = sess.run(softmax_tensor, \
                                     {'DecodeJpeg:0': augmented_images[i]})
                            predictions.append(prediction)
                    avg = np.average(predictions, axis=0)
                    top_k = avg[0].argsort()[-len(avg[0]):][::-1]
                    predict_label = label_lines[top_k[0]]
                    if predict_label == subdir:
                        correct += 1.0
                    count += 1.0
        # print(str(correct))
        # print(str(count))
        accuracy = correct/count*100.0
        # print("Test Accuracy: "+str(accuracy)+"%.")
        with open("test_output.txt", "w+") as output:
            output.write(str(accuracy))




if __name__=='__main__':
    test = Testing(sys.argv[1], sys.argv[2],sys.argv[3])
    test.run()
    # Sort to show labels of first prediction in order of confidence
    # top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
    # for node_id in top_k:
    #     human_string = label_lines[node_id]
    #     score = predictions[0][node_id]
    #     print('%s (score = %.5f)' % (human_string, score))

# python testing_with_augment.py 100X_split4 retrained_graph_11.pb retrained_labels_11.txt
