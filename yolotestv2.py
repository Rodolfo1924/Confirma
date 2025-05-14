import cv2
from ultralytics import YOLO

def main():
    # Cargar modelo YOLO
    face_model = YOLO("C:/Users/rodol/Downloads/archive/yolov8n-face-lindevs.pt")  # Modelo específico para rostros
    
    # Abrir cámara
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: No se pudo abrir la cámara")
        return
    
    print("Cámara abierta. Presiona 'q' para salir...")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: No se pudo leer el frame")
            break
        
        # Detectar rostros (solo el más prominente)
        results = face_model(frame, verbose=False)
        
        # Procesar solo el primer rostro detectado
        for r in results:
            if len(r.boxes) > 0:
                box = r.boxes[0]
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                
                if conf > 0.5:  # Filtro de confianza
                    # Dibujar rectángulo
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    # Mostrar texto
                    cv2.putText(frame, f"Rostro: {conf:.2f}", (x1, y1-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        # Mostrar frame
        cv2.imshow("Deteccion de Rostro", frame)
        
        # Salir con 'q' o al cerrar ventana
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if cv2.getWindowProperty("Deteccion de Rostro", cv2.WND_PROP_VISIBLE) < 1:
            break
    
    # Liberar recursos
    cap.release()
    cv2.destroyAllWindows()
    print("Cámara cerrada")

if __name__ == "__main__":
    main()