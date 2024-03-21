from ultralytics import YOLO

model = YOLO("models/yolov8s-cls.pt")
if __name__ == '__main__':
    model.train(data="datasets", epochs=12)