from keras.layers import Dense, Dropout
from keras.models import Sequential
from training.visual_callbacks import AccLossPlotter


class Trainer:
    def __init__(self, data, splitter):
        self.model = None
        self.batch_size = 0
        (self.x_train, self.y_train), (self.x_test, self.y_test) = splitter.split(data)
        print(self.x_test)

    def train(self, epochs=2000, error_function="mse", optimizer="nadam", batch_size=50,
              evaluation_metrices=None):
        if evaluation_metrices is None:
            evaluation_metrices = ['accuracy']
        model = Sequential()
        model.add(Dense(512, activation='tanh', input_shape=(self.x_train.shape[1],)))
        model.add(Dropout(0.5))
        model.add(Dense(512, activation='relu'))
        model.add(Dense(512, activation='relu'))
        model.add(Dense(512, activation='linear'))
        model.add(Dropout(0.5))
        model.add(Dense(self.y_test.shape[1], activation='linear'))
        model.compile(loss=error_function,
                      optimizer=optimizer,
                      metrics=evaluation_metrices)
        # if u want accuracy replace loss with acc
        plotter = AccLossPlotter(graphs=['loss'], save_graph=True)
        model.fit(self.x_train, self.y_train,
                  batch_size=batch_size,
                  verbose=1,
                  nb_epoch=epochs,
                  shuffle=True,
                  validation_split=0.2,
                  callbacks=[plotter])
        self.model = model
        self.batch_size = batch_size

    def save_model(self, path):
        self.model.save(path)

    def evaluate(self):
        score = self.model.evaluate(self.x_test, self.y_test,
                                    batch_size=self.batch_size, verbose=1)
        print('Test accuracy:', score[1])
        return score[0], score[1]
