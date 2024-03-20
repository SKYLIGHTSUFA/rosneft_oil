from ultralytics import YOLO

model = YOLO("yolov8n-cls.pt")
if __name__ == '__main__':
    model.train(data="datasets", epochs=9)