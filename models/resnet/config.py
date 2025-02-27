# some training parameters
EPOCHS = 1
BATCH_SIZE = 400
NUM_CLASSES = 10
image_height = 224
image_width = 224
channels = 3
save_model_dir = "saved_model/model"
dataset_dir = "$EBROOTECOHMEMMINTFMINEP/models/resnet/dataset/"
train_dir = dataset_dir + "train"
valid_dir = dataset_dir + "valid"
test_dir = dataset_dir + "test"

# choose a network
#model = "resnet18"
model = "resnet34"
#model = "resnet50"
#model = "resnet101"
# model = "resnet152"
