
import numpy as np
import cv2
import matplotlib.pyplot as plt


def switch_class():
    global selected_class, classes
    ind = classes.index(selected_class)
    if ind == len(classes)-1:
        ind = 0
    else:
        ind += 1
    selected_class = classes[ind]
    
def draw_obj(event,x,y,flags,param):
    global mouseX, mouseY, space, dataset
    if event == cv2.EVENT_LBUTTONDBLCLK:
        mouseX, mouseY = x,y
        if selected_class == 'circle':
            cv2.circle(space, (mouseX, mouseY), 10, (255, 0, 0), -1)
        elif selected_class == 'square':
            cv2.rectangle(space, (mouseX-20, mouseY-20), (mouseX+20, mouseY+20), (0, 255, 0), -1)
        elif selected_class == 'line':
            cv2.line(space, (mouseX-20, mouseY-20), (mouseX+20, mouseY+20), (0, 0, 255), 2, cv2.LINE_AA)
            cv2.line(space, (mouseX-20, mouseY+20), (mouseX+20, mouseY-20), (0, 0, 255), 2, cv2.LINE_AA)
        dataset.append([int((mouseX/space.shape[1])*100), 
                        int(((space.shape[0]-mouseY)/space.shape[0])*100), 
                        classes.index(selected_class)]
                        )

def save_to_csv(arr, name):
    rows = ["{},{},{}".format(i, j, k) for i, j, k in arr]
    text = "\n".join(rows)
    with open(name, 'w') as f:
        f.write(text)


space = np.zeros((600, 600, 3), np.uint8)
mouseX, mouseY = 0, 0
classes = ['circle', 'square', 'line']
selected_class = 'circle'
dataset = []

if __name__ == '__main__':
    cv2.namedWindow('Space')
    cv2.setMouseCallback('Space', draw_obj)

    while(1):
        cv2.imshow('Space',space)
        cv2.putText(space, selected_class, (10, 30), cv2.FONT_HERSHEY_PLAIN, 2, (255,255,255), 1, cv2.LINE_AA)
        if cv2.waitKey(1) == ord('c'):
            space[:60, :140] = 0
            switch_class()
        if cv2.waitKey(1) == ord('q'):
            break

    if len(dataset) > 0:
        dataset = np.array(dataset)
        print(dataset.shape, '\n', dataset)
        circles = dataset[dataset[:, 2] == 0]
        squares = dataset[dataset[:, 2] == 1]
        crosses = dataset[dataset[:, 2] == 2]
        plt.xlim(0, 100)
        plt.ylim(0, 100)
        plt.scatter(circles[:, 0], circles[:, 1], c ="blue") if len(circles) > 0 else None
        plt.scatter(squares[:, 0], squares[:, 1], c ="red") if len(squares) > 0 else None
        plt.scatter(crosses[:, 0], crosses[:, 1], c ="green") if len(crosses) > 0 else None
        plt.show()
        save_to_csv(dataset, 'data.csv')

    cv2.destroyAllWindows()


