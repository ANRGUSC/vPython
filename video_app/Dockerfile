FROM vcimg
WORKDIR /app
COPY . /app/
# From https://github.com/docker-library/golang
RUN cd /app/
RUN rm -f *.txt
RUN touch vpython.txt
RUN pip3 install Cython
RUN touch stack.txt
RUN apt-get install python-numpy zip unzip -y
WORKDIR /app/
RUN pip3 install opencv-python-headless
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
