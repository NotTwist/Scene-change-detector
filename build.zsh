set -o xtrace

setup_root() {
    apt-get install -qq -y \
        python3-pip \
        python3-tk \
        cmake \
        python3-opencv

    pip3 install -qq \
        pandas \
        pytest \
        scikit-image \
        scikit-learn \
        tqdm \
        matplotlib \
        opencv-python \
        pybind11
}

setup_checker() {
    python3 -c 'import sys, pandas, pytest, skimage, sklearn, tqdm, matplotlib, cv2, pybind11; print("python3\t\t", sys.version); print("pandas\t\t", pandas.__version__); print("pytest\t\t", pytest.__version__); print("scikit-image\t", skimage.__version__); print("scikit-learn\t", sklearn.__version__); print("tqdm\t\t", tqdm.__version__); print("matplotlib\t", matplotlib.__version__); print("opencv-python\t", cv2.__version__); print("pybind11\t", pybind11.__version__)'
}

"$@"