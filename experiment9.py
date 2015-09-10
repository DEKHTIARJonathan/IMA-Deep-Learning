import theano
import lasagne
import numpy
import uuid
from lasagne.layers import get_output, get_all_params
from deepsix.train import *
from deepsix.data import load_datasets

input_directory = 'data/solid+rect'
num_epochs = 100


def build_network(input_var=None):
    network = lasagne.layers.InputLayer(
        shape=(None, 1, 64, 64),
        input_var=input_var)

    network = lasagne.layers.Conv2DLayer(
        network, num_filters=8, filter_size=(5, 5),
        nonlinearity=lasagne.nonlinearities.leaky_rectify)

    network = lasagne.layers.MaxPool2DLayer(network, pool_size=(2, 2))

    network = lasagne.layers.Conv2DLayer(
        network, num_filters=8, filter_size=(5, 5),
        nonlinearity=lasagne.nonlinearities.leaky_rectify)

    network = lasagne.layers.MaxPool2DLayer(network, pool_size=(2, 2))

    network = lasagne.layers.DenseLayer(
        lasagne.layers.dropout(network, p=.5),
        num_units=2,
        nonlinearity=lasagne.nonlinearities.softmax)

    return network


def build_model(input_var=None, target_var=None, network=None):
    def loss(test=False):
        return lasagne.objectives.categorical_crossentropy(
            get_output(network, deterministic=test), target_var).mean()

    optimizer = lasagne.updates.nesterov_momentum(
        loss(),
        get_all_params(network, trainable=True),
        learning_rate=0.001,
        momentum=0.1)

    return {
        'input_var': input_var,
        'target_var': target_var,
        'network': network,
        'loss': loss,
        'updates': optimizer
    }


def main(input_directory, num_epochs=5):
    print("Loading data...")
    data = load_datasets(input_directory)

    print("Building model...")
    input_var = theano.tensor.tensor4('inputs')
    target_var = theano.tensor.ivector('targets')
    network = build_network(input_var)
    model = build_model(input_var, target_var, network)

    print("Starting training...")
    train_network(data, model, num_epochs)

    print("\nLearned parameters:")
    params = numpy.array(lasagne.layers.get_all_param_values(network))
    param_file = 'output/{}.npy'.format(str(uuid.uuid4()))
    print("Parameters written to {}".format(param_file))
    params.dump(param_file)


if __name__ == '__main__':
    main(input_directory, num_epochs)
