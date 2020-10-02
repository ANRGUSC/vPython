FROM debian:buster
WORKDIR /app
COPY . /app/
# From https://github.com/docker-library/golang
RUN apt-get update && \
  apt-get install -y --no-install-recommends \
  g++ \
  gcc \
  libc6-dev \
  make \
  zlib1g-dev \
  cmake \
  cmake-gui \
  cmake-curses-gui \
  libssl-dev \
  git \
  ca-certificates \
  libffi-dev \
  libc-dev \
  build-essential \
  wget \
  && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get -y install openssh-client sshpass libblas-dev liblapack-dev
RUN DEBIAN_FRONTEND="noninteractive" apt-get -y install tzdata
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
#RUN mkdir mqtt-install
#RUN cd mqtt-install
#RUN git clone https://github.com/eclipse/paho.mqtt.c.git
#RUN make
#RUN make install
EXPOSE 22
#RUN mkdir debug
#RUN cd debug  
#RUN /app/configure CFLAGS='-DPy_DEBUG -DPy_TRACE_REFS' --with-pydebug --with-trace-refs
#RUN /app/configure CFLAGS='-DPy_DEBUG' --with-pydebug
RUN /app/configure
RUN rm -f vpython.txt
RUN rm -f stack.txt
RUN make -j "$(nproc)"
RUN rm -f vpython.txt
RUN rm -f stack.txt
#RUN make test 
RUN make install
RUN rm -f vpython.txt
RUN rm -f stack.txt
#RUN cd /app/
#RUN touch vpython.txt
RUN pip3 install --upgrade pip setuptools
RUN rm -f vpython.txt
RUN rm -f stack.txt
RUN pip3 install wheel
RUN rm -f vpython.txt
RUN rm -f stack.txt
RUN pip3 install Cython
RUN rm -f vpython.txt
RUN rm -f stack.txt
#RUN touch stack.txt
RUN pip3 install numpy --no-use-pep517
RUN rm -f vpython.txt
RUN rm -f stack.txt
RUN pip3 install -U scikit-learn
RUN rm -f vpython.txt
RUN rm -f stack.txt
WORKDIR /
ENV OPENCV_VERSION="3.4.2"
RUN wget https://github.com/opencv/opencv/archive/${OPENCV_VERSION}.zip \
&& unzip ${OPENCV_VERSION}.zip \
&& mkdir /opencv-${OPENCV_VERSION}/cmake_binary \
&& cd /opencv-${OPENCV_VERSION}/cmake_binary \
&& cmake -DBUILD_TIFF=ON \
  -DBUILD_opencv_java=OFF \
  -DWITH_CUDA=OFF \
  -DWITH_OPENGL=ON \
  -DWITH_OPENCL=ON \
  -DWITH_IPP=ON \
  -DWITH_TBB=ON \
  -DWITH_EIGEN=ON \
  -DWITH_V4L=ON \
  -DBUILD_TESTS=OFF \
  -DBUILD_PERF_TESTS=OFF \
  -DCMAKE_BUILD_TYPE=RELEASE \
  -DCMAKE_INSTALL_PREFIX=$(python -c "import sys; print(sys.prefix)") \
  -DPYTHON_EXECUTABLE=$(which python) \
  -DPYTHON_INCLUDE_DIR=$(python -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())") \
  -DPYTHON_PACKAGES_PATH=$(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())") \
  .. \
&& make install \
&& rm /${OPENCV_VERSION}.zip \
&& rm -r /opencv-${OPENCV_VERSION}
#RUN python3 tests/t2.py > output.txt
#RUN python3 /app/video_app/yolo_opencv.py --image /app/video_app/frame100.jpg --config /app/video_app/yolov3.cfg --weights /app/video_app/yolov3.weights --classes /app/video_app/yolov3.txt
#RUN chmod 400 id_ed2551
#RUN ./run.sh
#RUN rm -f vpython.txt
#RUN scp -o StrictHostKeyChecking=no -i id_ed2551 vpython* stack.txt object-detection.jpg gowri@neptune.usc.edu:/home/gowri/
#RUN chmod 644 vedge.pub
#RUN ssh-copy-id 
#RUN scp -i vedge.pub vpython.txt gowri@eclipse.usc.edu:/home/gowri/vedge_files/
ENTRYPOINT ["sleep", "infinity"]
