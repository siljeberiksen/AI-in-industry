
import tensorflow as tf
import tensorflow_probability as tfp
import matplotlib.pyplot as plt

def build_nn_model(input_shape, output_shape, hidden, output_activation='linear'):
    model_in = tf.keras.Input(shape=input_shape, dtype='float32')
    x = model_in
    for h in hidden:
        x = tf.keras.layers.Dense(h, activation='relu')(x)
    model_out = tf.keras.layers.Dense(output_shape, activation=output_activation)(x)
    model = tf.keras.Model(model_in, model_out)
    return model

def build_nn_normal_model(input_shape, hidden, stddev_guess=1):
    model_in = tf.keras.Input(shape=input_shape, dtype='float32')
    x = model_in
    for h in hidden:
        x = keras.layers.Dense(h, activation='relu')(x)
    mu_logsigma = tf.keras.layers.Dense(2, activation='linear')(x)
    lf = lambda t: tfp.distributions.Normal(loc=t[:, :1], scale=tf.math.exp(t[:, 1:]))
    model_out = tfp.layers.DistributionLambda(lf)(mu_logsigma)
    model = tf.keras.Model(model_in, model_out)
    return model


def plot_pred_scatter(y_true, y_pred, figsize=None, print_metrics=True):
    plt.figure(figsize=figsize)
    plt.scatter(y_pred, y_true, marker='.', alpha=0.1)
    xl, xu = plt.xlim()
    yl, yu = plt.ylim()
    l, u = min(xl, yl), max(xu, yu)
    plt.plot([l, u], [l, u], ':', c='0.3')
    plt.grid(linestyle=':')
    plt.xlim(l, u)
    plt.ylim(l, u)
    plt.xlabel('prediction')
    plt.ylabel('target')
    plt.tight_layout()

    if print_metrics:
        print(f'R2: {metrics.r2_score(y_true, y_pred):.2f}')
        print(f'MAE: {metrics.mean_absolute_error(y_true, y_pred):.2f}')


def train_nn_model(model, X, y, loss,
        verbose=0, patience=10,
        validation_split=0.0, **fit_params):
    # Compile the model
    model.compile(optimizer='Adam', loss=loss)
    # Build the early stop callback
    cb = []
    if validation_split > 0:
        cb += [keras.callbacks.EarlyStopping(patience=patience,
            restore_best_weights=True)]
    # Train the model
    history = model.fit(X, y, callbacks=cb,
            validation_split=validation_split,
            verbose=verbose, **fit_params)
    return history
