## Scene Assets

This project utilizes 3D scene assets from the [ArtVIP](https://huggingface.co/datasets/x-humanoid-robomind/ArtVIP) dataset, which have been specifically adapted for **MotrixSim**.

* **Source Scene:** `parlour` (Living room environment)
* **Original Source:** [x-humanoid-robomind/ArtVIP](https://huggingface.co/datasets/x-humanoid-robomind/ArtVIP)
* **Original License:** Apache-2.0
* **Processing Notes:**
    * Extracted the geometric structures and textures of the `parlour` scene.
    * Converted the original USD format into **MJCF (.xml)** format for compatibility with the MotrixSim physical simulation environment.
    * Optimized the **collision meshes** and adjusted physical parameters, such as friction and damping, to meet simulation requirements.
    * Enhanced and optimized the **rendering lights** to improve visual fidelity within the simulator.

### License & Attribution
The converted MJCF assets in this repository are distributed under the **Apache-2.0 License**. Original author copyright notices have been preserved. For detailed information, please refer to the `LICENSE` files located in the directory.