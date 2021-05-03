import tensorflow as tf

# General parameters
EPOCHS = 20

# Our model
class SMARTModel(tf.keras.Model):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Initialize the weights to `5.0` and the bias to `0.0`
        # In practice, these should be randomly initialized
        self.w = tf.Variable(5.0)
        self.b = tf.Variable(0.0)

    def call(self, x):
        return self.w * x + self.b

NUM_EXAMPLES = 1000
n = tf.random.normal(shape=[NUM_EXAMPLES]) # Some noise
x = tf.random.normal(shape=[NUM_EXAMPLES]) # A vector of random x values (a paragraph from SQuAD)
y = x * 3.0 + 2.0 + n                      # Calculate y (a question from SQuAD)

# Create and train a model
model = SMARTModel()
model.compile(
    # By default, fit() uses tf.function(). You can
    # turn that off for debugging, but it is on now.
    run_eagerly=False,
    # Using a built-in optimizer, configuring as an object
    optimizer=tf.keras.optimizers.SGD(learning_rate=0.1),
    # Keras comes with built-in MSE error
    # However, you could use your own loss function
    loss=tf.keras.losses.mean_squared_error,
)
model.fit(x, y, epochs=EPOCH, batch_size=1000)