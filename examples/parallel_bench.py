import time

from absl import app, flags

import motrixsim as mtx

_File = flags.DEFINE_string("file", None, "path to model", required=True)
_BatchSize = flags.DEFINE_integer("batch", 1024, "number of instances to simulate", lower_bound=0)
_NumSteps = flags.DEFINE_integer("steps", 3000, "number of simulation steps to run", lower_bound=1)


def main(argv):
    batch_size = _BatchSize.value
    # Load the scene model
    model = mtx.load_model(_File.value)
    # Create the physics data of the model
    data = mtx.SceneData(model, batch=(batch_size,))

    t0 = time.monotonic()
    for _ in range(_NumSteps.value):
        model.step(data)
    elapsed = time.monotonic() - t0

    print(f"Summary: {_NumSteps.value} steps for {batch_size} instances in {elapsed:.3f} seconds")
    print(f"Average: {(_NumSteps.value * batch_size) / elapsed:.3f} steps/second")


if __name__ == "__main__":
    app.run(main)
