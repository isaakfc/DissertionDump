from keras.layers import Conv2D, Conv2DTranspose, BatchNormalization
from tensorflow import keras

"""
class Encoder(keras.layers.Layer):
    def __init__(self, filters, l2_reg):
        super(Encoder, self).__init__()
        self.conv1 = Conv2D(filters=filters[0],
                            kernel_size=3,
                            strides=1,
                            padding='same',
                            kernel_regularizer=keras.regularizers.l2(l2_reg))
        self.conv1_strided = Conv2D(filters=filters[0],
                                    kernel_size=3,
                                    strides=2,
                                    padding='same',
                                    kernel_regularizer=keras.regularizers.l2(l2_reg))
        self.conv2 = Conv2D(filters=filters[1],
                            kernel_size=3,
                            strides=1,
                            padding='same',
                            kernel_regularizer=keras.regularizers.l2(l2_reg))
        self.conv2_strided = Conv2D(filters=filters[1],
                                    kernel_size=3,
                                    strides=2,
                                    padding='same',
                                    kernel_regularizer=keras.regularizers.l2(l2_reg))

        self.relu = keras.activations.relu
        self.batch_norm1 = keras.layers.BatchNormalization()
        self.batch_norm2 = keras.layers.BatchNormalization()

    def call(self, input_tensor, training=False):
        x = self.conv1(input_tensor)
        x = self.batch_norm1(x, training=training)
        x = self.relu(x)
        x = self.conv1_strided(x)
        x = self.conv2(x)
        x = self.batch_norm2(x, training=training)
        x = self.relu(x)
        x = self.conv2_strided(x)
        return x


class Decoder(keras.layers.Layer):
    def __init__(self, filters):
        super(Decoder, self).__init__()
        self.conv1 = Conv2D(filters=filters[1], kernel_size=3, strides=1, padding='same')
        self.conv1_transpose = Conv2DTranspose(filters=filters[1], kernel_size=3, strides=2, padding='same')
        self.conv2 = Conv2D(filters=filters[0], kernel_size=3, strides=1, padding='same')
        self.conv2_transpose = Conv2DTranspose(filters=filters[0], kernel_size=3, strides=2, padding='same')
        self.conv3 = Conv2D(1, 3, 1, activation='sigmoid', padding='same')
        self.relu = keras.activations.relu

    def call(self, encoded):
        x = self.conv1(encoded)
        x = self.relu(x)
        x = self.conv1_transpose(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.conv2_transpose(x)
        return self.conv3(x)

class Autoencoder(keras.Model):
    def __init__(self, filters, l2_reg):
        super(Autoencoder, self).__init__()
        self.loss = []
        self.encoder = Encoder(filters, l2_reg)
        self.decoder = Decoder(filters)

    def call(self, input_features, training=False):
        #print(input_features.shape)
        encoded = self.encoder(input_features, training=training)
        #print(encoded.shape)
        reconstructed = self.decoder(encoded)
        #print(reconstructed.shape)
        return reconstructed

"""

from keras.layers import Conv2D, MaxPooling2D, UpSampling2D, BatchNormalization
from tensorflow import keras

class Encoder(keras.layers.Layer):
    def __init__(self, filters, l2_reg):
        super(Encoder, self).__init__()
        self.conv1 = Conv2D(filters=filters[0],
                            kernel_size=3,
                            strides=1,
                            padding='same',
                            kernel_regularizer=keras.regularizers.l2(l2_reg),)
        self.conv2 = Conv2D(filters=filters[1],
                            kernel_size=3,
                            strides=1,
                            padding='same',
                            kernel_regularizer=keras.regularizers.l2(l2_reg),)
        self.pool = MaxPooling2D((2, 2), padding='same')
        self.relu = keras.activations.relu
        self.batch_norm1 = keras.layers.BatchNormalization()
        self.batch_norm2 = keras.layers.BatchNormalization()

    def call(self, input_tensor, training=False):
        x = self.conv1(input_tensor)
        x = self.batch_norm1(x, training=training)
        x = self.relu(x)
        x = self.pool(x)
        x = self.conv2(x)
        x = self.batch_norm2(x, training=training)
        x = self.relu(x)
        x = self.pool(x)
        return x

class Decoder(keras.layers.Layer):
    def __init__(self, filters):
        super(Decoder, self).__init__()
        self.conv1 = Conv2D(filters=filters[1], kernel_size=3, strides=1, padding='same')
        self.conv2 = Conv2D(filters=filters[0], kernel_size=3, strides=1, padding='same')
        self.conv3 = Conv2D(1, 3, 1, activation='sigmoid', padding='same')
        self.upsample = UpSampling2D((2, 2))
        self.relu = keras.activations.relu

    def call(self, encoded):
        x = self.conv1(encoded)
        x = self.relu(x)
        x = self.upsample(x)
        x = self.conv2(x)
        x = self.relu(x)
        x = self.upsample(x)
        return self.conv3(x)

class Autoencoder(keras.Model):
    def __init__(self, filters, l2_reg):
        super(Autoencoder, self).__init__()
        self.loss = []
        self.encoder = Encoder(filters, l2_reg)
        self.decoder = Decoder(filters)

    def call(self, input_features, training=False):
        #print(input_features.shape)
        encoded = self.encoder(input_features, training=training)
        #print(encoded.shape)
        reconstructed = self.decoder(encoded)
        #print(reconstructed.shape)
        return reconstructed