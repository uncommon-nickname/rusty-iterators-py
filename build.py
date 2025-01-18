import os
import shutil


def copy_stub_files():
    stub_src = os.path.join(os.path.dirname(__file__), "stubs", "rusty_iterators")
    package_dst = os.path.join(os.path.dirname(__file__), "rusty_iterators")

    if not os.path.exists(stub_src):
        raise OSError("stubs directory not found!")

    for root, _, files in os.walk(stub_src):
        rel_path = os.path.relpath(root, stub_src)
        target_path = os.path.join(package_dst, rel_path)
        os.makedirs(target_path, exist_ok=True)

        for file in files:
            if file.endswith(".pyi") or file == "py.typed":
                shutil.copyfile(
                    os.path.join(root, file), os.path.join(target_path, file)
                )
                print(
                    f"Copied: {os.path.join(root, file)} -> {os.path.join(target_path, file)}"
                )


if __name__ == "__main__":
    copy_stub_files()
