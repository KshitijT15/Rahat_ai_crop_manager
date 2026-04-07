import h5py

with h5py.File("models/model.weights.h5", "r") as f:
    def print_keys(name, obj):
        if isinstance(obj, h5py.Dataset):
            print(f"{name}: shape={obj.shape}")
    f.visititems(print_keys)
    