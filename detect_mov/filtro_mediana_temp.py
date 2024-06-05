import numpy as np
import cv2

video_path = 'videos/Cars.mp4'
video_output = 'videos/Cars_resultado.avi'

cap = cv2.VideoCapture(video_path)

hasframe, frame = cap.read()

fourcc = cv2.VideoWriter_fourcc(*'XVID')   #Gravar o video de resultado - XVID formato
writer = cv2.VideoWriter(video_output,fourcc,25,(frame.shape[1], frame.shape[0]),False)

framesId = cap.get(cv2.CAP_PROP_FRAME_COUNT) * np.random.uniform(size=25)

frames_bg = []
for i in framesId:
    cap.set(cv2.CAP_PROP_POS_FRAMES,i)
    _,frame_atual = cap.read()
    frames_bg.append(frame_atual)

mediana_frame = np.median(frames_bg, axis=0).astype(dtype=np.uint8)

cv2.imwrite('bg_final_mediana.jpg',mediana_frame)

cap.set(cv2.CAP_PROP_POS_FRAMES,0)                           
graymedian = cv2.cvtColor(mediana_frame,cv2.COLOR_BGR2GRAY)

while(True):
    hasframe, frame = cap.read()

    if not hasframe:
        print('Error')
        break

    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    dframe = cv2.absdiff(framegray,graymedian)
    #th,dframe = cv2.threshold(diframe,120,255,cv2.THRESH_BINARY)
    th,dframe = cv2.threshold(dframe,0,255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    print(th)

    cv2.imshow('frame',dframe)
    writer.write(dframe)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

writer.release()
cap.release()