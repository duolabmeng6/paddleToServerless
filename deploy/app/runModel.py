import cv2
import paddlehub as hub
module = hub.Module(name="kunchongjiance")
def getResult(image):
    images = [image]
    results = module.predict(images=images)
    return results[0]

if __name__ == "__main__":
    print(getResult(cv2.imread("static/test.jpg")))